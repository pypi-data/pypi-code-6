#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


def get_pos_map(tagset):
    """Return part-of-speech map for given tag set. See
    https://code.google.com/p/universal-pos-tags/

    """
    usurper_dir = os.path.dirname(os.path.realpath(__file__))
    # Usurper_dir = os.path.abspath(os.path.join(usurper_dir, os.pardir))
    # map_path = os.path.join(Usurper_dir, "data", "universal-pos-tags", tagset + ".map")
    map_path = os.path.join(usurper_dir, "data", tagset + ".map")
    mapping = {}
    with open(map_path) as fh:
        for line in fh:
            t = line.rstrip().split("\t")
            mapping[t[0]] = t[1]
    return mapping
