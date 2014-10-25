"""Frontend interface to the boil library.

Each class is designed for a particular language and inherits its
features from different parent classes.

"""


import cmi
from core import *
from linegen import LineCodeGen
import comments


class Unknown(Gen):
    
    """The unknown language."""

    pass


class Python(comments.Shell, LineCodeGen):

    """The Python language."""

    pass


class RacketConstantGen(Gen):

    """Auto generate constants for Racket code.

    """

    @cmi.nonNoneCMI(lambda: RacketConstantGen)
    def matchComment(self, comm):
        return HookedRegex(r'Constant Gen: (\S+) (.*)\n',
                            '(define \g<0> {})\n', comm)


class Racket(RacketConstantGen, comments.Lisp, LineCodeGen):

    """The Racket language."""

    pass


class C(comments.C, LineCodeGen):

    """The C language."""

    pass


class CXX(comments.CXX, LineCodeGen):

    """The C++ language."""

    pass


class Java(CXX):

    """The Java language."""

    pass


__all__ = ['C', 'CXX', 'Java', 'Python', 'Racket', 'Unknown']
