#!/usr/bin/env python
 
#  Copyright (c) 2006, The Regents of the University of California, through 
#  Lawrence Berkeley National Laboratory (subject to receipt of any required
#  approvals from the U.S. Dept. of Energy).  All rights reserved.

#  This software is distributed under the new BSD Open Source License.
#  <http://www.opensource.org/licenses/bsd-license.html>
#
#  Redistribution and use in source and binary forms, with or without 
#  modification, are permitted provided that the following conditions are met: 
#
#  (1) Redistributions of source code must retain the above copyright notice, 
#  this list of conditions and the following disclaimer. 
#
#  (2) Redistributions in binary form must reproduce the above copyright 
#  notice, this list of conditions and the following disclaimer in the 
#  documentation and or other materials provided with the distribution. 
#
#  (3) Neither the name of the University of California, Lawrence Berkeley 
#  National Laboratory, U.S. Dept. of Energy nor the names of its contributors 
#  may be used to endorse or promote products derived from this software 
#  without specific prior written permission. 
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
#  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
#  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE 
#  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE 
#  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR 
#  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
#  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS 
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN 
#  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
#  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE 
#  POSSIBILITY OF SUCH DAMAGE. 
from __future__ import division

import unittest
from math import log,  sqrt, pi

from test_corebio import *
from corebio.moremath import *


class test_misc_math(unittest.TestCase):

    def test_argmax(self):
        self.assertEqual(argmax((0, 1, 2, 3)), 3)
        self.assertEqual(argmax((0, 1, 2, -1)), 2)
        self.assertEqual(argmax((3, 2, 3, 3)), 3)

    def test_argmin(self):
        self.assertEqual(argmin((1, 2, 3, 4)), 0)
        self.assertEqual(argmin((1, 2, 3, -1)), 3)
        self.assertEqual(argmin((3, 5, 3, 3)), 0)


