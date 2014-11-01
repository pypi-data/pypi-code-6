from __future__ import absolute_import
from collections import OrderedDict
import os

from flake8.engine import get_style_guide
from pep8 import BaseReport

from diffmetrics.metrics import Metrics, Metric, Severity


class Flake8Metric(Metric):
    def __init__(self, key, **kwargs):
        super(Flake8Metric, self).__init__(**kwargs)
        self.key = key

    @property
    def category(self):
        return self.key and self.key[0]

    def compared_to(self, other):
        other_value = other.value if other is not None else 0
        if any([self.value < other_value,
                self.category == 'E' and self.value <= other_value,
                ]):
            return Severity.low
        elif any([self.value == other_value,
                  self.category == 'E',
                  ]):
            return Severity.medium
        else:
            return Severity.high


class Flake8Metrics(Metrics):
    NAME = 'Flake8'
    DEFAULT = Flake8Metric(key=None, value=0)

    def calculate_mapping(self):
        if not os.path.isfile(self.filename):
            return {}

        style_guide = get_style_guide()
        report = style_guide.init_report(BaseReport)
        style_guide.input_file(self.filename)

        sorted_items = sorted(report.messages.items())

        return OrderedDict(
            ('{} {}'.format(key, message),
             Flake8Metric(key=key, value=report.counters[key]))
            for key, message in sorted_items
        )
