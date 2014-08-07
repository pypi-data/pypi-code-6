# coding=utf8

"""
bell.analyzer
~~~~~~~~~~~~~
"""

import time
from threading import Thread

import numpy

import bell.signals as signals
from bell.base import serve_wrapper, Service
from bell.configs import configs
from bell.logger import logger
from bell.utils import pickle, Queue


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
        self.hooks_enable = configs['hooks']['enable']

        if self.hooks_enable:
            hook_modules = configs['hooks']['modules']
            map(__import__, hook_modules)
            self.hook_thread = HookThread()
            self.hook_thread.start()

    def zset_name(self, series_name):
        zset_prefix = configs['ssdb']['series']['zsets']['namePrefix']
        return zset_prefix + series_name

    def reserve_job(self):
        job = self.beans.reserve()
        return job

    def filter(self, zset, timestamp):
        """Filter datapoints by periodicity from database."""
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

    def save_datapoint(self, zset, datapoint):
        # datapoint: (time, value, is_anomaly)
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
        """3-sigma based anomalies analyzation: states that nearly all
        values(99.7%) lie within 3 standard deviations of the mean in a
        normal distribution."""
        strict = configs['analyzer']['strict']

        if strict:
            tail = series[-1]
        else:
            tail = sum(series[-3:]) / 3

        series = numpy.array(series)

        if series.size < configs['analyzer']['minSeriesSize']:
            return False  # trust in earlier datapoints

        mean = series.mean()
        std = series.std()
        return abs(tail - mean) > 3 * std

    def shutdown(self):
        self.beans.close()

    def send_signal(self, signal, sender):
        if self.hooks_enable:
            self.hook_thread.queue.put((signal, sender))

    @serve_wrapper
    def serve(self):
        self.initialize()

        while 1:
            job = self.reserve_job()
            (name, (timestamp, value)) = pickle.loads(job.body)
            if value is None:
                job.delete()
                continue
            self.send_signal(signals.datapoint_reserved,
                             (name, (timestamp, value)))
            start_time = time.time()
            zset = self.zset_name(name)
            keys = self.filter(zset, timestamp)

            series = []
            for key in keys:
                val, isa, _ = key.split(':')
                if not int(isa):
                    series.append(float(val))
            series.append(value)

            is_anomaly = int(self.analyze(series))
            if is_anomaly:
                self.send_signal(signals.anomaly_detected,
                                 (name, (timestamp, value)))

            # save this datapoint to database
            key = self.save_datapoint(zset, (timestamp, value, is_anomaly))
            self.set_status(name, is_anomaly)

            job.delete()  # !important

            # logging
            duration = time.time() - start_time
            logger.info('(%.2fs) Analyzed: (%d) %s - %s', duration,
                        is_anomaly, name, key)
            self.send_signal(signals.analyzation_done,
                             (name, (timestamp, value, is_anomaly)))


analyzer = Analyzer()
