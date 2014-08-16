#!/usr/bin/env python

import numpy

class OnlineArray(numpy.ndarray):
    """
    This class mimics a multidimensional numpy array, except it does not store
    any data, instead all values are calculated on the fly. This can be
    convenient when an array gets too large and the receiving function only
    accepts an array.
    """
    def __new__(cls, shape, dtype=float, buffer=None, offset=0,
              strides=None, order=None, function=None, index=(),
              unbounded=False):
        """
        Constructor for OnlineArray.

        For more documentation, see the help of {ndarray}.

        :arg function: General function having only integer arguments.
        :type function: function
        :arg index: The index of this arrray in its parent array.
        :type index: tuple(int)
        :arg unbounded: Create an unbounded array.
        :type unbounded: bool
        """
        array = super(OnlineArray, cls).__new__(cls, shape, dtype, buffer,
            offset, strides, order)
        array.function = function
        array.index = index
        array.unbounded = unbounded

        return array
    #__new__

    def __getitem__(self, index):
        """
        Retrieve an item from the array.

        :arg index: The index of the element.
        :type index: int or tuple(int)

        :returns: Either a sub-array or an element.
        :rtype: OnlineArray or unknown
        """
        # NumPy style indexing.
        if type(index) == tuple:
            checked_index = self._check_boundaries(index)

            # A sub-array was requested.
            if len(checked_index) < self.ndim:
                return OnlineArray(self.shape[len(checked_index):],
                    function=self.function, index=self.index + checked_index,
                    unbounded=self.unbounded)

            # An element was requested.
            return self.function(*checked_index)
        #if
        else:
            checked_index = self._check_boundaries((index, ))[0]

        # Nested list style indexing.
        if self.ndim > 1:
            return OnlineArray(self.shape[1:],
                function=self.function, index=self.index + (checked_index, ),
                unbounded=self.unbounded)

        # Recursion has ended, all indices are known.
        return self.function(*self.index + (checked_index, ))
    #__getitem__

    def __getslice__(self, a, b, c=0):
        print a, b, c

    def __str__(self):
        return "{} contains no data".format(repr(self))

    def __repr__(self):
        return str(self.__class__)

    def _check_boundaries(self, index):
        """
        Check the boundaries and correct for negative indices.

        :arg index: The index of the element.
        :type index: tuple(int)

        :returns: Checked and corrected indices.
        :rtype: tuple(int)
        """
        if self.unbounded:
            return index

        checked_index = ()
        for position, value in enumerate(index):
            if not -self.shape[position] <= value < self.shape[position]:
                raise IndexError("index {} is out of bounds for axis {} with "
                    "size {}".format(value, position, self.shape[position]))
            checked_index += (value % self.shape[position], )
        return checked_index
    #_check_boundaries
#OnlineArray

def online_array(function, shape):
    """
    Make an OnlineArray instance and initialise it.

    :arg function: General function having only integer arguments.
    :type function: function(*(int))
    :arg shape: Shape of the array (not used, but receiving functions may rely
        on it).
    :type shape: tuple(int)
    """
    return OnlineArray(shape, function=function)
#online_array
