#!/usr/bin/env python3
"""
Claude findings remediation.

Reads the SAST (Semgrep SARIF), SCA (Trivy SARIF), and DAST (ZAP JSON) output
from the security pipeline, and lets Claude triage each finding against the
CHECKED-OUT REPO (not just the finding text): read the surrounding code,
decide whether it's a real bug vs. intentionally-vulnerable example/training
content, and edit the file only when it is confident the fix is correct,
minimal, and safe.

Every finding gets a recorded disposition (fixed / skipped + why), written to
a markdown report - this becomes the pull request body, so nothing is fixed
or skipped silently.

SAFETY: this script only ever edits files in the working tree. It does not
commit, push, or open a PR - the calling workflow does that, and stops short
of merging, so a human always reviews before anything reaches main. If the
repo is itself a security-training target (e.g. an intentionally vulnerable
app), the system prompt instructs Claude to leave that code alone regardless
of confidence - see the in_scope check in record_decision.

Env / args:
  ANTHROPIC_API_KEY   (required)  your Anthropic API key
  CLAUDE_MODEL        (optional)  default: claude-sonnet-5
  --semgrep-sarif     path to Semgrep SARIF (optional, skipped if missing)
  --trivy-sarif       path to Trivy SARIF (optional, skipped if missing)
  --zap-json          path to ZAP JSON report (optional, skipped if missing)
  --max-steps         tool-call budget to cap time/cost (default 60)
  --report            markdown report output path (default remediation-report.md)
"""

import argparse
import json
import os
import re
import sys

from anthropic import Anthropic

MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")
MAX_FILE_CHARS = 6000
MAX_SEARCH_RESULTS = 40

SYSTEM_PROMPT = """\
You are triaging SAST/SCA/DAST security findings for a code repository you
have direct read/write access to via tools. Your job is NOT to blindly fix
everything - it's to reason about each finding like a careful security
engineer doing remediation, the same way a human would.

For EVERY finding (or tight group of near-identical findings, e.g. the same
rule firing on many files), you must:
1. Investigate: read the flagged file(s) around the reported location, and
   enough surrounding context (README, CLAUDE.md, directory names, comments)
   to understand what the code is FOR.
2. Decide in_scope: is this a genuine defect, or is it intentionally-vulnerable
   example/training/lab/CTF content whose entire purpose is to demonstrate
   the flaw? Signals it's NOT in scope: paths/dirs named like
   "vulnerabilities/", "vuln", "dvwa", "juice-shop", "insecure-by-design";
   comments or docs stating the app is deliberately vulnerable for
   practice/training/scanning demos; a "fixed" or "impossible" variant of the
   same code living right next to the "vulnerable" one (a strong sign the
   vulnerable one is meant to stay vulnerable). If out of scope, do not edit
   it - record why and move on. Getting this wrong (breaking a teaching tool)
   is a real failure mode, so default to caution.
3. If in scope, decide confidence (high/medium/low) that you understand the
   correct, minimal, behavior-preserving fix. Only actually edit the file
   when confidence is high AND the fix cannot plausibly break other
   functionality. A DAST header/config finding is "high confidence" only
   once you've located the actual place in THIS codebase responsible for it
   (e.g. by grepping for how other headers are already set) - never guess at
   a fix without reading real code first.
4. medium/low confidence, or anything needing a product/design judgment call
   a human should make, must NOT be edited - record it as skipped with your
   reasoning and a suggested direction, so a human can pick it up.
5. Call record_decision for every finding you considered, whether or not you
   edited anything. This is the audit trail - never silently drop a finding.

Be efficient with your tool budget: group near-duplicate findings (e.g. the
same Semgrep rule on 12 files that are clearly all part of the same
intentional lab) into one investigation and one record_decision call rather
than repeating the same conclusion 12 times, unless they genuinely need
different dispositions.
"""

