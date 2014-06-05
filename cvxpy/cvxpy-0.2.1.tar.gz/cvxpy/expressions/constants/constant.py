"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

import cvxpy.utilities as u
import cvxpy.interface as intf
import cvxpy.settings as s
from cvxpy.expressions.leaf import Leaf
import cvxpy.lin_ops.lin_utils as lu

class Constant(Leaf):
    """
    A constant, either matrix or scalar.
    """
    def __init__(self, value):
        # Keep sparse matrices sparse.
        if intf.is_sparse(value):
            self._value = intf.DEFAULT_SPARSE_INTERFACE.const_to_matrix(value)
            self._sparse = True
        else:
            self._value = intf.DEFAULT_INTERFACE.const_to_matrix(value)
            self._sparse = False
        # Set DCP attributes.
        self.init_dcp_attr()

    def name(self):
        return str(self.value)

    @property
    def value(self):
        return self._value

    # Return the DCP attributes of the constant.
    def init_dcp_attr(self):
        shape = u.Shape(*intf.size(self.value))
        # If scalar, check sign. Else unknown sign.
        if shape.size == (1, 1):
            sign = u.Sign.val_to_sign(self.value)
        else:
            sign = u.Sign.UNKNOWN
        self._dcp_attr = u.DCPAttr(sign, u.Curvature.CONSTANT, shape)

    def canonicalize(self):
        """Returns the graph implementation of the object.

        Returns:
            A tuple of (affine expression, [constraints]).
        """
        obj = lu.create_const(self.value, self.size, self._sparse)
        return (obj, [])
