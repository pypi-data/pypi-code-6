import numpy

import rasterio.dtypes

def test_np_dt_complex():
    assert rasterio.dtypes.check_dtype(numpy.complex_)
