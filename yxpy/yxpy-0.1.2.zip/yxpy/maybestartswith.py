# -*- coding: utf-8 -*-
def maybe_startswith(s, *prefixes):
    '''
    @return: True -- yes, False -- no, None -- not sure.
    '''
    rev_matches = []
    for prefix in prefixes:
        if s.startswith(prefix):
            return True
        rev_matches.append(prefix.startswith(s))
    if not any(rev_matches):
        return False
    return None
