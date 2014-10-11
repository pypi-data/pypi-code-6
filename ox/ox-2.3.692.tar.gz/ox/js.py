#!/usr/bin/python
# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

from six import PY2
from .utils import json

def minify(source, comment=''):
    # see https://github.com/douglascrockford/JSMin/blob/master/README
    def get_next_non_whitespace_token():
        pass
    # python2 performance with unicode string is terrible
    if PY2:
        if isinstance(source, unicode):
            source = source.encode('utf-8')
        if isinstance(comment, unicode):
            comment = comment.encode('utf-8')
    tokens = tokenize(source)
    length = len(tokens)
    minified = '/*' + comment + '*/' if comment else ''
    for i, token in enumerate(tokens):
        if token['type'] in ['linebreak', 'whitespace']:
            prevToken = None if i == 0 else tokens[i - 1]
            next = i + 1
            while next < length and tokens[next]['type'] in ['comment', 'linebreak', 'whitespace']:
                next += 1
            nextToken = None if next == length else tokens[next]            
        if token['type'] == 'linebreak':
            # replace a linebreak between two tokens that are identifiers or
            # numbers or strings or unary operators or grouping operators
            # with a single newline, otherwise remove it
            if prevToken and nextToken\
                    and (prevToken['type'] in ['identifier', 'number', 'string']\
                        or prevToken['value'] in ['++', '--', ')', ']', '}'])\
                    and (nextToken['type'] in ['identifier', 'number', 'string']\
                        or nextToken['value'] in ['+', '-', '++', '--', '~', '!', '(', '[', '{']):
                minified += '\n'
        elif token['type'] == 'whitespace':
            # replace whitespace between two tokens that are identifiers or
            # numbers, or between a token that ends with "+" or "-" and one that
            # begins with "+" or "-", with a single space, otherwise remove it
            if prevToken and nextToken\
                    and ((prevToken['type'] in ['identifier', 'number']\
                        and nextToken['type'] in ['identifier', 'number'])
                    or (prevToken['value'] in ['+', '-', '++', '--']
                        and nextToken['value'] in ['+', '-', '++', '--'])):
                minified += ' '
        elif token['type'] != 'comment':
            # remove comments and leave all other tokens untouched
            minified += token['value']
    return minified

def parse_JSONC(source):
    return json.loads(minify(source))

def tokenize(source):
    # see https://github.com/mozilla/narcissus/blob/master/lib/jslex.js
    IDENTIFIER = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ$_'
    KEYWORD = [
        'break',
        'case', 'catch', 'class', 'const', 'continue',
        'debugger', 'default', 'delete', 'do',
        'else', 'enum', 'export', 'extends',
        'finally', 'for', 'function',
        'if', 'implements', 'import', 'in', 'instanceof', 'interface',
        'let', 'module',
        'new',
        'package', 'private', 'protected', 'public',
        'return',
        'super', 'switch', 'static',
        'this', 'throw', 'try', 'typeof',
        'var', 'void',
        'yield',
        'while', 'with'
    ]
    LINEBREAK = '\n\r'
    NUMBER = '01234567890'
    OPERATOR = [
        # arithmetic
        '+', '-', '*', '/', '%', '++', '--',
        # assignment
        '=', '+=', '-=', '*=', '/=', '%=',
        '&=', '|=', '^=', '<<=', '>>=', '>>>=',
        # bitwise
        '&', '|', '^', '~', '<<', '>>', '>>>',
        # comparison
        '==', '!=', '===', '!==', '>', '>=', '<', '<=',
        # conditional
        '?', ':',
        # grouping
        '(', ')', '[', ']', '{', '}',
        # logical
        '&&', '||', '!',
        # other
        '.', ',', ';'
    ]
    REGEXP = 'abcdefghijklmnopqrstuvwxyz'
    STRING = '\'"'
    WHITESPACE = ' \t'
    def is_regexp():
        # checks if a forward slash is the beginning of a regexp,
        # as opposed to the beginning of an operator
        i = len(tokens) - 1
        # scan back to the previous significant token,
        # or to the beginnig of the source
        while i >= 0 and tokens[i]['type'] in ['comment', 'linebreak', 'whitespace']:
            i -= 1
        if i == -1:
            # source begins with forward slash
            is_regexp = True
        else:
            token = tokens[i]
            is_regexp = (
                token['type'] == 'identifier' and token['value'] in KEYWORD
            ) or (
                token['type'] == 'operator' and not token['value'] in ['++', '--', ')', ']', '}']
            )
        return is_regexp
    column = 1
    cursor = 0
    length = len(source)
    tokens = []
    line = 1
    while cursor < length:
        char = source[cursor]
        start = cursor
        cursor += 1
        if char == '/' and cursor < length - 1 and source[cursor] in '/*':
            type = 'comment'
            cursor += 1
            while cursor < length:
                cursor += 1
                if source[start + 1] == '/' and source[cursor] == '\n':
                    break
                elif source[start + 1] == '*' and source[cursor:cursor + 2] == '*/':
                    cursor += 2
                    break
        elif char in IDENTIFIER:
            type = 'identifier'
            while cursor < length and source[cursor] in IDENTIFIER + NUMBER:
                cursor += 1
        elif char in LINEBREAK:
            type = 'linebreak'
            while cursor < length and source[cursor] in LINEBREAK:
                cursor += 1
        elif char in NUMBER:
            type = 'number'
            while cursor < length and source[cursor] in NUMBER + '.':
                cursor += 1
        elif char == '/' and is_regexp():
            type = 'regexp'
            while cursor < length and source[cursor] != '/':
                cursor += (2 if source[cursor] == '\\' else 1)
            cursor += 1
            while cursor < length and source[cursor] in REGEXP:
                cursor += 1
        elif char in OPERATOR:
            type = 'operator'
            if cursor < length:
                string = char + source[cursor]
                while cursor < length and string in OPERATOR:
                    cursor += 1
                    string += source[cursor]
        elif char in STRING:
            type = 'string'
            while cursor < length and source[cursor] != source[start]:
                cursor += (2 if source[cursor] == '\\' else 1)
            cursor += 1
        elif char in WHITESPACE:
            type = 'whitespace'
            while cursor < length and source[cursor] in WHITESPACE:
                cursor += 1
        value = source[start:cursor]
        tokens.append({
            'column': column,
            'line': line,
            'type': type,
            'value': value
        })
        if type == 'comment':
            lines = value.split('\n');
            column = len(lines[-1])
            line += len(lines) - 1
        elif type == 'linebreak':
            column = 1
            column = 1
            line += len(value)
        else:
            column += len(value)
    return tokens
