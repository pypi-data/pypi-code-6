from __future__ import division
import numpy as np
from pyoperators.utils.testing import assert_same
from qubic import QubicAcquisition, QubicInstrument, create_random_pointings
from qubic.mapmaking import tod2map_all, tod2map_each, _get_operator


def test():
    instruments = (QubicInstrument('monochromatic,nopol')[:10],
                   QubicInstrument('monochromatic')[:10])
    sampling = create_random_pointings([0, 90], 30, 5)
    sampling.angle_hwp = np.random.random_integers(0, 7, len(sampling)) * 11.25
    skies = np.ones(12 * 256**2), np.ones((12 * 256**2, 3))

    def func(acq, max_sampling, sky, ref1, ref2, ref3, ref4, ref5, ref6):
        nbytes_per_sampling = acq.get_projection_nbytes() // len(acq.sampling)
        max_nbytes = None if max_sampling is None \
                          else max_sampling * nbytes_per_sampling
        H = _get_operator(acq, max_nbytes=max_nbytes)
        actual1 = H(sky)
        assert_same(actual1, ref1, atol=10)
        actual2 = H.T(actual1)
        assert_same(actual2, ref2, atol=10)
        actual2 = (H.T * H)(sky)
        assert_same(actual2, ref2, atol=10)
        actual3, actual4 = tod2map_all(acq, ref1, max_nbytes=max_nbytes,
                                       disp=False)
        assert_same(actual3, ref3, atol=10)
        assert_same(actual4, ref4)
        actual5, actual6 = tod2map_each(acq, ref1, max_nbytes=max_nbytes,
                                        disp=False)
        assert_same(actual5, ref5, atol=1000)
        assert_same(actual6, ref6)

    for instrument, sky in zip(instruments, skies):
        acq = QubicAcquisition(instrument, sampling)
        H = acq.get_operator()
        ref1 = H(sky)
        ref2 = H.T(ref1)
        ref3, ref4 = tod2map_all(acq, ref1, disp=False)
        ref5, ref6 = tod2map_each(acq, ref1, disp=False)
        for max_sampling in None, 10, 29, 30:
            yield (func, acq, max_sampling, sky, ref1, ref2, ref3, ref4,
                   ref5, ref6)
