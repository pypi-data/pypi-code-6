import os
import re

from setuptools import find_packages
from setuptools import setup

with file(os.path.join('retain', 'retain.py')) as init:
    source = init.read()
    m = re.search("__version__ = '(\d+\.\d+\.\d+)'", source, re.M)
    __version__ = m.groups()[0]

setup(
    name="py-retain",
    version=__version__,
    description="Retcin.cc API wrapper",
    long_description=open('README').read(),
    author="Rick Mak",
    author_email="rick.mak@gmail",
    license="MIT License",
    url="http://github.com/retaincc/py-retain",
    keywords='Retaincc Reainc python',
    classifiers=[],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests"],
    zip_safe=False
)