TOOLS = [
    {
        "name": "list_directory",
        "description": "List files and subdirectories at a path relative to the repo root.",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "Relative path, '.' for root."}},
            "required": ["path"],
        },
    },
    {
        "name": "read_file",
        "description": "Read a text file relative to the repo root. Returns line-numbered content.",
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "offset": {"type": "integer", "description": "1-indexed start line (optional)."},
                "limit": {"type": "integer", "description": "Max lines to return (optional)."},
            },
            "required": ["path"],
        },
    },
    {
        "name": "search_code",
        "description": "Regex-search file contents across the repo. Returns matching file:line:text.",
        "input_schema": {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "Python regex."},
                "path": {"type": "string", "description": "Subdirectory to search under (optional, default '.')."},
            },
            "required": ["pattern"],
        },
    },
    {
        "name": "edit_file",
        "description": (
            "Replace an exact text occurrence in a file. old_string must match "
            "EXACTLY ONCE in the file (fails otherwise, same as a find-and-replace "
            "that refuses to guess). Use this to apply the fix once you're certain."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "old_string": {"type": "string"},
                "new_string": {"type": "string"},
            },
            "required": ["path", "old_string", "new_string"],
        },
    },
    {
        "name": "record_decision",
        "description": "Record the disposition of one finding (or finding group). Call this for every finding you consider.",
        "input_schema": {
            "type": "object",
            "properties": {
                "finding": {"type": "string", "description": "Short name of the finding/rule."},
                "files": {"type": "string", "description": "File(s) affected."},
                "in_scope": {"type": "boolean"},
                "confidence": {"type": "string", "enum": ["high", "medium", "low", "n/a"]},
                "action": {"type": "string", "enum": ["fixed", "skipped_out_of_scope", "skipped_needs_human"]},
                "reasoning": {"type": "string"},
            },
            "required": ["finding", "files", "in_scope", "confidence", "action", "reasoning"],
        },
    },
]


def parse_sarif(path, tool_label):
    if not path or not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    findings = []
    for run in data.get("runs", []):
        for result in run.get("results", []):
            rule_id = result.get("ruleId", "unknown")
            message = (result.get("message", {}) or {}).get("text", "")
            for loc in result.get("locations", []) or [{}]:
                phys = (loc.get("physicalLocation") or {})
                uri = (phys.get("artifactLocation") or {}).get("uri", "")
                line = (phys.get("region") or {}).get("startLine")
                findings.append({
                    "tool": tool_label, "rule": rule_id, "file": uri,
                    "line": line, "message": message[:300],
                })
    return findings


def parse_zap(path):
    if not path or not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    findings = []
    for site in data.get("site", []):
        for alert in site.get("alerts", []):
            instances = alert.get("instances", []) or []
            urls = ", ".join(sorted({i.get("uri", "") for i in instances}))[:300]
            findings.append({
                "tool": "DAST-ZAP", "rule": alert.get("name", "unknown"),
                "file": urls, "line": None,
                "message": (alert.get("desc", "") or "")[:300],
                "risk": alert.get("riskdesc", ""),
            })
    return findings


def group_findings(findings):
    grouped = {}
    for f in findings:
        key = (f["tool"], f["rule"])
        grouped.setdefault(key, []).append(f)
    lines = []
    for i, ((tool, rule), items) in enumerate(grouped.items(), 1):
        files = sorted({it["file"] for it in items if it["file"]})[:10]
        lines.append(
            f"{i}. [{tool}] {rule} - {len(items)} instance(s)\n"
            f"   files: {', '.join(files) or '(n/a)'}\n"
            f"   e.g.: {items[0]['message']}"
        )
    return "\n".join(lines)


def make_tool_handlers(repo_root):
    def list_directory(inp):
        target = os.path.join(repo_root, inp.get("path", "."))
        try:
            entries = sorted(os.listdir(target))
            return {"entries": entries[:200]}
        except OSError as e:
            return {"error": str(e)}

    def read_file(inp):
        target = os.path.join(repo_root, inp["path"])
        try:
            with open(target, encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
        except OSError as e:
            return {"error": str(e)}
        offset = max(inp.get("offset", 1) - 1, 0)
        limit = inp.get("limit", 200)
        chunk = lines[offset:offset + limit]
        numbered = "".join(f"{offset + i + 1}\t{line}" for i, line in enumerate(chunk))
        return {"content": numbered[:MAX_FILE_CHARS]}

    def search_code(inp):
        pattern = re.compile(inp["pattern"])
        base = os.path.join(repo_root, inp.get("path", "."))
        results = []
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "vendor")]
            for name in files:
                fp = os.path.join(root, name)
                try:
                    with open(fp, encoding="utf-8", errors="ignore") as f:
                        for lineno, line in enumerate(f, 1):
                            if pattern.search(line):
                                rel = os.path.relpath(fp, repo_root)
                                results.append(f"{rel}:{lineno}:{line.strip()[:200]}")
                                if len(results) >= MAX_SEARCH_RESULTS:
                                    return {"matches": results, "truncated": True}
                except OSError:
                    continue
        return {"matches": results, "truncated": False}

    def edit_file(inp):
        target = os.path.join(repo_root, inp["path"])
        try:
            with open(target, encoding="utf-8") as f:
                content = f.read()
        except OSError as e:
            return {"error": str(e)}
        count = content.count(inp["old_string"])
        if count == 0:
            return {"error": "old_string not found - re-read the file, it may have changed."}
        if count > 1:
            return {"error": f"old_string matches {count} times - make it unique before editing."}
        content = content.replace(inp["old_string"], inp["new_string"], 1)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return {"edited": True}

    return {
        "list_directory": list_directory,
        "read_file": read_file,
        "search_code": search_code,
        "edit_file": edit_file,
    }


