#!/bin/env python
# -*- coding: utf-8 -*-

import re


class InvalidTokenError(Exception):
    pass


class WrongParameterCountError(Exception):
    pass


class Token(object):
    def __init__(self, type, name='', parameters=None, string=''):
        self.type = type
        self.name = name
        self.parameters = parameters
        self.string = string


class Node(object):
    allowed_nodes = ['string', 'b', 'u', 's', 'i', 'mod', 'spoiler', 'm',
                     'code', 'php', 'img', 'quote', 'url', 'list', 'table']
    invalid_string_recovery = 'none'
    invalid_start_recovery = 'string'
    invalid_end_recovery = 'string'

    bbname = ''

    def __init__(self, parameters=None):
        self.children = []
        self.parent = None

    def __str__(self):
        string = ''
        for child in self.children:
            string += str(child)
        return string

    def append(self, child):
        self.children.append(child)
        child.parent = self

    def get_invalid_start_recovery(self, name):
        return self.invalid_start_recovery


class String(Node):
    def __init__(self, string):
        super().__init__()
        self.string = string

    def __str__(self):
        return self.string

    def append(self, string):
        self.string += string


class Tag(Node):
    bbname = ''
    parameter_count = [0]


class SimpleTag(Tag):
    invalid_start_recovery = 'close'
    invalid_end_recovery = 'reopen'

    tagname = ''
    pre_format = '<%s>'
    post_format = '</%s>'

    def __str__(self):
        cstring = ''
        for child in self.children:
            cstring += str(child)
        if cstring == '':
            return ''
        else:
            format = "%s%%s%s" % (self.pre_format, self.post_format)
            return format % (self.tagname, cstring, self.tagname)


class StrongTag(SimpleTag):
    bbname = 'b'
    tagname = 'Strong'


class EmTag(SimpleTag):
    bbname = 'i'
    tagname = 'Em'


class StrikeTag(SimpleTag):
    bbname = 's'
    tagname = 'Strike'


class UnderlineTag(SimpleTag):
    bbname = 'u'
    tagname = 'Underline'


class InlineCodeTag(SimpleTag):
    bbname = 'm'
    tagname = 'InlineCode'
    allowed_nodes = ['string']


class CodeTag(SimpleTag):
    bbname = 'code'
    tagname = 'Code'
    allowed_nodes = ['string']


class PhpCodeTag(SimpleTag):
    bbname = 'php'
    tagname = 'Code'
    pre_format = '<%s Language="PHP">'
    allowed_nodes = ['string']


class SpoilerTag(SimpleTag):
    bbname = 'spoiler'
    tagname = 'Spoiler'
    invalid_end_recovery = 'close'


class HighlightTag(SimpleTag):
    bbname = 'mod'
    tagname = 'Highlight'


class ParameterTag(Tag):
    tagname = ''
    pre_format = {0: '<%s>'}
    post_format = '</%s>'

    def __init__(self, parameters):
        Tag.__init__(self)
        self.parameters = parameters

    def __str__(self):
        if len(self.parameters) == 0:
            string = self.pre_format[0] % self.tagname
        else:
            string = self.pre_format[len(self.parameters)] % ((self.tagname,) +
                                                              tuple(self.parameters))
        for child in self.children:
            string += str(child)
        string += self.post_format % self.tagname
        return string


class QuoteTag(ParameterTag):
    bbname = 'quote'
    tagname = 'Quote'
    parameter_count = [0, 3]
    pre_format = {0: '<%s>', 3: '<%s ThreadId="%s" PostId="%s" Author="%s">'}
    invalid_end_recovery = 'close'


class ListTag(SimpleTag):
    bbname = 'list'
    tagname = 'List'
    allowed_nodes = ['*']
    invalid_string_recovery = 'add *'
    invalid_start_recovery = 'add *'
    invalid_end_recovery = 'close'


class ItemTag(SimpleTag):
    bbname = '*'
    tagname = 'Item'
    invalid_end_recovery = 'close'


