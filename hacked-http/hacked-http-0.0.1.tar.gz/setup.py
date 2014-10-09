# -*- coding:utf-8 -*-
import os
import sys
from setuptools import setup, find_packages

# Hack to silence atexit traceback in newer python versions
try:
    import multiprocessing
except ImportError:
    pass

DESCRIPTION = u'Hacked Urllib2 는 warning.or.kr 같은 방어벽을 뚫는데 목적이 있습니다.' 
LONG_DESCRIPTION = None
try:
    LONG_DESCRIPTION = open('README.rst').read()
except:
    pass


def get_version(version_tuple):
    if not isinstance(version_tuple[-1], int):
        return '.'.join(map(str, version_tuple[:-1])) + version_tuple[-1]
    return '.'.join(map(str, version_tuple))

# Dirty hack to get version number from monogengine/__init__.py - we can't
# import it as it depends on PyMongo and PyMongo isn't installed until this
# file is read
init = os.path.join(os.path.dirname(__file__), 'hacked_http', '__init__.py')
version_line = list(filter(lambda l: l.startswith('VERSION'), open(init)))[0]

VERSION = get_version(eval(version_line.split('=')[-1]))
print(VERSION)

CLASSIFIERS = [
    #'Development Status :: 1 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.1",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: Implementation :: CPython",
    'Topic :: Database',
    'Topic :: Software Development :: Libraries :: Python Modules',
    
]


setup(name='hacked-http',
      version=VERSION,
      author='Chang Min Jo (Anderson)',
      author_email='a141890@{nospam}gmail.com',
      maintainer="Chang Min Jo (Anderson)",
      maintainer_email="a141890@{nospam}gmail.com",
      url='https://bitbucket.org/jochangmin/hacked-urllib2',
      download_url='https://bitbucket.org/jochangmin/hacked-urllib2/get/125df231b1ef.zip',
      license='MIT',
      include_package_data=True,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      platforms=['any'],
      classifiers=CLASSIFIERS,
      packages=find_packages(exclude=['tests*']), # 'hacked_http'
      #install_requires=[],
)