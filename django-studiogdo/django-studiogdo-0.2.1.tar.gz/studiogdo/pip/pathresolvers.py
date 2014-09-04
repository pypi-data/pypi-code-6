# -*- coding: utf-8 -*-
import re
from collections import OrderedDict


def path(exp, skel, context=None, template_name=None):
    context = context or {}
    reg = re.compile(r'%s' % (exp,))
    if isinstance(skel, basestring):
        skel = [skel]
    skel_dict = {'skel': skel, 'context': context, }
    if template_name:
        skel_dict['template_name'] = template_name
    return (reg, skel_dict)


class Patterns(object):

    def __init__(self, *kwargs):
        self._regexes = OrderedDict()
        for elt in kwargs:
            self._regexes[elt[0]] = elt[1]

    def __getitem__(self, name):
        for regex, value in self._regexes.items():
            m = regex.match(name)
            if m is not None:
                value.update(m.groupdict())
                return value.copy()
        raise KeyError('Key %s does not match any regex' % name)

    def iterkeys(self):
        return self._regexes.iterkeys()

    def iteritems(self):
        return self._regexes.iteritems()

    def keys(self):
        return [reg.pattern for reg in self._regexes.iterkeys()]

patterns = Patterns