class TableTag(SimpleTag):
    bbname = 'table'
    tagname = 'Table'
    allowed_nodes = ['--']
    invalid_string_recovery = 'add --'
    invalid_start_recovery = 'add --'
    invalid_end_recovery = 'close'


class RowTag(SimpleTag):
    bbname = '--'
    tagname = 'Row'
    allowed_nodes = ['||']
    invalid_string_recovery = 'add ||'
    invalid_start_recovery = 'add ||'
    invalid_end_recovery = 'close'

    def get_invalid_start_recovery(self, name):
        if name == '--':
            return 'close'
        else:
            return self.invalid_start_recovery


class CellTag(SimpleTag):
    bbname = '||'
    tagname = 'Cell'
    invalid_end_recovery = 'close'


class ShortTag(ParameterTag):
    def __init__(self, parameters):
        if not parameters:
            self.need_parameter = True
            ParameterTag.__init__(self, [''])
        else:
            self.need_parameter = False
            ParameterTag.__init__(self, parameters)

    def append(self, child):
        if isinstance(child, String) and self.need_parameter:
            self.parameters[0] += child.string
        else:
            ParameterTag.append(self, child)


class ImageTag(ShortTag):
    bbname = 'img'
    allowed_nodes = ['string']
    invalid_start_recovery = 'string'
    invalid_end_recovery = 'string'

    def __str__(self):
        return '<Image Source="%s" />' % self.parameters[0]


class LinkTag(ShortTag):
    bbname = 'url'
    allowed_nodes = ['string']
    invalid_start_recovery = 'string'
    invalid_end_recovery = 'string'
    parameter_count = [0, 1]

    def __init__(self, parameters):
        ShortTag.__init__(self, parameters)
        self.need_parameter = True
        if parameters:
            self.parameters = [''] + self.parameters

    def __str__(self):
        if len(self.parameters) == 1:
            string = '<Link Target="%s" />' % self.parameters[0]
        else:
            string = '<Link Target="%s">%s</Link>' % (self.parameters[1],
                                                      self.parameters[0])
        return string


