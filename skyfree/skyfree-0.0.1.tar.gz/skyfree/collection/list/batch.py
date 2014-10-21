#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright @ 2014 OPS, Qunar Inc. (qunar.com)
#
# Author: tingfang.bao <tingfang.bao@qunar.com>
# DateTime: 14-7-22 下午4:40


# noinspection PyShadowingNames
def make_batch_array(values, batch_len):
    """
    批量分组：
    例如values=[1,4,6,7,8,9,10].batch_len=2
    返回[[1,4],[6,7],[8,9],[10]]
    :param values:
    :param batch_len:
    :return:
    """
    values_len = len(values)
    row = values_len / batch_len + 1
    batch_values = [([]) for i in range(row)]

    i = 0
    index = 0
    for value in values:
        batch_values[index].append(value)
        i += 1
        if i == batch_len:
            index += 1
            i = 0
    return batch_values


if __name__ == '__main__':
    values = [1, 4, 6, 7, 8, 9, 10]
    ret = make_batch_array(values, 3)
    print ret