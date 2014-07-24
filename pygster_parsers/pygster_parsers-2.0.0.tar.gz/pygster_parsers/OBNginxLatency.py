#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OBNginxLatency parser parses Nginx Latency logs.

This assumes a log format similar to:
    '$remote_addr - $msec $request_time $pipe $request_length $bytes_sent '
    '$http_authentication $status $request';

Which results in a log as such:
    1.2.3.4 - 1400013980.009 5.711 . 570 219 - 204 PATCH /userstat/600 HTTP/1.1
    1.2.3.4 - 1400013982.741 0.574 . 373 196 - 200 POST /login HTTP/1.1
    1.2.3.4 - 1400013989.364 0.116 . 313 824 - 200 GET /user/601 HTTP/1.1

Source:: https://github.com/OnBeep/pygster_parsers
"""

__author__ = 'Greg Albrecht <gba@onbeep.com>'
__copyright__ = 'Copyright 2014 OnBeep, Inc.'
__license__ = 'Apache License, Version 2.0'


import optparse
import re

from pygster.parsers import stats_helper

from pygster.pygster_helper import MetricObject, PygsterParser


class OBNginxLatency(PygsterParser):

    """OBNginxLatency Object Class."""

    LATENCY_REX = r'^(?P<remote_addr>[^\s]+) - (?P<msec>\d+\.\d+) ' \
        r'(?P<request_time>\d+\.\d+) (?P<pipe>[^\s]{1}) ' \
        r'(?P<request_length>\d+) (?P<bytes_sent>\d+) ' \
        r'(?P<http_authentication>[^\s]+) (?P<status>\d{3}) ' \
        r'(?P<request_method>\w+) (?P<request_path>[^\s]+) ' \
        r'(?P<request_protocol>HTTP/\d\.\d)$'

    def __init__(self, option_string=None):
        if option_string:
            options = option_string.split()
        else:
            options = []

        optparser = optparse.OptionParser()
        optparser.add_option(
            '--percentiles',
            '-p',
            dest='percentiles',
            default='90',
            help='Comma separated list of integer percentiles to track.'
            'Default: 90'
        )

        opts, _ = optparser.parse_args(args=options)

        self.percentiles = opts.percentiles.split(',')
        self.latencies = {}
        self.latency_rex = re.compile(self.LATENCY_REX)

    def parse_line(self, line):
        """
        Updates object state variables, one line at a time.

        :param line: Line to be parsed.
        :type line: str
        """
        latency_match = self.latency_rex.match(line)
        if latency_match:
            latency_dict = latency_match.groupdict()

            if (latency_dict.get('request_time') and
                    latency_dict.get('request_path') and
                    latency_dict.get('status')):

                request_endpoint = latency_dict.get(
                    'request_path').split('/')[1]

                if request_endpoint:

                    metric_path = '.'.join([
                        request_endpoint,
                        latency_dict.get('request_method'),
                        latency_dict.get('status')
                    ])

                    count_metric = '.'.join([metric_path, 'count'])

                    if count_metric not in self.latencies:
                        self.latencies[count_metric] = {
                            'unit': 'connections',
                            'values': [1]
                        }

                    self.latencies[count_metric]['values'][0] += 1

                    latency_metric = '.'.join([metric_path, 'latency'])

                    if latency_metric not in self.latencies:
                        self.latencies[latency_metric] = {
                            'unit': 'msec',
                            'values': []
                        }

                    self.latencies[latency_metric]['values'].append(
                        float(latency_dict.get('request_time')))

                    bytes_sent_metric = '.'.join([metric_path, 'bytes_sent'])

                    if bytes_sent_metric not in self.latencies:
                        self.latencies[bytes_sent_metric] = {
                            'unit': 'bytes',
                            'values': []
                        }

                    self.latencies[bytes_sent_metric]['values'].append(
                        float(latency_dict.get('bytes_sent')))

                    request_length_metric = '.'.join([
                        metric_path, 'request_length'])

                    if request_length_metric not in self.latencies:
                        self.latencies[request_length_metric] = {
                            'unit': 'bytes',
                            'values': []
                        }

                    self.latencies[request_length_metric]['values'].append(
                        float(latency_dict.get('request_length')))

    def get_state(self, duration):
        metrics = []

        for metric_path in self.latencies:
            values = self.latencies[metric_path]['values']
            unit = self.latencies[metric_path]['unit']

            metrics.append(
                MetricObject(
                    '.'.join([metric_path, 'mean']),
                    stats_helper.find_mean(values),
                    unit
                )
            )

            metrics.append(
                MetricObject(
                    '.'.join([metric_path, 'median']),
                    stats_helper.find_mean(values),
                    unit
                )
            )

            for pct in self.percentiles:
                metrics.append(
                    MetricObject(
                        '.'.join([metric_path, "%sth_percentile" % pct]),
                        stats_helper.find_percentile(values, int(pct)),
                        unit
                    )
                )

        return metrics
