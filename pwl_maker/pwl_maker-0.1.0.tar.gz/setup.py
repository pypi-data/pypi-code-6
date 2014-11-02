import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup (
    name = "pwl_maker",
    version = "0.1.0",
    author = "Louis Simons",
    author_email = "lousimons@gmail.com",
    description = "Utilities for creating LTSpice PWL files",
    long_description = read('README'),
    url = "https://github.com/superlou/pwl-maker",
    license = "GPLv3",
    packages = ['pwl_maker', 'tests']
)
