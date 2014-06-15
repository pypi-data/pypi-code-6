#!/usr/bin/env python
"""setup.py

This module demonstrates documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

:copyright: (c) 2014 by Sean Anthony Finucane.
:license: MIT, see LICENSE for more details.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import sys

__python_version__ = dict()
try:
    __python_version__['major'] = sys.version_info.major
except AttributeError:
    __python_version__['major'] = sys.version_info[0]
try:
    __python_version__['minor'] = sys.version_info.minor
except AttributeError:
    __python_version__['minor'] = sys.version_info[1]

from distutils.core import setup
from pkgutil import walk_packages

import finucane


def find_packages(root_path, prefix=""):
    yield prefix
    prefix += "."
    for _, name, ispkg in walk_packages(root_path, prefix):
        if ispkg:
            yield name


with open('README.md') as file:
    long_description = file.read()

REQ_PKGS_ALL = ['future']
REQ_PKGS_PY26 = ['argparse']

required_packages = REQ_PKGS_ALL
if (__python_version__['major'], __python_version__['minor']) in [(2, 6)]:
    required_packages += REQ_PKGS_PY26

setup(name='finucane-apputils',
      version='0.4.3',
      description='Finucane Research application framework and utilities for Python',
      long_description=long_description,
      keywords='application framework utilities development finucane',
      author='Sean Anthony Finucane',
      author_email='s.finucane001@gmail.com',
      url='https://github.com/sfinucane/finucane-apputils',
      license='MIT',
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: MacOS :: MacOS X',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: POSIX',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Topic :: Software Development :: Libraries :: Application Frameworks',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Utilities'
      ],
      install_requires=required_packages,
      zip_safe=True,
      platforms='any',
      provides=['finucane.apputils'],
      data_files=[('', ['README.md',
                        'LICENSE',
                        'NOTICE',
                        'requirements.txt',
                        'requirements26.txt'])],
      namespace_packages=["finucane"],
      packages=list(find_packages(finucane.__path__, finucane.__name__)),
)
