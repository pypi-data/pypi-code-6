#!/usr/bin/env python
'''
General utilities.
'''

import re
import urllib

def match(things, **kwds):
    '''Return list of matching elements from sequence <things>.  

    The <kwds> hold things to match on.  Keys must name attributes of
    the elements of <things> or are ignored.  Values be regular
    expressions (not globs).

    '''
    def match_one(thing):
        for name, pat in kwds.items():
            string = getattr(thing, name, None)
            if string is None:
                continue

            if pat.startswith('re:'):
                pat = pat[3:]
                m = re.match(pat, string)
                if not m:
                    return
                g = m.group()
                if not g:
                    return
                if g != m.string:
                    return
                continue
            if pat != string:
                return

        return thing

    ret = list()
    for thing in things:
        if match_one(thing):
            ret.append(thing)
    return ret

def download(url, target):
    fd = urllib.urlopen(url)
    rc = fd.getcode() 
    if rc == 200:
        open(target,'wb').write(fd.read())
    else:
        raise RuntimeError, 'Failed to download (%d) %s' % (rc, url)
    return target

