"""Lookaheadtools provides look-ahead iterators.
Lookahead(someIter) turns a generic iterator into a look-ahead iterator.
FileLookahead(anOpenFile) and LexAhead(someOpenfile) provide look-ahead
iteration over text files.
"""

# Copyright (c) 2014, David B. Curtis
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from collections import namedtuple
import re

class Lookahead(object):
    "Turn any iterator into a look-ahead iterator."
    def __init__(self, anIterator):
        self._iter = anIterator
        self._buff = []
    def __iter__(self):
        return self
    def next(self):
        return self.__next__()
    def __next__(self):
        self._extendBuff(1)
        if len(self._buff) == 0:
            raise StopIteration
        return self._buff.pop(0)
    def __getitem__(self, key):
        "Look-ahead by an arbitrary offset or slice."
        if isinstance(key, slice):
            if key.start < 0:
                raise IndexError("Negative index not allowed.")
            if key.stop == None:
                raise IndexError("Open-ended slice not allowed.")
            minlen = key.stop
        elif isinstance(key, int):
            minlen = key+1
        else:
            raise TypeError("Invalid argument type.")
        self._extendBuff(minlen)
        try:
            return self._buff[key]
        except IndexError:
            return None
    def _extendBuff(self, minLen):
        "Extends internal buffer to minimum length specifed, if possible."
        while len(self._buff) < minLen:
            try:
                self._buff.append(next(self._iter))
            except StopIteration:
                break

class LinesOf(object):
    "Emulate file __iter__()'s line-by-line behavior on a string."
    def __init__(self, aString):
        self._s = aString
    def __iter__(self):
        return self
    def next(self):
        return self.__next__()
    def __next__(self):
        "Each call returns one line of text, including trailing newline, if any."
        if len(self._s) == 0:
            raise StopIteration
        p = self._s.find('\n') + 1
        if p == 0:
            t, self._s = self._s, ''
        else:
            t, self._s = self._s[0:p],self._s[p:]
        return t
    def __enter__(self):
        # Allows LinesOf() to be used in 'with' clauses like a file.
        return self        
    def __exit__(self, *args):
        # Allows LinesOf() to be used in 'with' clauses like a file.
        pass
    
# Lexpos is a namedtuple for reporting lexical position tracking.
Lexpos = namedtuple('Lexpos', 'lineno colno charpos cookie')

class FileLookahead(Lookahead):
    "Fetch a text file a character at a time, with look-ahead and lexical tracking."
    _lineWrap = re.compile(r'([^\n])*(\n)(\s)*(\S)') # not_newline*, newline, white*, non-white
    def __init__(self, anOpenFile, cookie = None):
        self._f = anOpenFile
        self._fla = Lookahead(iter(self._f)) # Fetch from _f by lines.
        self.cookie = cookie # Simply handed back in tracking for convenience.
        self._buff = '' # We're assuming a file of characters.
        self._lineno = 1 # Reported by tracking.
        self._peekLine = 0 # Look-ahead line number.
        self._colno = 0 # Reported by tracking.
        self._charpos = 0 # Reported by tracking.
    def __next__(self):
        self._extendBuff(1)
        if len(self._buff) == 0:
            raise StopIteration            
        c, self._buff = self._buff[0], self._buff[1:]
        if c == '\n':
            # Track new line number, resetting column number.
            self._lineno += 1
            self._colno = 0
            next(self._fla)
        else:
            self._colno += 1 # Track column number.
        self._charpos += 1 # Track file seek position.
        return c
    @property
    def curln(self):
        "Returns the entire line containing the character next() will yield."
        return self._fla[0]
    @property
    def lexpos(self):
        "Returns the lexical position of the character next() will yield."
        return Lexpos(self._lineno, self._colno, self._charpos, self.cookie)
    def _extendBuff(self, minLen, wrap=False):
        "Extends internal buffer to/beyond minimum length specifed, if possible."
        # wrap can be True, or any instance with attr 'match()'
        # wrap == True means wrap past a newline char to at least one
        # non-whitespace character.  Otherwise, extend buffer until
        # wrap.match() returns True for current buffer contents.
        if wrap:
            wraptest = wrap if hasattr(wrap,'match') else self._lineWrap
        while len(self._buff) < minLen \
        or (wrap and not wraptest.match(self._buff)):
            self._peekLine += 1
            t = self._fla[self._peekLine - self._lineno]
            if t == None:
                self._peekLine -= 1
                return
            self._buff += t
    
