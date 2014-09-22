import os
import sys
from setuptools import setup, find_packages

sys.path.insert(0, os.path.abspath('lib'))

setup(
    name='ansible-lint',
    version='1.0.1',
    description=('checks playbooks for practices and behaviour that could potentially be improved'),
    keywords='ansible, lint',
    author='Will Thames',
    author_email='will@thames.id.au',
    url='https://github.com/willthames/ansible-lint',
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    zip_safe=False,
    install_requires=['ansible'],
    scripts=['bin/ansible-lint'],
)
