#!/usr/bin/env python
# vim: set fileencoding=utf-8
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

import facereclib

# Cropping
CROPPED_IMAGE_HEIGHT = 80
CROPPED_IMAGE_WIDTH = CROPPED_IMAGE_HEIGHT

# eye positions for frontal images
RIGHT_EYE_POS = (int(round(CROPPED_IMAGE_HEIGHT / 3.5)), CROPPED_IMAGE_WIDTH / 2 - 10*CROPPED_IMAGE_WIDTH/24/2 -1)
LEFT_EYE_POS  = (int(round(CROPPED_IMAGE_HEIGHT / 3.5)), CROPPED_IMAGE_WIDTH / 2 + 10*CROPPED_IMAGE_WIDTH/24/2)

# eye and mouth position for profile images
# (only appropriate for left profile images; change them for right profiles)
EYE_POS = (16, 20)
MOUTH_POS = (52, 20)

# define the preprocessor
preprocessor = facereclib.preprocessing.FaceCrop(
    cropped_image_size = (CROPPED_IMAGE_HEIGHT, CROPPED_IMAGE_WIDTH),
    cropped_positions = {'leye' : LEFT_EYE_POS, 'reye' : RIGHT_EYE_POS, 'eye' : EYE_POS, 'mouth' : MOUTH_POS}
)
