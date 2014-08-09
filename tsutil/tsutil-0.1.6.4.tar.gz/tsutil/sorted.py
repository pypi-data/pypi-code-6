#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Turbidsoul Chen
# @Date:   2014-07-30 10:07:05
# @Last Modified by:   Turbidsoul Chen
# @Last Modified time: 2014-08-08 14:26:08


def quick_sorted(lst, func=cmp, reversed=False):
    """
    >>> l = [2,3,1,0,6,4,7,8,5,9]
    >>> quick_sorted(l)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> quick_sorted(l, func=lambda a, b: cmp(b, a))
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    >>> quick_sorted(l, reversed=True)
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    >>> quick_sorted(l, func=lambda a, b: cmp(b, a), reversed=True)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
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


def head_sorted(lst, func=cmp, reversed=False):
    """
    >>> l = [2,3,1,0,6,4,7,8,5,9]
    >>> head_sorted(l)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> head_sorted(l, func=lambda a, b: cmp(b, a))
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    >>> head_sorted(l, reversed=True)
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    >>> head_sorted(l, func=lambda a, b: cmp(b, a), reversed=True)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
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
    return lst[::-1] if reversed else lst


def merge_sorted(lst,  func=cmp, reversed=False):
    """
    >>> l = [2,3,1,0,6,4,7,8,5,9]
    >>> merge_sorted(l)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> merge_sorted(l, func=lambda a, b: cmp(b, a))
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    >>> merge_sorted(l, reversed=True)
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    >>> merge_sorted(l, func=lambda a, b: cmp(b, a), reversed=True)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    assert isinstance(lst, list)
    if len(lst) <= 1:
        return lst

    def merge(a, b):
        mlst = []
        while a and b:
            mlst.append(a.pop(0) if func(a[0], b[0]) < 0 else b.pop(0))
        return mlst + a + b
    m = len(lst) / 2
    a = merge_sorted(lst[:m], func=func)
    b = merge_sorted(lst[m:], func=func)
    l = merge(a, b)
    return l[::-1] if reversed else l


if __name__ == '__main__':
    __import__('doctest').testmod()