# -*- coding: utf-8 -*-
"""
colibri.serialization
~~~~~~~~~~~~~~~~~~~~~

This module contains methods to convert between AMQP types
and their C-type representations.

"""
from __future__ import absolute_import

from io import BytesIO
from time import mktime
from decimal import Decimal
from datetime import datetime
from struct import pack, unpack_from

from .utils import maybe_list


# This may be confusing, but different broker implementations
# use type lables that differ from the spec
# Read more here: https://www.rabbitmq.com/amqp-0-9-1-errata.html#section_3
#
# Types below are defined for RabbitMq/QPID, if you have some issues
# using other broker please, report an issue on github
BIT = 'b'
OCTET = 'o'
SHORT = 'B'
LONG = 'l'
LONGLONG = 'L'
SHORTSTR = 's'
LONGSTR = 'S'
TABLE = 'F'
TIMESTAMP = 'L'

TYPE_BY_NAME = {
    'bit': BIT,
    'octet': OCTET,
    'short': SHORT,
    'long': LONG,
    'longlong': LONGLONG,
    'shortstr': SHORTSTR,
    'longstr': LONGSTR,
    'table': TABLE,
    'timestamp': TIMESTAMP,
}


def _read_item(buf, offset=0, unpack_from=unpack_from):
    ftype = chr(buf[offset])
    offset += 1

    # 'S': long string
    if ftype == 'S':
        slen, = unpack_from('!I', buf, offset)
        offset += 4
        val = buf[offset:offset + slen]
        if isinstance(val, bytes):
            val = val.decode('utf-8')
        offset += slen
    # 's': short string
    elif ftype == 's':
        slen, = unpack_from('!B', buf, offset)
        offset += 1
        val = buf[offset:offset + slen]
        if isinstance(val, bytes):
            val = val.decode('utf-8')
        offset += slen
    # 'b': short-short int
    elif ftype == 'b':
        val, = unpack_from('!B', buf, offset)
        offset += 1
    # 'B': short-short unsigned int
    elif ftype == 'B':
        val, = unpack_from('!b', buf, offset)
        offset += 1
    # 'U': short int
    elif ftype == 'U':
        val, = unpack_from('!h', buf, offset)
        offset += 2
    # 'u': short unsigned int
    elif ftype == 'u':
        val, = unpack_from('!H', buf, offset)
        offset += 2
    # 'I': long int
    elif ftype == 'I':
        val, = unpack_from('!i', buf, offset)
        offset += 4
    # 'i': long unsigned int
    elif ftype == 'i':
        val, = unpack_from('!I', buf, offset)
        offset += 4
    # 'L': long long int
    elif ftype == 'L':
        val, = unpack_from('!q', buf, offset)
        offset += 8
    # 'l': long long unsigned int
    elif ftype == 'l':
        val, = unpack_from('!Q', buf, offset)
        offset += 8
    # 'f': float
    elif ftype == 'f':
        val, = unpack_from('!f', buf, offset)
        offset += 4
    # 'd': double
    elif ftype == 'd':
        val, = unpack_from('!d', buf, offset)
        offset += 8
    # 'D': decimal
    elif ftype == 'D':
        d, = unpack_from('!B', buf, offset)
        offset += 1
        n, = unpack_from('!i', buf, offset)
        offset += 4
        val = Decimal(n) / Decimal(10 ** d)
    # 'F': table
    elif ftype == 'F':
        tlen, = unpack_from('!I', buf, offset)
        offset += 4
        limit = offset + tlen
        val = {}
        while offset < limit:
            keylen, = unpack_from('!B', buf, offset)
            offset += 1
            key = buf[offset:offset + keylen]
            if isinstance(key, bytes):
                key = key.decode('utf-8')
            offset += keylen
            val[key], offset = _read_item(buf, offset)
    # 'A': array
    elif ftype == 'A':
        alen, = unpack_from('!I', buf, offset)
        offset += 4
        limit = offset + alen
        val = []
        while offset < limit:
            v, offset = _read_item(buf, offset)
            val.append(v)
    # 't' (bool)
    elif ftype == 't':
        val, = unpack_from('!B', buf, offset)
        val = bool(val)
        offset += 1
    # 'T': timestamp
    elif ftype == 'T':
        val, = unpack_from('!Q', buf, offset)
        offset += 8
        val = datetime.utcfromtimestamp(val)
    # 'V': void
    elif ftype == 'V':
        val = None
    else:
        raise ValueError(
            'Unknown value in table: {0!r} ({1!r})'.format(
                ftype, type(ftype)))
    return val, offset


