from os import getenv, path, listdir, remove, makedirs
from scipy.stats import scoreatpercentile
import re
import random
import bisect
import numpy
import subprocess
import xml.dom.minidom as minidom
from overhead_params import *

OVERHEADS_DIR = getenv('OVERHEADS', '/home/felipe/overheads')
TASKSETS_DIR = path.join(OVERHEADS_DIR, 'tasksets')
TRACES_DIR = path.join(OVERHEADS_DIR, 'traces')
SPLIT_DIR = path.join(OVERHEADS_DIR, 'split')
COMPLETED_DIR = path.join(OVERHEADS_DIR, 'completed')
FILTERED_DIR = path.join(OVERHEADS_DIR, 'filtered')
MODEL_DIR = path.join(OVERHEADS_DIR, 'model')
OVSET_DIR = path.join(OVERHEADS_DIR, 'ovset')

def get_tasks_per_cpu(taskset_file):
    tasks_per_cpu = [0 for x in range(CPUS)]

    try:
        taskset = minidom.parse(taskset_file)
    except IOError as (msg):
        raise IOError("Could not read task set file: %s", (msg))

    for task in taskset.getElementsByTagName("task"): # For each task
        if not task.getAttribute("slices"):
            cpu = int(task.getAttribute("cpu"))
            tasks_per_cpu[cpu] += 1
        else:
            for slice in task.getElementsByTagName("slice"): # For each slice
                slice_cpu = int(slice.getAttribute("cpu"))
                tasks_per_cpu[slice_cpu] += 1
    return tasks_per_cpu

def decode(name):
    params = {}
    parts = re.split('_(?!RESCHED|LATENCY|TIMER)', name) # Fix for event names with underscore
    for p in parts:
        kv = p.split('=')
        k = kv[0]
        v = kv[1] if len(kv) > 1 else None
        params[k] = v
    return params

def get_config(fname):
    return path.splitext(path.basename(fname))[0]  

def organize_trace_files(path):
    trace_files = {}
    for tfile in listdir(path):
        params = decode(get_config(tfile))
        sched = params['scheduler']
        overhead = params['overhead']
        n = params['n']

         # The list hasn't been created yet
        if not trace_files.has_key(sched):
            trace_files[sched] = {}
        if not trace_files[sched].has_key(overhead):
            trace_files[sched][overhead] = {}
        if not trace_files[sched][overhead].has_key(n):
            trace_files[sched][overhead][n] = []

        trace_files[sched][overhead][n].append(tfile)
    return trace_files

def organize_by_overhead(path):
    trace_files = {}
    for tfile in listdir(path):
        params = decode(get_config(tfile))
        overhead = params['overhead']

         # The list hasn't been created yet
        if not trace_files.has_key(overhead):
            trace_files[overhead] = []

        trace_files[overhead].append(tfile)
    return trace_files

def create_dir(dirpath):
    try:
        if not path.exists(dirpath):
            makedirs(dirpath)
    except OSError as (msg):
        raise OSError ("Could not create overhead directory: %s", (msg))

def ft2csv_to_list(seq, path):
    try:
        f = open(path, 'r')

        line = f.readline()
        while line:
            seq.append(int(line.split(', ')[2]))
            line = f.readline()
        f.close()
    except IOError as (msg):
        raise IOError("Could not read trace file '%s': %s" % (fname, msg))

# Basic binary search operations:
# Based on http://docs.python.org/library/bisect.html
def find_lt(a, x):
    'Find rightmost value less than x'
    i = bisect.bisect_left(a, x)
    if i:
        return i-1
    else:
        return None

def find_gt(a, x):
    'Find leftmost value greater than x'
    i = bisect.bisect_right(a, x)
    if i != len(a):
        return i
    else:
        return None

def apply_iqr(seq, extent = 1.5):
    # Apply IQR filter
    # Parameter seq is an ordered list of values

    q1 =  scoreatpercentile(seq, 25)
    q3 =  scoreatpercentile(seq, 75)
    iqr = q3 - q1

    start = 0 
    end = len(seq) - 1
        
    l = find_lt(seq, q1 - extent*iqr) # Rightmost element to exclude
    if l is not None:
        start = l + 1

    r = find_gt(seq, q3 + extent*iqr) # Leftmost element to exclude
    if r is not None:
        end = r - 1

    seq = seq[start:end+1] # Apply filter

    return (seq, q1 - extent*iqr, q3 + extent*iqr) # Return seq, mincutoff, maxcutoff

def tracefile_to_list(seq, path):
    try:
        f = open(path, 'r')

        line = f.readline()
        while line:
            seq.append(int(line))
            line = f.readline()
        f.close()
    except IOError as (msg):
        raise IOError("Could not read trace file '%s': %s" % (path, msg))

def list_to_tracefile(seq, path):
    try:
        f = open(path, 'w')

        # write values
        for value in seq:
            f.write('%d\n' % (value));
        f.close()
    except IOError as (msg):
        raise IOError("Could not write trace file '%s': %s" % (path, msg))

def organize_filtered_files(path):
    trace_files = {}
    for tfile in listdir(path):
        params = decode(get_config(tfile))
        sched = params['scheduler']
        overhead = params['overhead']
        n = params['n']

        if len(n) == 1:
            n = '0' + n

         # The list hasn't been created yet
        if not trace_files.has_key(sched):
            trace_files[sched] = {}
        if not trace_files[sched].has_key(overhead):
            trace_files[sched][overhead] = {}

        trace_files[sched][overhead][n] = tfile
    return trace_files

def cycles_to_ms(c):
    return c / (CLOCK * 1000.0)
