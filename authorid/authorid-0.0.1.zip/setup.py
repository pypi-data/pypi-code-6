import os
from setuptools import setup, find_packages
import authorid

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "authorid",
    version = authorid.__version__,
    author = "Manan Shah",
    author_email = "manan.shah.777@gmail.com",
    description = ("A utility to determine the author of a document using linguistic analysis"),
    license = "MIT",
    keywords = "linguistics author finding",
    packages=['authorid'],
    long_description=read('README.txt'),
    entry_points={
        'console_scripts':
            ['authorid = authorid:print_message']
        }
)