def loads(fmt, buf, offset=0, ord=ord, maybe_list=maybe_list,
          unpack_from=unpack_from, _read_item=_read_item):
    """
    bit = b
    octet = o
    short = B
    long = l
    long long = L
    float = f
    shortstr = s
    longstr = S
    table = F
    array = A
    """
    bitcount = bits = 0

    values = []
    append = values.append

    if len(fmt) == 1:
        buf = maybe_list(buf)

    for p in fmt:
        if p == 'b':
            if not bitcount:
                bits = ord(buf[offset:offset + 1])
            bitcount = 8
            val = (bits & 1) == 1
            bits >>= 1
            bitcount -= 1
            offset += 1
        elif p == 'o':
            bitcount = bits = 0
            val, = unpack_from('!B', buf, offset)
            offset += 1
        elif p == 'B':
            bitcount = bits = 0
            val, = unpack_from('!H', buf, offset)
            offset += 2
        elif p == 'l':
            bitcount = bits = 0
            val, = unpack_from('!I', buf, offset)
            offset += 4
        elif p == 'L':
            bitcount = bits = 0
            val, = unpack_from('!Q', buf, offset)
            offset += 8
        elif p == 'f':
            bitcount = bits = 0
            val, = unpack_from('!d', buf, offset)
            offset += 8
        elif p == 's':
            bitcount = bits = 0
            slen, = unpack_from('B', buf, offset)
            offset += 1
            val = buf[offset:offset + slen]
            if isinstance(val, bytes):
                val = val.decode('utf-8')
            offset += slen
        elif p == 'S':
            bitcount = bits = 0
            slen, = unpack_from('!I', buf, offset)
            offset += 4
            val = buf[offset:offset + slen]
            if isinstance(val, bytes):
                val = val.decode('utf-8')
            offset += slen
        elif p == 'F':
            bitcount = bits = 0
            tlen, = unpack_from('!I', buf, offset)
            offset += 4
            limit = offset + tlen
            val = {}
            while offset < limit:
                keylen, = unpack_from('!B', buf, offset)
                offset += 1
                key = buf[offset:offset + keylen]
                if isinstance(key, bytes):
                    key = key.decode('utf-8')
                offset += keylen
                val[key], offset = _read_item(buf, offset)
        elif p == 'A':
            bitcount = bits = 0
            alen, = unpack_from('!I', buf, offset)
            offset += 4
            limit = offset + alen
            val = []
            while offset < limit:
                aval, offset = _read_item(buf, offset)
                val.append(aval)
        elif p == 'T':
            bitcount = bits = 0
            val, = unpack_from('!Q', buf, offset)
            offset += 8
            val = datetime.fromtimestamp(val)
        else:
            raise Exception('WTF WTF')
        append(val)
    return values, offset


def _flushbits(bits, write, pack=pack):
    if bits:
        write(pack('B' * len(bits), *bits))
        bits[:] = []
    return 0


def dumps(fmt, values, maybe_list=maybe_list):
    """"
    bit = b
    octet = o
    short = B
    long = l
    long long = L
    shortstr = s
    longstr = S
    table = F
    array = A
    """
    bitcount = 0
    bits = []
    out = BytesIO()
    write = out.write

    if len(fmt) == 1:
        values = maybe_list(values)

    for i, val in enumerate(values):
        p = fmt[i]
        if p == 'b':
            val = 1 if val else 0
            shift = bitcount % 8
            if shift == 0:
                bits.append(0)
            bits[-1] |= (val << shift)
            bitcount += 1
        elif p == 'o':
            bitcount = _flushbits(bits, write)
            write(pack('B', val))
        elif p == 'B':
            bitcount = _flushbits(bits, write)
            write(pack('!H', int(val)))
        elif p == 'l':
            bitcount = _flushbits(bits, write)
            write(pack('!I', val))
        elif p == 'L':
            bitcount = _flushbits(bits, write)
            write(pack('!Q', val))
        elif p == 's':
            val = val or ''
            bitcount = _flushbits(bits, write)
            write(pack('B', len(val)))
            if isinstance(val, str):
                val = val.encode('utf-8')
            write(val)
        elif p == 'S':
            val = val or ''
            bitcount = _flushbits(bits, write)
            write(pack('!I', len(val)))
            if isinstance(val, str):
                val = val.encode('utf-8')
            write(val)
        elif p == 'F':
            bitcount = _flushbits(bits, write)
            _write_table(val or {}, write, bits)
        elif p == 'A':
            bitcount = _flushbits(bits, write)
            _write_array(val or [], write, bits)
        elif p == 'T':
            write(pack('!q', int(mktime(val.timetuple()))))
    _flushbits(bits, write)

    return out.getvalue()


def _write_table(d, write, bits, pack=pack):
    out = BytesIO()
    twrite = out.write
    for k, v in d.items():
        twrite(pack('B', len(k)))
        if isinstance(k, str):
            k = k.encode('utf-8')
        twrite(k)
        try:
            _write_item(v, twrite, bits)
        except ValueError:
            raise ValueError('Table type {!r} for key {!r} not handled by '
                             'amqp.[value: {!r}]'.format(type(v), k, v))
    table_data = out.getvalue()
    write(pack('!I', len(table_data)))
    write(table_data)


def _write_array(l, write, bits, pack=pack):
    out = BytesIO()
    awrite = out.write
    for v in l:
        try:
            _write_item(v, awrite, bits)
        except ValueError:
            raise ValueError('Table type {0!r} not handled by amqp. '
                             '[value: {1!r}]'.format(type(v), v))
    array_data = out.getvalue()
    write(pack('!I', len(array_data)))
    write(array_data)


def _write_item(v, write, bits, pack=pack,
                str=str, bytes=bytes, bool=bool,
                float=float, int=int,
                Decimal=Decimal, datetime=datetime, dict=dict, list=list,
                tuple=tuple, None_t=None):
    if isinstance(v, str):
        write(pack('!cI', b'S', len(v)))
        write(v.encode('utf-8'))
    elif isinstance(v, bytes):
        write(pack('!cI', b'S', len(v)))
        write(v)
    elif isinstance(v, bool):
        write(pack('!cB', b't', int(v)))
    elif isinstance(v, float):
        write(pack('!cd', b'd', v))
    elif isinstance(v, int):
        write(pack('!ci', b'I', v))
    elif isinstance(v, Decimal):
        sign, digits, exponent = v.as_tuple()
        v = 0
        for d in digits:
            v = (v * 10) + d
        if sign:
            v = -v
        write('!cBi', b'D', -exponent, v)
    elif isinstance(v, datetime):
        # TODO use UTC
        write(pack('!cq', b'T', int(mktime(v.timetuple()))))
    elif isinstance(v, dict):
        write(b'F')
        _write_table(v, write, bits)
    elif isinstance(v, (list, tuple)):
        write(b'A')
        _write_array(v, write, bits)
    elif v is None_t:
        write(b'V')
    else:
        raise ValueError
