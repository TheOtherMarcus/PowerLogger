#!/usr/bin/python

import time
import sys
from datetime import datetime
from logreader import filtered_blinks

bpkwh = 1000.0
ampere = 16.0

duration = int(sys.argv[1])
interval = int(sys.argv[2])
logdir=sys.argv[3]

bs = filtered_blinks(logdir)
e = bs.next()
cut = e
last = e
c = 0

for s in bs:
    c = c + 1
    w = 3600.0*1000/(bpkwh/c)/(e-s)
    if interval < cut-s:
        print str(datetime.fromtimestamp((e+s)/2)) + "," + str(w) + "," + str(1.0*c/bpkwh)
        e = s
        cut = cut - interval
        c = 0
    if (last-s) > duration:
        break    
if c != 0 and w < 3*244*ampere:
    print str(datetime.fromtimestamp((e+s)/2)) + "," + str(w) + "," + str(1.0*c/bpkwh)
