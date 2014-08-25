import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name='natspec_utils',
        version='1.0.2',
        description='Decorators and Utilities needed for NatSpec - A tool for ATDD with natural language',
        maintainer='DevBoost GmbH',
        maintainer_email='contact@devboost.de',
        license="EPL",
        url='http://nat-spec.com',
        packages=['natspec_utils'],
        classifiers=[
            "Development Status :: 5 - Production/Stable",
        ],
     )
