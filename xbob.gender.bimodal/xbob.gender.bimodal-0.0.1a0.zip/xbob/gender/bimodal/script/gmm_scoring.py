#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Fri Oct 25 16:14:10 CEST 2013
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
import bob
import numpy
import os

from facereclib import utils as face_utils
from .. import utils


def gmm_scoring(args, command_line_parameters):
  """GMM scoring"""

  input_dir = args.features_directory
  gmm_male_filename = args.gmm_male_filename
  gmm_female_filename = args.gmm_female_filename
  output_dir = args.output_directory
  database = face_utils.resources.load_resource(''.join(args.database), 'database')
  db = database.m_database
  protocol = database.protocol

  # Create database
  input_ext = '.hdf5'

  utils.ensure_directory(output_dir)
  gmm_male = bob.machine.GMMMachine(bob.io.HDF5File(os.path.join(gmm_male_filename)))
  gmm_female = bob.machine.GMMMachine(bob.io.HDF5File(os.path.join(gmm_female_filename)))

  for group in ['dev', 'eval']:
    # Get the list of training files
    print("Scoring and saving scores for group %s..." % group)
    probe_list = db.objects(protocol=protocol, groups=group, purposes='probe')
    filename = os.path.join(output_dir, 'scores-%s' %group)
    f = open(filename, 'w')
    for p in probe_list:
      probe = bob.io.load(p.make_path(input_dir, input_ext))
      score = 0
      for pi in range(probe.shape[0]):
        score += gmm_male.forward(probe[pi,:]) - gmm_female.forward(probe[pi,:])
      if p.client_id == 'male':
        f.write('%s %s %s %f\n' % ('male', p.client_id, p.path, score))
        f.write('%s %s %s %f\n' % ('female', p.client_id, p.path, -score))
      else:
        f.write('%s %s %s %f\n' % ('male', p.client_id, p.path, score))
        f.write('%s %s %s %f\n' % ('female', p.client_id, p.path, -score))
    f.close()


def parse_args(command_line_parameters):
  """This function parses the given options (which by default are the command line options)."""
  # set up command line parser
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('--features-directory', metavar = 'DIR', required = True,
      help = 'Directory where the input features are stored.')
  parser.add_argument('--gmm-male-filename', metavar = 'FILE', required = True,
      help = 'Filename with the GMM male model.')
  parser.add_argument('--gmm-female-filename', metavar = 'FILE', required = True,
      help = 'Filename with the GMM female model.')
  parser.add_argument('-d', '--database', metavar = 'STR', required = True,
        help = 'Database and the protocol; registered databases are: %s'%face_utils.resources.resource_keys('database'))
  parser.add_argument('--output-directory', metavar = 'DIR', required = True,
      help = 'Output directory, where the models and scores should be stored')
  parser.add_argument('--do-training', action='store_true', default=False, help='Do GMM training')

  return parser.parse_args(command_line_parameters) 


def main(command_line_parameters = sys.argv):
  """GMM scoring"""
  # do the command line parsing
  args = parse_args(command_line_parameters[1:])

  # perform GMM-based gender verification test
  gmm_scoring(args, command_line_parameters)

if __name__ == "__main__":
  main()

