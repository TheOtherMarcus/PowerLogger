# PowerLogger
This repo contains the software for the power logger descibed at http://formallanguage.blogspot.se/2017/04/power-logger.html.

The software monitors the sensor GPIO and writes a timestamp to a log file for every registered blink. A new log file is created at every 1000 blinks. The first timestamp in the new file is the same as the last timestamp in the previous file. A timestamp records the number of seconds since epoch.

It is possible to draw a PNG graph for a time period with a selectable sample resolution. Data can also be exported to a CSV file. These functions are accessed using a Web frontend.

The software runs on a standard Raspbian installation.

### LCD Support
```
sudo apt-get install python-dev
sudo apt-get install python-setuptools
sudo easy_install -U distribute
sudo apt-get install python-pip
sudo pip install rpi.gpio
sudo pip install adafruit-charlcd
```

### Backend
```
sudo pip install numpy matplotlib
wget https://raw.githubusercontent.com/TheOtherMarcus/PowerLogger/master/backend/powermon.py
wget https://raw.githubusercontent.com/TheOtherMarcus/PowerLogger/master/backend/powergraph.py
wget https://raw.githubusercontent.com/TheOtherMarcus/PowerLogger/master/backend/powerlist.py
wget https://raw.githubusercontent.com/TheOtherMarcus/PowerLogger/master/backend/logreader.py
chmod +x powermon.py powergraph.py powerlist.py
mkdir powerlog
crontab -e
```
Add the following line to the crontab.
```
@reboot /home/pi/powermon.py &
```

### Frontend
```
sudo apt-get install apache2 php5 libapache2-mod-php5
cd /var/www/html
sudo mv index.html index.debian
sudo wget https://raw.githubusercontent.com/TheOtherMarcus/PowerLogger/master/frontend/index.php
sudo mkdir graphs
udo chmod 777 graphs
```

