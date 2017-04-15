
import glob
import os

def blinks(logdir):
    filenames = glob.glob(logdir + "/*")
    filenames.sort(key=os.path.getmtime)
    start = 0
    for filename in reversed(filenames):
        with open(filename) as f:
            lines = list(reversed(f.readlines()))
            for line in lines[start:]:
                yield float(line)
            start = 1
            
def filtered_blinks(logdir):
    i = blinks(logdir)
    bs = list()
    bs.append(i.next())
    yield bs[0]
    bs.append(i.next())
    yield bs[1]
    bs.append(i.next())
    bs.append(i.next())
    bs.append(i.next())
    for b in i:
        t = min(bs[0] - bs[1], bs[3] - bs[4])
        v = min(bs[1] - bs[2], bs[2] - bs[3])
        if 2*v < t:
            # Remove spurious blink
            del bs[2]
        else:
            yield bs[2]
            del bs[0]
        bs.append(b)

