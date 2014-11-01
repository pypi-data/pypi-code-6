from collections import OrderedDict
import os

from radon.cli import Config
from radon.cli.harvest import CCHarvester
from radon.complexity import SCORE

from diffmetrics.metrics import Metrics, Metric, ParseError, Severity


class CyclomaticComplexityMetrics(Metrics):
    NAME = 'Cyclomatic Complexity'

    def calculate_mapping(self):
        if not os.path.isfile(self.filename):
            return {}

        config = Config(exclude=[],
                        ignore=[],
                        no_assert=True,
                        order=SCORE,
                        min='A',
                        max='F',
                        )
        harvester = CCHarvester([self.filename], config)
        blocks = list(harvester.results)[0][1]
        if 'error' in blocks:
            raise ParseError('Error in {}: {}'.format(self.filename,
                                                      blocks['error']))
        keys_to_blocks = sorted(
            (self.get_key(b), CyclomaticComplexityMetric(b.complexity))
            for b in blocks
        )
        return OrderedDict(keys_to_blocks)

    @staticmethod
    def get_key(block):
        classname = getattr(block, 'classname', None)
        if classname:
            return '{}.{}'.format(classname, block.name)
        else:
            return block.name


class CyclomaticComplexityMetric(Metric):
    def compared_to(self, other):
        other_value = other.value if other is not None else 0
        if any([self.value < other_value,
                self.value <= 4,
                self.value <= 6 and self.value == other_value,
                ]):
            return Severity.low
        elif any([self.value == other_value,
                  self.value <= 8,
                  ]):
            return Severity.medium
        else:
            return Severity.high
