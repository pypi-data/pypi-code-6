from distutils.core import setup
from setuptools import find_packages

setup(
    name="git-archive",
    version="0.1.0",
    author="Eric Chiang",
    author_email="eric@yhathq.com",
    url="https://github.com/EricChiang/git-archive",
    packages=find_packages(),
    description="Go back into the git archive",
    license="MIT",
    scripts=['bin/git-archive'],
)
