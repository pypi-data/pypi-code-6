#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Turbidsoul Chen
# @Date:   2014-07-30 10:07:05
# @Last Modified by:   Turbidsoul Chen
# @Last Modified time: 2014-08-07 17:51:57



def quick_sorted(lst, func=lambda a, b: cmp(a, b), reversed=False):
    if len(lst) <= 1:
        return lst
    pivot = lst[0]
    before = []
    after = []
    for s in lst[1:]:
        res = func(s, pivot)
        if res > 0:
            after.append(s)
        else:
            before.append(s)
    before = quick_sorted(before, func=func)
    after = quick_sorted(after, func=func)
    if reversed:
        return (before + [pivot] + after)[::-1]
    else:
        return before + [pivot] + after


def head_sort(lst, func=lambda a, b: cmp(a, b), reversed=False):
    def make_maxhead(lst, start, end):
        root = start
        while 1:
            left = root * 2 + 1
            right = root * 2 + 2
            if left > end:
                break
            child = left
            if right <= end and func(lst[left], lst[right]) < 0:
                child = right
            if func(lst[root], lst[child]) < 0:
                lst[root], lst[child] = lst[child],lst[root]
                root = child
            else:
                break
    n = len(lst)
    for i in range(n, -1, -1):
        make_maxhead(lst, i, n-1)
    for end in range(n-1, -1, -1):
        lst[0], lst[end] = lst[end], lst[0]
        make_maxhead(lst, 0, end-1)
    return lst if reversed else lst[::-1]
