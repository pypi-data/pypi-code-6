from __future__ import division
import numpy as np
from copy import copy
from pyoperators import MPI
from numpy.testing import assert_equal
from pyoperators.utils.testing import assert_same
from qubic import QubicAcquisition, QubicInstrument, create_random_pointings
from qubic.mapmaking import tod2map_all, tod2map_each, _get_operator

rank = MPI.COMM_WORLD.rank
size = MPI.COMM_WORLD.size


def test():
    instruments = (QubicInstrument('monochromatic,nopol')[:10],
                   QubicInstrument('monochromatic')[:10])
    np.random.seed(0)
    sampling = create_random_pointings([0, 90], 30, 5)
    sampling.angle_hwp = np.random.random_integers(0, 7, len(sampling)) * 11.25
    skies = np.ones(12 * 256**2), np.ones((12 * 256**2, 3))

    def func(instrument, sampling, sky, ref1, ref2, ref3, ref4, ref5, ref6):
        nprocs_instrument = max(size // 2, 1)
        acq = QubicAcquisition(instrument, sampling,
                               nprocs_instrument=nprocs_instrument)
        assert_equal(acq.comm.size, size)
        assert_equal(acq.instrument.detector.comm.size, nprocs_instrument)
        assert_equal(acq.sampling.comm.size, size / nprocs_instrument)
        H = _get_operator(acq)
        tod = H(sky)
        #actual1 = acq.unpack(H(sky))
        #assert_same(actual1, ref1, atol=10)
        actual2 = H.T(tod)
        assert_same(actual2, ref2, atol=10)
        actual2 = (H.T * H)(sky)
        assert_same(actual2, ref2, atol=10)
        actual3, actual4 = tod2map_all(acq, tod, disp=False)
        assert_same(actual3, ref3, atol=100)
        assert_same(actual4, ref4)
        #actual5, actual6 = tod2map_each(acq, tod, disp=False)
        #assert_same(actual5, ref5, atol=1000)
        #assert_same(actual6, ref6)

    for instrument, sky in zip(instruments, skies):
        acq = QubicAcquisition(instrument, sampling, comm=MPI.COMM_SELF)
        assert_equal(acq.comm.size, 1)
        H = acq.get_operator()

        tod = H(sky)
        ref1 = acq.unpack(tod)
        ref2 = H.T(tod)
        ref3, ref4 = tod2map_all(acq, tod, disp=False)
        ref5, ref6 = None, None #tod2map_each(acq, tod, disp=False)
        yield (func, copy(instrument), copy(sampling), sky, ref1, ref2, ref3,
               ref4, ref5, ref6)
