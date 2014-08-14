
from setuptools import setup, find_packages
import sys, os

version = '0.1'

requirements = [
    'validate_email',
    'phonenumbers',
    'jinja2',
    'python-dateutil'
]

setup(
    name = 'liquid4m',
    version = version,
    description = "Liquid form management for dummies",
    packages = find_packages( exclude = [ 'ez_setup'] ),
    include_package_data = True,
    zip_safe = False,
    author = 'Bence Faludi',
    author_email = 'b.faludi@mito.hu',
    license = 'GPL',
    dependency_links = [],
    install_requires = requirements,
    test_suite = "liquid4m.tests"
)