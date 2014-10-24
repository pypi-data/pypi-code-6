from core import *
import re


class Shell(Extractor):

    """Handle shell style comments.

    """

    __regex = re.compile(r'^#+ (.*\n)', re.M)

    def lineComment(self, text, start):
        return self.__regex.search(text, start)


class Lisp(Extractor):

    """Handle lisp style comments.

    """

    __regex = re.compile(r'^;+ (.*\n)', re.M)

    def lineComment(self, text, start):
        return self.__regex.search(text, start)

__all__ = ['Shell', 'Lisp']
