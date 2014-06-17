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

"""another test, of an older implementation...
"""

import logging

from datetime import datetime

logger = logging.getLogger("")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)


class MyFormatter(logging.Formatter):
    converter = datetime.fromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S")
            s = "%s.%03d" % (t, record.msecs)
        return s

formatter = MyFormatter('[ %(levelname)s %(name)s %(asctime)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


from pyspectral.rsr_reader import RelativeSpectralResponse
from pyspectral.solar import (
    SolarIrradianceSpectrum, TOTAL_IRRADIANCE_SPECTRUM_2000ASTM)
modis = RelativeSpectralResponse('eos', '2', 'modis')
solar_irr = SolarIrradianceSpectrum(
    TOTAL_IRRADIANCE_SPECTRUM_2000ASTM, dlambda=0.005)
sflux = solar_irr.inband_solarflux(modis.rsr['20'])
print("Solar flux over Band: ", sflux)

from pyspectral.nir_reflectance import Calculator
sunz = 80.
tb3 = 290.0
tb4 = 282.0
refl37 = Calculator(modis.rsr['20'], solar_flux=sflux)
print refl37.reflectance_from_tbs(sunz, tb3, tb4)
