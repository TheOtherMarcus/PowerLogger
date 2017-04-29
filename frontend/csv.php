<?php

header('Content-Type:text/csv');
header('Content-Disposition:attachment;filename=' . $_GET["duration"] . '.csv');
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");

system("~pi/powerlist.py " . $_GET["duration"] . " " . $_GET["interval"] . " ~pi/powerlog");

?>
