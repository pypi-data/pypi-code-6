# coding=utf8

"""
bell.analyzer
~~~~~~~~~~~~~
"""

import imp
import sys
import time
from threading import Thread

if sys.version_info[0] < 3:
    from Queue import Queue
else:
    from queue import Queue

import numpy

from bell.base import serve_wrapper, Service
from bell.configs import configs
from bell.logger import logger
from bell.signals import anomaly_detected, analyzation_done, datapoint_reserved
from bell.utils import pickle


class Analyzer(Service):

    name = 'analyzer'

    def __init__(self):
        super(Analyzer, self).__init__()
        self.beans = None
        self.ssdb = None
        self.hook_thread = None

    def initialize(self):
        self.initialize_logger()
        self.ssdb = self.initialize_ssdb()
        self.beans = self.initialize_beans(as_watcher=True)
        self.initialize_hooks()

    def initialize_hooks(self):
        hooks_enable = configs['hooks']['enable']
        hooks_script = configs['hooks']['script']
        self.hook_thread = HookThread()
        if hooks_enable:
            imp.load_source('bell.hooks', hooks_script)
            self.hook_thread.start()

    def zset_name(self, series_name):
        zset_prefix = configs['ssdb']['series']['zsets']['namePrefix']
        return zset_prefix + series_name

    def reserve(self):
        job = self.beans.reserve()
        return job

    def filter(self, zset, timestamp):
        offset = configs['analyzer']['filterOffset']
        periodicity = configs['analyzer']['periodicity']
        timespan = offset * periodicity

        series = []
        while 1:
            start, stop = timestamp - timespan, timestamp + timespan
            lst = self.ssdb.zkeys(zset, '', start, stop, -1)
            if not lst:
                break
            else:
                series.extend(lst)
                timestamp -= periodicity
        return series  # [key1, key2 ..]

    def append(self, zset, datapoint):  # datapoint: (time, value, is_anomaly)
        timestamp, value, is_anomaly = datapoint
        score = int(timestamp)
        key = '%s:%d:%d' % (value, is_anomaly, timestamp)
        max_size = configs['ssdb']['series']['zsets']['maxSize']
        size = self.ssdb.zsize(zset)
        if size > max_size:  # Currently we could only use this way
            self.ssdb.zremrangebyrank(zset, 0, size - max_size)
        self.ssdb.zset(zset, key, score)
        return key

    def set_status(self, series_name, is_anomaly):
        hashmap = configs['ssdb']['allSeries']['hashmap']
        return self.ssdb.hset(hashmap, series_name, int(is_anomaly))

    def analyze(self, series):
        strict = configs['analyzer']['strict']

        if strict:
            tail = series[-1]
        else:
            tail = sum(series[-3:]) / 3

        series = numpy.array(series)

        if series.size < configs['analyzer']['minSeriesSize']:
            return False  # trust in earlies datapoints

        mean = series.mean()
        std = series.std()
        return abs(tail - mean) > 3 * std

    def shutdown(self):
        self.beans.close()

    def send_signal(self, signal, sender):
        self.hook_thread.queue.put((signal, sender))

    @serve_wrapper
    def serve(self):
        self.initialize()

        while 1:
            job = self.reserve()
            (series_name, (timestamp, value)) = pickle.loads(job.body)

            if value is None:
                continue   # skip null value datapoints

            # trigger hooks on datapoint reserved
            self.send_signal(datapoint_reserved,
                             (series_name, timestamp, value))

            start_time = time.time()

            # fetch series from database
            zset = self.zset_name(series_name)
            keys = self.filter(zset, timestamp)

            # format series
            series = []
            for key in keys:
                val, isa, _ = key.split(':')
                if not int(isa):
                    series.append(float(val))
            series.append(value)

            # do analyzation
            is_anomaly = int(self.analyze(series))

            # trigger hooks on anomaly detected
            if is_anomaly:
                self.send_signal(anomaly_detected,
                                 (series_name, (timestamp, value)))

            # append this datapoint to db and set current series status
            key = self.append(zset, (timestamp, value, is_anomaly))
            self.set_status(series_name, is_anomaly)

            # logging
            duration = time.time() - start_time
            logger.info('(%.2f) Analyzed: (%d) %s - %s', duration,
                        is_anomaly, series_name, key)

            job.delete()  # !important
            # trigger hooks on analyzation
            datapoint = (series_name, (timestamp, value, is_anomaly))
            self.send_signal(analyzation_done, datapoint)


class HookThread(Thread):

    def __init__(self):
        super(HookThread, self).__init__()
        self.setDaemon(True)
        self.queue = Queue()

    def start(self):
        super(HookThread, self).start()

    def run(self):
        while 1:
            signal, sender = self.queue.get()  # blocking!
            signal.send(sender)
            self.queue.task_done()


analyzer = Analyzer()
