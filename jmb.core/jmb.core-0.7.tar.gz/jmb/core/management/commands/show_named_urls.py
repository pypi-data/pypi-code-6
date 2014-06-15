from django.core import urlsresolver

def _get_named_patterns():

    "Returns list of (pattern-name, pattern) tuples"

    resolver = urlresolvers.get_resolver(None)
    patterns = sorted([
        (key, value[0][0][0])
        for key, value in resolver.reverse_dict.items()
        if isinstance(key, basestring)
    ])
    return patterns

def show():

    longest = max([len(pair[0]) for pair in _get_named_patterns()])
    for key, value in _get_named_patterns():
        print '%s %s\n' % (key.ljust(longest + 1), value)

    
