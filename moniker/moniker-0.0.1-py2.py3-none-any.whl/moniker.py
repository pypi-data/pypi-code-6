from __future__ import print_function, unicode_literals

import os
import re

from collections import defaultdict

__all__ = ['tree_walk']

# Recursive Tree Definition
Tree = lambda: defaultdict(Tree)

def add(t, key, replace):
    t[key[0]] = [i for i in key[1]]


def tree_walk(top, pattern, replace):
    """
    Walk file system heiarchy for the base directory generating files matching
    unix glob pattern.
    """
    root  = Tree()

    pat = re.compile(re.escape(pattern))
    for path, dirname, filelist in os.walk(top):

        if not any([files for files in filelist if files.endswith(pattern)]):
            continue

        base = os.path.relpath(path, start=top)
        node = [base, [{files: pat.sub(replace, files)} for files in filelist if files.endswith(pattern)]]
        add(root, node, replace)

    return root
