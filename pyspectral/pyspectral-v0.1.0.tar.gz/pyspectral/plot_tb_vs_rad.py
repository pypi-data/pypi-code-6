#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2014 Adam.Dybbroe

# Author(s):

#   Adam.Dybbroe <a000680@c14526.ad.smhi.se>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Plot the Tb as a fucntion of radiance using the EUMETSAT published
parameters for the non-linear regression algorithm.
"""

import numpy as np
from pyspectral.radiance_tb_conversion import RadTbConverter

sev = RadTbConverter(
    'meteosat', '8', 'seviri', 'IR3.9', wavespace='wavenumber')
tb_ = np.arange(150., 350., 0.1)
retv = sev.tb2radiance_simple(tb_, 'IR3.9')
rad = retv['radiance']
retv2 = sev.tb2radiance(tb_, 'IR3.9')
rad2 = retv2['radiance']

tb_rad_obs_file = "/local_disk/laptop/Satsa/Pytroll/demo/refl39/tbs_and_rads.npz"
this = np.load(tb_rad_obs_file)

from matplotlib import pylab

fig = pylab.figure(figsize=(9, 6))
#pylab.plot(rad * 10**5, tb_, color='blue')
#pylab.plot(tb_, (rad - rad2) / rad, color='blue')
#pylab.plot(tb_, rad2 * 100000, color='green')
pylab.plot(tb_, rad * 100000, color='red')
pylab.plot(this['tbs'], this['rad'], 'b+')
#pylab.plot(rad, rad2, color='red')
pylab.grid()
pylab.show()
