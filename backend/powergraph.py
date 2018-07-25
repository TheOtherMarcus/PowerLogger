#!/usr/bin/python

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import time
import sys
from datetime import datetime
import glob
import os
from logreader import filtered_blinks
import sqlite3

duration = int(sys.argv[1])
interval = int(sys.argv[2])
graph = sys.argv[3]
logdir=sys.argv[4]

x = list()
y = list()

conn = sqlite3.connect(logdir + ".sqlite")

c = conn.cursor()
for row in c.execute("select max(a.time), ifnull(3600.0*1000*count(a.time)/(max(a.time) - (select max(b.time) from wh b where b.time < min(a.time))), 0), ((select max(d.time) from wh d) - a.time)/(?*1000) as bin from wh a where a.time > ((select max(c.time) from wh c) - ?*1000) group by bin order by max(a.time)", (interval, duration)):
    x = x + [datetime.fromtimestamp(row[0]/1000.0)]
    y = y + [row[1]]
conn.commit()

c = conn.cursor()
for row in c.execute("select max(a.time), ifnull(3600.0*1000*count(a.time)/(max(a.time) - (select max(b.time) from wh b where b.time < min(a.time))), 0), count(a.time)/1000.0, ifnull(3600.0*1000*count(a.time)/(max(a.time) - (select max(b.time) from wh b where b.time < min(a.time))), 0)*24*365/1000, ((select max(d.time) from wh d) - a.time)/(?*1000) as bin from wh a where a.time > ((select max(c.time) from wh c) - ?*1000) group by bin order by max(a.time)", (duration, duration)):
    print str(int(row[1])) + " W"
    print str(row[2]) + " kWh"
    print str(int(row[3])) + " kWh/year"
conn.commit()

plt.plot(list(reversed(x)), list(reversed(y)))
plt.gcf().autofmt_xdate()
plt.savefig(graph)
