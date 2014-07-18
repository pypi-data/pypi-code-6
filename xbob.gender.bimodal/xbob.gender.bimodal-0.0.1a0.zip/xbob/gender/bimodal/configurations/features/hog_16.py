#!/usr/bin/env python
# vim: set fileencoding=utf-8
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Mon Apr  7 23:50:02 CEST 2014
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

import xbob.gender.bimodal

# feature extraction
feature_extractor = xbob.gender.bimodal.features.HOG(
    height = 16,
    width = 16,
    nb_bins = 8,
    full_orientation = False,
    # cell setup
    cell_size = 4,
    cell_overlap = 0,
    # block setup
    block_size = 2,
    block_overlap = 1,
)
