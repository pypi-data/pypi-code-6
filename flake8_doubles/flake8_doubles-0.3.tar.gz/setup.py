# -*- coding: utf-8 -*-
from __future__ import with_statement

from setuptools import setup


def get_version(fname='flake8_doubles.py'):
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                return eval(line.split('=')[-1])


def get_long_description():
    descr = []
    for fname in ('README.md',):
        with open(fname) as f:
            descr.append(f.read())
    return '\n\n'.join(descr)


setup(
    name='flake8_doubles',
    version=get_version(),
    description="flake8 doubles checker, ensures mock.patch is not used",
    long_description=get_long_description(),
    keywords='flake8 doubles',
    author='Jia Zou',
    author_email='jiazou@uber.com',
    py_modules=['flake8_doubles'],
    url='https://github.com/jiazou/flake8-doubles',
    license='Expat license',
    zip_safe=False,
    entry_points={
        'flake8.extension': [
            'flake8_doubles = flake8_doubles:DoublesChecker',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Quality Assurance',
    ],
)
