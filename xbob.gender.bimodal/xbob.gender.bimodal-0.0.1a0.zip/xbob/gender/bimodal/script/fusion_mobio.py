#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
# Tue Jan  8 13:36:12 CET 2013
#
# Copyright (C) 2014 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""This script fuses MOBIO scores from various systems.
"""

import bob, os, sys

from .. import utils

def mobio_fusion(args, command_line_parameters):
  """Score fusion of Mobio scores"""
 
  DATABASE = 'mobio'
  PROTOCOL = 'protocol'
  systems_subdir = [[os.path.join('linear_c%d' % k) for k in [1, 5, 10, 20, 100, 1000, 10000]],
                    [os.path.join('scores')],
                    [os.path.join('scores')],
                    [os.path.join('scores', PROTOCOL, 'nonorm')]]
  fusion_subdir = [os.path.join('linear'),
                   os.path.join('scores'),
                   os.path.join('scores'),
                   os.path.join('scores', PROTOCOL, 'nonorm')]

  #tv_svm, isv, gmm, tv_cos
  facesystems_basedir   = [os.path.join('crop80x80_dct', 'ivec', 'svm'),
                           os.path.join('crop80x80_dct', 'isv'),
                           os.path.join('crop80x80_dct', 'gmm'),
                           os.path.join('crop80x80_dct', 'ivec', 'cosine')]
  speechsystems_basedir = [os.path.join('mfcc60', 'ivec', 'svm'),
                           os.path.join('mfcc60', 'isv'),
                           os.path.join('mfcc60', 'gmm'),
                           os.path.join('mfcc60', 'ivec', 'cosine')]
  fusionsystems_basedir = [os.path.join('fusion', 'ivec', 'svm'),
                           os.path.join('fusion', 'isv'),
                           os.path.join('fusion', 'gmm'),
                           os.path.join('fusion', 'ivec', 'cosine')]

  facesystems_filename_dev    = [None] * len(facesystems_basedir)
  facesystems_filename_eval   = [None] * len(facesystems_basedir)
  speechsystems_filename_dev  = [None] * len(speechsystems_basedir)
  speechsystems_filename_eval = [None] * len(speechsystems_basedir)

  for bdi,bd in enumerate(facesystems_basedir):
    acc_max = None
    filename_dev_max = None
    filename_eval_max = None
    face_vals = None
    for sdi, sd in enumerate(systems_subdir[bdi]):
      filename_dev = os.path.join(args.results_directory, DATABASE, bd, sd, 'scores-dev')
      filename_eval = os.path.join(args.results_directory, DATABASE, bd, sd, 'scores-eval')
      # read score file
      acc, tpr, tnr = utils.accuracy_tpr_tnr(filename_dev)
      if acc_max == None or acc > acc_max:
        acc_max = acc
        filename_dev_max = filename_dev
        filename_eval_max = filename_eval
        face_vals = [acc, tpr, tnr]
    facesystems_filename_dev[bdi]  = filename_dev_max
    facesystems_filename_eval[bdi] = filename_eval_max

  for bdi,bd in enumerate(speechsystems_basedir):
    acc_max = None
    filename_dev_max = None
    filename_eval_max = None
    speech_vals = None
    for sdi, sd in enumerate(systems_subdir[bdi]):
      filename_dev = os.path.join(args.results_directory, DATABASE, bd, sd, 'scores-dev')
      filename_eval = os.path.join(args.results_directory, DATABASE, bd, sd, 'scores-eval')
      # read score file
      acc, tpr, tnr = utils.accuracy_tpr_tnr(filename_dev)
      if acc_max == None or acc > acc_max:
        acc_max = acc
        filename_dev_max = filename_dev
        filename_eval_max = filename_eval
        speech_vals = [acc, tpr, tnr]
    speechsystems_filename_dev[bdi]  = filename_dev_max
    speechsystems_filename_eval[bdi] = filename_eval_max

  assert len(facesystems_filename_dev) == len(facesystems_filename_eval)
  assert len(facesystems_filename_dev) == len(speechsystems_filename_dev)
  assert len(facesystems_filename_dev) == len(speechsystems_filename_eval)

  # read data
  n_systems = len(facesystems_filename_dev)
  for i in range(n_systems):
    if not os.path.isfile(facesystems_filename_dev[i]): raise IOError("The score file '%s' does not exist" % facesystems_filename_dev[i])
    if not os.path.isfile(speechsystems_filename_dev[i]): raise IOError("The score file '%s' does not exist" % speechsystems_filename_dev[i])
    if not os.path.isfile(facesystems_filename_eval[i]): raise IOError("The score file '%s' does not exist" % facesystems_filename_eval[i])
    if not os.path.isfile(speechsystems_filename_eval[i]): raise IOError("The score file '%s' does not exist" % speechsystems_filename_eval[i])

    fusion_filename_dev  = os.path.join(args.results_directory, DATABASE, fusionsystems_basedir[i], fusion_subdir[i], 'scores-dev')
    fusion_filename_eval = os.path.join(args.results_directory, DATABASE, fusionsystems_basedir[i], fusion_subdir[i], 'scores-eval')
    utils.ensure_dir(fusion_filename_dev)

    data = []
    data.append(bob.measure.load.split_four_column(facesystems_filename_dev[i]))
    data.append(bob.measure.load.split_four_column(speechsystems_filename_dev[i]))

    import numpy
    data_neg = numpy.vstack([data[k][0] for k in range(2)]).T.copy()
    data_pos = numpy.vstack([data[k][1] for k in range(2)]).T.copy()
    trainer = bob.trainer.CGLogRegTrainer(0.5, 1e-10, 10000)
    machine = trainer.train(data_neg, data_pos)

    # fuse development scores
    data_dev = []
    data_dev.append(bob.measure.load.four_column(facesystems_filename_dev[i]))
    data_dev.append(bob.measure.load.four_column(speechsystems_filename_dev[i]))
    #for i in range(n_systems):
    #  data_dev.append({'4column' : bob.measure.load.four_column, '5column' : bob.measure.load.five_column}[args.parser](args.score_development[i]))
    ndata = len(data_dev[0])
    outf = open(fusion_filename_dev, 'w')
    for k in range(ndata):
      scores = numpy.array([[v[k][-1] for v in data_dev]], dtype=numpy.float64)
      s_fused = machine.forward(scores)[0,0]  
      line = " ".join(data_dev[0][k][0:-1]) + " " + str(s_fused) + "\n"
      outf.write(line)

    # fuse evaluation scores
    data_eval = []
    data_eval.append(bob.measure.load.four_column(facesystems_filename_eval[i]))
    data_eval.append(bob.measure.load.four_column(speechsystems_filename_eval[i]))
    ndata = len(data_eval[0])
    outf = open(fusion_filename_eval, 'w')
    for k in range(ndata):
      scores = numpy.array([[v[k][-1] for v in data_eval]], dtype=numpy.float64)
      s_fused = machine.forward(scores)[0,0]
      line = " ".join(data_eval[0][k][0:-1]) + " " + str(s_fused) + "\n"
      outf.write(line)

  return 0

def parse_command_line(command_line_options):
  """Parse the program options"""
  import argparse
  parser = argparse.ArgumentParser(description=__doc__,
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  # This option is not normally shown to the user...
  parser.add_argument('-r', '--results-directory', metavar="DIR", required=True,
      help="Name of the results directory")
  return parser.parse_args(command_line_options)

def main(command_line_parameters = sys.argv):
  """Fuses scores on MOBIO"""
  args = parse_command_line(command_line_parameters[1:])
  
  mobio_fusion(args, command_line_parameters[1:])

if __name__ == '__main__':
  main(sys.argv[1:])
