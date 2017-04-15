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

bpkwh = 1000.0
ampere = 16.0

duration = int(sys.argv[1])
interval = int(sys.argv[2])
graph = sys.argv[3]
logdir=sys.argv[4]

bs = filtered_blinks(logdir)
e = bs.next()
cut = e
last = e
x = list()
y = list()
c = 0
blink = 0

for s in bs:
    c = c + 1
    blink = blink + 1
    w = 3600.0*1000/(bpkwh/c)/(e-s)
    if interval < cut-s:
        x = x + [datetime.fromtimestamp((e+s)/2)]
        y = y + [w]
        e = s
        cut = cut - interval
        c = 0
    if (last-s) > duration:
        break    
if c != 0 and w < 3*244*ampere:
    x = x + [datetime.fromtimestamp((e+s)/2)]
    y = y + [w]

print "+" + str(last-s)

print str(1000.0*3600*blink/bpkwh/(last-s)).split('.')[0] + " W"
print str(1.0*blink/bpkwh) + " kWh"
print str(1.0*blink/bpkwh*(365*24*3600)/(last-s)).split('.')[0] + " kWh/year"

plt.plot(list(reversed(x)), list(reversed(y)))
plt.gcf().autofmt_xdate()
plt.savefig(graph)
