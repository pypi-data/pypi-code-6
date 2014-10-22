# -*- coding: utf-8 -*-

from __future__ import division

import numpy as np
from nose.tools import assert_raises

from .. import ExperimentDesign


def test_design():
    """experiment design"""

    # construct simple test design
    theta = np.arange(10).reshape((5, 2))
    x = 1, 2
    y = 2*theta, 3*theta

    design = ExperimentDesign(theta, x, y)

    # design shape
    assert design.nsamples == 10, \
        'Incorrect number of samples.'

    assert design.ndim == 3, \
        'Incorrect number of design dimensions.'

    assert design.nfeatures == 2, \
        'Incorrect number of features.'

    # bad input
    y_fail = 2*theta, 3*theta, 4*theta
    assert_raises(ValueError, ExperimentDesign, theta, x, y_fail)

    y_fail = [np.arange(12).reshape(6, 2)] * 2
    assert_raises(ValueError, ExperimentDesign, theta, x, y_fail)

    # test point
    t = 4, 9

    xt = design.theta_at_all_x(t, scaled=False)
    assert np.array_equal(xt, ((1, 4, 9), (2, 4, 9))), \
        'Incorrect (x, theta) test point.'

    xt_scaled = design.theta_at_all_x(t, scaled=True)
    assert np.array_equal(xt_scaled, ((0, .5, 1), (1, .5, 1))), \
        'Incorrect scaled (x, theta) test point.'

    # too many thetas
    assert_raises(ValueError, design.theta_at_all_x, (4, 5, 6))

    # out of range
    assert_raises(ValueError, design.theta_at_all_x, (4, 20))

    # full (x, theta) design
    full = design.full_design(scaled=False)

    assert full.shape == (10, 3), \
        'Incorrect full design dimensions.'

    assert np.array_equiv(full[0], (1, 0, 1)), \
        'Incorrect full design first element.'

    assert np.array_equiv(full[-1], (2, 8, 9)), \
        'Incorrect full design last element.'

    # scaled design
    full_scaled = design.full_design(scaled=True)

    assert np.all((full_scaled >= 0) & (full_scaled <= 1)), \
        'Design is not properly scaled to [0, 1].'

    assert np.array_equiv(full_scaled[0], (0, 0, 0)), \
        'Incorrect scaled design first element.'

    assert np.array_equiv(full_scaled[-1], (1, 1, 1)), \
        'Incorrect scaled design last element.'

    assert np.array_equiv(full_scaled, (full - (1, 0, 1))/(1, 8, 8)), \
        'Scaled and unscaled designs are inconsistent.'
