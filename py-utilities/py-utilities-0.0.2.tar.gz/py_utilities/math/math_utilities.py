#!/usr/bin/env python
# -*- coding: utf-8 -*-


def gcd(a, b):
    """
    Returns the greatest common divisor using Euclid's algo

    >>> gcd(12, 24)
    12

    >>> gcd(48, 4)
    4

    >>> gcd(2, 4)
    2

    >>> gcd(36, 48)
    12
    """
    while b:
        a, b = b, a % b
    return a


def gcd_seq(seq):
    """
    Returns the greatest common divisor of seq

    >>> gcd_seq([12, 24, 48])
    12
    """
    return reduce(gcd, seq)


def lcm(a, b):
    """
    Returns lowest common multiple

    >>> lcm(4, 8)
    8
    """
    return (a * b) / gcd(a, b)

# vim: filetype=python
