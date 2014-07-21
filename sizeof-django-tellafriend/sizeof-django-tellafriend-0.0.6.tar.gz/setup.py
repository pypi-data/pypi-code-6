# -*- coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright (c) 2010-2014 Mariusz Smenzyk <mariusz.smenzyk@sizeof.pl>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""

@author: Mariusz Smenzyk
@license: MIT License
@contact: mariusz.smenzyk@sizeof.pl
"""
import os
import re

from setuptools import setup, find_packages


REQUIREMENTS = [
    'django-simple-captcha>=0.4.2',
    'south>=0.7.3'
]

CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Environment :: Web Environment",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Framework :: Django",
    "License :: OSI Approved :: MIT License",
]


def dependency_links(packages):
    auth = '%s:%s@' % (os.environ.get('SIZEOF_PYPI_USER', ''), os.environ.get('SIZEOF_PYPI_PASSWORD', ''))
    pypi = 'http://%spypi.sizeof.pl/simple/' % (auth if len(auth) > 2 else '')
    return ['%s%s' % (pypi, re.search('[\w+-]*', p).group(0)) for p in packages if p.startswith('sizeof')]


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='sizeof-django-tellafriend',
    author='SIZEOF.PL | Mariusz Smenżyk',
    author_email='mariusz@sizeof.pl',
    url="https://bitbucket.org/sizeof/sizeof-django-tellafriend/",
    description="SIZEOF.PL | Django Tell a Friend",
    license='MIT',
    keywords="django tellafriend recommend",
    version=__import__('tellafriend').get_version(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIREMENTS,
    dependency_links=dependency_links(REQUIREMENTS),
    long_description=read('README.md'),
    package_data={
        'tellafriend': [
            'templates/tellafriend/*.html',
            'templates/tellafriend/*.txt',
            'locale/*/LC_MESSAGES/*',
        ],
    },
)
