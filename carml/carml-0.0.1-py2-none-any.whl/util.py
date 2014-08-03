import time
import datetime
import functools

from twisted.python import log
_log = functools.partial(log.msg, system='carml')

import colors

class NoColor(object):
    def __init__(self):
        self._overrides = filter(lambda x: not x.startswith('__'), dir(colors))

    def __getattr__(self, name):
        '''
        All the "things" in the colors library are methods; so, if we
        didn't ask for a magic-python method, we return the "noop"
        function which doesn't do anything to your string. The colors
        library would add ANSI commands around it.
        '''
        def noop(s):
            return s
        if name in self._overrides:
            return noop
        return self.__dict__[name]

def turn_off_color():
    global colors
    colors = NoColor()

def wrap(text, width, prefix=''):
    """
    Simple word-wrapping thing. Might be worth considering a
    dependency on 'textwrap' if this gets longer than a few lines ;)
    """
    words = text.split()
    lines = []
    while len(words):
        line = prefix
        while len(words) and len(line) < width:
            word = words.pop(0)
            line += ' ' + word
        lines.append(line)
    return '\n'.join(lines)

def format_net_location(loc, verbose_asn=False):
    rtn = '(%s ' % loc.ip
    comma = False
    if loc.asn:
        if verbose_asn:
            rtn += loc.asn
        else:
            rtn += loc.asn.split()[0]
        comma = True
    if loc.countrycode:
        if comma: rtn += ', '
        rtn += loc.countrycode
        comma = True
    if loc.city and loc.city[0]:
        if comma: rtn += ', '
        rtn += ','.join(loc.city)
        comma = True
    return rtn + ')'


def nice_router_name(router, color=True):
    """
    returns a router name with ~ at the front if it's not a named router
    """
    green = str
    italic = str
    if color:
        green = colors.green
        italic = colors.italic
    if router.name_is_unique:
        return green(router.name)
    return italic('~%s' % router.name)


def dump_circuits(state, verbose):
    _log('  %-4s | %-5s | %-42s | %-8s | %-12s' % ('ID', 'Age', 'Path (router names, ~ means no Named flag)', 'State', 'Purpose'))
    _log(' ------+-------+' + ('-'*44) + '+' + (10*'-') + '+' + (12*'-'))
    circuits = state.circuits.values()
    circuits.sort(lambda a, b: cmp(a.id, b.id))
    now = datetime.datetime.utcnow()
    for circ in circuits:
        path = '->'.join(map(nice_router_name, circ.path))
        plain_router_name = functools.partial(nice_router_name, color=False)
        plain_path = '->'.join(map(plain_router_name, circ.path))
        real_len = len(plain_path)
        if real_len > 42:
            # revert to uncoloured path since we don't know where ANSI controls are
            path = plain_path[:(42 - 13)] + '...' + plain_path[-10:]
        elif len(path) == 0:
            path = '(empty)'
        else:
            path = path + ((42 - real_len) * ' ')
        age = circ.age(now)
        if age > 300:
            age = '%2dmin' % (age/60.0)
        else:
            age = '%ds' % age

        # path is already padded to 42 chars, as it contains ANSI controls
        _log(colors.bold('  %4d | %5s | %s | %-8s | %-12s' % (circ.id, age, path, circ.state, circ.purpose)))
#        print str(circ.flags)
        if verbose:
            padding = ' ' * 17
            _log(' ' * 8, ', '.join([(str(k) + '=' + str(v)) for (k, v) in circ.flags.items()]))
            for r in circ.path:
                if r.ip != 'unknown':
                    _log(padding, '%s=%s' % (r.name, format_net_location(r.location)))
    _log(' ------+-------+' + ('-'*44) + '+' + (10*'-') + '+' + (12*'-'))

