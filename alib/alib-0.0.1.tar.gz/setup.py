# Based upon https://github.com/pypa/sampleproject/blob/master/setup.py

# # Copied from pypa/sampleproject (and changed to get it to work with Python 2.6.
from distutils.core import setup  # Always prefer setuptools over distutils
# from codecs import open  # To use a consistent encoding
# from os import path

# here = path.abspath(path.dirname(__file__))

# # Get the long description from the relevant file
# with open(path.join(here, 'DESCRIPTION.rst'), encoding='utf-8') as f:
#     long_description = f.read()
# # End of copied from pypa/sampleproject

# Copied this text into setup.py because about external read not
# working during installation.
long_description = '''Alib provides simple testing without boilerplate.  For example, if
*myfile.py* contains the line::

     7 * 8 == 54  # I'm not sure about this!

then running::

    $ python -m alib.test myfile.py

will, because the test fails, report the test line and the nature of
the failure::

    line 3:  7 * 8 == 54  # I'm not sure about this!
    (['Eq'], [ReturnValue(56), ReturnValue(54)])

Exceptions are caught.  The input line::

    (1 + '2') == 3  # Can we add a string to a number?

produces::

    line 4:  (1 + '2') == 3  # Can we add a string to a number?
    (['Eq'], [ExceptionInstance(TypeError), ReturnValue(3)]

This test line succeeds (because the left hand side raises the right
hand side).::

    (1 + '2') ** TypeError  # We can't add a string to a number.

To test all Python files in the folder *path/to/mydir* run the command::

    $ python -m alib.test path/to/mydir
'''

setup(
    name = 'alib',
    packages = ['alib', 'alib/testtools'],
    version = '0.0.1',        # For version numbering see PEP440.
    description = 'A LIB-rary of useful Python code',
    long_description = long_description,
    author = 'Jonathan Fine',
    author_email = 'jfine@pytex.org',
    license = 'Apache',
    url = 'https://github.com/jonathanfine/py-alib',
    download_url = 'https://github.com/jonathanfine/py-alib/tarball/0.0.1',
    keywords = ['testing'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ],
)
