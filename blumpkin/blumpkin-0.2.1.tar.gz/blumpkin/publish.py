from __future__ import unicode_literals

import os
from subprocess import call
import click

from . import config

@click.command('publish')
@click.option('--branch', nargs=1, default=config['PUBLISH_BRANCH'])
@click.option('--index', nargs=1, default=config['PYPI_INDEX'])
def publish(branch, index):
    if branch and branch != os.environ.get('TRAVIS_BRANCH', branch):
        click.echo('Not on the publishing branch')
        return
    args = ['python', 'setup.py', 'sdist', 'upload']
    if index is not None:
        args += ['-r', 'alt']
    return call(args)
