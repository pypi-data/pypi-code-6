import sys


def clear():
    sys.stdout.write("\x1b[H\x1b[2J")


def pretty_unit(value, base=1000, minunit=None, format="%0.1f"):
    '''Finds the correct unit and returns a pretty string

    pretty_unit(4190591051, base=1024) = "3.9 Gi"
    '''
    if not minunit:
        minunit = base

    # Units based on base
    if base == 1000:
        units = [' ', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
    elif base == 1024:
        units = ['  ', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi', 'Yi']
    else:
        raise ValueError("The unit base has to be 1000 or 1024")

    # Divide until below threshold or base
    v = float(value)
    u = base
    for unit in units:
        if v >= base or u <= minunit:
            v = v/base
            u = u * base
        else:
            if v >= 10:
                return "%0.0f %s" % (v, unit)
            else:
                return format % v + units[0] + unit
