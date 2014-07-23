#!/usr/bin/env python

#  Copyright 2013-2014 NaviNet Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import sys
from distutils.core import setup
from os.path import join, dirname

sys.path.append(join(dirname(__file__), 'ExcelLibrary'))

execfile(join(dirname(__file__), 'ExcelLibrary', 'version.py'))

DESCRIPTION = """
This test library provides some keywords to allow
opening, reading, writing, and saving Excel files
from Robot Framework.
"""[1:-1]

setup(name              = 'robotframework-excellibrary',
      version           = VERSION,
      description       = 'Robot Framework',
      long_description  = DESCRIPTION,
      author            = 'jyrkiwahlstedt, Simon McMorran',
      author_email      = '<smcmorran@navinet.net>',
      url               = 'https://github.com/NaviNet/robotframework-excellibrary',
      license           = 'Apache License 2.0',
      keywords          = 'robotframework testing testautomation excel',
      platforms         = 'any',
      classifiers       = [
                              "License :: OSI Approved :: Apache Software License",
                              "Programming Language :: Python",
                              "Development Status :: 4 - Beta",
                              "Intended Audience :: Developers",
                              "Programming Language :: Python :: 2.7",
                              "Topic :: Software Development :: Testing",
                              "Topic :: Software Development :: Quality Assurance"
                        ],
      install_requires  = [
                                                      'robotframework >= 2.8.5',
                                                      'xlutils >= 1.7.1',
                                                      'natsort >= 3.3.0'
                        ],
      packages          = ['ExcelLibrary'],
      data_files        = [('ExcelRobotTest', ['Tests/acceptance/ExcelRobotTest.txt', 'Tests/acceptance/ExcelRobotTest.xls', 'doc/ExcelLibrary-KeywordDocumentation.html', 'doc/ChangeLog.txt'])],
      download_url      = 'https://github.com/NaviNet/robotframework-excellibrary/tarball/0.0.2',
      )
