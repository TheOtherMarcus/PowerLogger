# PowerLogger
This repo contains the software for the power logger descibed at http://formallanguage.blogspot.se/2017/04/power-logger.html.

The software monitors the sensor GPIO and writes a timestamp to a log file for every registered blink. A new log file is created at every 1000 blinks. The first timestamp in the new file is the same as the last timestamp in the previous file. A timestamp records the number of seconds since epoch.

The software runs on a standard Raspbian installation.

### Backend

### Frontend

