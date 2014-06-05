import string
import re
from django.core.exceptions import SuspiciousOperation


def compose_path(*args):

    # iter on not null argument
    path = ""
    for arg in (a for a in args if a):
        if arg.startswith('/'):
            path = arg
        else:
            # compose skipping '.'
            p = string.join((x for x in arg.split('/') if x and x != "."), '/')
            if p:
                path = '%s/%s' % (path if path != '/' else '', p) if path else p

    # remove ..
    parent_pattern = r'[^/]*/\.\./?'
    while re.search(parent_pattern, path):
        path = re.sub(parent_pattern, '', path)
    if ".." in path:
        raise SuspiciousOperation(".. in %s not allowed" % (path,))

    # remove last /
    if path == '/':
        return path
    return path if path[-1:] != '/' else path[:-1]
