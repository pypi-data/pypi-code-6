#!/usr/bin/python
# -*- coding: ascii -*-
############################################################################
# csexp.py - Canonical S-expression Library
#
# Copyright (C) 2008  Dwayne C. Litzenberger <dlitz@dlitz.net>
# All rights reserved.
# 
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation.
# 
# THE AUTHOR PROVIDES THIS SOFTWARE ``AS IS'' AND ANY EXPRESSED OR 
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES 
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, 
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, 
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY 
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
###########################################################################
# History:
#
# 2008-02-11 Dwayne C. Litzenberger <dlitz@dlitz.net>
#   - Initial Release (v0.1)
#
###########################################################################

"""Library for generating and parsing SPKI canonical s-expressions

See http://people.csail.mit.edu/rivest/Sexp.txt for a description of the
encoding.
"""

__version__ = "0.1"

import cStringIO as StringIO

class error(Exception):
    pass

class strhint(object):
    """String with a display-hint"""

    __slots__ = ('value', 'display_hint')

    def __init__(self, value='', display_hint=None):
        if display_hint is None:    # so strhint(strhint('foo', 'bar')) works
            display_hint = getattr(value, 'display_hint', None)
        object.__setattr__(self, 'value', str(value))
        object.__setattr__(self, 'display_hint', str(display_hint))

    def __repr__(self):
        return "%s(%r, %r)" % (self.__class__.__name__, self.value, self.display_hint)

    def __str__(self):
        return self.value

    def __setattr__(self, attrname, value):
        raise TypeError("object is immutable")

    def __eq__(self, other):
        my_dh = getattr(self, 'display_hint', None)
        other_dh = getattr(other, 'display_hint', None)
        return (str(self) == str(other)) and (my_dh == other_dh)

    def __ne__(self, other):
        return not (self == other)

def _getch(file, ungetch=None):
    if ungetch is not None:
        ch = ungetch
    else:
        ch = file.read(1)
    if not ch:
        raise error("input truncated")
    if len(ch) != 1 or not (0 <= ord(ch) <= 255):
        raise error("file.read(1) returned %r instead of single-octet string" % (ch,))
    return ch

def _generic_decode(read_func, name, s, *args, **kwargs):
    f = StringIO.StringIO(s)
    try:
        retval = read_func(f, *args, **kwargs)
        if f.tell() != len(s):
            raise error("found extra junk at end of " + name)
    except error, exc:
        raise error("at offset %d: %s" % (f.tell()-1, exc.args[0]))
    return retval

def _coerce_object(data):
    """Coerce the specified object into one of the following types: (str, strhint, list)
    
    Return a tuple (type, obj) containing the type and the object.

    NB: This performs a shallow coersion only.
    """
    if isinstance(data, unicode):
        raise TypeError("unicode strings not supported")
    
    display_hint = getattr(data, 'display_hint', None)
    if display_hint is not None:    # string with display-hint
        return (strhint, strhint(data))
    elif isinstance(data, str):     # string without display-hint
        return (str, str(data))
    else:   # list
        return (list, list(data))

def verbatim_encode(s):
    """Return the verbatim encoding of a given octet string."""
    # Make sure we have a byte string
    s = str(s)
    return "%d:%s" % (len(s), s)

def verbatim_read(file, ungetch=None, declared_length=None):
    """Decode a string passed in using verbatim encoding.

    This function takes an iterator, which must return one octet per iteration.

    @param file: a file-like object that this function will read octets from
    @param ungetch: a single octet to be consumed before any other octets are consumed from C{file}
    @param declared_length: if set, start reading as if the length of the string has already been read
    """
    if declared_length is None:
        # Read the length
        ch = _getch(file, ungetch)
        if ch == '0':   # Possible zero-length string.
            ch = _getch(file)
            if ch != ':':
                raise error("verbatim string length prefixed with '0'")
            # Zero-length string.  Return it.
            return ""
        elif ch not in "123456789":
            raise error("%r found where digit expected" % (ch,))
        else:
            length = int(ch)
            ch = _getch(file)
            while ch != ':':
                if ch not in "0123456789":
                    raise error("%r found where digit or colon expected" % (ch,))
                length = (length * 10) + int(ch)
                ch = _getch(file)
    else:
        # Length assumed (most likely already read by the caller)
        length = declared_length
        ch = _getch(file, ungetch)
        if ch != ':':
            raise error("%r found where colon expected" % (ch,))
        if length == 0:
            # Zero-length string.  Return it.
            return ""

    # Read the string itself
    data = file.read(length)
    if len(data) < length:
        raise error("verbatim string truncated")
    elif len(data) > length:    # This should never happen
        raise AssertionError("assertion failed: len(data) <= length")
    else:
        assert len(data) == length
        return data

def verbatim_decode(s):
    return _generic_decode(verbatim_read, 'verbatim string', s)

def csexp_encode(data):
    """Encode the given data as a canonical s-expression.

    An s-expression is a hierarchical structure consisting of lists, strings,
    and strings with attached "display_hints" attributes.
    """
    (dtype, data) = _coerce_object(data)
    if dtype is str:
        return verbatim_encode(data)
    elif dtype is strhint:
        display_hint = getattr(data, 'display_hint', None)
        encoded_str = verbatim_encode(str(data))
        return "[%s]%s" % (verbatim_encode(display_hint), encoded_str)
    elif dtype is list:
        retval = []
        for item in data:
            retval.append(csexp_encode(item))
        return "(%s)" % ("".join(retval),)
    else:
        raise AssertionError

def csexp_read(file, ungetch=None):
    ch = _getch(file, ungetch)
    if ch == '(':   # Start of list
        retval = []
        while True:
            ch = _getch(file)
            if ch == ')':
                break
            elif ch in "([0123456789":
                retval.append(csexp_read(file, ch))
            else:
                raise error("unexpected input %r" % (ch,))
        return retval
    elif ch == '[': # Start of string with display-hint
        display_hint = verbatim_read(file)
        ch = _getch(file)
        if ch != ']':
            raise error("expected ']', got %r" % (ch,))
        return strhint(verbatim_read(file), display_hint)
    elif ch in "0123456789":    # Start of string without display-hint
        return verbatim_read(file, ch)
    else:
        raise error("unexpected input %r" % (ch,))

def csexp_decode(s):
    return _generic_decode(csexp_read, 'canonical s-expression', s)

# vim:set ts=4 sw=4 sts=4 expandtab:
