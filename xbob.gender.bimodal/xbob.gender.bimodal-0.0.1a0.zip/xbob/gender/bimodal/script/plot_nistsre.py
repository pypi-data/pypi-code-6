#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Mon Apr  7 11:51:11 CEST 2014
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

from .. import utils

def plot_nistsre(args, command_line_parameters):
  """Plotting ROC on NIST SRE"""

  outfilename = args.output_filename

  DATABASE = 'nistsre'
  PROTOCOL = 'protocol'
  systems_subdir = [[os.path.join('linear_c%d' % k) for k in [1, 5, 10, 20, 100, 1000, 10000]],
                    [os.path.join('scores')],
                    [os.path.join('scores')],
                    [os.path.join('scores', PROTOCOL, 'nonorm')]]
  systems_scores = [None] * len(systems_subdir)
 
  #tv_svm, isv, gmm, tv_cos
  systems_basedir = [os.path.join('mfcc60', 'ivec', 'svm'),
                     os.path.join('mfcc60', 'isv'),
                     os.path.join('mfcc60', 'gmm'),
                     os.path.join('mfcc60', 'ivec', 'cosine')]
    
  for bdi,bd in enumerate(systems_basedir):
    acc_max = None
    filename_max = None
    for sdi, sd in enumerate(systems_subdir[bdi]):
      filename = os.path.join(args.results_directory, DATABASE, bd, sd, 'scores-dev')
      filename_eval = os.path.join(args.results_directory, DATABASE, bd, sd, 'scores-eval')
      # read score file
      acc, tpr, tnr = utils.accuracy_tpr_tnr(filename)
      if acc_max == None or acc > acc_max:
        acc_max = acc
        filename_max = filename_eval
    systems_scores[bdi] = filename_max

  # Generates the plot
  legends = ['TV-SVM', 'ISV', 'GMM', 'TV-Cosine']
  is_cosine = [False, False, False, True]

  import matplotlib
  if not hasattr(matplotlib, 'backends'): matplotlib.use('pdf')
  from matplotlib.backends.backend_pdf import PdfPages
  pp = PdfPages(outfilename)
  utils.plot_roc(systems_scores, legends, is_cosine, pp)
  pp.close()


def parse_args(command_line_parameters):
  """This function parses the given options (which by default are the command line options)."""
  # set up command line parser
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-r', '--results-directory', metavar="DIR", required=True,
      help="Name of the results directory")
  parser.add_argument('-o', '--output-filename', default="nistsre.pdf",
      help="Name of the output pdf file (defaults to %(default)s)", metavar="FILE")
  return parser.parse_args(command_line_parameters) 


def main(command_line_parameters = sys.argv):
  """Main routine"""
  # do the command line parsing
  args = parse_args(command_line_parameters[1:])

  plot_nistsre(args, command_line_parameters)

if __name__ == "__main__":
  main()

