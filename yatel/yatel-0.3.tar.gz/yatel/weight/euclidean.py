#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#==============================================================================
# DOCS
#==============================================================================

"""Euclidean distance implementation of Yatel.

- http://en.wikipedia.org/wiki/Euclidean_distance


"""

#==============================================================================
# IMPORTS
#==============================================================================

import numpy as np

from yatel.weight import core


#==============================================================================
# EUCLIDEAN
#==============================================================================

class Euclidean(core.BaseWeight):
    """Calculates "ordinary" distance/weight between two haplotypes given by 
    the Pythagorean formula.

    Every attribute value is converted to a number by a ``to_num`` function.
    The default behavior of ``to_num`` is a sumatory of base64 ord value of
    every attribute value. Example:

    .. code-block:: python

        def to_num(attr):
            value = 0
            for c in str(attr).encode("base64"):
                value += ord(c)
            return value

        to_num("h") # 294

    For more info about euclidean distance:
    http://en.wikipedia.org/wiki/Euclidean_distance

    """

    @classmethod
    def names(cls):
        """Synonims names to call this weight calculation.
        
        """
        return "euclidean", "euc", "ordinary"

    def __init__(self, to_num=None):
        """Creates a new instance.

        Parameters
        ----------
        to_num : callable
            Convert to a number an haplotype attribute value. The default 
            behavior of ``to_num`` is a sumatory of base64 ord value of every 
            attribute value.

        .. code-block:: python

            def to_num(attr):
                value = 0
                for c in str(attr).encode("base64"):
                    value += ord(c)
                return value

            to_num("h") # 294

        """
        self.to_num = to_num_default if to_num is None else to_num

    def weight(self, hap0, hap1):
        """A ``float`` distance between 2 :py:class:`yatel.dom.Haplotype` 
        instances"""
        s = 0.0
        for name in set(hap0.keys() + hap1.keys()):
            v0 = self.to_num(hap0.get(name, ""))
            v1 = self.to_num(hap1.get(name, ""))
            s += (v1 - v0) ** 2
        return np.sqrt(s)


#==============================================================================
# FUNCTION
#==============================================================================

def to_num_default(attr):
    """The default behavior of ``to_num`` is a sumatory of base64 ord value 
    of every attribute value.
    
    """
    value = 0
    for c in str(attr).encode("base64"):
        value += ord(c)
    return value


#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
