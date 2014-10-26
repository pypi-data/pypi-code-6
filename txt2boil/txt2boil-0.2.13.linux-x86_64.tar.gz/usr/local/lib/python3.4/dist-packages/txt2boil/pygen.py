"""A generator that uses python code to generate its output.

"""

import textwrap
from .core import *
from . import cmi


class _PyGenHookedRegex(HookedRegex):
    
    """A special object that returns the regex r'^.*$' for the trigger.

    """

    def group(self, n=0):
        if n == 0:
            return super(_PyGenHookedRegex, self).group(n)
        elif n == 1:
            return r'(?s)^(.*)$'
        else:
            return super(_PyGenHookedRegex, self).group(n - 1)

    def output(self, match):
        code = 'def foo(env):\n' + self.group(2)
        code = code.splitlines()
        code = '\n    '.join(code)
        env = {}
        eval(code, env)
        return env['foo'](match.group(0))


class PyGen(Gen):

    """Generate output code using the python code provided in a comment.

    The code is treated as the body of a function who's argument is
    env.  This function is provided with the full text of the source
    file (with comments stripped) inside of env and is expected to
    return a string of the code to be inserted.  For example::

        # Python Gen:
        # if env.startswith('#!'):
        #     return 'I am in a unix script'
        # else:
        #     return 'I am an ordinary module'

        ...
    
    Would then become:

        # Python Gen:
        # if env.startswith('#!'):
        #     return 'I am in a unix script'
        # else:
        #     return 'I am an ordinary module'
        I am an ordinary module

        ...

    Note that even though there was no newline at the end of the
    string, one as added anyways.

    """

    @cmi.nonNoneCMI(lambda: PyGen)
    def matchComment(self, comm):
        return _PyGenHookedRegex(r'(?s)Python Gen:\n(.*)', '', comm)
