# -*- coding: utf-8 -*-
"""
    setup

    :copyright: © 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import os
from setuptools import setup, Command


class RunAudit(Command):
    """Audits source code using PyFlakes for following issues:
        - Names which are used but not defined or used before they are defined.
        - Names which are redefined without having been used.
    """
    description = "Audit source code with PyFlakes"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import sys
        try:
            import pyflakes.scripts.pyflakes as flakes
        except ImportError:
            print "Audit requires PyFlakes installed in your system."
            sys.exit(-1)

        warns = 0
        # Define top-level directories
        dirs = ('.')
        for dir in dirs:
            for root, _, files in os.walk(dir):
                if root.startswith(('./build', './doc')):
                    continue
                for file in files:
                    if not file.endswith(('__init__.py', 'upload.py')) \
                            and file.endswith('.py'):
                        warns += flakes.checkPath(os.path.join(root, file))
        if warns > 0:
            print "Audit finished with total %d warnings." % warns
            sys.exit(-1)
        else:
            print "No problems found in sourcecode."
            sys.exit(0)


setup(
    name='Avatax',
    version='0.1',
    author='Openlabs Technologies & Consulting (P) Limited',
    author_email='info@openlabs.co.in',
    packages=['avatax', 'avatax.test'],
    license='',
    long_description=open('README.rst').read(),
    install_requires=[
        'requests',
    ],
    test_suite="avatax.test.suite",
    zip_safe=False,
    cmdclass={
        'audit': RunAudit,
    },
)
