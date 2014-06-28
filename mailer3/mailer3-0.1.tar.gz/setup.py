from setuptools import setup
import sys

extra = {}
if sys.version_info >= (3,0):
    extra.update( use_2to3 = True )

setup (
    name = 'mailer3',
    version = "0.1",
    description = "A copy of https://pypi.python.org/pypi/mailer with 2to3 run over all the .py files.",
    author = "Joe Borg",
    url = "https://github.com/joedborg/mailer",
    py_modules = ["mailer"],
    keywords = ["email", "smtp"],
    license = "MIT License",
    classifiers = [
        'Programming Language :: Python :: 3',
    ],
    **extra
)
