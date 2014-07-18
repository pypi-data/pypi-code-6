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

def plot_mobio(args, command_line_parameters):
  """Plotting ROC on MOBIO"""

  outfilename = args.output_filename

  import matplotlib
  if not hasattr(matplotlib, 'backends'): matplotlib.use('pdf')
  from matplotlib.backends.backend_pdf import PdfPages
  pp = PdfPages(outfilename)


  DATABASE = 'mobio'
  PROTOCOL = 'protocol'

  # Visual
  systems_subdir = [[os.path.join('linear_c%d' % k) for k in [1, 5, 10, 20, 100, 1000, 10000]],
                    [os.path.join('scores')],
                    [os.path.join('scores')],
                    [os.path.join('scores', PROTOCOL, 'nonorm')],
                    [os.path.join('linear_c%d' % k) for k in [1, 5, 10, 20, 100, 1000, 10000]],
                    [os.path.join('linear_c%d' % k) for k in [1, 5, 10, 20, 100, 1000, 10000]],
                    [os.path.join('linear_c%d' % k) for k in [1, 5, 10, 20, 100, 1000, 10000]]]
  systems_scores = [None] * len(systems_subdir)
  face_acc_tpr_tnr = [None, None, None, None]
 
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
    face_vals = None
    for sdi, sd in enumerate(systems_subdir[bdi]):
      filename = os.path.join(args.results_directory, DATABASE, bd, sd, 'scores-dev')
      filename_eval = os.path.join(args.results_directory, DATABASE, bd, sd, 'scores-eval')
      # read score file
      acc, tpr, tnr = utils.accuracy_tpr_tnr(filename)
      if acc_max == None or acc > acc_max:
        acc_max = acc
        filename_max = filename_eval
        face_vals = [acc, tpr, tnr]
    systems_scores[bdi] = filename_max
    if bdi < 4:
      face_acc_tpr_tnr[bdi] = face_vals

  # Generates the plot
  legends = ['TV-SVM', 'ISV', 'GMM', 'TV-Cosine', 'LBP-SVM', 'HOG-SVM', 'Raw-SVM']
  is_cosine = [False, False, False, True, False, False, False]
  utils.plot_roc(systems_scores, legends, is_cosine, pp, 'ROC Curves on MOBIO Face')


  # Audio
  systems_subdir = [[os.path.join('linear_c%d' % k) for k in [1, 5, 10, 20, 100, 1000, 10000]],
                    [os.path.join('scores')],
                    [os.path.join('scores')],
                    [os.path.join('scores', PROTOCOL, 'nonorm')]]
  systems_scores = [None] * len(systems_subdir)
  speech_acc_tpr_tnr = [None, None, None, None]
 
  #tv_svm, isv, gmm, tv_cos
  systems_basedir = [os.path.join('mfcc60', 'ivec', 'svm'),
                     os.path.join('mfcc60', 'isv'),
                     os.path.join('mfcc60', 'gmm'),
                     os.path.join('mfcc60', 'ivec', 'cosine')]
    
  for bdi,bd in enumerate(systems_basedir):
    acc_max = None
    filename_max = None
    speech_vals = None
    for sdi, sd in enumerate(systems_subdir[bdi]):
      filename = os.path.join(args.results_directory, DATABASE, bd, sd, 'scores-dev')
      filename_eval = os.path.join(args.results_directory, DATABASE, bd, sd, 'scores-eval')
      # read score file
      acc, tpr, tnr = utils.accuracy_tpr_tnr(filename)
      if acc_max == None or acc > acc_max:
        acc_max = acc
        filename_max = filename_eval
        speech_vals = [acc, tpr, tnr]
    systems_scores[bdi] = filename_max
    speech_acc_tpr_tnr[bdi] = speech_vals

  # Generates the plot
  legends = ['TV-SVM', 'ISV', 'GMM', 'TV-Cosine']
  is_cosine = [False, False, False, True]
  utils.plot_roc(systems_scores, legends, is_cosine, pp, 'ROC Curves on MOBIO Speech', True)


  # Fusion
  systems_subdir = [[os.path.join('linear')],
                    [os.path.join('scores')],
                    [os.path.join('scores')],
                    [os.path.join('scores', PROTOCOL, 'nonorm')]]
  systems_scores = [None] * len(systems_subdir)
  fusion_acc_tpr_tnr = [None, None, None, None]
 
  #tv_svm, isv, gmm, tv_cos
  systems_basedir = [os.path.join('fusion', 'ivec', 'svm'),
                     os.path.join('fusion', 'isv'),
                     os.path.join('fusion', 'gmm'),
                     os.path.join('fusion', 'ivec', 'cosine')]
    
  for bdi,bd in enumerate(systems_basedir):
    acc_max = None
    filename_max = None
    speech_vals = None
    for sdi, sd in enumerate(systems_subdir[bdi]):
      filename = os.path.join(args.results_directory, DATABASE, bd, sd, 'scores-dev')
      filename_eval = os.path.join(args.results_directory, DATABASE, bd, sd, 'scores-eval')
      # read score file
      acc, tpr, tnr = utils.accuracy_tpr_tnr(filename)
      if acc_max == None or acc > acc_max:
        acc_max = acc
        filename_max = filename_eval
        speech_vals = [acc, tpr, tnr]
    systems_scores[bdi] = filename_max
    fusion_acc_tpr_tnr[bdi] = speech_vals


  acc_face = []
  acc_spk = []
  acc_bimodal = []
  for i in range(len(systems_basedir)):
    acc_face.append(face_acc_tpr_tnr[i][0]*100)
    acc_spk.append(speech_acc_tpr_tnr[i][0]*100)
    acc_bimodal.append(fusion_acc_tpr_tnr[i][0]*100)
    if i < 3:
      acc_face.append(0)
      acc_spk.append(0)
      acc_bimodal.append(0)

 
  import matplotlib.pyplot as mpl
  fig = mpl.figure(figsize=(8, 3))
  figure_title = "Accuracy on MOBIO"
  mpl.text(1.3, 102.6, figure_title)
  N = len(acc_face)
  ind = numpy.arange(N)    # the x locations for the groups
  width = 0.5       # the width of the bars: can also be len(x) sequence
  p1 = mpl.bar(ind-width, acc_face, width, color='r')
  p2 = mpl.bar(ind, acc_spk, width, color='g')
  p3 = mpl.bar(ind+width, acc_bimodal, width, color='b')
  mpl.ylabel('Accuracy (\%)')
  mpl.xticks(ind+width/2., ( 'TV-SVM', '', 'ISV', '', 'GMM', '', 'TV-Cosine', '',  'All-Fusion') )
  mpl.xlim([-0.8,7.2])
  mpl.ylim([83,100])
  mpl.legend( (p1[0], p2[0], p3[0]), ('Face', 'Speech', 'Bimodal'), bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=3, mode="expand", borderaxespad=0. )
  mpl.grid(True, color=(0.3,0.3,0.3))
  pp.savefig(fig, bbox_inches='tight')

  # Closes PDF
  pp.close() 


  print(" \t \t TV-SVM\t ISV\t GMM\t TV-Cosine")
  print("-" * 50)
  for i,measure in enumerate(['Acc', 'TPR', 'TNR']):
    print("Face \t %s \t %.1f \t %.1f \t %.1f \t %.1f" % (measure, 100*face_acc_tpr_tnr[0][i], 100*face_acc_tpr_tnr[1][i], 100*face_acc_tpr_tnr[2][i], 100*face_acc_tpr_tnr[3][i]))
  print("-" * 50)
  for i,measure in enumerate(['Acc', 'TPR', 'TNR']):
    print("Speech \t %s \t %.1f \t %.1f \t %.1f \t %.1f" % (measure, 100*speech_acc_tpr_tnr[0][i], 100*speech_acc_tpr_tnr[1][i], 100*speech_acc_tpr_tnr[2][i], 100*speech_acc_tpr_tnr[3][i]))



def parse_args(command_line_parameters):
  """This function parses the given options (which by default are the command line options)."""
  # set up command line parser
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-r', '--results-directory', metavar="DIR", required=True,
      help="Name of the results directory")
  parser.add_argument('-o', '--output-filename', default="mobio.pdf",
      help="Name of the output pdf file (defaults to %(default)s)", metavar="FILE")
  return parser.parse_args(command_line_parameters) 


def main(command_line_parameters = sys.argv):
  """Main routine"""
  # do the command line parsing
  args = parse_args(command_line_parameters[1:])

  plot_mobio(args, command_line_parameters)

if __name__ == "__main__":
  main()

