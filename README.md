# PowerLogger
This repo contains the software for the power logger descibed at http://formallanguage.blogspot.se/2017/04/power-logger.html.

The software monitors the sensor GPIO and writes a timestamp to a sqlite database for each registered blink. A timestamp records the number of milliseconds since epoch.

It is possible to draw a PNG graph for a time period with a selectable sample resolution. Data can also be exported to a CSV file. These functions are accessed using a Web frontend.

The software runs on a standard Raspbian installation. For headless wifi configuration see https://davidmaitland.me/2015/12/raspberry-pi-zero-headless-setup/.

### Timezone
```
sudo dpkg-reconfigure tzdata
```

### LCD Support
```
sudo apt-get install git build-essential python-dev python-smbus python-pip
sudo pip install rpi.gpio
git clone https://github.com/adafruit/Adafruit_Python_CharLCD.git
cd Adafruit_Python_CharLCD
sudo python setup.py install
```

### Backend
```
sudo apt-get install sqlite3 python-requests python-numpy python-scipy python-matplotlib ipython python-pandas python-sympy python-nose
wget https://raw.githubusercontent.com/TheOtherMarcus/PowerLogger/master/backend/powermon.py
wget https://raw.githubusercontent.com/TheOtherMarcus/PowerLogger/master/backend/powergraph.py
wget https://raw.githubusercontent.com/TheOtherMarcus/PowerLogger/master/backend/powerlist.py
wget https://raw.githubusercontent.com/TheOtherMarcus/PowerLogger/master/backend/logreader.py
chmod +x powermon.py powergraph.py powerlist.py
chmod aug+rwx .
touch powerlog.sqlite
chmod aug+rw powerlog.sqlite
crontab -e
```
Add the following line to the crontab.
```
@reboot /home/pi/powermon.py powerlog &
```
Reboot to start power monitoring.

### Frontend
```
sudo apt-get install apache2 php libapache2-mod-php
cd /var/www/html
sudo mv index.html index.debian
sudo wget https://raw.githubusercontent.com/TheOtherMarcus/PowerLogger/master/frontend/index.php
sudo wget https://raw.githubusercontent.com/TheOtherMarcus/PowerLogger/master/frontend/csv.php
sudo mkdir graphs
sudo chmod aug+rwx graphs
```

The first access takes forever as matplotlib renders fonts.
