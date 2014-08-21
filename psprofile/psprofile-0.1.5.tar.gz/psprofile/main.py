from __future__ import division
import time
from collections import OrderedDict, defaultdict
import os
import signal
import sys
import psutil

from .util import mean, max, poll_children


def main(command, poll_interval, shell):
    try:
        # Declare data store variables
        records = defaultdict(list)
        output = OrderedDict()
        for place_holder in ['percent_cpu', 'wall_time', 'cpu_time', 'avg_rss_mem_kb', 'avg_vms_mem_kb', 'max_rss_mem_kb', 'max_vms_mem_kb']:
            output[place_holder] = None

        # Run the command and do the polling
        start_time = time.time()
        proc = psutil.Popen(' '.join(command), shell=shell)
        num_polls = 0
        while proc.poll() is None:
            num_polls += 1
            for name, value in poll_children(proc):
                if name in ['rss_mem_kb', 'vms_mem_kb', 'num_threads', 'num_fds']:
                    # TODO consolidate values to avoid using too much ram.  need to save max to do this
                    # if num_polls % 3600 == 0:
                    # records[name] = [_mean(records[name])]

                    records[name].append(value)
                else:
                    output[name] = int(value)

            time.sleep(poll_interval)

    except KeyboardInterrupt:
        print >> sys.stderr, 'Caught a SIGINT (ctrl+c), terminating'
        os.kill(proc.pid, signal.SIGINT)

    # Get means and maxes
    for name in ['rss_mem_kb', 'vms_mem_kb', 'num_threads', 'num_fds']:
        output['avg_%s' % name] = mean(records[name])
        output['max_%s' % name] = max(records[name])

    # Calculate some extra fielsd
    output['exit_status'] = proc.poll()
    end_time = time.time()  # waiting till last second
    output['num_polls'] = num_polls
    output['wall_time'] = int(end_time - start_time)
    if output.get('cpu_time'):
        output['percent_cpu'] = int(round(float(output.get('cpu_time', 0) / float(output['wall_time']), 2) * 100))
    else:
        output['percent_cpu'] = 0
    output['cpu_time'] = output.get('user_time', 0) + output.get('system_time', 0)

    return output