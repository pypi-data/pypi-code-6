from collections import namedtuple, OrderedDict, deque
from filecmp import cmp
from itertools import islice
from os import walk, path

from termcolor import colored

from diffmetrics.metrics import Severity
from diffmetrics.metrics.flake8 import Flake8Metrics
from diffmetrics.metrics.radon.cc import CyclomaticComplexityMetrics


class Diff(object):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __iter__(self):
        raise NotImplementedError


class PackageDiff(Diff):
    def __iter__(self):
        l_files = self.get_python_files(self.left)
        r_files = self.get_python_files(self.right)

        all_files = l_files | r_files

        for f in sorted(all_files):
            l_file = path.join(self.left, f)
            r_file = path.join(self.right, f)
            if not (path.isfile(l_file) and
                    path.isfile(r_file) and
                    cmp(l_file, r_file)):  # if files are not the same
                yield ModuleDiff(left=l_file,
                                 right=r_file,
                                 common=f,
                                 )

    @staticmethod
    def get_python_files(dirname):
        all_files = []

        len_prefix = len(PackageDiff.get_components(dirname))

        for root, dirs, files in walk(dirname):
            new_files = [f for f in files if f.endswith('.py')]
            if new_files:
                base = PackageDiff.remove_dir_prefix(root, len_prefix)
                all_files.extend([path.join(base, f) for f in new_files])

        return set(all_files)

    @staticmethod
    def get_components(dirname):
        components = deque()

        head = dirname
        while head:
            head, tail = path.split(head)
            if tail:
                components.appendleft(tail)
            else:
                components.appendleft(head)
                break

        return components

    @staticmethod
    def remove_dir_prefix(dirname, num_parents):
        components = PackageDiff.get_components(dirname)
        deprefixed = list(islice(components, num_parents, None))
        if deprefixed:
            return path.join(*deprefixed)
        else:
            return ''


class ModuleDiff(Diff):
    def __init__(self, common=None, **kwargs):
        super(ModuleDiff, self).__init__(**kwargs)
        self.common = common

    def __iter__(self):
        for metrics_type in (Flake8Metrics, CyclomaticComplexityMetrics):
            yield MetricsDiff(metrics_type, self.left, self.right)

    @staticmethod
    def get_all_keys(left_metrics, right_metrics):
        base = OrderedDict()
        for metrics in (right_metrics, left_metrics):
            base.update(metrics.as_mapping())
        return base.keys()


class MetricsDiff(Diff):
    def __init__(self, metrics_type, *args):
        super(MetricsDiff, self).__init__(*args)
        self.metrics_type = metrics_type

    def __iter__(self):
        l_metrics = self.metrics_type(self.left)
        r_metrics = self.metrics_type(self.right)
        default = self.metrics_type.DEFAULT

        for metric_key in self.get_all_keys(l_metrics, r_metrics):
            l_value = l_metrics.get(metric_key, default)
            r_value = r_metrics.get(metric_key, default)
            yield DiffLine(metric_key, l_value, r_value)

    @staticmethod
    def get_all_keys(left_metrics, right_metrics):
        base = OrderedDict()
        for metrics in (right_metrics, left_metrics):
            base.update(metrics.as_mapping())
        return base.keys()


class DiffLine(namedtuple('BaseDiffLine', ['name', 'left', 'right'])):
    @property
    def severity(self):
        if not self.right:
            return Severity.low
        else:
            return self.right.compared_to(self.left)

    def with_color(self, color):
        return '{}: {}'.format(
            self.name,
            colored('{} -> {}'.format(self.left, self.right), color),
        )
