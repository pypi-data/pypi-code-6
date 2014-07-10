#!/usr/bin/env python3

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

#try:
#    from pypandoc import convert
#    read_md = lambda filename: convert(filename, 'rst')
#except ImportError:
#    print("warning: pypandoc module not found, could not convert Markdown to RST")
#    read_md = lambda filename: open(filename, mode='r').read()
#long_description = read_md('README.md')

#import pandoc
#pandoc.PANDOC_PATH = '/usr/bin/pandoc'
#doc = pandoc.Document()
#doc.markdown = open('README.md', mode='r').read()
#long_description = doc.rst

long_description = open('README.md', mode='r').read()

setup(
    name = 'python-yr',
    version = '1.3.1',
    description = 'Get the forecast from the norwegian wheather service yr.no in python',
    long_description = long_description,
    author = 'Alexander Hansen',
    author_email = 'alexander.l.hansen@gmail.com',
    maintainer = 'GNU Knight',
    maintainer_email = 'idxxx23@gmail.com',
    url = 'https://github.com/wckd/python-yr',
    packages = ['yr'],
    package_data = {
        'yr': [
            'examples/*.py',
            'languages/*.json',
            'locations/*.gz',
        ]
    },
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Internet',
    ],
    install_requires = ['xmltodict'], # $$solve$$ ~> /usr/lib/python3.4/distutils/dist.py:260: UserWarning: Unknown distribution option: 'install_requires' warnings.warn(msg)
)
