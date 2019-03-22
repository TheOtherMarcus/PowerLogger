<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="utf-8">
</head>

<body>

  <?php
     function graph($duration, $interval) {
       if ($duration == "1") $label = "Now";
       if ($duration == "60") $label = "Last Minute";
       if ($duration == "3600") $label = "Last Hour";
       if ($duration == "86400") $label = "Last 24 Hours";
       if ($duration == "604800") $label = "Last Week";
       if ($duration == "2628000") $label = "Last Month";
       if ($duration == "31536000") $label = "Last Year";
       if ($duration == "3153600000") $label = "Last 100 Years";
       print "<h3>" . $label . ": &nbsp; ";
       $rows = explode("\n", shell_exec("~pi/powergraph.py " . $duration . " " . $interval . " /var/www/html/graphs/" . $duration . ".png ~pi/powerlog.sqlite"));
       foreach ($rows as $row) {
         if ("+" != substr($row, 0, 1)) {
           print $row . " &nbsp; ";
         }
       }
       print "</h3><img src=\"graphs/" . $duration . ".png\"/>";
     }
  ?>

<form action="." method="get">
~| Duration:
  <select name="duration">
    <option value="10">Last 10 Seconds</option>
    <option value="60">Last Minute</option>
    <option value="3600" selected>Last Hour</option>
    <option value="86400">Last 24 Hours</option>
    <option value="604800">Last Week</option>
    <option value="2628000">Last Month</option>
    <option value="31536000">Last Year</option>
    <option value="3153600000">Last 100 Years</option>
  </select>
  Interval:
  <select name="interval">
    <option value="10" selected>10 Seconds</option>
    <option value="60">1 Minute</option>
    <option value="3600">1 Hour</option>
    <option value="86400">24 Hours</option>
    <option value="604800">1 Week</option>
    <option value="2628000">1 Month</option>
    <option value="31536000">1 Year</option>
  </select>
  <button type="submit">Draw Graph</button> |~
</form>

<?php graph($_GET["duration"], $_GET["interval"]); ?>

<form action="csv.php" method="get">
~| Duration:
  <select name="duration">
    <option value="10">Last 10 Seconds</option>
    <option value="60">Last Minute</option>
    <option value="3600" selected>Last Hour</option>
    <option value="86400">Last 24 Hours</option>
    <option value="604800">Last Week</option>
    <option value="2628000">Last Month</option>
    <option value="31536000">Last Year</option>
    <option value="3153600000">Last 100 Years</option>
  </select>
  Interval:
  <select name="interval">
    <option value="10" selected>10 Seconds</option>
    <option value="60">1 Minute</option>
    <option value="3600">1 Hour</option>
    <option value="86400">24 Hours</option>
    <option value="604800">1 Week</option>
    <option value="2628000">1 Month</option>
    <option value="31536000">1 Year</option>
  </select>
  <button type="submit">Get CSV</button> |~
</form>

</body>

</html>
