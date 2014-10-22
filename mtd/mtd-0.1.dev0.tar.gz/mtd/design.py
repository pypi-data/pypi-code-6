# -*- coding: utf-8 -*-

from __future__ import division

import numpy as np

__all__ = 'ExperimentDesign',


def _atleast_2d_column(array):
    array = np.atleast_2d(array)
    if array.shape[0] == 1:
        array = array.T
    return array


class ExperimentDesign(object):
    """
    Store and manipulate multidimensional simulator input and output.

    theta: (nthetasamples, ntheta) or (nthetasamples,)
        Test points for calibration parameters theta.
    x: (nsettings, nx) or (nxsamples,)
        Settings for controllable / measurable parameters x.  It is assumed
        that the theta design is repeated for each x.
    y: (nxsamples, nthetasamples, nfeatures)
        Observations at each (x, theta).

    """
    def __init__(self, theta, x, y):
        self._theta = _atleast_2d_column(theta).astype(float, copy=False)
        self._x = _atleast_2d_column(x).astype(float, copy=False)
        self._y = np.atleast_3d(y).astype(float, copy=False)

        # verify dimensions match
        if self._y.shape[:2] != (self.nxsamples, self.nthetasamples):
            raise ValueError(
                'Mismatched dimensions: shape of y must be '
                '(nxsamples, nthetasamples, nfeatures) == ({}, {}, nfeatures).'
                .format(self.nxsamples, self.nthetasamples)
            )

        # cache for (x, theta) rescaling
        self._x_min = self._x.min(axis=0)
        self._x_max = self._x.max(axis=0)
        self._x_range = self._x.ptp(axis=0)
        self._theta_min = self._theta.min(axis=0)
        self._theta_max = self._theta.max(axis=0)
        self._theta_range = self._theta.ptp(axis=0)
        self._x_theta_min = np.concatenate((self._x_min, self._theta_min))
        self._x_theta_max = np.concatenate((self._x_max, self._theta_max))
        self._x_theta_range = np.concatenate((self._x_range,
                                              self._theta_range))

    @property
    def nthetasamples(self):
        return self._theta.shape[0]

    @property
    def nxsamples(self):
        return self._x.shape[0]

    @property
    def nsamples(self):
        return self.nthetasamples * self.nxsamples

    @property
    def ntheta(self):
        return self._theta.shape[1]

    @property
    def nx(self):
        return self._x.shape[1]

    @property
    def ndim(self):
        return self.ntheta + self.nx

    @property
    def nfeatures(self):
        return self._y.shape[2]

    def theta_at_all_x(self, theta, scaled=True):
        """
        Construct an array of theta repeated at all x, i.e.
        ((x0, theta), (x1, theta), ...).

        scaled: boolean
            If true (default), scale the (x, theta) array to the unit hypercube
            [0, 1]^ndim.

        """
        theta = np.atleast_2d(theta)
        nthetasamples, ntheta = theta.shape

        if ntheta != self.ntheta:
            raise ValueError('Shape of theta does not match design.')

        if np.any((theta < self._theta_min) | (theta > self._theta_max)):
            raise ValueError('At least one theta is out of the design range.')

        x_theta = np.column_stack((
            np.repeat(self._x, nthetasamples, axis=0),
            np.tile(theta, (self.nxsamples, 1))
        ))

        if scaled:
            x_theta -= self._x_theta_min
            x_theta /= self._x_theta_range

        return x_theta

    def full_design(self, scaled=True):
        """
        Construct the full (x, theta) design matrix.

        scaled: boolean
            Passed to theta_at_all_x().

        """
        return self.theta_at_all_x(self._theta, scaled=scaled)
