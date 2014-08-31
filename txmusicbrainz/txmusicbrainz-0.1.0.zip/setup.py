import os

from setuptools import find_packages, setup

from txmusicbrainz import __version__


with open(os.path.join(os.path.dirname(__file__), "README.rst")) as readme:
    long_description = readme.read()

classifiers = [
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: Implementation :: CPython",
    "Programming Language :: Python :: Implementation :: PyPy"
]

setup(
    name="txmusicbrainz",
    version=__version__,
    packages=find_packages(),
    author="Julian Berman",
    author_email="Julian@GrayVines.com",
    classifiers=classifiers,
    description="Twisted API client for the MusicBrainz API",
    license="MIT",
    long_description=long_description,
    url="https://github.com/Julian/txmusicbrainz",
)
