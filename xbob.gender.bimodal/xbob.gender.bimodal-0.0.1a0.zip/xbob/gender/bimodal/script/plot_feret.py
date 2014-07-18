#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Mon Apr  7 19:31:53 CEST 2014
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

def plot_feret(args, command_line_parameters):
  """Plot results on the FERET database"""

  import matplotlib
  if not hasattr(matplotlib, 'backends'): matplotlib.use('pdf')
  import matplotlib.pyplot as mpl
  from matplotlib.backends.backend_pdf import PdfPages

  outfilename = args.output_filename

  x_pixels = [16, 24, 32, 48, 64, 80]
  DATABASE = 'feret'
  PROTOCOL = 'protocol'
  # for k in [1, 5, 10, 20, 100, 1000, 10000]
  systems_subdir = [[os.path.join('linear_c%d' % k) for k in [5]],
                    [os.path.join('scores')],
                    [os.path.join('scores')],
                    [os.path.join('scores', PROTOCOL, 'nonorm')],
                    [os.path.join('linear_c%d' % k) for k in [5]],
                    [os.path.join('linear_c%d' % k) for k in [5]],
                    [os.path.join('linear_c%d' % k) for k in [5]]]
  systems_acc = [[], [], [], [], [], [], []]

  for xi,x in enumerate(x_pixels):
    #tv_svm, isv, gmm, tv_cos, lbp_svm, hog_svm, raw_svm]
    systems_basedir = [os.path.join('crop%dx%d_dct' % (x, x), 'ivec', 'svm'),
                       os.path.join('crop%dx%d_dct' % (x, x), 'isv'),
                       os.path.join('crop%dx%d_dct' % (x, x), 'gmm'),
                       os.path.join('crop%dx%d_dct' % (x, x), 'ivec', 'cosine'),
                       os.path.join('crop%dx%d_lbp' % (x, x), 'svm'),
                       os.path.join('crop%dx%d_hog' % (x, x), 'svm'),
                       os.path.join('crop%dx%d_raw' % (x, x), 'svm')]
    
    for bdi,bd in enumerate(systems_basedir):
      acc_max = None
      for sdi, sd in enumerate(systems_subdir[bdi]):
        filename = os.path.join(args.results_directory, DATABASE, bd, sd, 'scores-dev')
        acc, tpr, tnr = utils.accuracy_tpr_tnr(filename)
        if acc_max == None or acc > acc_max:
          acc_max = acc
      systems_acc[bdi].append(acc_max)

  legends = ['TV-SVM', 'ISV', 'GMM', 'TV-Cosine', 'LBP-SVM', 'HOG-SVM', 'Raw-SVM']
  colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
  linestyles = [':s']#, '--', ':', '_']
  dashes = [(None,None), (6,2)]

  pp = PdfPages(outfilename)

  fig = mpl.figure()
  for i in range(len(systems_acc)):
    mpl.plot(x_pixels, [100.* v for v in systems_acc[i]], color=colors[i % len(colors)], linewidth=2, linestyle=linestyles[i % len(linestyles)], dashes=dashes[i % len(dashes)], label=legends[i])
 
  #mpl.axis([0,100,0,100])
  mpl.title("Accuracy on FERET")
  mpl.xlabel('Images height in pixels')
  mpl.ylabel('Accuracy (\%)')
  mpl.grid(True, color=(0.3,0.3,0.3))
  mpl.legend(loc='lower right')
  mpl.xlim([14,82])
  mpl.xticks( x_pixels, x_pixels )
  pp.savefig(fig)

  pp.close()

  print("Resolution \t TV-SVM \t ISV \t GMM \t TV-Cosine \t HOG-SVM \t LBP-SVM \t Neural Network \t Raw-SVM \t AdaBoost")
  print("24x24      \t %.1f \t\t %.1f \t %.1f \t %.1f \t\t %.1f \t\t %.1f \t\t %.1f \t\t\t %.1f \t\t %.1f" % (100*systems_acc[0][1], 100*systems_acc[1][1], 100*systems_acc[2][1], 100*systems_acc[3][1], 100*systems_acc[4][1], 76.9, 84.2, 82.6, 81.5))
  print("48x48      \t %.1f \t\t %.1f \t %.1f \t %.1f \t\t %.1f \t\t %.1f \t\t %.1f \t\t\t %.1f \t\t %.1f" % (100*systems_acc[0][2], 100*systems_acc[1][2], 100*systems_acc[2][2], 100*systems_acc[3][2], 100*systems_acc[4][2], 82.1, 82.9, 84.0, 83.9))


def parse_args(command_line_parameters):
  """This function parses the given options (which by default are the command line options)."""
  # set up command line parser
  parser = argparse.ArgumentParser(description=__doc__,
      formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument('-r', '--results-directory', metavar="DIR", required=True,
      help="Name of the results directory")
  parser.add_argument('-o', '--output-filename', default="feret.pdf",
      help="Name of the output pdf file (defaults to %(default)s)", metavar="FILE")

  return parser.parse_args(command_line_parameters) 


def main(command_line_parameters = sys.argv):
  """Main routine"""
  # do the command line parsing
  args = parse_args(command_line_parameters[1:])

  plot_feret(args, command_line_parameters)

if __name__ == "__main__":
  main()

