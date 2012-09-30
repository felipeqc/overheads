from os import path, listdir
import numpy
from overhead_util import *

def force_mono_inc(l):
    # Change the sequence to make it monotonically increasing
    for i in range(1, len(l)):
        if l[i] < l[i-1]:
            l[i] = l[i-1]

def read_max():
    max_x = {}
    max_y = {}

    for fname in listdir(MODEL_DIR):
        params = decode(get_config(path.join(MODEL_DIR, fname)))
        sched = params['scheduler']
        overhead = params['overhead']

        if not max_x.has_key(sched):
            max_x[sched] = {}
        if not max_y.has_key(sched):
            max_y[sched] = {}

        max_x[sched][overhead] = []
        max_y[sched][overhead] = []

        try:
            f = open(path.join(MODEL_DIR, fname), 'r')

            line = f.readline()
            while line:
                split_line = line.split()
                max_x[sched][overhead].append(int(split_line[2]))
                max_y[sched][overhead].append(float(split_line[5]))
                line = f.readline()
            f.close()
        except IOError as (msg):
            raise IOError("Could not read model file '%s': %s" % (fname, msg))

        # Force the sequence to be monotonically increasing
        force_mono_inc(max_y[sched][overhead])

    return (max_x, max_y)

def main():
    # Group files by type of overhead
    (max_x, max_y) = read_max()

    for sched in max_x.keys():
        print 'Scheduler:', sched
        for overhead in max_x[sched].keys():
            if overhead != 'SCHED' and overhead != 'SCHED2':
                print overhead
                print '{',
                for n in range(1, 81):
                    print str(numpy.interp(n, max_x[sched][overhead], max_y[sched][overhead])) + ',',
                print '}'

        print 'SCHED'
        print '{',
        for n in range(1, 81):
            print str(numpy.interp(n, max_x[sched]['SCHED'], max_y[sched]['SCHED']) + numpy.interp(n, max_x[sched]['SCHED2'], max_y[sched]['SCHED2'])) + ',',
        print '}'

        print "\n"

if __name__ == '__main__':
    main()
