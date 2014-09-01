#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#==============================================================================
# DOC
#==============================================================================

"""yatel.weights package tests"""


#==============================================================================
# IMPORTS
#==============================================================================

import itertools

from yatel import weight
from yatel.tests.core import YatelTestCase


#==============================================================================
# VALIDATE TESTS
#==============================================================================

class TestWeights(YatelTestCase):

    def test_weight(self):
        generator = itertools.combinations(self.nw.haplotypes(), 2)
        for syns in weight.SYNONYMS:
            for hap0, hap1 in generator:
                wgths = []
                for calc in syns:
                    wgths.append(weight.weight(calc, hap0, hap1))
                self.assertAllTheSame(wgths)

    def test_weights(self):
        for syns in weight.SYNONYMS:
            wgths = {}
            for calc in syns:
                for to_same in [True, False]:
                    generator = weight.weights(calc, self.nw, to_same)
                    for key, w in generator:
                        wgths.setdefault(key,[]).append(w)
                    for env in self.nw.environments():
                        generator = weight.weights(calc, self.nw, to_same, env)
                        for key, w in generator:
                            wgths.setdefault(key,[]).append(w)
            for v in wgths.values():
                self.assertAllTheSame(v)



#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
