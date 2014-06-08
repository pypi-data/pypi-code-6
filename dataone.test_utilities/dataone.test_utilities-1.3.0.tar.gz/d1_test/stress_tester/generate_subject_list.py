#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

''':mod:`generate_subject_list`
===============================

:Synopsis: Generate a list of test subjects.
:Author: DataONE (Dahl)
'''
# Stdlib.
import logging
import optparse
import os
import re
import sys
import unittest

# D1.
from d1_test.instance_generator import random_data

# App.
_here = lambda * x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
sys.path.append(_here('./shared/'))
import settings
import subject_dn

# Get an instance of a logger.
logger = logging.getLogger()


def main():
  log_setup()

  # Command line opts.
  parser = optparse.OptionParser('usage: %prog [options] <number of subjects to create>')
  parser.add_option('--verbose', dest='verbose', action='store_true', default=False)
  (options, arguments) = parser.parse_args()

  if len(arguments) != 1 or not arguments[0].isdigit():
    logging.error('Must provide the number of subjects to create')
    exit()

  n_subjects = int(arguments[0])

  create_subject_list(n_subjects)

  print '{0} test subjects written to {1}'.format(n_subjects, settings.SUBJECTS_PATH)


def create_subject_list(n_subjects):
  with open(settings.SUBJECTS_PATH, 'w') as f:
    for i in range(n_subjects):
      cn = random_data.random_3_words()
      f.write(subject_dn.get_dataone_compliant_dn_serialization_by_subject(cn))
      f.write('\n')


def log_setup():
  logging.getLogger('').setLevel(logging.INFO)
  formatter = logging.Formatter('%(levelname)-8s %(message)s')
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)


if __name__ == '__main__':
  main()
