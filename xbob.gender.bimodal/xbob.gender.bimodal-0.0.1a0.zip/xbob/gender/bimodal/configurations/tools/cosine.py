#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Sat Nov 23 16:51:32 CET 2013
#
# Copyright (C) 2013-2014 Idiap Research Institute, Martigny, Switzerland
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

import scipy.spatial
import xbob.gender.bimodal

tool = xbob.gender.bimodal.tools.Distance(
    distance_function = scipy.spatial.distance.cosine,
    is_distance_function = True,
    multiple_model_scoring = 'max',
    multiple_probe_scoring = 'average',
)

