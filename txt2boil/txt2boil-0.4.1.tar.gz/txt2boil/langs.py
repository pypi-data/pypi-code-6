# Copyright (C) 2014 Kieran Colford
#
# This file is part of txt2boil.
#
# txt2boil is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# txt2boil is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with txt2boil.  If not, see <http://www.gnu.org/licenses/>.

"""Frontend interface to the txt2boil library.

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
