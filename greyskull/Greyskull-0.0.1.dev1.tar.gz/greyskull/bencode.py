# -*- coding: utf-8 -*-
"""
Bencode encoding code by Petru Paler, slightly simplified by uriel, additionally
modified by Carlos Killpack
"""

from itertools import chain


def bencode(x):
    r = []
    if isinstance(x, (int, bool)):
        r.extend(('i', str(x), 'e'))
    elif isinstance(x, str):
        r.extend((str(len(x)), ':', x))
    elif isinstance(x, (list, tuple)):  # FIXME do interface checking rather than type checking
        r.append('l')
        r.extend(bencode(i) for i in x)
        r.append('e')
    elif isinstance(x, dict):
        for key in x.keys():
            if isinstance(key, int):
                raise TypeError
        r.append('d')
        encoded_list = [(bencode(k), bencode(v)) for k, v in sorted(x.items())]
        r.extend(tuple(chain(*encoded_list)))
        r.append('e')
    return ''.join(r)
