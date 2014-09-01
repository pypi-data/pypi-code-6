#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#==============================================================================
# DOCS
#==============================================================================

"""hamming distance implementation of yatel.

http://en.wikipedia.org/wiki/Hamming_distance


"""

#==============================================================================
# IMPORTS
#==============================================================================

from yatel.weight import core


#==============================================================================
# HAMMING
#==============================================================================

class Hamming(core.BaseWeight):
    """Calculate the hamming distance
    (http://en.wikipedia.org/wiki/Hamming_distance) between two haplotypes, by
    counting the number of diferences in attributes.

    The distances is incremented by "1" by two reasons:
        #. haplotype0.attr_a != haplotype1.attr_a
        #. attr_a exist in haplotype0 but not exist in haplotype1.


    Examples
    --------

    >>> from yatel import dom, weigth
    >>> h0 = dom.Haplotype("0", attr_a="a", attr_b="b", attr_c=0)
    >>> h1 = dom.Haplotype("1", attr_a="a", attr_c="0")
    >>> hamming = weight.Hamming()
    >>> dict(hamming(h0, h1))
    {(<haplotype0>, <haplotype1>): 2.0}

    """

    @classmethod
    def names(cls):
        return "hamming", "ham"

    def weight(self, hap0, hap1):
        """A ``float`` distance between 2 `dom.Haplotype` instances"""
        w = 0
        for name in set(hap0.keys() + hap1.keys()):
            if name not in hap0.keys() \
               or name not in hap1.keys() \
               or hap0.get(name) != hap1.get(name):
                w += 1
        return w

#==============================================================================
# MAIN
#==============================================================================

if __name__ == "__main__":
    print(__doc__)
