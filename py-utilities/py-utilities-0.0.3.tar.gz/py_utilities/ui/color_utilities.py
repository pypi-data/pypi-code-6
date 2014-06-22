#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


def random_hex_color():
    """
    Returns a random hex color
    """
    def decimal_to_hex(dec):
        return "{0:02X}".format(dec)

    return '#{0}{1}{2}'.format(
        decimal_to_hex(random.randint(0, 255)),
        decimal_to_hex(random.randint(0, 255)),
        decimal_to_hex(random.randint(0, 255)),
    )

# vim: filetype=python
