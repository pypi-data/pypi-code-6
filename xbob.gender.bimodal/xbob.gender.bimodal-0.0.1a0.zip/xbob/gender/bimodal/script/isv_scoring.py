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


def isv_scoring(args, command_line_parameters):
  """ISV scoring"""

  features_dir = args.features_directory
  gmm_dir = args.gmm_directory
  isv_dir = args.isv_directory
  database = face_utils.resources.load_resource(''.join(args.database), 'database')
  db = database.m_database
  protocol = database.protocol

  projected_ubm_dir = os.path.join(gmm_dir, 'projected')
  projected_isv_dir = os.path.join(isv_dir, 'projected')
  ubm_filename = os.path.join(gmm_dir, 'Projector.hdf5')
  isv_base_filename = os.path.join(isv_dir, 'isv.hdf5')
  zf_filename = os.path.join(isv_dir, 'zf.hdf5')
  zm_filename = os.path.join(isv_dir, 'zm.hdf5')
  output_dir = os.path.join(isv_dir, 'scores')

  # Create database
  input_ext = '.hdf5'

  ubm = bob.machine.GMMMachine(bob.io.HDF5File(ubm_filename))
 
  utils.ensure_directory(output_dir)

  isv_base = bob.machine.ISVBase(bob.io.HDF5File(isv_base_filename))
  zf = bob.io.load(zf_filename)
  zm = bob.io.load(zm_filename)
  # Make ubm means m equal to m+Dz_female
  d = isv_base.d
  u = isv_base.u
  m = ubm.mean_supervector
  m_dzf = m + d * zf
  m_dzm = m + d * zm
  a = ubm.means.copy()
  gmm_female = bob.machine.GMMMachine(ubm)
  gmm_male = bob.machine.GMMMachine(ubm)
  gmm_female.mean_supervector = m_dzf
  gmm_male.mean_supervector = m_dzm

  for group in ['dev', 'eval']:
    # Get the list of training files
    print("Scoring and saving scores for group %s..." % group)
    probe_list = db.objects(protocol=protocol, groups=group, purposes='probe')
    filename = os.path.join(output_dir, 'scores-%s' %group)
    f = open(filename, 'w')
    gmm_female_t = bob.machine.GMMMachine(gmm_female)
    gmm_male_t = bob.machine.GMMMachine(gmm_male)
    probe_isv = numpy.ndarray(shape=(ubm.dim_c*ubm.dim_d,), dtype=numpy.float64)
    for p in probe_list:
      probe_f = bob.io.load(p.make_path(features_dir, input_ext))
      probe_ubm = bob.machine.GMMStats(bob.io.HDF5File(p.make_path(projected_ubm_dir, input_ext)))
      probe_isv = bob.io.load(p.make_path(projected_isv_dir, input_ext))
    
      mf_ux = gmm_female.mean_supervector + probe_isv
      gmm_female_t.mean_supervector = mf_ux
      mm_ux = gmm_male.mean_supervector + probe_isv
      gmm_male_t.mean_supervector = mm_ux
      score = 0
      for pi in range(probe_f.shape[0]):
        score += gmm_male_t.forward(probe_f[pi,:]) - gmm_female_t.forward(probe_f[pi,:])
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
      help = 'Directory where the features are stored.')
  parser.add_argument('--gmm-directory', metavar = 'DIR', required = True,
      help = 'Base directory where the ubm is stored.')
  parser.add_argument('--isv-directory', metavar = 'DIR', required = True,
      help = 'Base directory where ISV is stored.')
  parser.add_argument('-d', '--database', metavar = 'STR', required = True,
        help = 'Database and the protocol; registered databases are: %s'%face_utils.resources.resource_keys('database'))

  return parser.parse_args(command_line_parameters) 


def main(command_line_parameters = sys.argv):
  """Main routine"""
  # do the command line parsing
  args = parse_args(command_line_parameters[1:])

  # perform ISV scoring
  isv_scoring(args, command_line_parameters)

if __name__ == "__main__":
  main()

