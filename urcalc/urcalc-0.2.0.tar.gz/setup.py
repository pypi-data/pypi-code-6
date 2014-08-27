#!/usr/bin/env python3
# Copyright (C) 2014 Yu-Jie Lin
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

import codecs
from distutils.core import setup

try:
  from wheel.bdist_wheel import bdist_wheel
except ImportError:
  bdist_wheel = None


package_name = 'urcalc'
module_file = 'c.py'
script_name = 'c'

# ============================================================================
# https://groups.google.com/d/msg/comp.lang.python/pAeiF0qwtY0/H9Ki0WOctBkJ
# Work around mbcs bug in distutils.
# http://bugs.python.org/issue10945

try:
  codecs.lookup('mbcs')
except LookupError:
  ascii = codecs.lookup('ascii')
  func = lambda name, enc=ascii: {True: enc}.get(name == 'mbcs')
  codecs.register(func)


# ============================================================================


with open(module_file) as f:
  meta = dict(
    (k.strip(' _'), eval(v)) for k, v in
      # There will be a '\n', with eval(), it's safe to ignore
      (line.split('=') for line in f if line.startswith('__'))
  )

  # renaming meta-data keys
  meta_renames = [
    ('module', 'name'),
    ('website', 'url'),
    ('email', 'author_email'),
  ]
  for old, new in meta_renames:
    if old in meta:
      meta[new] = meta[old]
      del meta[old]

  # keep these
  meta_keys = ['name', 'description', 'version', 'license', 'url', 'author',
               'author_email']
  meta = dict([m for m in meta.items() if m[0] in meta_keys])

meta['name'] = package_name

with open('README.rst') as f:
  long_description = f.read()

classifiers = [
  'Development Status :: 3 - Alpha',
  'Environment :: Console',
  'Environment :: Console :: Curses',
  'Intended Audience :: End Users/Desktop',
  'License :: OSI Approved :: MIT License',
  'Natural Language :: English',
  'Operating System :: POSIX :: Linux',
  'Programming Language :: Python :: 3',
  'Topic :: Office/Business',
  'Topic :: Scientific/Engineering :: Mathematics',
  'Topic :: Utilities',
]

setup_d = dict(
  long_description=long_description,
  cmdclass={
  },
  classifiers=classifiers,
  py_modules=[module_file.replace('.py', '')],
  scripts=[script_name],
  **meta
)

if bdist_wheel:
  setup_d['cmdclass']['bdist_wheel'] = bdist_wheel

if __name__ == '__main__':
  setup(**setup_d)
