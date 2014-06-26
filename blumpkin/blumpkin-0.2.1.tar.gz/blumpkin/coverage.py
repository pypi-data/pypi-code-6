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
    coverage_results = {}
    classes = FILES_XPATH(root)

    for cls in classes:
        class_path = cls.get('filename')
        class_coverage = float(cls.get('line-rate', '0.0')) * 100
        clses = class_path[:-3].split('/')
        for count in range(len(clses) + 1, 1, -1):
            target = '.'.join(clses[:count - 1])
            if target in package_coverage_dict:
                coverage_results.setdefault(target, [])
                coverage_results[target].append(class_coverage)
                break

    failed = False

    for package, coverages in coverage_results.iteritems():
        actual = sum(coverages) / len(coverages)
        required = package_coverage_dict[package]
        logger.info('Checking package {} -- needs {}% coverage'.format(
            package, required))
        if actual < required:
            logger.warning(
                'FAILED - Coverage for package {} is {}% -- minimum is '
                '{}%'.format(
                    package, actual, required
                )
            )
            failed = True
        else:
            logger.info('PASS {}% >= {}%'.format(actual, required))

    if set(package_coverage_dict.keys()) - set(coverage_results.keys()):
        failed = True
        not_found = ','.join(
            set(package_coverage_dict.keys()) - set(coverage_results.keys())
        )
        logger.warning(
            "FAILED - couldn't determine coverage for package(s) {}".format(
                not_found
            )
        )

    return failed


def run_coverage(filename, package_coverage_dict):
    xml = open(filename, 'r').read()
    root = etree.fromstring(xml)
    package_failed = False
    if package_coverage_dict:
        package_failed = check_package_coverage(root, package_coverage_dict)
    return package_failed


@click.command()
@click.argument('filename')
@click.argument('packages', nargs=10)
def coverage(filename, packages):
    package_coverage_dict = {
        package: int(required_coverage) for
        package, required_coverage in (x.split(':') for x in packages if x)
    }

    package_failed = run_coverage(
        filename, package_coverage_dict
    )

    if package_failed:
        click.echo('Coverage test FAILED')
        sys.exit(1)

    click.echo('Coverage test SUCCEEDED')
