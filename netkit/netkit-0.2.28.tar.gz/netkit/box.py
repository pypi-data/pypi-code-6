# -*- coding: utf-8 -*-
"""
HEADER_ATTRS 可以自定义，但是必须满足 packet_len 或 body_len 其中之一存在
"""

import struct
from collections import OrderedDict
from .log import logger

# 如果header字段变化，那么格式也会变化
HEADER_ATTRS = OrderedDict([
    ('magic', ('I', 2037952207)),
    ('version', ('I', 0)),
    ('packet_len', ('I', 0)),
    ('cmd', ('i', 0)),
    ('ret', ('i', 0)),
])


class Box(object):
    """
    类
    """

    # 如果header字段变化，那么格式也会变化
    header_attrs = None

    # 如果调用unpack成功的话，会置为True
    unpack_done = None

    # body
    body = ''

    def __init__(self, buf=None, header_attrs=None):
        self.header_attrs = header_attrs or HEADER_ATTRS
        self.unpack_done = False

        # 先做初始化
        for k, v in self.header_attrs.items():
            setattr(self, k, v[1])

        # 为了简写代码
        if buf:
            self.unpack(buf)

    @property
    def header_format(self):
        return '!' + ''.join(value[0] for value in self.header_attrs.values())

    @property
    def header_len(self):
        return struct.calcsize(self.header_format)

    @property
    def body_len(self):
        return len(self.body)

    @body_len.setter
    def body_len(self, value):
        # 什么也不要做
        pass

    @property
    def packet_len(self):
        return self.header_len + self.body_len

    @packet_len.setter
    def packet_len(self, value):
        # 什么也不需要做，因为不能让别人来赋值
        pass

    def pack(self):
        """
        打包
        """
        values = [getattr(self, k) for k in self.header_attrs]

        header = struct.pack(self.header_format, *values)

        return header + self.body

    def unpack(self, buf):
        """
        从buf里面生成，返回格式为 ret

        >0: 成功生成obj，返回了使用的长度，即剩余的部分buf要存起来
        <0: 报错
        0: 继续收
        """

        if len(buf) < self.header_len:
            logger.error('buf.len(%s) should > header_len(%s)' % (len(buf), self.header_len))
            # raise ValueError('buf.len(%s) should > header_len(%s)' % (len(buf), HEADER_LEN))
            return 0

        try:
            values = struct.unpack(self.header_format, buf[:self.header_len])
        except Exception, e:
            logger.error('unpack fail.', exc_info=True)
            return -1

        dict_values = dict([(key, values[i]) for i, key in enumerate(self.header_attrs.keys())])

        if hasattr(self, 'magic'):
            magic = dict_values.get('magic')
            if magic != self.magic:
                logger.error('magic not equal. %s != %s' % (magic, self.magic))
                # raise ValueError('magic not equal. %s != %s' % (magic, HEADER_MAGIC))
                return -2

        if 'packet_len' in dict_values:
            packet_len = dict_values.get('packet_len')
        elif 'body_len' in dict_values:
            packet_len = dict_values.get('body_len') + self.header_len
        else:
            logger.error('there is no packet_len or body_len in header')
            return -3

        if len(buf) < packet_len:
            # 还要继续收
            return 0

        for k, v in dict_values.items():
            setattr(self, k, v)

        self.body = buf[self.header_len:packet_len]

        self.unpack_done = True

        return self.packet_len

    def __repr__(self):
        values = [(k, getattr(self, k)) for k in self.header_attrs]

        values.append(('body', self.body))

        return repr(values)

    __str__ = __repr__
