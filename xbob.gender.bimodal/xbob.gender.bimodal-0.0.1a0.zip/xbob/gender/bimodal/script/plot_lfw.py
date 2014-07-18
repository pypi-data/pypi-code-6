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

def plot_lfw(args, command_line_parameters):
  """Plotting ROC on LFW"""

  outfilename = args.output_filename

  DATABASE = 'lfw-fold0'
  PROTOCOL = 'fold0'
  # for k in [1, 5, 10, 20, 100, 1000, 10000]
  systems_subdir = [[os.path.join('linear_c%d' % k) for k in [5]],
                    [os.path.join('scores')],
                    [os.path.join('scores')],
                    [os.path.join('scores', PROTOCOL, 'nonorm')],
                    [os.path.join('linear_c%d' % k) for k in [5]],
                    [os.path.join('linear_c%d' % k) for k in [5]],
                    [os.path.join('linear_c%d' % k) for k in [5]]]
  systems_scores = [None] * len(systems_subdir)
 
  #tv_svm, isv, gmm, tv_cos, lbp_svm, hog_svm, raw_svm]
  systems_basedir = [os.path.join('crop80x80_dct', 'ivec', 'svm'),
                     os.path.join('crop80x80_dct', 'isv'),
                     os.path.join('crop80x80_dct', 'gmm'),
                     os.path.join('crop80x80_dct', 'ivec', 'cosine'),
                     os.path.join('crop80x80_lbp', 'svm'),
                     os.path.join('crop80x80_hog', 'svm'),
                     os.path.join('crop80x80_raw', 'svm')]
    
  for bdi,bd in enumerate(systems_basedir):
    acc_max = None
    filename_max = None
    for sdi, sd in enumerate(systems_subdir[bdi]):
      filename = os.path.join(args.results_directory, DATABASE, bd, sd, 'scores-dev')
      # read score file
      acc, tpr, tnr = utils.accuracy_tpr_tnr(filename)
      if acc_max == None or acc > acc_max:
        acc_max = acc
        filename_max = filename
    systems_scores[bdi] = filename_max

  # Generates the plot
  legends = ['TV-SVM', 'ISV', 'GMM', 'TV-Cosine', 'LBP-SVM', 'HOG-SVM', 'Raw-SVM']
  is_cosine = [False, False, False, True, False, False, False]

  import matplotlib
  if not hasattr(matplotlib, 'backends'): matplotlib.use('pdf')
  from matplotlib.backends.backend_pdf import PdfPages
  pp = PdfPages(outfilename)
  utils.plot_roc(systems_scores, legends, is_cosine, pp, 'ROC Curves on LFW Fold 0')
  pp.close() 


  FOLDS = ['fold0', 'fold1', 'fold2', 'fold3', 'fold4']
  systems_scores = [None] * len(FOLDS)
  acc_sum = 0
  tpr_sum = 0
  tnr_sum = 0
  for f in FOLDS:
    DATABASE = 'lfw-%s' % f
    PROTOCOL = f
    systems_subdir = [os.path.join('linear_c%d' % k) for k in [5]]
 
    #tv_svm
    system_basedir = os.path.join('crop80x80_dct', 'ivec', 'svm')
    
    acc_max = None
    tpr_max = None
    tnr_max = None
    filename_max = None
    for sdi, sd in enumerate(systems_subdir):
      filename = os.path.join(args.results_directory, DATABASE, system_basedir, sd, 'scores-dev')
      # read score file
      acc, tpr, tnr = utils.accuracy_tpr_tnr(filename)
      if acc_max == None or acc > acc_max:
        acc_max = acc
        tpr_max = tpr
        tnr_max = tnr
    acc_sum += acc_max
    tpr_sum += tpr_max
    tnr_sum += tnr_max
  
  acc_sum = acc_sum / len(FOLDS)
  tpr_sum = tpr_sum / len(FOLDS)
  tnr_sum = tnr_sum / len(FOLDS)
  
  print("System \t\t\t\t\t\t\t Acc \t TPR \t TNR")
  print("-" * 80)
  print("TV-SVM (80x80) \t\t\t\t\t\t %.1f \t %.1f \t %.1f" % (100*acc_sum, 100*tpr_sum, 100*tnr_sum))
  print("Gabor-PCA-SVM (120x105) [Dagog-Casas et al, 2011] \t 94.0 \t 97.5 \t 82.2")
  print("LBP-PCA-SVM (120x105) [Dagog-Casas et al, 2011] \t 93.8 \t 97.0 \t 83.0")
  print("Raw-PCA-SVM (120x105) [Dagog-Casas et al, 2011] \t 89.2 \t 95.4 \t 68.1")
  

def parse_args(command_line_parameters):
  """This function parses the given options (which by default are the command line options)."""
  # set up command line parser
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-r', '--results-directory', metavar="DIR", required=True,
      help="Name of the results directory")
  parser.add_argument('-o', '--output-filename', default="lfw.pdf",
      help="Name of the output pdf file (defaults to %(default)s)", metavar="FILE")
  return parser.parse_args(command_line_parameters) 


def main(command_line_parameters = sys.argv):
  """Main routine"""
  # do the command line parsing
  args = parse_args(command_line_parameters[1:])

  plot_lfw(args, command_line_parameters)

if __name__ == "__main__":
  main()

