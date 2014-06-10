#!/usr/bin/env python
from setuptools import setup

def linelist(text):
    """
    Returns each non-blank line in text enclosed in a list.
    """
    return [ l.strip() for l in text.strip().splitlines() if l.strip() ]
    

setup(
    name='fireflask',
    version='0.1.1',
    author='Jonathan Eunice',
    author_email='jonathan.eunice@gmail.com',
    description="Simple, beautiful logging from Flask web apps to FireBug console",
    long_description=open('README.rst').read(),
    url='https://bitbucket.org/jeunice/fireflask',
    py_modules=['fireflask'],
    install_requires=['firepython>=0.9', 'flask'],
    zip_safe = False,
    keywords='webapp Flask debug log logging FireBug FireLogger FirePython',
    classifiers=linelist("""
        Development Status :: 4 - Beta
        Operating System :: OS Independent
        License :: OSI Approved :: BSD License
        Intended Audience :: Developers
        Programming Language :: Python
        Programming Language :: Python :: 2.6
        Programming Language :: Python :: 2.7
        Programming Language :: Python :: Implementation :: CPython
        Topic :: Software Development :: Debuggers
        Topic :: Software Development :: Libraries :: Python Modules
        Framework :: Flask
        Environment :: Web Environment
    """)
)
