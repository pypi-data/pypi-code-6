# Copyright (c) 2014 Susam Pal
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in
#      the documentation and/or other materials provided with the
#      distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


"""Dot Object Notation (DON) parser.

DON stands for Dot Object Notation. It is a convenient way to write
simple configuration files.
"""


__version__ = '0.1.1'
__date__ = '19 October 2014'
__author__ = 'Susam Pal <susam@susam.in>'
__credits__ = ('JSON and YAML, the inspiration behind DSON.')


import collections
import re


def parse(s):
    """Parse DON string into DON object.

    Return: Root DON object that represents the parsed DON
            (type: don.Object)

    Raise:
    don.Error -- When an error is encountered while parsing DON
    """
    parser = Parser()
    parser.parse(s)
    return parser.root


def parse_file(s):
    """Parse DON file into DON object.

    Return: Root DON object that represents the parsed DON
            (type: don.Object)

    Raise:
    don.Error -- When an error is encountered while parsing DON
    """
    parser = Parser()
    parser.parse_file(s)
    return parser.root
    

class Object(collections.UserDict):

    """Parsed DON object.

    An instance of this class behaves like a dictionary as well as an
    object. Values can be accessed with their keys like in a normal
    dictionary as well as by attribute references where the attribute
    name is same as the key name.
    """

    def __getattr__(self, name):
        """Return the value for the specified key.

        Arguments:
        name -- Key (type: str)

        Return: Value associated with the key
                (type: str or don.Object)
        """
        return self.data[name]


class Parser:

    """DON parser.

    This class may be used to parse configuration files written in DON
    format.

    Methods:
    parse      -- Parse a DON string into DON object.
    parse_file -- Parse a DON file into DON object.

    Attributes:
    root -- Root DON object that represents the parsed DON
            (type: don.Object)
    """

    def __init__(self):
        """Initialize the parser."""
        self.root = Object()
        self._line = 0
        self._source = ''
        self._previous_key = None
        self._current_key = None
        self._current_resolved_key = None
        self._previous_key_tokens = None
        self._current_key_tokens = None
        self._current_value = None

    def parse(self, s):
        """Parse DON string into DON object.

        Return: Root DON object that represents the parsed DON
                (type: don.Object)

        Raise:
        don.Error -- When an error is encountered while parsing DON
        """
        self._line = 0
        self._source = '<str>'
        for line in s.splitlines():
            self._line += 1
            self._process_line(line)
        return self.root

    def parse_file(self, filepath):
        """Parse DON string into DON object.

        Return: Root DON object that represents the parsed DON
                (type: don.Object)

        Raise:
        don.Error -- When an error is encountered while parsing DON
        """
        self._line = 0
        self._source = filepath
        with open(filepath) as f:
            for line in f:
                self._line += 1
                self._process_line(line)

    def _process_line(self, s):
        """Process a line of DON and update DON object."""
        # Ignore blank lines and comments
        s = s.strip()
        if s == '' or s[0] == '#': 
            return

        # Split line into key-value pair
        tokens = s.split(':', 1)
        if len(tokens) != 2:
            self._error('Cannot split {!r} into key and value', s)
        else:
            k, v = tokens[0].rstrip(), tokens[1].lstrip()

        self._current_key = k
        self._current_value = v

        self._parse_key()
        self._current_resolved_key = '.'.join(self._current_key_tokens)

        if self._current_value:
            self._update_object()

        self._previous_key = self._current_key
        self._previous_resolved_key = self._current_resolved_key
        self._previous_key_tokens = self._current_key_tokens

    def _parse_key(self):
        """Parse key in the current line being processed."""
        self._current_key_tokens = self._current_key.split('.')
        explicit_token_found = False
        token_re = re.compile('^[^\d\W]\w*$')
        for i, t in enumerate(self._current_key_tokens):
            if not explicit_token_found:
                if t == '':
                    self._populate_empty_token(i)
                else:
                    explicit_token_found = True
            if explicit_token_found and token_re.search(t) is None:
                    self._error('Invalid token {!r} in key {!r}',
                                t, self._current_key)

    def _populate_empty_token(self, i):
        """Replace empty tokens in current key with explicit tokens."""
        if i < len(self._previous_key_tokens):
            self._current_key_tokens[i] = self._previous_key_tokens[i]
        else:
            self._error('Number of empty tokens in key {!r} exceeds '
                        'number of tokens in the previous key {!r}',
                        self._current_key, self._previous_key)

    def _update_object(self):
        """Update DON object with the current key and value."""
        d = self.root
        tokens_traversed = []
        for k in self._current_key_tokens[:-1]:
            if k not in d:
                d[k] = Object()
            d = d[k]
            tokens_traversed.append(k)
            if type(d) is str:
                self._error('Cannot define {!r} with value {!r} '
                            'because {!r} is already defined with '
                            'value {!r}', self._current_resolved_key,
                             self._current_value,
                             '.'.join(tokens_traversed), d)

        k = self._current_key_tokens[-1]
        if k in d:
            self._error('Cannot redefine key {!r} with value {!r} '
                        'to value {!r}', self._current_resolved_key,
                        d[k], self._current_value)
        else:
            d[k] = self._current_value

    def _error(self, msg, *args):
        """Raise don.Error."""
        msg = msg.format(*args)
        msg = '{}:{}: {}'.format(self._source, self._line, msg)
        raise Error(msg)
        
        
class Error(Exception):
    """DON parsing related exception."""
