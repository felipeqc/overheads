from os import getenv, path, listdir, remove
from scipy.stats import scoreatpercentile
import random
import numpy
import subprocess
from overhead_util import *
from overhead_params import *

#
# split_traces()
# Read binary ft_trace files and separate traces by type of overhead
#
def split_traces():
    create_dir(SPLIT_DIR)

    trace_id = 0
    for trace_file in listdir(TRACES_DIR):
        trace_id += 1

        taskset_file = get_config(trace_file) + ".ats"
        tasks_per_cpu = get_tasks_per_cpu(path.join(TASKSETS_DIR, taskset_file)) # Get number of tasks in each cpu
        params = decode(get_config(taskset_file))

        for cpu in range(CPUS):
            # Split trace files by type of overhead (counting by partition)

            for ev in events: # Normal events
                split_fname = 'trace_id=%d_scheduler=%s_n=%s_overhead=%s.ft' % (trace_id, params['scheduler'], tasks_per_cpu[cpu], ev)
                split_path = path.join(SPLIT_DIR, split_fname)
                ft2csv_path = 'ft2csv -o %d %s %s > %s' % (cpu, ev, path.join(TRACES_DIR, trace_file), split_path)
                try:
                    proc = subprocess.Popen(ft2csv_path, shell=True, stdout=subprocess.PIPE)
                    proc.wait()
                    if path.getsize(split_path) == 0:
                        remove(split_path)
                except OSError as (msg):
                    raise OSError("Could not split trace file '%s': %s" % (split_fname, msg))

            for ev in be_events: # BE events
                split_fname = 'trace_id=%d_scheduler=%s_n=%s_overhead=%s.ft' % (trace_id, params['scheduler'], tasks_per_cpu[cpu], ev)
                split_path = path.join(SPLIT_DIR, split_fname)
                ft2csv_path = 'ft2csv -b -o %d %s %s > %s' % (cpu, ev, path.join(TRACES_DIR, trace_file), split_path)
                try:
                    proc = subprocess.Popen(ft2csv_path, shell=True, stdout=subprocess.PIPE)
                    proc.wait()
                    if path.getsize(split_path) == 0:
                        remove(split_path)
                except OSError as (msg):
                    raise OSError("Could not create taskset '%s': %s" % (fname, msg))

#
# join_and_sort()
# Join split traces in one file (in sorted order)
#
def join_and_sort():
    create_dir(COMPLETED_DIR)

    trace_files = organize_trace_files(SPLIT_DIR) # Organize trace files by scheduler, number of tasks and overhead

    for sched in trace_files.keys(): # For each scheduler
        for overhead in trace_files[sched].keys(): # For each type of overhead
            for n in trace_files[sched][overhead].keys(): # For each number of tasks
                seq = []

                # Group traces into one file

                for fname in trace_files[sched][overhead][n]:
                    ft2csv_to_list(seq, path.join(SPLIT_DIR, fname))

                seq.sort() # Sort traces

                completed_file = 'trace_scheduler=%s_n=%s_overhead=%s.ft' % (sched, n, overhead)
                list_to_tracefile(seq, path.join(COMPLETED_DIR, completed_file))

#
# remove_outliers_and_create_model():
# Use IQR to remove outliers and create overhead model
#
def remove_outliers_and_create_model():
    create_dir(MODEL_DIR)

    # Group files by type of overhead
    trace_files = organize_filtered_files(COMPLETED_DIR)

    for sched in trace_files.keys():
        for overhead in trace_files[sched].keys():
            fname = 'model_scheduler=%s_overhead=%s' % (sched, overhead)
            try:
                f = open(path.join(MODEL_DIR, fname), 'w')

                for n in iter(sorted(trace_files[sched][overhead].iterkeys())):
                    print 'Reading', trace_files[sched][overhead][n], '.'

                    seq = numpy.fromfile(path.join(COMPLETED_DIR, trace_files[sched][overhead][n]), dtype=numpy.int32, sep='\n')

                    # Remove outliers
                    samples = len(seq)
                    (seq, mincutoff, maxcutoff) = apply_iqr(seq, 1.5)
                    filtered_samples = len(seq)

                    output = {}

                    output['scheduler'] = sched
                    output['overhead_type'] = overhead
                    output['number_of_tasks'] = int(n)
                    output['number_of_samples'] = samples
                    output['number_of_filtered_samples'] = filtered_samples
                    output['maximum_overhead'] = cycles_to_ms(numpy.max(seq))
                    output['average_overhead'] = cycles_to_ms(numpy.mean(seq))
                    output['minimum_overhead'] = cycles_to_ms(numpy.min(seq))
                    output['median_overhead'] = cycles_to_ms(numpy.median(seq))
                    output['standard_deviation'] = cycles_to_ms(numpy.std(seq))
                    output['variance'] = cycles_to_ms(cycles_to_ms(numpy.var(seq))) # unit is squared
                    output['maximum_cutoff'] = cycles_to_ms(maxcutoff) # maxcutoff
                    output['minimum_cutoff'] =  cycles_to_ms(mincutoff) # mincutoff

                    f.write('%s\t%s\t%d\t%d\t%d\t%.12e\t%.12e\t%.12e\t%.12e\t%.12e\t%.12e\t%.12e\t%.12e\n' % (output['scheduler'],  output['overhead_type'], output['number_of_tasks'], output['number_of_samples'], output['number_of_filtered_samples'], output['maximum_overhead'], output['average_overhead'], output['minimum_overhead'], output['median_overhead'], output['standard_deviation'], output['variance'], output['maximum_cutoff'], output['minimum_cutoff']))

                f.close()
            except IOError as (msg):
                raise IOError("Could not write model file '%s': %s" % (fname, msg))

if __name__ == '__main__':
    random.seed()

    #split_traces()
    #join_and_sort()
    remove_outliers_and_create_model()
