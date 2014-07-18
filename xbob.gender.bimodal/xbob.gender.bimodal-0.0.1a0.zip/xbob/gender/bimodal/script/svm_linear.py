#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
#
# Copyright (C) 2014 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


import argparse
import sys
import os
import subprocess

from facereclib import utils

def svm_linear(args, command_line_parameters):
  """SVM training and scoring"""

  input_dir = args.features_directory
  output_dir = args.output_directory
  database = args.database

  base_call = ['bin/svm.py', '--features-directory', input_dir, '--database', database]
  cost_list = [1, 5, 10, 20, 100, 1000, 10000]
  cost_name_list = ['c1', 'c5', 'c10', 'c20', 'c100', 'c1000', 'c10000']

  # Linear SVM
  for c in range(len(cost_list)):
    out = 'linear_%s' % (cost_name_list[c])
    call = base_call[:]
    call += ['--output-directory'] + [os.path.join(output_dir, out)]
    call += ['--cost'] + [str(cost_list[c])]
    print(" ".join(call))
    subprocess.call(call)

def parse_args(command_line_parameters):
  """This function parses the given options (which by default are the command line options)."""
  # set up command line parser
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--features-directory', metavar = 'DIR', required = True,
      help = 'Directory where the input features are stored.')
  parser.add_argument('-d', '--database', metavar = 'STR', required = True,
        help = 'Database and the protocol; registered databases are: %s'%utils.resources.resource_keys('database'))
  parser.add_argument('--output-directory', metavar = 'DIR', required = True,
      help = 'Output directory, where the models and scores should be stored')

  return parser.parse_args(command_line_parameters) 


def main(command_line_parameters = sys.argv):
  """Main routine"""
  # do the command line parsing
  args = parse_args(command_line_parameters[1:])

  # perform SVM-based gender verification test
  svm_linear(args, command_line_parameters)

if __name__ == "__main__":
  main()

