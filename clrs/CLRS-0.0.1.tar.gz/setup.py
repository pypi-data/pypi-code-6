import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="CLRS",
    version="0.0.1",
    author="Pengcheng Zhang",
    author_email="zpc010@gmail.com",
    license="BSD",
    keywords="algorithms",
    url="https://github.com/pc-zhang/CLRS.git",
    packages=['sorting', 'tree'],
    description=('Algorithms from CLRS -- Introduction to Algorithms'),
    long_description=read('README'),
)
