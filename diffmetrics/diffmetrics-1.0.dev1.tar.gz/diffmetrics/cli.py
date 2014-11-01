from argparse import ArgumentParser
from itertools import chain, groupby
from os import path
import sys

from termcolor import colored

from diffmetrics.diff import PackageDiff, ModuleDiff
from diffmetrics.metrics import ParseError, Severity


SEVERITY_TO_COLOR = {
    Severity.low: 'green',
    Severity.medium: 'yellow',
    Severity.high: 'red',
}


ERROR_COLOR = 'red'


def parse_args():
    parser = ArgumentParser(
        prog='diffmetrics',
        description='Calculate a diff of Python code metrics',
    )
    parser.add_argument(
        'left',
        metavar='FILE1',
        help='the base file',
    )
    parser.add_argument(
        'right',
        metavar='FILE2',
        help='the updated file',
    )
    parser.add_argument(
        '-n',
        '--min',
        choices=[s.name for s in Severity],
        default=Severity.medium.name,
        help='the minimum severity of issue to display',
    )
    return parser.parse_args()


def get_diff_lines(args, min_severity):
    args = parse_args()

    min_severity = Severity[args.min]

    if path.isfile(args.left) or path.isfile(args.right):
        return get_module_diff_lines(
            ModuleDiff(left=args.left, right=args.right),
            min_severity=min_severity,
        )
    else:
        return get_package_diff_lines(
            args=args,
            min_severity=min_severity,
        )


def get_package_diff_lines(args, **kwargs):
    return list(chain.from_iterable(
        get_module_diff_lines(module_diff, **kwargs)
        for module_diff in PackageDiff(args.left, args.right)
    ))


def get_module_diff_lines(module_diff, min_severity):
    return [(module_diff, metrics_diff, line)
            for metrics_diff in module_diff
            for line in metrics_diff
            if line.severity >= min_severity]


def print_lines(diff_lines):
    for module_diff, module_elements in groupby(diff_lines, lambda t: t[0]):
        if module_diff.common:
            print colored(module_diff.common, attrs=['bold'])
        else:
            print colored(module_diff.left, attrs=['bold'])
            print colored(module_diff.right, attrs=['bold'])
        for metrics_diff, metrics in groupby(module_elements, lambda t: t[1]):
            print ' - {}'.format(metrics_diff.metrics_type.NAME)
            for _, _, line in metrics:
                color = SEVERITY_TO_COLOR[line.severity]
                print '   {}'.format(line.with_color(color))


def run():
    args = parse_args()
    min_severity = Severity[args.min]
    try:
        diff_lines = get_diff_lines(args, min_severity)
    except ParseError as e:
        print colored(e.message, ERROR_COLOR)
        sys.exit(1)
    else:
        print_lines(diff_lines)
        if diff_lines:
            sys.exit(1)
