import pypandoc
from cutest import __version__
from distutils.core import setup

setup(
    name='cutest.py',
    version=__version__,
    author='Kasper Lecnim',
    author_email='lecnim@gmail.com',
    py_modules=['cutest'],
    url='https://github.com/lecnim/cutest.py',
    license='LICENSE',
    description='The colorful and beautiful terminal output of python unittest.',
    long_description=pypandoc.convert('README.md', 'rst')
)
