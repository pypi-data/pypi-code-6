import random as _random
import math
import array

__all__ = ["WELL1024a","seed","random","uniform","randint","choice","sample",
           "randrange","shuffle","normalvariate","lognormvariate",
           "expovariate","vonmisesvariate","gammavariate","triangular",
           "gauss","betavariate","paretovariate","weibullvariate",
           "getstate","setstate", "getrandbits"]

SCALE = 1.0 / ((1 << 32)-1)
INT_MASK = (1 << 32) - 1
LOG2 = math.log(2)


class WELL1024a(_random.Random):
    _state = None
    _n = None
    next_bit = 0
    available_bits = 0
    bit_state = None
    VERSION = 1
    
    def seed(self, a=None):
        state = self.genstate(a)
        self.setstate([self.VERSION, state, 0, None, None, 0,0])
        self.next_bit = 0
        self.available_bits = 0
    
    def genstate(self, x=None):
        if x is not None:
            _random.seed(x)
        res = array.array('I', [_random.randrange(1<<32) for _ in range(32)])
        return res

    def getstate(self):
        return self.VERSION, self._state, self._n, self.gauss_next, \
        self.bit_state, self.next_bit, self.available_bits

    def setstate(self, state):
        version, _state, _n, gauss_next, bit_state, next_bit, av_bits = state
        if len(_state) != 32:
            raise ValueError('State vector is not 32 entries long!')
        self._n = _n
        self._state = _state
        self.gauss_next = gauss_next
        self.bit_state = bit_state
        self.next_bit = next_bit
        self.available_bits = av_bits
    
    def _rand(self):
        _state = self._state
        _n = self._n
        z0 = _state[(_n+31)&31]
        v_m1 = _state[(_n+3)&31]
        v_m2 = _state[(_n+24)&31]
        v_m3 = _state[(_n+10)&31]
        z1 = z0 ^ (v_m1 ^ (v_m1 >> 8));
        z2 = v_m2 ^ (v_m2 << 19) ^ v_m3 ^ (v_m3 << 14)
        _state[_n] = (z1 ^ z2)  & INT_MASK
        self._n = _n = (_n + 31) & 31
        _state[_n] = (z0 ^ (z0 << 11) ^ z1 ^ (z1 << 7) 
                     ^ z2 ^ (z2 << 13)) & INT_MASK
        return _state[_n] & INT_MASK
    
    def random(self):
        return self._rand() * SCALE
    
    def getrandbits(self, bits):
        mask = (1 << bits) - 1
        unshift = 0
        if self.next_bit + bits <= self.available_bits:
            unshift = self.next_bit
            self.next_bit += bits
        else:
            result = self._rand(True)
            nb = int(bits/32)
            for _ in range(nb):
                result = (result << 32) | self._rand(True)
            self.bit_state = result
            self.next_bit = bits
            self.available_bits = (1 + nb)*32 - bits
        return (self.bit_state >> unshift) & mask



## -------------------- test program --------------------
import time
from math import sqrt as _sqrt
    
def _test_generator(n, func, args):
    print n, 'times', func.__name__
    total = 0.0
    sqsum = 0.0
    smallest = 1e10
    largest = -1e10
    t0 = time.time()
    for i in range(n):
        x = func(*args)
        total += x
        sqsum = sqsum + x*x
        smallest = min(x, smallest)
        largest = max(x, largest)
    t1 = time.time()
    print round(t1-t0, 3), 'sec,',
    avg = total/n
    stddev = _sqrt(sqsum/n - avg*avg)
    print 'avg %g, stddev %g, min %g, max %g' % \
              (avg, stddev, smallest, largest)


def _test(N=2000):
    _test_generator(N, random, ())
    _test_generator(N, normalvariate, (0.0, 1.0))
    _test_generator(N, lognormvariate, (0.0, 1.0))
    _test_generator(N, vonmisesvariate, (0.0, 1.0))
    _test_generator(N, gammavariate, (0.01, 1.0))
    _test_generator(N, gammavariate, (0.1, 1.0))
    _test_generator(N, gammavariate, (0.1, 2.0))
    _test_generator(N, gammavariate, (0.5, 1.0))
    _test_generator(N, gammavariate, (0.9, 1.0))
    _test_generator(N, gammavariate, (1.0, 1.0))
    _test_generator(N, gammavariate, (2.0, 1.0))
    _test_generator(N, gammavariate, (20.0, 1.0))
    _test_generator(N, gammavariate, (200.0, 1.0))
    _test_generator(N, gauss, (0.0, 1.0))
    _test_generator(N, betavariate, (3.0, 3.0))
    _test_generator(N, triangular, (0.0, 1.0, 1.0/3.0))

_inst = WELL1024a()
seed = _inst.seed
random = _inst.random
uniform = _inst.uniform
triangular = _inst.triangular
randint = _inst.randint
choice = _inst.choice
randrange = _inst.randrange
sample = _inst.sample
shuffle = _inst.shuffle
normalvariate = _inst.normalvariate
lognormvariate = _inst.lognormvariate
expovariate = _inst.expovariate
vonmisesvariate = _inst.vonmisesvariate
gammavariate = _inst.gammavariate
gauss = _inst.gauss
betavariate = _inst.betavariate
paretovariate = _inst.paretovariate
weibullvariate = _inst.weibullvariate
getstate = _inst.getstate
setstate = _inst.setstate
getrandbits = _inst.getrandbits


if __name__ == '__main__':
    _test()
