#!/usr/bin/env python

from setuptools import setup

if __name__ == '__main__':
    setup(
          name = 'pybuilder_jedi_plugin',
          version = '0.0.3',
          description = '''Lint python sources with the jedi linter (experimental)''',
          long_description = '''Lints your sources with the jedi linter: https://jedi.jedidjah.ch/latest''',
          author = "Maximilien Riehl",
          author_email = "max@riehl.io",
          license = 'Apache License, Version 2.0',
          url = 'https://github.com/mriehl/pybuilder_jedi_plugin',
          scripts = [],
          packages = ['pybuilder_jedi_plugin'],
          py_modules = [],
          classifiers = ['Development Status :: 1 - Planning', 'Environment :: Console', 'Intended Audience :: Developers', 'License :: OSI Approved :: Apache Software License', 'Programming Language :: Python', 'Programming Language :: Python :: 2', 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.0', 'Programming Language :: Python :: 3.1', 'Programming Language :: Python :: 3.2', 'Programming Language :: Python :: 3.3', 'Topic :: Utilities'],
          entry_points={
          'console_scripts':
              []
          },
             #  data files
             # package data
          install_requires = [ "committer" ],
          
          zip_safe=True
    )
