#!/usr/bin/env python

try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup

setup(name='djeasyroute',
      version='0.0.1',
      description='A simple class based route system for django similar to flask',
      author='Ryan Goggin',
      author_email='info@ryangoggin.net',
      url='https://github.com/Goggin/djeasyroute',
      download_url='',
      classifiers=[
            "Development Status :: 3 - Alpha",
            "Framework :: Django",
            "License :: OSI Approved :: MIT",
            "Operating System :: OS Independent",
            "Intended Audience :: Developers",
            "Topic :: Software Development",
      ],
      install_requires=[
            'django',
      ],
      packages=[
            'djeasyroute',
      ],
)
