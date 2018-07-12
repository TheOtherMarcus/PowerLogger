#!/usr/bin/python

from datetime import datetime
import time
import sys
import os
import socket
import requests
import sqlite3

import Adafruit_CharLCD as LCD

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# GPIO pins
button_pin = 16
sensor_pin = 10

# Power meter blinks per kWh
bpkwh = 1000.0
ampere = 16.0

# Raspberry Pi pin configuration:
lcd_rs        = 25
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 21
lcd_d7        = 22
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

remote = ""
user = ""
passwd = ""
# Command line parameters
sys.argv = sys.argv[1:]
while len(sys.argv) > 1:
    if sys.argv[0] == "-remote":
        remote = sys.argv[1]
        sys.argv = sys.argv[2:]
    elif sys.argv[0] == "-user":
        user = sys.argv[1]
        sys.argv = sys.argv[2:]
    elif sys.argv[0] == "-passwd":
        passwd = sys.argv[1]
        sys.argv = sys.argv[2:]
    else:
        print "usage: powermon.py [-remote server:port] powerlog"
        exit()
logdir = sys.argv[0]


# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)
lcd.set_backlight(0);

# Setup GPIO
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sensor_pin, GPIO.IN)

# Setup the database
conn = sqlite3.connect(logdir + '.sqlite')
c = conn.cursor()
c.execute("pragma journal_mode = WAL");
c.execute("create table if not exists blink (time integer unique)")
c.execute("create view if not exists wh as select a.time as time, (select max(b.time) - (select max(c.time) from blink c where c.time < max(b.time)) from blink b where b.time < a.time) as prev_interval, a.time - (select max(b.time) from blink b where b.time < a.time) as interval, (select min(b.time) from blink b where b.time > a.time) - a.time as next_interval from blink a where interval*2 > prev_interval or interval*2 > next_interval");
conn.commit()
conn.close()

# Find out the IP address
def get_ip():
    ip = ""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",53))
        ip = s.getsockname()[0]
        s.close()
    except:
        None
    return ip

# Show ip immediately
ip = get_ip()
lcd.message(ip +"\n\n")

# Logfile
logfile = None

# Blinks in current logfile. Each file will have bpkwh+1 time entries
# to cover a whole kwh. The first entry in the next file will be the
# last in the previous.
bif = -1

# Timekeeper
blinktime = 0

# Sensor interrupt
def sensor_isr(channel):
    global blinktime, logfile, bpkwh, bif, ip
    now = time.time()
    print "Blink"

    # Display logic
    w = str(0)
    if blinktime != 0:
        w = str(3600*1000/bpkwh/(now-blinktime))
        print "Usage: " + w
        lcd.clear()
        lcd.message(ip + "\n" + time.strftime("%H:%M:%S", time.localtime(now)) + " " + w.split(".")[0] + " W" + "\n")
    blinktime = now

    # Logging
    if bif > 0: # Keep on logging in existing file
        logfile.write(repr(now) + "\n")
        logfile.flush()
    bif = bif + 1
    if bif > bpkwh: # We want one extra blink time per file
        logfile.close()
        bif = 0
    if bif == 0: # Log to new file
        logfile = file(logdir + "/" + datetime.fromtimestamp(now).isoformat(), 'w+b')
        logfile.write(repr(now) + "\n")
        bif = bif + 1
        # Time to see if IP has changed
        ip = get_ip()

    # sqlite logging
    conn = sqlite3.connect(logdir + '.sqlite')
    c = conn.cursor()
    c.execute("insert into blink values (?)", (int(now*1000),) )
    conn.commit()
    conn.close()
    
    # Remote logging to ctrl-home
    if len(remote) > 0:
        print "http://" + remote + "/tail"
        r = requests.post("http://" + remote + "/tail", auth=requests.auth.HTTPBasicAuth(user, passwd),
                          data={'id': "power", 'legend': ':Wh:W', 'value': "1 " + w})
        print(r.status_code, r.reason)
        
GPIO.add_event_detect(sensor_pin, GPIO.RISING, callback=sensor_isr, bouncetime=int(1000*1000/bpkwh*3600/(244*ampere*3)))

try:
    while True:
        GPIO.wait_for_edge(button_pin, GPIO.FALLING)
        lcd.set_backlight(1)
        time.sleep(0.5)
        while not GPIO.input(button_pin):
            time.sleep(0.1)
        lcd.set_backlight(0)
except KeyboardInterrupt:
    GPIO.cleanup()
    if logfile != None:
        logfile.close()

GPIO.cleanup()
if logfile != None:
    logfile.close()
