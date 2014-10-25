"""Frontend interface to the boil library.

Each class is designed for a particular language and inherits its
features from different parent classes.

"""


import cmi
from core import *
from linegen import LineCodeGen
import comments


class Python(comments.Shell, LineCodeGen):

    """Update all code found in a Python source file.

    """

    pass


class RacketConstantGen(Gen):

    """Auto generate constants for Racket code.

    """

    @cmi.nonNoneCMI(lambda: RacketConstantGen)
    def matchComment(self, comm):
        return HookedRegex(r'Constant Gen: (\S+) (.*)\n',
                            '(define \g<0> {})\n', comm)


class Racket(RacketConstantGen, comments.Lisp, LineCodeGen):

    """Update all code found in a Racket sourcefile.

    """

    pass


__all__ = ['Python', 'Racket']