class test_specfunc(unittest.TestCase):


    def test_cgammma(self):
        self.assertAlmostEqual(cgamma(1.).real, 1.0)
        self.assertAlmostEqual(cgamma(0.5).real, sqrt(pi) )
        self.assertAlmostEqual(cgamma(3j).real, 0.0112987)
        self.assertAlmostEqual(cgamma(3j).imag, -0.00643092)

    def test_gammma(self):
        self.assertAlmostEqual(gamma(1.), 1.0)
        self.assertAlmostEqual(gamma(0.5), sqrt(pi) )
        # Test values from GSL
        self.assertAlmostEqual(gamma(1.0 + 1.0/4096.0), 0.9998591371459403421)
        self.assertAlmostEqual(gamma(1.0 + 1.0/4096.0), 0.9998591371459403421)
        self.assertAlmostEqual(gamma(1.0 + 1.0/32.0), 0.9829010992836269148)
        self.assertAlmostEqual(gamma(2.0 + 1.0/256.0), 1.0016577903733583299)
        self.assertAlmostEqual(gamma(9.0), 40320.0)
        self.assertAlmostEqual(gamma(10.0), 362880.0)
        self.assertAlmostEqual(gamma(100.0) / 9.332621544394415268e+155, 1.0)
        self.assertAlmostEqual(gamma(170.0) / 4.269068009004705275e+304, 1.0)
        self.assertAlmostEqual(gamma(171.0) / 7.257415615307998967e+306, 1.0)
        self.assertAlmostEqual(gamma(-10.5), -2.640121820547716316e-07)
        self.assertAlmostEqual(gamma(-11.25), 6.027393816261931672e-08)
        self.assertAlmostEqual(gamma(-1.0 + 1.0 / 65536.0) / -65536.422805878,
                               1.0)

    def test_lngamma(self):
        # Test values from GSL
        self.assertAlmostEqual(lngamma(100.0), 359.1342053695753)
        self.assertAlmostEqual(lngamma(1.0e-08), 18.420680738180208905)
        self.assertAlmostEqual(lngamma(0.1), 2.252712651734205)
        self.assertAlmostEqual(lngamma(1.0 + 1.0 / 256.0), -0.0022422226599611)
        self.assertAlmostEqual(lngamma(2.0 + 1.0 / 256.0), 0.001656417755696)
        self.assertAlmostEqual(lngamma(-1.0-1.0 / 65536.0), 11.09034843809004)
        self.assertAlmostEqual(lngamma(-1.0-1.0 / 268435456.0), 19.4081210541)

    def test_clngamma(self):
        self.assertAlmostEqual(clngamma(0.5+ 2.5j).real, -3.00805, 5)
        self.assertAlmostEqual(clngamma(0.5+ 2.5j).imag, -0.192442, 6)

    def test_factorial(self):
        self.assertEqual(factorial(3), 6)
        for n in range(1, 30):
            fac1 = factorial(n)
            fac2 = factorial(n+1)
            self.assertAlmostEqual(fac2 / fac1, n+1)

    def test_digammma(self):
        self.assertAlmostEqual(digamma(1.), -euler_gamma)
        self.assertAlmostEqual(digamma(0.5), -euler_gamma - 2* log(2))
        # Test values from GSL
        self.assertAlmostEqual(digamma(2), 0.42278433509846713939)
        self.assertAlmostEqual(digamma(3), 0.92278433509846713939)
        self.assertAlmostEqual(digamma(4), 1.2561176684318004727)
        self.assertAlmostEqual(digamma(5), 1.5061176684318004727)
        self.assertAlmostEqual(digamma(100), 4.600161852738087400)
        self.assertAlmostEqual(digamma(110), 4.695928024251535633)
        self.assertAlmostEqual(digamma(5000), 8.517093188082904107)
        self.assertAlmostEqual(digamma(-10.5), 2.3982391295357816134)

    def test_trigamma(self):
        self.assertAlmostEqual(trigamma(10.0),
                            -(9778141./6350400) +pi*pi/6.)
        self.assertAlmostEqual(trigamma(2.0), pi*pi/6. -1.)
        self.assertAlmostEqual(trigamma(1.0), pi*pi/6.)
        self.assertAlmostEqual(trigamma(0.5), pi*pi/2.)
        self.assertAlmostEqual(trigamma(100.), 0.0100502)
        self.assertAlmostEqual(trigamma(1000.), 0.0010005)

    def test_cdigamma(self):
        self.assertAlmostEqual(cdigamma(0.5+ 2.5j).real, 0.909417, 5)
        self.assertAlmostEqual(cdigamma(0.5+ 2.5j).imag, 1.5708, 5)

    def test_ctrigamma(self):
        self.assertAlmostEqual(ctrigamma(0.5+ 2.5j).real, 2.97473E-6, 5)
        self.assertAlmostEqual(ctrigamma(0.5+ 2.5j).imag, -0.405685, 5)



    def test_incomplete_gamma(self):
        self.assertAlmostEqual(incomplete_gamma(10.0,0.), gamma(10.))
        # Various test values taken from GSL
        self.assertAlmostEqual(incomplete_gamma(  0.001,   0.001), 6.3087159394864007261)
        self.assertAlmostEqual(incomplete_gamma(  1.0,     0.001), 0.99900049983337499167, 2)
        self.assertAlmostEqual(incomplete_gamma( 10.0,     0.001), 362880.0)
        self.assertAlmostEqual(incomplete_gamma(  0.001,   1.0),0.21948181320730279613,5)
        self.assertAlmostEqual(incomplete_gamma( 10.0,     1.0)/ 362879.95956592242045, 1.0, 6)
        self.assertAlmostEqual(incomplete_gamma(100.0,     1.0)/ 9.3326215443944152682e+155 , 1.0)
        self.assertAlmostEqual(incomplete_gamma(  0.001, 100.0), 3.7006367674063550631e-46)
        self.assertAlmostEqual(incomplete_gamma(  1.0,   100.0), 3.7200759760208359630e-44)
        self.assertAlmostEqual(incomplete_gamma( 10.0,   100.0), 4.0836606309106112723e-26)
        # Check limiting values
        self.assertAlmostEqual(normalized_incomplete_gamma( 10.,   0.0) , 1.0)
        self.assertAlmostEqual(normalized_incomplete_gamma( 10.,   10000.0) , 0.0)

    def test_entropy(self):
        ent = entropy((1., 1.))
        self.assertAlmostEqual(ent, log(2))

    def test_entropy_with_flat_distribution(self):
        for n in range(1, 100):
            pvec = [1./n for i in range(0, n)]
            ent = entropy(pvec)
            self.assertAlmostEqual(ent, log(n))

    def test_entropy_unnormalized(self):
        for n in range(1, 100):
            pvec = [1. for i in range(0, n)]
            ent = entropy(pvec)
            self.assertAlmostEqual(ent, log(n))

    def test_entropy_with_integer(self):
        ent = entropy((1, 1, 1, 0))
        self.assertAlmostEqual(ent, log(3))

    def test_entropy_with_short_pvec(self):
        ent = entropy((1,))
        self.assertEqual(ent, 0)
        ent = entropy((1, 0, 0, 0, 0))
        self.assertEqual(ent, 0)

    def test_entropy_invalid_pvec(self):
        self.assertRaises(ValueError, entropy, ())
        self.assertRaises(ValueError, entropy, (1, -1))

    def test_entropy_base(self):
        ent = entropy((2, 2, 2, 2, 0), 2)
        self.assertAlmostEqual(ent,  2)


if __name__ == '__main__':
    unittest.main()
