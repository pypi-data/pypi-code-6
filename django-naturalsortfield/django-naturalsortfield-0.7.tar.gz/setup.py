#!/usr/bin/env python

from setuptools import find_packages, setup
from setuptools.command.test import test as BaseTestCommand
import os.path
import sys

sys.path = [
    os.path.join(os.path.dirname(__file__), 'src'),
    os.path.join(os.path.dirname(__file__), 'testproject')
] + sys.path

class TestCommand(BaseTestCommand):
    def run(self):
        import os

        from django.core.management import call_command

        os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
        call_command('test')

setup(
    name='django-naturalsortfield',
    url='https://github.com/nathforge/django-naturalsortfield',
    version='0.7',
    description='Natural sorting for Django CharFields.',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
    
    author='Nathan Reynolds',
    author_email='email@nreynolds.co.uk',
    
    packages=find_packages(),

    cmdclass={'test': TestCommand},

    tests_require=['django'],

    zip_safe=True
)
