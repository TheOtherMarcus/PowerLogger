#!/usr/bin/python

import sqlite3
import time
import sys
from datetime import datetime
from logreader import filtered_blinks

duration = int(sys.argv[1])
interval = int(sys.argv[2])
logdir=sys.argv[3]

conn = sqlite3.connect(logdir + ".sqlite")

c = conn.cursor()
for row in c.execute("select max(a.time), 3600.0*1000*count(a.time)/(max(a.time) - (select max(b.time) from wh b where b.time < min(a.time))), count(a.time)/1000.0, ((select max(d.time) from wh d) - a.time)/(?*1000) as bin from wh a where a.time > ((select max(c.time) from wh c) - ?*1000) group by bin order by max(a.time)", (interval, duration)):
    print str(datetime.fromtimestamp(row[0]/1000.0)) + "," + str(row[1]) + "," + str(row[2])

conn.commit()
conn.close()

