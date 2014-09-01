#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.

#===============================================================================
# DOC
#===============================================================================

"""yatel.vq package tests"""


#===============================================================================
# IMPORTS
#===============================================================================

import random, unittest

from yatel.cluster import kmeans
from yatel.tests import core


#===============================================================================
# VALIDATE TESTS
#===============================================================================

class TestKmeans(core.YatelTestCase):

    @unittest.skipUnless(core.MOCK, "require mock")
    def test_kmeans(self):
        codebook, distortion = kmeans.kmeans(
            self.nw, self.nw.environments(), 2, whiten=False, coordc=None
        )
        self.assertEquals(codebook, None)
        self.assertEquals(distortion, None)
        codebook, distortion = kmeans.kmeans(
            self.nw, self.nw.environments(), 1, whiten=True,
            coordc=lambda nw, env: [0,0]
        )
        self.assertEquals(codebook, None)
        self.assertEquals(distortion, None)

    def test_hap_in_env_coords(self):
        haps_id = [hap.hap_id for hap in self.nw.haplotypes()]
        haps_id.sort()
        for env in self.nw.environments():
            true_indexes = []
            for hap in self.nw.haplotypes_by_environment(env):
                idx = haps_id.index(hap.hap_id)
                true_indexes.append(idx)
            coords = kmeans.hap_in_env_coords(self.nw, env)
            for cidx, coord in enumerate(coords):
                if coord:
                    self.assertIn(cidx, true_indexes)
                else:
                    self.assertNotIn(cidx, true_indexes)

    def test_nw2obs(self):
        haps_id = [hap.hap_id for hap in self.nw.haplotypes()]
        haps_id.sort()
        envs = list(self.nw.environments())
        coords_iterator = enumerate(
            kmeans.nw2obs(self.nw, envs, whiten=False, coordc=None)
        )
        for idx, coords0 in coords_iterator:
            coords1 = kmeans.hap_in_env_coords(self.nw, envs[idx])
            self.assertTrue((coords0==coords1).all())


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
