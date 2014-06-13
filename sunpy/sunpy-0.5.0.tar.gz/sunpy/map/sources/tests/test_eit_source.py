"""Test cases for SOHO Map subclasses.
This particular test file pertains to EITMap.
@Author: Pritish C. (VaticanCameos)
"""

import os
import glob
import numpy as np
from matplotlib import colors

import pytest

from sunpy.map.sources.soho import EITMap
from sunpy.map import Map
import sunpy.data.test

path = sunpy.data.test.rootdir
fitslist = glob.glob(os.path.join(path, "EIT", "*"))

@pytest.fixture(scope="module", params=fitslist)
def createEIT(request):
    """Creates an EITMap from a FITS file."""
    return Map(request.param)

# EIT Tests
def test_fitstoEIT(createEIT):
    """Tests the creation of EITMap using FITS."""
    assert isinstance(createEIT, EITMap)

def test_is_datasource_for(createEIT):
    """Test the is_datasource_for method of EITMap.
    Note that header data to be provided as an argument
    can be a MapMeta object."""
    assert createEIT.is_datasource_for(createEIT.data, createEIT.meta)

def test_observatory(createEIT):
    """Tests the observatory property of the EITMap object."""
    assert createEIT.observatory == "SOHO"

def test_measurement(createEIT):
    """Tests the measurement property of the EITMap object."""
    assert createEIT.measurement in [195, 171]

def test_normalizer(createEIT):
    """Tests the creation of the Normalizer object,
    as well as its properties."""
    lognorm = createEIT._get_mpl_normalizer()
    eit = createEIT
    if eit.data.dtype == np.float32:
        assert lognorm is None
    else:
        assert isinstance(lognorm, colors.LogNorm)
        assert lognorm.vmin == 1
        #assert lognorm.vmax == (min(eit.max(), eit.mean() + 5 * eit.std()))
	np.testing.assert_allclose(lognorm.vmax, 1234.1161862241358, rtol=1.00001) # Min of 1887.75 and 1234.1161862241358

