from __future__ import division

import numpy as np
from itertools import izip
from pyoperators import (
    BlockColumnOperator, BlockDiagonalOperator, DiagonalOperator,
    MPIDistributionIdentityOperator, PackOperator, pcg, proxy_group,
    rule_manager)
from .acquisition import QubicAcquisition
from .utils import progress_bar

__all__ = ['map2tod', 'tod2map_all', 'tod2map_each']


def _get_operator(acq, max_nbytes=None, verbose=True):
    projection = _get_projection(acq, max_nbytes=max_nbytes, verbose=verbose)
    hwp = _get_hwp(acq, max_nbytes=max_nbytes)
    polarizer = acq.get_polarizer_operator()
    response = acq.get_detector_response_operator()

    with rule_manager(inplace=True):
        H = response * polarizer * (hwp * projection)
    if acq.scene.kind == 'QU':
        H = acq.get_subtract_grids_operator() * H

    return H


def _get_projection(acq, max_nbytes=None, verbose=True):
    nbytes = acq.get_projection_nbytes()
    if max_nbytes is None or nbytes <= max_nbytes:
        P = acq.get_projection_operator(verbose=verbose)
    else:
        n = int(np.ceil(nbytes / max_nbytes))
        samplings = acq.sampling.split(n)
        acqs = [QubicAcquisition(acq.instrument, _, acq.scene)
                for _ in samplings]

        def callback(i):
            return acqs[i].get_projection_operator(verbose=False)
        P = BlockColumnOperator(proxy_group(n, callback), axisout=1)
    return _distribute(acq, P)


def _get_projection_restricted(acq, P, mask, max_nbytes=None, verbose=True):
    nbytes = acq.get_projection_nbytes()
    if max_nbytes is None or nbytes <= max_nbytes:
        if acq.comm.size > 1:
            P = P.operands[0]
        P.restrict(mask)
    else:
        n = int(np.ceil(nbytes / max_nbytes))
        samplings = acq.sampling.split(n)
        acqs = [QubicAcquisition(acq.instrument, _, acq.scene)
                for _ in samplings]

        def callback(i):
            p = acqs[i].get_projection_operator(verbose=False)
            p.restrict(mask)
            return p
        P = BlockColumnOperator(proxy_group(n, callback), axisout=1)
    return _distribute(acq, P)


def _get_hwp(acq, max_nbytes=None):
    nbytes = acq.get_projection_nbytes()
    if max_nbytes is None or nbytes <= max_nbytes:
        return acq.get_hwp_operator()

    n = int(np.ceil(nbytes / max_nbytes))
    samplings = acq.sampling.split(n)
    acqs = [QubicAcquisition(acq.instrument, _) for _ in samplings]

    def callback(i):
        return acqs[i].get_hwp_operator()
    return BlockDiagonalOperator(proxy_group(n, callback), axisout=1)


def _distribute(acq, H):
    if acq.comm.size > 1:
        H = H(MPIDistributionIdentityOperator(acq.comm))
    return H


def map2tod(acq, map, convolution=False, max_nbytes=None):
    """
    tod = map2tod(acquisition, map)
    tod, convolved_map = map2tod(acquisition, map, convolution=True)

    Parameters
    ----------
    acq : QubicAcquisition
        The QUBIC acquisition.
    map : I, QU or IQU maps
        Temperature, QU or IQU maps of shapes npix, (npix, 2), (npix, 3)
        with npix = 12 * nside**2
    convolution : boolean, optional
        Set to True to convolve the input map by a gaussian and return it.
    max_nbytes : int
        Maximum number of bytes for the pointing matrix. If the actual size
        is greater than this number, the computation of the pointing matrix
        will be performed on the fly at each iteration.

    Returns
    -------
    tod : array
        The Time-Ordered-Data of shape (ndetectors, ntimes).
    convolved_map : array
        The convolved map, if the convolution keyword is set.

    """
    if convolution:
        convolution = acq.get_convolution_peak_operator()
        map = convolution(map)

    H = _get_operator(acq, max_nbytes=max_nbytes)
    tod = H(map)

    if convolution:
        return tod, map

    return tod


