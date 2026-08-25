<?php

define( 'DVWA_WEB_PAGE_TO_ROOT', '' );
require_once DVWA_WEB_PAGE_TO_ROOT . 'dvwa/includes/dvwaPage.inc.php';

dvwaPageStartup( array( 'authenticated') );

// INFO_ENVIRONMENT/INFO_VARIABLES are excluded: they dump $_SERVER, which
// leaks the container's internal network address. This page is a plain
// diagnostic utility (not one of the vulnerabilities/ labs), so there's no
// teaching value in that leak - just information a real deployment
// wouldn't want handed out.
phpinfo( INFO_GENERAL | INFO_CREDITS | INFO_CONFIGURATION | INFO_MODULES | INFO_LICENSE );

?>
