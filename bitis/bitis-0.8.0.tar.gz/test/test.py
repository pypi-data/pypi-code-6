#!/usr/bin/python
# .+
# .context    : Binary Timed Signal Processing Library
# .title      : Test Suite
# .kind	      : python source
# .author     : Fabrizio Pollastri
# .site	      : Torino - Italy
# .creation   :	26-Sep-2013
# .copyright  :	(c) 2013 Fabrizio Pollastri
# .license    : GNU General Public License (see below)
#
# This file is part of "BITIS, Binary Timed Signal Processing Library".
#
# BITIS is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# BITIS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software. If not, see <http://www.gnu.org/licenses/>.
#
# .-


import bitis as bt
import random
from sys import maxint
import unittest

import matplotlib.pyplot as pl


class TestBitis(unittest.TestCase):

    def setUp(self):
        """ Prepare testing signals """

        # test signal instance
        self.test = bt.Signal()
        self.test.test()

        # test signals: a base signal and its shifted copies.
        # Graph of base signal __|^|_|^^ """
        times = [0,2,3,4,6]
        self.base = bt.Signal(times,slevel=0,tscale=1)
        self.shift1 = bt.Signal([i + 1 for i in times],slevel=0,tscale=1)
        self.shift2 = bt.Signal([i + 2 for i in times],slevel=0,tscale=1)
        self.shift3 = bt.Signal([i + 3 for i in times],slevel=0,tscale=1)
        self.shift4 = bt.Signal([i + 4 for i in times],slevel=0,tscale=1)
        self.shift5 = bt.Signal([i + 5 for i in times],slevel=0,tscale=1)
        self.shift6 = bt.Signal([i + 6 for i in times],slevel=0,tscale=1)
        self.shift7 = bt.Signal([i + 7 for i in times],slevel=0,tscale=1)


    def test_clone(self):
        """ Test creation of an identical copy of signal. """

        # compare original test signal and output signal
        self.assertEqual(self.test,self.test.clone())


    def test_shift(self):
        """ Test signal shifting. """

        # shift forward, backward and to same place again
        testing= self.test.clone()
        testing.shift(13)
        testing.shift(-23)
        testing.shift(10)

        # test expected offsets
        self.assertEqual(self.test,testing)


    def test_reverse(self):
        """ Test signal edge reversing. """

        # reverse 
        testing = self.base.clone()
        testing.reverse()

        # compare expected signal and testing result
        expected = bt.Signal([0,2,3,4,6],slevel=1,tscale=1)
        self.assertEqual(expected,testing)


    def test_join_split(self):
        """ Make a number of split/join over a random signal.  Test
        equality of original and splitted/joined signal. """

        # make random sequence repeteable
        random.seed(1)

        # test 100 random binary codes sequences
        for s in range(100):

            # build random input data
            start = random.uniform(-100.,100.)
            end = random.uniform(start,start + 100.)
            split = random.uniform(start+0.001,end-0.001)
            period_mean = (end - start) / 100.
            width_mean = 0.2  * period_mean
            original = bt.noise(start,end,period_mean=period_mean,
                    width_mean=width_mean)

            # split and join
            signal_a, signal_b = original.split(split)
            signal_out = signal_a.join(signal_b)

            # compare original and out signals
            self.assertEqual(original,signal_out)


    def test_chop_join(self):
        """ Make a number of chop over a random signal.  Test
        equality of original and chopped/joined signal. """

        # make random sequence repeteable
        random.seed(1)

        # test 10 random binary codes sequences
        for s in range(10):

            # build random input data
            start = random.uniform(-100.,100.)
            end = random.uniform(start,start + 100.)
            period_mean = (end - start) / 100.
            width_mean = 0.02  * period_mean
            original = bt.noise(start,end,period_mean=period_mean,
                    width_mean=width_mean)
            period = 1.

            # chop and join
            chops = original.chop(period,max_chops=200)
            signal_out = chops[0]
            for chop in chops[1:]:
                signal_out.join(chop,inplace=True)

            # compare original and out signals
            self.assertEqual(original,signal_out)


    def test__intersect(self):
        """ Test intersection parameters. """

        testing = self.base._intersect(self.base)
        self.assertEqual((0,6,1,3,0,1,3,0),testing)

        testing = self.base._intersect(self.shift1)
        self.assertEqual((1,6,1,3,0,1,3,0),testing)

        testing = self.base._intersect(self.shift2)
        self.assertEqual((2,6,1,3,0,1,3,0),testing)

        testing = self.base._intersect(self.shift3)
        self.assertEqual((3,6,2,3,1,1,2,0),testing)

        testing = self.base._intersect(self.shift4)
        self.assertEqual((4,6,3,3,0,1,1,0),testing)
 
        testing = self.base._intersect(self.shift5)
        self.assertEqual((5,6,4,3,1,1,0,0),testing)

        testing = self.base._intersect(self.shift6)
        self.assertEqual(None,testing)

        testing = self.base._intersect(self.shift7)
        self.assertEqual(None,testing)


    def test_invert(self):
        """ Test logical not on test signal. """

        # from original signal to itself through a doble not
        testing = ~ ~self.base

        # compare original test signal and output signal
        self.assertEqual(self.base,testing)


    def test_and(self):
        """ Test logical and on test signal. """

        testing = self.base & self.base
        self.assertEqual(self.base,testing)

        testing = self.base & self.shift1
        expected = bt.Signal([1,5,6],slevel=0,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base & self.shift2
        expected = bt.Signal([2,4,5,6,6],slevel=0,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base & self.shift3
        expected = bt.Signal([3,5,6,6],slevel=0,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base & self.shift4
        expected = bt.Signal([4,6,6],slevel=0,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base & self.shift5
        expected = bt.Signal([5,6],slevel=0,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base & self.shift6
        expected = None
        self.assertEqual(expected,testing)

        testing = self.base & self.shift7
        expected = None
        self.assertEqual(expected,testing)


    def test_or(self):
        """ Test logical or on test signal. """

        testing = self.base | self.base
        self.assertEqual(self.base,testing)

        testing = self.base | self.shift1
        expected = bt.Signal([1,2,6],slevel=0,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base | self.shift2
        expected = bt.Signal([2,2,3,4,6],slevel=0,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base | self.shift3
        expected = bt.Signal([3,3,4,6],slevel=1,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base | self.shift4
        expected = bt.Signal([4,4,6],slevel=0,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base | self.shift5
        expected = bt.Signal([5,6],slevel=1,tscale=1)
        self.assertEqual(expected,testing)


    def test_xor(self):
        """ Test logical xor on test signal. """

        testing = self.base ^ self.base
        expected = bt.Signal([0,6],slevel=0,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base ^ self.shift1
        expected = bt.Signal([1,2,5,6],slevel=0,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base ^ self.shift2
        expected = bt.Signal([2,2,3,5,6],slevel=0,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base ^ self.shift3
        expected = bt.Signal([3,3,4,5,6],slevel=1,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base ^ self.shift4
        expected = bt.Signal([4,4,6],slevel=0,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base ^ self.shift5
        expected = bt.Signal([5,6],slevel=1,tscale=1)
        self.assertEqual(expected,testing)

        testing = self.base ^ self.shift6
        expected = None
        self.assertEqual(expected,testing)

        testing = self.base ^ self.shift7
        expected = None
        self.assertEqual(expected,testing)


    def test_logic(self):
        """ Test signal logic functions by computing the xor of two
        signals in two ways. The first, directly by xor method. The
        second using the equation a xor b = a and not b or not a and b.
        Signal times are floats. """

        # make repeatable random sequences
        random.seed(1)

        # iterate test on several random signals
        for t in range(20):

            # create random signals
            start_a = random.uniform(-100.,100.)
            end_a = random.uniform(start_a,start_a + 100.)
            start_b = (start_a + end_a) / 2.
            end_b = random.uniform(start_b,start_b + 100.)
            in_a = bt.noise(start_a,end_a,period_mean=0.1,width_mean=3)
            in_b = bt.noise(start_b,end_b,period_mean=0.3,width_mean=2)

            # direct xor
            xor1 = in_a ^ in_b

            # xor from equation
            xor2 = in_a & ~in_b | ~in_a & in_b

            # compare original test signal and output signal
            self.assertEqual(xor1,xor2)


    def test_integral(self):
        """ Test integral of signal computation. """

        self.assertEqual(30,self.test.integral(1))
        self.assertEqual(33,self.test.integral(0))
        self.assertEqual(33,(~self.test).integral(1))
        self.assertEqual(30,(~self.test).integral(0))


    def test_correlation(self):
        """ Test correlation function of two signals (*self* and *other*). """

        # create test signals
        in_a = bt.Signal([-2,-1,1,2,7,12])
        in_b = bt.Signal([-2,0,3,5,8,12])
        expected_corr =  [  1,  2,  2,  2, 2, 2, 2, 3, 4, 5, 6, 6, 6]
        expected_times = [-13,-12,-11,-10,-9,-8,-7,-6,-5,-4,-3,-2,-1]
        expected_corr +=  [9,10,9,7,3,3,3,3,2,1, 2, 1, 1, 1]
        expected_times += [0, 1,2,3,4,5,6,7,8,9,10,11,12,13]

        # do correlation
        corr, times = in_a.correlation(in_b)

        # test correlation
        self.assertEqual(expected_corr,corr)
        self.assertEqual(expected_times,times)


    def test_pwm_codec_noperiod(self):
        """ Make a number of conversion from a random code to the
        corresponding pwm signal and back again to code. Test
        equality of input and output codes. Use pulse elapse
        conversion method. """

        # make random sequence repeteable
        random.seed(1)

        # test 100 random binary codes sequences
        for s in range(100):

            # build random input data
            bit_length = random.randint(0,32)
            code = random.randint(-maxint-1,maxint)
            code_in = (bit_length,code)
            period = random.randint(10,20)
            elapse_0 = random.randint(1,2)
            elapse_1 = random.randint(1,2) + elapse_0
            active = random.randint(0,1)
            origin = random.uniform(-100.,100.)

            # clear unused code bits into code_in
            mask = 0
            for i in range(code_in[0]):
                mask <<= 1
                mask |= 1
            code_in = (code_in[0],code_in[1] & mask)

            # from codes to pulses and back again
            pwm = bt.bin2pwm(code_in,period,elapse_0,elapse_1,active,origin)
            code_out = bt.pwm2bin(pwm,elapse_0,elapse_1)

            # compare in and out codes
            self.assertEqual(code_in,code_out)


    def test_pwm_codec_period(self):
        """ Make a number of conversion from a random code to the
        corresponding pwm signal and back again to code. Test
        equality of input and output codes. Use pulse correlation
        conversion method. """

        # make random sequence repeteable
        random.seed(1)

        # test 100 random binary codes sequences
        for s in range(100):

            # build random input data
            bit_length = random.randint(0,32)
            code = random.randint(-maxint-1,maxint)
            code_in = (bit_length,code)
            period = random.randint(10,20)
            elapse_0 = random.randint(1,2)
            elapse_1 = random.randint(1,2) + elapse_0
            active = random.randint(0,1)
            origin = random.uniform(-100.,100.)

            # clear unused code bits into code_in
            mask = 0
            for i in range(code_in[0]):
                mask <<= 1
                mask |= 1
            code_in = (code_in[0],code_in[1] & mask)

            # from codes to pulses and back again
            pwm = bt.bin2pwm(code_in,period,elapse_0,elapse_1,active,origin)
            code_out, error = bt.pwm2bin(pwm,elapse_0,elapse_1,active,period=period)

            # compare in and out codes
            self.assertEqual(0,error)
            self.assertEqual(code_in,code_out)


    def test_serial_tx_rx(self):
        """ Simulate encode and decode of a list of chars over a serial line.
        Test the equality of the original char list with the received one. """

        # constants
        parity_keys = ['off','odd','even']

        # make random sequence repeteable
        random.seed(1)

        # make whole test 10 time
        for j in range(10):

            # make random serial parameters
            char_bits = random.randint(7,8)
            parity = parity_keys[random.randint(0,2)]
            stop_bits = random.randint(1,2)

            # make random chars and timings
            chars_in = []
            timings_in = []
            start = 0
            for i in range(10):
                chars_in.append(chr(random.randint(0,2**char_bits-1)))
                start += abs(int(random.gauss(0,500))) + 240
                timings_in.append(start)

            # transmit and receive
            sline = bt.serial_tx(chars_in,timings_in,char_bits=char_bits,
                    parity=parity,stop_bits=stop_bits)
            chars_out, timings_out, status = bt.serial_rx(sline,
                    char_bits=char_bits,parity=parity,stop_bits=stop_bits)

            # compare in and out chars, theirs timings and test for ok status
            self.assertEqual(zip(chars_in,timings_in),
                   zip(chars_out,timings_out))
            self.assertTrue(all([s == 0 for s in status]))


    def test_stream(self):
        """ Divide a signal in several chunks by subsequent splits. Pass them
        to a stream signal. Save stream excess into an accumulator. Compare
        at each split the original signal with the concatenation of
        accumulator, stream and most recent part of the last split. """
        
        # make random sequence repeteable
        random.seed(1)

        # create signals
        original = bt.noise(0,200)
        stream = bt.Signal()
        accumulator = bt.Signal()

        # split original several times, pass first splited part to a stream
        # signal, append stream excess to an accumulator signal.
        # At each step, check if original is equal to part b + stream + acc.
        start = original.start()
        tosplit = original
        for i in range(10):
            split = random.uniform(start,200.)
            start = split
            part_a, part_b = tosplit.split(split)
            tosplit = part_b
            excess, stream = stream.stream(part_a,30)
            accumulator.append(excess)
            self.assertEqual(original,accumulator + stream + part_b)


# main

if __name__ == '__main__':
    unittest.main()

#### END