def _tod2map(acq, tod, coverage_threshold, disp_pcg, disp_pmatrix,
             max_nbytes, tol):
    projection = _get_projection(acq, max_nbytes=max_nbytes,
                                 verbose=disp_pmatrix)
    shape = len(acq.instrument), len(acq.sampling)
    kind = acq.scene.kind
    if kind == 'I':
        ones = np.ones(shape)
    elif kind == 'IQU':
        ones = np.zeros(shape + (3,))
        ones[..., 0] = 1
    else:
        raise NotImplementedError()
    coverage = projection.T(ones)
    if kind == 'IQU':
        coverage = coverage[..., 0]
    mask = coverage > coverage_threshold
    projection = _get_projection_restricted(
        acq, projection, mask, max_nbytes=max_nbytes, verbose=disp_pmatrix)
    pack = PackOperator(mask, broadcast='rightward')
    hwp = _get_hwp(acq, max_nbytes=max_nbytes)
    polarizer = acq.get_polarizer_operator()
    response = acq.get_detector_response_operator()
    H = response * polarizer * (hwp * projection)
    if acq.scene.kind == 'QU':
        H = acq.get_subtract_grid_operator() * H

    invNtt = acq.get_invntt_operator()
    preconditioner = DiagonalOperator(1/coverage[mask], broadcast='rightward')
    A = H.T * invNtt * H
    solution = pcg(A, H.T(invNtt(tod)), M=preconditioner,
                   disp=disp_pcg, tol=tol)
    output_map = pack.T(solution['x'])
    return output_map, coverage


def tod2map_all(acquisition, tod, coverage_threshold=0, disp=True, tol=1e-4,
                max_nbytes=None):
    """
    Compute map using all detectors.

    map, coverage = tod2map_all(acquisition, tod, [coverage_threshold,
                                coverage_threshold, disp, tol])

    Parameters
    ----------
    acquisition : QubicAcquisition
        The QUBIC acquisition.
    tod : array-like
        The Time-Ordered-Data of shape (ndetectors, ntimes).
    coverage_threshold : float, optional
        The coverage threshold used to reject map pixels from
        the reconstruction.
    disp : boolean, optional
        Display of solver's iterations.
    tol : float, optional
        Solver tolerance.
    max_nbytes : int
        Maximum number of bytes for the pointing matrix. If the actual size
        is greater than this number, the computation of the pointing matrix
        will be performed on the fly at each iteration.

    Returns
    -------
    map : I, QU or IQU maps
        Temperature, QU or IQU maps of shapes npix, (npix, 2), (npix, 3)
        with npix = 12 * nside**2
    """
    return _tod2map(acquisition, tod, coverage_threshold, disp, True,
                    max_nbytes, tol)


def tod2map_each(acquisition, tod, coverage_threshold=0, disp=True, tol=1e-4,
                 max_nbytes=None):
    """
    Compute average map from each detector.

    map, coverage = tod2map_each(acquisition, tod, [coverage_threshold,
                                 coverage_threshold, disp, tol])

    Parameters
    ----------
    acquisition : QubicAcquisition
        The QUBIC acquisition.
    tod : array-like
        The Time-Ordered-Data of shape (ndetectors, ntimes).
    coverage_threshold : float, optional
        The coverage threshold used to reject map pixels from
        the reconstruction.
    disp : boolean, optional
        Display of solver's iterations.
    tol : float, optional
        Solver tolerance.
    max_nbytes : int
        Maximum number of bytes for the pointing matrix. If the actual size
        is greater than this number, the computation of the pointing matrix
        will be performed on the fly at each iteration.

    Returns
    -------
    map : I, QU or IQU maps
        Temperature, QU or IQU maps of shapes npix, (npix, 2), (npix, 3)
        with npix = 12 * nside**2

    """
    instrument = acquisition.instrument
    x = np.zeros(acquisition.scene.shape)
    n = np.zeros(acquisition.scene.shape[0])
    if disp:
        bar = progress_bar(len(instrument), 'TOD2MAP_EACH')
    for i, t in izip(instrument, tod):
        acq = QubicAcquisition(i, acquisition.sampling)
        x_, n_ = _tod2map(acq, t[None, :], coverage_threshold, False, False,
                          max_nbytes, tol)
        x += x_
        n += n_
        if disp:
            bar.update()

    if acq.scene.kind == 'I':
        return np.nan_to_num(x / n), n
    return np.nan_to_num(x / n[:, None]), n