class LexAhead(FileLookahead):
    "Text file look-ahead iterator with simple lexical utilities."
    @property
    def eol(self):
        "Returns True if next() will yield newline or end-of-file."
        cur = self[0]
        return cur == '\n' or cur == None
    def consume(self, require=None):
        "Consume next character.  Optionally, check membership in 'require'."
        # The 'require' string/set is intended to catch internal parsing
        # logic errors, therefore it raises AssertError if the character
        # to be consumed is not in 'require'.
        if require != None:
            assert self[0] in require
        return next(self)
    def accept(self, aTest, limit=1):
        "Consume/return up to <limit> chars if they pass test, else return ''"
        # aTest can be a string, a set, a list, or anything that supports
        # the 'in' operator, or aTest can be a callable taking a single
        # argument of one character and returning a boolean.
        def strPredicate(c):
            return c in aTest
        predicate = aTest if callable(aTest) else strPredicate
        i,s = 0,''
        while (limit == None or i < limit) and predicate(self[0]):
            s += next(self)
            i += 1
        return s
    def accept_not(self, aTest, limit=1):
        "Consume/return chars if they DO NOT pass aTest, are not NL, not EOF."
        # A useful idom is: accept_not('',None)
        # which has the effect of consuming the remainder of a line up to but
        # not including the newline.  Note that the newline might not be
        # present at the eof-of-file.
        def strPredicate(c):
            return c in aTest or c == '\n'
        predicate = aTest if callable(aTest) else strPredicate
        i,s = 0,''
        while (self[0] != None) and (limit == None or i < limit) \
              and not predicate(self[0]):
            s += next(self)
        return s
    def accept_re(self, aMatcher, fetchAhead = True):
        "Consume/return characters accepted by aMatcher.match()."
        # Presumeably, aMatcher will usually be a compiled regular expression,
        # but need not be, as long as it has match() and group() attributes.
        # The default fetch-ahead attempts to wrap past at least one newline
        # and up through at least one non-white-space character if possible.
        # Most interesting token matches should not run out of buffer.
        # For special cases, the caller may supply a fetchAhead compiled re.
        self._extendBuff(0, fetchAhead)
        if len(self._buff) == 0:
            raise StopIteration
        m = aMatcher.match(self._buff)
        s = m.group(0) if m else ''
        # FIXME: Investigate faster methods of updating lexpos tracking.
        if len(s) > 0:
            self._buff = self._buff[len(s):]
            self._charpos += len(s)
            for c in s:
                if c == '\n':
                    next(self._fla)
                    self._lineno += 1
                    self._colno = 0
                else:
                    self._colno += 1
        return s
    
if __name__ == '__main__':
    import unittest as ut
    class Smoketest(ut.TestCase):
        def setUp(self):
            self.testFileName = 'testfile.txt'
            with open(self.testFileName,'w') as f:
                f.write('foobar\nblivit\n')
        def test_minimal(self):
            import re
            alpha = re.compile(r'[a-zA-Z]*')
            with open(self.testFileName) as f:
                it = LexAhead(f,f.name)
                self.assertEqual(it.accept('fo',None),'foo')
                self.assertEqual(it.accept_re(alpha),'bar')
                self.assertEqual(it[0], '\n')
                self.assertEqual(it.curln,'foobar\n')
                self.assertEqual(next(it),'\n')
                self.assertEqual(it.curln,'blivit\n')
                self.assertEqual(it.lexpos,Lexpos(2,0,7,'testfile.txt'))
                self.assertEqual(it[1:4],'liv')
                self.assertIsNone(it[1000])
                 
    ut.main()
        
