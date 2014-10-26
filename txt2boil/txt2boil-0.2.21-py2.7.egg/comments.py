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


class C(Extractor):
    
    """Handle C style /* ... */ comments.

    """

    __regex = re.compile(r'/\* (.*?)\*/', re.M | re.S)

    def blockComment(self, text, start):
        return self.__regex.search(text, start)


class CXX(C):

    """Handle C++ style // ... comments.

    """

    __regex = re.compile(r'^//+ (.*)', re.M)

    def lineComment(self, text, start):
        return self.__regex.search(text, start)

