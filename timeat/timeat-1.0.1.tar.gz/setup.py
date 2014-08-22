from distutils.core import setup

from os.path import isfile
from shutil import copy

script = module = 'timeat'


def _setup_script():
    '''Generate script without .py extension'''
    if not isfile(script):
        copy('{}.py'.format(module), script)
_setup_script()

setup(
    name='timeat',
    version='1.0.1',
    description='Show local time at given location',
    author='Miki Tebeka',
    author_email='miki.tebeka@gmail.com',
    url='https://bitbucket.org/tebeka/py-timeat',
    py_modules=[module],
    scripts=[script],

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
