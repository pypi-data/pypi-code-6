# -*- coding: utf-8 -*-
"""
    tlutil.helpers
"""


__all__ = [
    "ip2long", "long2ip", "get_start_end",
    "filter_fields"
]


def ip2long(s):
    """IP地址转换为整数
    :param s: IP地址
    """
    ipBytes = map(int, s.split('.'))
    if len(ipBytes) != 4:
        return 0
    ret = 0
    for i in xrange(4):
        ret |= ipBytes[i] << ((3 - i) * 8)
    return ret


def long2ip(inp):
    """整数转换为IP地址
    :param inp: 整数
    """
    ipBytes = []
    for i in xrange(4):
        one = (inp >> ((3 - i) * 8)) & 0xFF
        ipBytes.append(one)
    return '.'.join(map(str, ipBytes))


def get_start_end(offset, limit, is_redis=True):
    """获取数据开始和结束的位置
    :param offset: 开始位置
    :param limit: 数据条数
    :param is_redis: 是否为redis
    """
    offset, limit = int(offset), int(limit)
    if offset == 0 and limit == -1:
        start = 0
        end = None if not is_redis else -1
        return start, end
    start = offset
    end = start + limit
    if is_redis and end > 0:
        end -= 1
    return start, end


def filter_fields(args, filter_fields, exists=False):
    """过滤字段
    :param args: 被过滤的可迭代的类dict类型
    :param filter_fields: 过滤的字段列表
    :param exits: args的value必须存在
    """
    if not exists:
        return dict((k, v) for k, v in args.iteritems() if k in filter_fields)
    return dict((k, v) for k, v in args.iteritems() if k in filter_fields and v)
