from os import path, listdir
import numpy
import pickle
from overhead_util import *
from alloc_overhead import *

def main():
    create_dir(OVSET_DIR)

    overheads = {}

    for fname in listdir(MODEL_DIR):
        params = decode(get_config(path.join(MODEL_DIR, fname)))
        sched = params['scheduler']
        overheadtype = params['overhead']

        if not overheads.has_key(sched):
            overheads[sched] = OverheadSet()

        overheads[sched].createOverhead(overheadtype) # This method doesn't overwrite the data

        try:
            f = open(path.join(MODEL_DIR, fname), 'r')

            line = f.readline()
            while line:
                split_line = line.split()
                x, y = int(split_line[2]), float(split_line[5])
                overheads[sched].addValue(overheadtype, x, y)
                line = f.readline()
            f.close()
        except IOError as (msg):
            raise IOError("Could not read model file '%s': %s" % (fname, msg))

    for sched, overheadset in overheads.items():
        try:
            outputfile = open(path.join(OVSET_DIR, '%s.ovset' % sched), 'w')
            pickle.dump(overheadset, outputfile)
        except IOError as (msg):
            raise IOError("Could not write overheadset file '%s': %s" % (fname, msg))

if __name__ == '__main__':
    main()
