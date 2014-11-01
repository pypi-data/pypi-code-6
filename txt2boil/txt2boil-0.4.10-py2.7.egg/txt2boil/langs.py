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


from . import cmi
from .core import HookedRegex
from .generic_gen import GenericGen
from . import comments
import collections


class Unknown(GenericGen):
    
    """default"""

    pass


class Python(comments.Shell, GenericGen):

    """.py"""

    pass


class _RacketConstantGen(GenericGen):

    """Auto generate constants for Racket code.

    """

    @cmi.nonNoneCMI(lambda: _RacketConstantGen)
    def matchComment(self, comm):
        return HookedRegex(r'Constant Gen: (\S+) (.*)\n',
                            '(define \g<0> {})\n', comm)


class Racket(_RacketConstantGen, comments.Lisp, GenericGen):

    """.rkt"""

    pass


class C(comments.C, GenericGen):

    """.c .h"""

    pass


class CXX(comments.CXX, GenericGen):

    """.cc .cpp .hh .hpp"""

    pass


class Java(CXX):

    """.java"""

    pass


def setupLangs():
    """Return a dictionary that maps file extensions to languages.

    """

    ext_lang = collections.defaultdict(Unknown)
    for cls in globals().values():
        if not isinstance(cls, type): continue 
        if not issubclass(cls, comments.Comments): continue
        
        for ext in cls.__doc__.split():
            ext_lang[ext] = cls()
            ext_lang[ext.strip('.')] = cls()
    return ext_lang

ext_lang = setupLangs()

__all__ = ['C', 'CXX', 'Java', 'Python', 'Racket', 'Unknown', 'ext_lang']
