try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode


def isstr(s):
    try:
        return isinstance(s, str) or isinstance(s, unicode)
    except NameError:
        return isinstance(s, str)


def to_urlstr(p):
    params = []
    if any([isinstance(v, list) for v in p.values()]):
        removals = []
        for k, v in p.items():
            if not isinstance(v, list):
                continue
            params += map(lambda v: (k, v), v)
            removals.append(k)
        for k in removals:
            del p[k]
    return urlencode(list(p.items()) + params)
