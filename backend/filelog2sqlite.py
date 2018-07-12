#!/usr/bin/python

import time
import sys
from datetime import datetime
from logreader import blinks
import sqlite3

logdir=sys.argv[1]

conn = sqlite3.connect(logdir + ".test_sqlite")
c = conn.cursor()
c.execute("create table if not exists blink (time integer unique)")
conn.commit()

c = conn.cursor()
c = conn.cursor()
i = 0
for s in blinks(logdir):
    print repr(s) + " " + str(datetime.fromtimestamp(s))
    try:
        c.execute("insert into blink values (?)", (s,))
    except sqlite3.Error as e:
        print "Database error: %s" % e
    if i % 1000 == 0:
        conn.commit()
        c = conn.cursor()
    i = i + 1

conn.close()