class BbCodeParser(object):
    _REGEX_STR = r'(?P<string>.*?)((?P<starttoken>\[\s*(?P<sname>%s)\s*(=(?P<parameters>(\s*(("[^"]+")|([^,"]+?))\s*,)*(\s*(("[^"]+")|([^,"]+?))\s*)))?\])|(?P<endtoken>\[/(?P<ename>%s)\]))'
    _SPLIT_RGX = re.compile(r'\s*(("(?P<quoted>[^"]+)")|(?P<normal>[^,"]*[^,\s"]))\s*')

    _TAGS = {'b': StrongTag,
             'i': EmTag,
             's': StrikeTag,
             'u': UnderlineTag,
             'm': InlineCodeTag,
             'code': CodeTag,
             'php': PhpCodeTag,
             'spoiler': SpoilerTag,
             'mod': HighlightTag,
             'quote': QuoteTag,
             'list': ListTag,
             '*': ItemTag,
             'img': ImageTag,
             'url': LinkTag,
             'table': TableTag,
             '--': RowTag,
             '||': CellTag}

    @classmethod
    def _split_parameters(cls, string):
        if not string:
            return []

        parameters = []
        for match in cls._SPLIT_RGX.finditer(string):
            if match.group('quoted'):
                parameters.append(match.group('quoted'))
            elif match.group('normal'):
                parameters.append(match.group('normal'))
            else:
                raise Exception('split_parameters failed')
        return parameters

    @classmethod
    def _escape_regex(cls, string):
        return string.replace('*', r'\*').replace('|', r'\|')

    def __init__(self):
        self.tags = {}

    def _lexical_analysis(self):
        self.tokens = []

        bbtags = [self._escape_regex(tag) for tag in list(self._TAGS.keys())]
        bbtags = '(' + '|'.join(bbtags) + ')'

        regex = re.compile(self._REGEX_STR % (bbtags, bbtags), re.I | re.S)

        pos = 0

        for match in regex.finditer(self.string):
            if match.group('string'):
                self.tokens.append(Token('string',
                                         string=match.group('string')))
                pos += len(match.group('string'))
            if match.group('starttoken'):
                parameters = self._split_parameters(match.group('parameters'))
                self.tokens.append(Token('start',
                                         match.group('sname').lower(),
                                         parameters,
                                         match.group('starttoken')))
                pos += len(match.group('starttoken'))
            elif match.group('endtoken'):
                self.tokens.append(Token('end',
                                         match.group('ename').lower(),
                    [],
                                         match.group('endtoken')))
                pos += len(match.group('endtoken'))

        if pos < len(self.string):
            self.tokens.append(Token('string', string=self.string[pos:]))

    def parse(self, string):
        self.string = string.replace('<', '&lt;').replace('>', '&gt;')

        self.root = Node()
        self.idx = self.root

        self._lexical_analysis()

        while len(self.tokens) > 0:
            token = self.tokens[0]

            if token.type == 'string':
                try:
                    self._add_string(token.string)
                except InvalidTokenError:
                    policy = self.idx.invalid_string_recovery
                    if policy[0:3] == 'add':
                        self.tokens.insert(0, Token('start', policy[4:]))
                    else:
                        raise Exception('unknown invalid_string_recovery')
                    continue
            elif token.type == 'start':
                try:
                    self._add_start(token.name, token.parameters)
                except InvalidTokenError:
                    policy = self.idx.get_invalid_start_recovery(token.name)

                    if not self._is_tag_open2(token.name):
                        policy = 'string'

                    if policy == 'close':
                        self.tokens.insert(0, Token('end', self.idx.bbname))
                    elif policy == 'string':
                        token.type = 'string'
                    elif policy[0:3] == 'add':
                        self.tokens.insert(0, Token('start', policy[4:]))
                    else:
                        raise Exception('unknown invalid_start_recovery')
                    continue
                except WrongParameterCountError:
                    token.type = 'string'
                    continue
            elif token.type == 'end':
                try:
                    self._add_end(token.name)
                except InvalidTokenError:
                    policy = self.idx.invalid_end_recovery

                    if not self._is_tag_open(token.name):
                        policy = 'string'

                    if policy == 'reopen':
                        self.tokens.insert(0, Token('end', self.idx.bbname))
                        self.tokens.insert(2, Token('start', self.idx.bbname))
                    elif policy == 'close':
                        self.tokens.insert(0, Token('end', self.idx.bbname))
                    elif policy == 'string':
                        token.type = 'string'
                    else:
                        raise Exception('unknown invalid_end_recovery')
                    continue
            else:
                raise Exception('Unknown Token-Type: %s' % token.type)
            del self.tokens[0]

        return str(self.root)

    def _add_string(self, string):
        if 'string' not in self.idx.allowed_nodes:
            raise InvalidTokenError()
        self.idx.append(String(string))

    def _add_start(self, name, parameters):
        if name not in self.idx.allowed_nodes:
            raise InvalidTokenError()

        tag_class = self._TAGS[name]

        if parameters == None:
            parameters = []
        if len(parameters) not in tag_class.parameter_count:
            raise WrongParameterCountError()

        tag = tag_class(parameters)
        self.idx.append(tag)
        self.idx = tag

    def _add_end(self, name):
        if self.idx.bbname != name:
            raise InvalidTokenError()

        self.idx = self.idx.parent

    def _is_tag_open(self, name):
        node = self.idx

        while node != self.root:
            if node.bbname == name:
                break
            node = node.parent
        else:
            return False

        return True

    def _is_tag_open2(self, name):
        node = self.idx

        while node != self.root:
            if name in node.allowed_nodes:
                break
            node = node.parent
        else:
            return False

        return True
