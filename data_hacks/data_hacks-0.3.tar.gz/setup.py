#!/usr/bin/env python

from distutils.core import setup

version = "0.3"
setup(name='data_hacks',
      version=version,
      description='Command line utilities for data analysis',
      author='Jehiah Czebotar',
      author_email='jehiah@gmail.com',
      url='http://github.com/bitly/data_hacks',
      classifiers=[
            'Programming Language :: Python',
            'Intended Audience :: System Administrators',
            'Topic :: Terminals',
            ],
      scripts = ['data_hacks/histogram.py', 
                'data_hacks/ninety_five_percent.py',
                'data_hacks/run_for.py',
                'data_hacks/bar_chart.py',
                'data_hacks/sample.py']
     )
