from setuptools import setup
from nameme import __version__, __author__, __license__

setup(
    name='name-me',
    description='Generate random strings you can actually remember',
    version=__version__,
    author=__author__,
    author_email='k@mackwerk.dk',
    license=__license__,
    url='https://github.com/Dinoshauer/name-me',
    packages=['nameme']
)
