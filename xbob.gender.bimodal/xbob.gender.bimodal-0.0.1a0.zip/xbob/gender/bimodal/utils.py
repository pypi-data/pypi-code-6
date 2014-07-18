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

import os
def ensure_dir(f):
  d = os.path.dirname(f)
  if not os.path.exists(d):
    os.makedirs(d)

def ensure_directory(d):
  if not os.path.exists(d):
    os.makedirs(d)


import facereclib
class ParaGridParameters(facereclib.utils.GridParameters):
  """This class is defining the options that are required to submit parallel jobs to the SGE grid.
  """

  def __init__(
    self,
    # queue setup for the SGE grid (only used if grid = 'sge', the default)
    init_training_queue = '8G',
    **kwargs
  ):  

    # call base class constructor with its set of parameters
    facereclib.utils.GridParameters.__init__(self, **kwargs)

    # the queues
    self.init_training_queue = self.queue(init_training_queue)


def plot_roc(systems_scores, legends, is_cosine, pp, title=None, zoom=False):
  import matplotlib.pyplot as mpl
  import bob
  import numpy

  colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

  assert len(systems_scores) == len(legends)
  assert len(is_cosine) == len(legends)

  linestyles = ['_', '-', '--', ':']
  dashes = [(None,None), (6,2), (3,3)]

  fig = mpl.figure()
  npoints = 100
  for i in range(len(systems_scores)):
    lst = bob.measure.load.four_column(systems_scores[i])
    if is_cosine[i] == 'False':
      lst_p = numpy.array([l[3] for l in lst if l[0] == 'male' and l[1] == 'male'])
      lst_n = -numpy.array([l[3] for l in lst if l[0] == 'female' and  l[1] == 'female'])
    else:
      lst_p = numpy.array([l[3] for l in sorted(lst, key=lambda x: x[2]) if l[0] == 'male' and l[1] == 'male'])
      lst_pvsn = numpy.array([l[3] for l in sorted(lst, key=lambda x: x[2]) if l[0] == 'female' and l[1] == 'male'])
      lst_n = numpy.array([l[3] for l in  sorted(lst, key=lambda x: x[2]) if l[0] == 'female' and  l[1] == 'female'])
      lst_nvsp = numpy.array([l[3] for l in sorted(lst, key=lambda x: x[2]) if l[0] == 'male' and l[1] == 'female'])
      lst_p = lst_p - lst_pvsn
      lst_n = -(lst_n - lst_nvsp)
    out = bob.measure.roc(lst_n, lst_p, npoints)
    mpl.plot(100.0*out[1,:], 100.0*(1-out[0,:]), color=colors[i % len(colors)], linewidth=1.5, dashes=dashes[i % len(dashes)], linestyle=linestyles[i % len(linestyles)], label=legends[i])
 
  if zoom == True:
    mpl.axis([0,20,80,100])
  else:
    mpl.axis([0,100,0,100])
  if title == None:
    mpl.title('ROC Curves')
  else:
    mpl.title(title)
  mpl.xlabel('Fraction of females classified incorrectly (\%)')
  mpl.ylabel('Fraction of males classified correctly (\%)')
  mpl.grid(True, color=(0.3,0.3,0.3))
  mpl.legend(loc='lower right')
  pp.savefig(fig)


def accuracy_tpr_tnr(filename):
  import numpy
  score_file=open(filename, 'r')

  dictionary = {}
  for line in score_file:
    line=line.strip()
    probe = line.split(' ')[2]
    
    val = [line.split(' ')[0], line.split(' ')[1], float(line.split(' ')[3])]
    if not probe in dictionary:
      dictionary[probe]= [val]
    else:
      dictionary[probe].append(val)

  correct_classification_number = 0 
  true_positive = 0 # male
  num_positive = 0 

  true_negative = 0 # female
  num_negative = 0 

  total_number = len(dictionary)

  for probe in dictionary:
    max_score = numpy.float('-Inf')
    class_id = None
    real_id = None
    for list_scores in dictionary[probe]:
      if max_score < list_scores[2]:
        max_score = list_scores[2]
        class_id = list_scores[0]
        real_id = list_scores[1]
    if class_id == real_id:
      correct_classification_number = correct_classification_number + 1
      if real_id == 'male': # male is considered as positive
        true_positive = true_positive + 1
      else: 
        true_negative = true_negative + 1
    if real_id == 'male':
      num_positive = num_positive + 1
    else:
      num_negative = num_negative + 1

  accuracy = float(correct_classification_number)/ total_number
  tpr = float(true_positive)/num_positive
  tnr = float(true_negative)/num_negative
  return accuracy, tpr, tnr

