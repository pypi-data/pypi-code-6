#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'pybuilder_header_plugin',
          version = '0.0.2',
          description = '''PyBuilder Header PlugIn''',
          long_description = '''Please visit https://github.com/aelgru/pybuilder_header_plugin for more information!''',
          author = "Michael Gruber",
          author_email = "aelgru@gmail.com",
          license = 'Apache License, Version 2.0',
          url = 'https://github.com/aelgru/pybuilder_header_plugin',
          scripts = [],
          packages = ['pybuilder_header_plugin'],
          py_modules = [],
          classifiers = ['Development Status :: 1 - Planning', 'Environment :: Console', 'Intended Audience :: Developers', 'License :: OSI Approved :: Apache Software License', 'Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.0', 'Programming Language :: Python :: 3.1', 'Programming Language :: Python :: 3.2', 'Programming Language :: Python :: 3.3', 'Topic :: Utilities'],
             #  data files
             # package data
          install_requires = [ "committer", "wheel" ],
          
          zip_safe=True
    )
