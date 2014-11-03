try:
    from future_builtins import ascii, filter, hex, map, oct, zip
except ImportError:
    pass

try:
    input = raw_input
    range = xrange
except NameError:
    pass
