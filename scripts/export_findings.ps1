<#
  export_findings.ps1
  Export ALL findings from every section into one folder:
    - SAST (Semgrep) + SCA (Trivy)  -> from GitHub code scanning alerts
    - DAST (OWASP ZAP)              -> from the Security Pipeline run artifact
    - DAST (Claude)                 -> from the Claude Agentic DAST run artifact

  Usage (from your repo folder):
    ./scripts/export_findings.ps1 -Repo "owner/name"

  Requires: GitHub CLI (gh) authenticated (gh auth status).
#>

param(
  [Parameter(Mandatory = $true)][string]$Repo,   # e.g. "ALVINNNNN/DevSecOps-PoC"
  [string]$OutDir = "findings-export"
)

$ErrorActionPreference = "Stop"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
Write-Host "Exporting findings for $Repo -> $OutDir/`n"

Write-Host "[1/4] Code scanning alerts (SAST + SCA)..."
gh api "repos/$Repo/code-scanning/alerts?state=open&per_page=100" --paginate |
  Out-File -Encoding utf8 "$OutDir/all-code-scanning-alerts.json"

$all = Get-Content "$OutDir/all-code-scanning-alerts.json" -Raw | ConvertFrom-Json
if ($null -eq $all) { $all = @() }

$sast = @($all | Where-Object { $_.tool.name -match 'Semgrep' })
$sca  = @($all | Where-Object { $_.tool.name -match 'Trivy'  })
$sast | ConvertTo-Json -Depth 30 | Out-File -Encoding utf8 "$OutDir/sast-semgrep.json"
$sca  | ConvertTo-Json -Depth 30 | Out-File -Encoding utf8 "$OutDir/sca-trivy.json"
Write-Host "      SAST (Semgrep): $($sast.Count) | SCA (Trivy): $($sca.Count)"

$all | ForEach-Object {
  [pscustomobject]@{
    Number = $_.number; Tool = $_.tool.name
    Severity = $_.rule.security_severity_level; RuleId = $_.rule.id
    File = $_.most_recent_instance.location.path
    Line = $_.most_recent_instance.location.start_line
    State = $_.state; Message = $_.most_recent_instance.message.text
  }
} | Export-Csv -NoTypeInformation -Encoding utf8 "$OutDir/code-scanning-summary.csv"

Write-Host "[2/4] DAST - OWASP ZAP report..."
try {
  $zapRun = gh run list --workflow "Security Pipeline (SAST + SCA + DAST)" `
              --limit 1 --json databaseId --jq '.[0].databaseId'
  if ($zapRun) { gh run download $zapRun --name zap-dast-report --dir "$OutDir/dast-zap" }
} catch { Write-Host "      (No ZAP artifact yet - skipped.)" }

Write-Host "[3/4] DAST - Claude agentic findings..."
try {
  $claudeRun = gh run list --workflow "Claude Agentic DAST" `
                 --limit 1 --json databaseId --jq '.[0].databaseId'
  if ($claudeRun) { gh run download $claudeRun --name claude-dast-findings --dir "$OutDir/dast-claude" }
} catch { Write-Host "      (No Claude DAST artifact yet - skipped.)" }

try {
  gh issue list --label claude-dast --state all --limit 200 `
    --json number,title,state,labels,body |
    Out-File -Encoding utf8 "$OutDir/dast-claude-issues.json"
} catch { }

Write-Host "`n[4/4] Done. Files in '$OutDir':"
Get-ChildItem -Recurse $OutDir | Select-Object FullName, Length | Format-Table -AutoSize
