# -*- coding: ascii -*-
#
#  FortunaGenerator.py : Fortuna's internal PRNG
#
# Written in 2008 by Dwayne C. Litzenberger <dlitz@dlitz.net>
#
# ===================================================================
# The contents of this file are dedicated to the public domain.  To
# the extent that dedication to the public domain is not available,
# everyone is granted a worldwide, perpetual, royalty-free,
# non-exclusive license to exercise all rights associated with the
# contents of this file for any purpose whatsoever.
# No rights are reserved.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ===================================================================

from Crypto.Util.py3compat import *

import struct

from Crypto.Util.number import ceil_shift, exact_log2, exact_div
from Crypto.Util import Counter
from Crypto.Cipher import AES

import SHAd256

class AESGenerator(object):
    """The Fortuna "generator"

    This is used internally by the Fortuna PRNG to generate arbitrary amounts
    of pseudorandom data from a smaller amount of seed data.

    The output is generated by running AES-256 in counter mode and re-keying
    after every mebibyte (2**16 blocks) of output.
    """

    block_size = AES.block_size     # output block size in octets (128 bits)
    key_size = 32                   # key size in octets (256 bits)

    # Because of the birthday paradox, we expect to find approximately one
    # collision for every 2**64 blocks of output from a real random source.
    # However, this code generates pseudorandom data by running AES in
    # counter mode, so there will be no collisions until the counter
    # (theoretically) wraps around at 2**128 blocks.  Thus, in order to prevent
    # Fortuna's pseudorandom output from deviating perceptibly from a true
    # random source, Ferguson and Schneier specify a limit of 2**16 blocks
    # without rekeying.
    max_blocks_per_request = 2**16  # Allow no more than this number of blocks per _pseudo_random_data request

    _four_kiblocks_of_zeros = b("\0") * block_size * 4096

    def __init__(self):
        self.counter = Counter.new(nbits=self.block_size*8, initial_value=0, little_endian=True)
        self.key = None

        # Set some helper constants
        self.block_size_shift = exact_log2(self.block_size)
        assert (1 << self.block_size_shift) == self.block_size

        self.blocks_per_key = exact_div(self.key_size, self.block_size)
        assert self.key_size == self.blocks_per_key * self.block_size

        self.max_bytes_per_request = self.max_blocks_per_request * self.block_size

    def reseed(self, seed):
        if self.key is None:
            self.key = b("\0") * self.key_size

        self._set_key(SHAd256.new(self.key + seed).digest())
        self.counter()  # increment counter
        assert len(self.key) == self.key_size

    def pseudo_random_data(self, bytes):
        assert bytes >= 0

        num_full_blocks = bytes >> 20
        remainder = bytes & ((1<<20)-1)

        retval = []
        for i in xrange(num_full_blocks):
            retval.append(self._pseudo_random_data(1<<20))
        retval.append(self._pseudo_random_data(remainder))

        return b("").join(retval)

    def _set_key(self, key):
        self.key = key
        self._cipher = AES.new(key, AES.MODE_CTR, counter=self.counter)

    def _pseudo_random_data(self, bytes):
        if not (0 <= bytes <= self.max_bytes_per_request):
            raise AssertionError("You cannot ask for more than 1 MiB of data per request")

        num_blocks = ceil_shift(bytes, self.block_size_shift)   # num_blocks = ceil(bytes / self.block_size)

        # Compute the output
        retval = self._generate_blocks(num_blocks)[:bytes]

        # Switch to a new key to avoid later compromises of this output (i.e.
        # state compromise extension attacks)
        self._set_key(self._generate_blocks(self.blocks_per_key))

        assert len(retval) == bytes
        assert len(self.key) == self.key_size

        return retval

    def _generate_blocks(self, num_blocks):
        if self.key is None:
            raise AssertionError("generator must be seeded before use")
        assert 0 <= num_blocks <= self.max_blocks_per_request
        retval = []
        for i in xrange(num_blocks >> 12):      # xrange(num_blocks / 4096)
            retval.append(self._cipher.encrypt(self._four_kiblocks_of_zeros))
        remaining_bytes = (num_blocks & 4095) << self.block_size_shift  # (num_blocks % 4095) * self.block_size
        retval.append(self._cipher.encrypt(self._four_kiblocks_of_zeros[:remaining_bytes]))
        return b("").join(retval)

# vim:set ts=4 sw=4 sts=4 expandtab:
