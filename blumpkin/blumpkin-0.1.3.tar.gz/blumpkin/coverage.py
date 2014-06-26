#!/usr/bin/env python
"""
Jenkins' Cobertura plugin doesn't allow marking a build as successful or
failed based on coverage of individual packages -- only the project as a
whole. This script will parse the coverage.xml file and fail if the coverage of
specified packages doesn't meet the thresholds given
"""
from __future__ import unicode_literals
import ast
import logging
import logging.config
import os
import sys

import click
from lxml import etree


logger = logging.getLogger(__name__)


PACKAGES_XPATH = etree.XPath('/coverage/packages/package')
FILES_XPATH = etree.XPath('/coverage/packages/package/classes/class')
PACKAGE_SEPARATOR = '.'


def check_package_coverage(root, package_coverage_dict):
    failed = False

    packages = PACKAGES_XPATH(root)
    check_done = set()

    for package in packages:
        name = package.get('name')
        do_check = False
        check_name = name
        if name in package_coverage_dict:
            # We care about this one
            do_check = True
        else:
            # Check subpackages
            name_parts = name.split('.')
            for i in range(len(name_parts) - 1, 1, -1):
                possible_name = '.'.join(name_parts[:i])
                if possible_name in package_coverage_dict:
                    do_check = True
                    check_name = possible_name
                    break

        if do_check:
            check_done.add(check_name)
            logger.info('Checking package {} -- need {}% coverage'.format(
                name, package_coverage_dict[check_name]))
            coverage = float(package.get('line-rate', '100.0')) * 100
            if coverage < package_coverage_dict[check_name]:
                logger.warning('FAILED - Coverage for package {} is {}% -- '
                               'minimum is {}%'.format(
                    name, coverage, package_coverage_dict[check_name]))
                failed = True
            else:
                logger.info("PASS")

    if set(package_coverage_dict.keys()) - check_done:
        failed = True
        not_found = ','.join(set(package_coverage_dict.keys()) - check_done)
        logger.warning("FAILED - couldn't determine coverage for package(s) {}"
            .format(not_found))

    return failed


def check_file_coverage(root, coverage_file, default_coverage=90,
                        strict=False):
    if not coverage_file:
        raise Exception('Please supply a filename to store per-file '
                        'coverage information')

    coverage_history = {}
    failed = False
    if os.path.exists(coverage_file):
        with open(coverage_file, 'r') as f:
            try:
                coverage_history = ast.literal_eval(f.read())
            except:
                # We can't be strict with no previous data
                strict = False

    files = FILES_XPATH(root)
    for f in files:
        filename = f.get('filename')
        coverage = float(f.get('line-rate', '0.0')) * 100
        previous = coverage_history.get(filename, default_coverage)
        logger.info('{} - previous: {}  current: {}  result: {}'.format(
            filename, previous, coverage,
            ('PASS' if coverage >= previous else 'FAIL')))
        if coverage < previous:
            logger.warning('FAILED - Coverage for file {} is {}% -- '
                           'down from {}%'.format(filename, coverage, previous)
            )
            failed = True
        # Being non-strict will block files with < default_coverage on
        # initial commit, but allow them on subsequent commits, even if
        # coverage remains less than the default.
        if coverage > previous or not strict:
            coverage_history[filename] = coverage

    with open(coverage_file, 'w') as f:
        f.write('%r' % coverage_history)

    return failed


@click.command()
@click.argument('filename')
@click.argument('packages', nargs=10)
@click.option('--per-file', type=bool, default=False)
@click.option('--strict', type=bool, default=False)
def coverage(filename, packages, per_file, strict):
    package_coverage_dict = {
        package: int(coverage) for
        package, coverage in (x.split(':') for x in packages if x)
    }

    xml = open(filename, 'r').read()
    root = etree.fromstring(xml)

    package_failed = False
    if package_coverage_dict:
        package_failed = check_package_coverage(root, package_coverage_dict)

    file_failed = False
    if per_file:
        file_failed = check_file_coverage(root, filename, strict=strict)

    if package_failed or file_failed:
        click.echo("Coverage test FAILED")
        sys.exit(1)

    click.echo("Coverage test SUCCEEDED")
