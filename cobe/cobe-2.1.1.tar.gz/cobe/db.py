# Copyright (C) 2014 Peter Teichman

import array
import itertools
import random

_MAX_HEIGHT = 4

_KEY = 0
_VAL = 1
_NXT = 2

_ZERO_NODE = 0
_HEAD_NODE = -_NXT

def uvarint(data, offset):
    local_ord = ord
    val = shift = 0

    n = offset
    while 1:
        b = local_ord(data[n])
        val |= (b & 0x7f) << shift
        n += 1

        if not b & 0x80:
            break

        shift += 7

    return val, n - offset


def uvarint_encode(value):
    bits = value & 0x7f
    value >>= 7

    while value:
        yield chr(0x80 | bits)
        bits = value & 0x7f
        value >>= 7

    yield chr(bits)


def len_prefixed(data):
    # yield the varint-encoded length of data, then all its bytes
    return itertools.chain(uvarint_encode(len(data)), data)


class MemDB(object):
    def __init__(self, opts):
        self.height = 1
        self.kv_data = array.array('c')
        self.node_data = array.array('i', [0] * _MAX_HEIGHT)

    def __iter__(self):
        node_data, load = self.node_data, self.load

        c = node_data[0]
        while c != _ZERO_NODE:
            key_pos, val, c = node_data[c:c + _NXT + 1]
            yield load(key_pos), val

    def size(self):
        return len(self.kv_data) + len(self.node_data)

    def add(self, key, num):
        # lock mutex
        node_data = self.node_data
        prev = [0] * _MAX_HEIGHT

        n, exact = self.find_node(key, prev)
        if exact:
            self.node_data[n+_VAL] += num
            return

        # choose the new node's height
        h = 1
        while h < _MAX_HEIGHT and random.randint(0, 3) == 0:
            h += 1

        if h > self.height:
            for i in xrange(self.height, h):
                prev[i] = _HEAD_NODE

            self.height = h

        # insert the new node
        node = [0] * (_NXT + h)
        pos = len(node_data)

        node[0] = self.save(key)
        node[1] = num

        for i in xrange(h):
            j = prev[i] + _NXT + i
            node[_NXT + i] = node_data[j]
            node_data[j] = pos

        node_data.extend(node)

    def load(self, offset):
        if offset < 0:
            return None

        kv_data = self.kv_data

        length, n = uvarint(kv_data, offset)
        i, j = offset + n, offset + n + length
        return kv_data[i:j]

    def save(self, data):
        if len(data) == 0:
            raise ValueError("can't handle empty saved data for now")

        offset = len(self.kv_data)
        self.kv_data.extend(len_prefixed(data))
        return offset

    def find_node(self, key, prev):
        # returns n int, exact bool
        node_data, load = self.node_data, self.load

        # walk the skiplist at height h until we find the zero (tail)
        # node or one whose key is >= the search key
        p = _HEAD_NODE

        key = array.array('c', key)

        for h in xrange(self.height - 1, -1, -1):
            n = node_data[p + _NXT + h]

            while 1:
                if n == _ZERO_NODE:
                    exact = False
                    break

                offset = node_data[n + _KEY]

                c = cmp(load(offset), key)
                if c >= 0:
                    exact = (c == 0)
                    break

                p, n = n, node_data[n + _NXT + h]

            if prev is not None:
                prev[h] = p

        return n, exact
