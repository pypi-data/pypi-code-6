#!/usr/bin/env python2

import ez_setup
ez_setup.use_setuptools()

from setuptools import setup
from wok_hooks import version
import sys

extra = {}
if sys.version_info >= (3,):
    extra['use_2to3'] = True

setup(
    name='wok_hooks',
    version=version,
    author='Steffen Kampmann',
    author_email='steffen.kampmann@gmail.com',
    license='MIT',
    url='https://github.com/abbgrade/wok_hooks',
    description='Plugins for wok',
    long_description=
        "Wok is a static website generator. It turns a pile of templates, "
        "content, and resources (like CSS and images) into a neat stack of "
        "plain HTML. Wok_hooks is a set of plugins that adds extra functionality.",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        'Operating System :: POSIX',
        'Programming Language :: Python',
    ],
    install_requires=[
        'urllib3',
        'wok',
        'activitystreams',
        'paramiko',
        'html2text',
        'feedparser',
        'beautifulsoup4',
        'vobject',
        'gnupg',
    ],
    packages=['wok_hooks'],
    scripts=[],
    **extra
)
