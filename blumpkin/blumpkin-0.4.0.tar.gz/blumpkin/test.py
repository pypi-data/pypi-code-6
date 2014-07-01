from __future__ import unicode_literals
import sys

import click
import pytest


@click.command('test')
@click.option('--cov')
@click.option('--cov-report', nargs=2)
@click.argument('target')
def test(cov, cov_report, target):
    sys.exit(run(cov, cov_report, target))


def run(cov, cov_report, target):
    args = []
    if cov:
        args.append('--cov=' + cov)
    for report in cov_report:
        args.append('--cov-report=' + report)
    if target:
        args.append(target)
    arg_str = ' '.join(args)
    return pytest.main(str(arg_str))
