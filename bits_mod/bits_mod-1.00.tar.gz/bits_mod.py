
'''Provides an array of bits'''

import array


def my_range(number):
    '''range iterator with consistent semantics over Python 2.x and 3.x'''
    current_value = 0
    while current_value < number:
        yield current_value
        current_value += 1


def long_size():
    '''Calculate the size of one long'''
    array_ = array.array('L', [0])
    num_bytes = array_.itemsize
    num_bits = num_bytes * 8
    return num_bits


class Bits(object):
    '''"array of bits" using a python array of integers'''

    bits_per_word = long_size() - 1
    effs = 2 ** bits_per_word - 1

    def __init__(self, num_bits, ones=False):
        self.num_bits = num_bits
        self.num_words = (self.num_bits + Bits.bits_per_word - 1) // Bits.bits_per_word
        if ones:
            self.array_ = array.array('L', [Bits.effs]) * self.num_words
        else:
            self.array_ = array.array('L', [0]) * self.num_words

    def is_true(self, bitno):
        '''Return true iff bit number bitno is marked'''
        wordno, bit_within_wordno = divmod(bitno, Bits.bits_per_word)
        mask = 1 << bit_within_wordno
        return bool(self.array_[wordno] & mask)

    def mark(self, bitno):
        '''set bit number bitno to true'''
        wordno, bit_within_wordno = divmod(bitno, Bits.bits_per_word)
        mask = 1 << bit_within_wordno
        self.array_[wordno] |= mask

    def clear(self, bitno):
        '''clear bit number bitno - mark it false'''
        wordno, bit_within_wordno = divmod(bitno, Bits.bits_per_word)
        mask = Bits.effs - (2 ** bit_within_wordno)
        self.array_[wordno] &= mask

    # It'd be nice to do __iand__ and __ior__ in a base class, but that'd be Much slower

    def __iand__(self, other):
        assert self.num_bits == other.num_bits

        for wordno in my_range(self.num_words):
            self.array_[wordno] &= other.array_[wordno]

        return self

    def __ior__(self, other):
        assert self.num_bits == other.num_bits

        for wordno in my_range(self.num_words):
            self.array_[wordno] |= other.array_[wordno]

        return self

    def count(self):
        '''Return a count of the set bits'''
        total = 0
        for i in my_range(self.num_bits):
            total += self.is_true(i)
        return total

    def __str__(self):
        list_ = []
        for i in my_range(self.num_bits):
            if self.is_true(i):
                list_.append('1')
            else:
                list_.append('0')
        return ''.join(list_)