def run(args):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        sys.exit("ERROR: ANTHROPIC_API_KEY is not set.")

    findings = (
        parse_sarif(args.semgrep_sarif, "SAST-Semgrep")
        + parse_sarif(args.trivy_sarif, "SCA-Trivy")
        + parse_zap(args.zap_json)
    )
    if not findings:
        print("No findings to triage - nothing to do.")
        with open(args.report, "w", encoding="utf-8") as f:
            f.write("# Claude Remediation Report\n\nNo findings were passed in.\n")
        return

    repo_root = os.getcwd()
    handlers = make_tool_handlers(repo_root)
    client = Anthropic(api_key=api_key)
    decisions = []

    findings_summary = group_findings(findings)
    messages = [{
        "role": "user",
        "content": (
            f"Here are the findings from this run's SAST/SCA/DAST scan, grouped by "
            f"rule:\n\n{findings_summary}\n\n"
            "Investigate each group in this repo and triage it per your instructions. "
            "Work through all of them, then stop."
        ),
    }]

    for step in range(args.max_steps):
        resp = client.messages.create(
            model=MODEL, max_tokens=4096, system=SYSTEM_PROMPT,
            tools=TOOLS, messages=messages,
        )
        messages.append({"role": "assistant", "content": resp.content})

        if resp.stop_reason != "tool_use":
            for block in resp.content:
                if getattr(block, "type", None) == "text":
                    print(f"[claude] {block.text}")
            break

        tool_results = []
        for block in resp.content:
            if getattr(block, "type", None) != "tool_use":
                continue
            if block.name == "record_decision":
                decisions.append(block.input)
                result = {"recorded": True}
                print(f"[decision] {block.input.get('action')}: {block.input.get('finding')}")
            elif block.name in handlers:
                result = handlers[block.name](block.input)
            else:
                result = {"error": f"unknown tool {block.name}"}
            tool_results.append({
                "type": "tool_result", "tool_use_id": block.id,
                "content": json.dumps(result)[:6000],
            })
        messages.append({"role": "user", "content": tool_results})
    else:
        print(f"[info] Reached max-steps budget ({args.max_steps}).")

    fixed = [d for d in decisions if d.get("action") == "fixed"]
    skipped = [d for d in decisions if d.get("action") != "fixed"]

    report = ["# Claude Remediation Report\n"]
    report.append(f"Triaged {len(decisions)} finding group(s): "
                   f"**{len(fixed)} fixed**, **{len(skipped)} left for human review**.\n")
    report.append("| Finding | Files | In scope | Confidence | Action | Reasoning |")
    report.append("|---|---|---|---|---|---|")
    for d in decisions:
        report.append(
            f"| {d.get('finding','')} | {d.get('files','')} | {d.get('in_scope','')} "
            f"| {d.get('confidence','')} | {d.get('action','')} | {d.get('reasoning','').replace(chr(10), ' ')} |"
        )
    if not fixed:
        report.append("\n_No changes were made - nothing met the bar for an automatic fix._")

    with open(args.report, "w", encoding="utf-8") as f:
        f.write("\n".join(report) + "\n")
    print(f"\nWrote report to {args.report}: {len(fixed)} fixed, {len(skipped)} skipped.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--semgrep-sarif", default=None)
    ap.add_argument("--trivy-sarif", default=None)
    ap.add_argument("--zap-json", default=None)
    ap.add_argument("--max-steps", type=int, default=60)
    ap.add_argument("--report", default="remediation-report.md")
    run(ap.parse_args())
