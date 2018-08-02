#!/usr/bin/python

from datetime import datetime
import time
import sys
import os
import socket
import sqlite3

import Adafruit_CharLCD as LCD

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

# GPIO pins
button_pin = 16
sensor_pin = 10

# Power meter blinks per kWh
bpkwh = 1000.0

# Used for interrrupt bounce time calculation
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

# Sqlite database
db = sys.argv[1]

# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)
lcd.set_backlight(0);

# Setup GPIO
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(sensor_pin, GPIO.IN)

# Setup the database
conn = sqlite3.connect(db)
c = conn.cursor()
c.execute("pragma journal_mode = WAL");
c.execute("create table if not exists blink (time integer unique)")

# Use blinks unchanged
c.execute("create view if not exists wh as select a.time as time from blink a");

# Alternative filter for spurious blinks
#c.execute("create view if not exists wh as select a.time as time, (select max(b.time) - (select max(c.time) from blink c where c.time < max(b.time)) from blink b where b.time < a.time) as prev_interval, a.time - (select max(b.time) from blink b where b.time < a.time) as interval, (select min(b.time) from blink b where b.time > a.time) - a.time as next_interval from blink a where interval*2 > prev_interval or interval*2 > next_interval");

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
blinks = 0
ip = get_ip()
lcd.message(ip +"\n\n")

# Timekeeper
blinktime = 0

# Sensor interrupt
def sensor_isr(channel):
    global blinktime, bpkwh, blinks, ip
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

    # sqlite logging
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute("insert into blink values (?)", (int(now*1000),) )
    conn.commit()
    conn.close()
    
    blinks = blinks + 1
    if blinks % 1000 == 0:
        # Time to update IP
        ip = get_ip()


GPIO.add_event_detect(sensor_pin, GPIO.FALLING, callback=sensor_isr, bouncetime=int(1000*1000/bpkwh*3600/(244*ampere*3)))

try:
    while True:
        GPIO.wait_for_edge(button_pin, GPIO.FALLING)
        lcd.set_backlight(1)
        # Debounce time
        time.sleep(0.5)
        # Wait here while button pressed
        while not GPIO.input(button_pin):
            time.sleep(0.1)
        lcd.set_backlight(0)
except KeyboardInterrupt:
    GPIO.cleanup()

GPIO.cleanup()
