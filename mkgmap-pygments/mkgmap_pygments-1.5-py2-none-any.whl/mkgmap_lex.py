# -*- coding: utf-8 -*-
"""
	A pygments lexer for mkmgmap style files.

	:copyright: Copyright 2014 Steve Ratcliffe
	:license: BSD, see LICENSE for details.
"""

import re

from pygments.lexer import Lexer, RegexLexer, do_insertions, bygroups, include, combined
from pygments.token import Punctuation, \
	 Text, Comment, Operator, Keyword, Name, String, Number, Generic, Literal


__all__ = ['MkgmapLexer']

line_re = re.compile('.*?\n')

# List of all commands.  The apply and apply_once are omitted as they are special.
actions = '''
	set add setaccess addaccess
	name addlabel delete deletealltags echo echotags
'''.split()


class MkgmapLexer(RegexLexer):
	"""
	A pygments lexer for the mkgmap style file syntax.
	"""

	# flags = re.U|re.M
	name = 'Mkgmap style files'
	aliases = ['mkgmap', 'mkgmap_style']
	filenames = ['*.style']
	mimetypes = ['text/plain']

	tokens = {
		'root': [
			# At the top level, we are usually expecting the start of an expression. There are a few
			# other possibilities, such as comments and includes.
			include('comment'),
			(r'<<<(lines|relations|points|polygons)>>>\n', Keyword),
			(r'<<<[^>]+>>>\n', Keyword, 'skip'),
			(r'include\s+(?![=<>!~])', Keyword, ('end', 'string')),
			(r'<finalize>\s*', Keyword),
			(r'(?=[\'"])', Text, ('term', 'string')),
			(r'\$?[\w:]+(\(\))?', Name.Attribute, 'term'),
			(r'\${[\w:]+}', Name.Attribute, 'term'),
			(r'[&|()!]', Punctuation),
			(r'{', Punctuation, 'action'),
			(r'\[', Punctuation, 'type'),
		],
		'skip': [
			include('comment'),
			(r'(?=<<<)', Text, '#pop'),
			(r'[^<]+', Text),
		],
		'end': [
			include('comment'),
			(r';', Punctuation, '#pop'),
		],
		'term': [
			include('comment'),
			(r'([!<>]?=|[=<>~])', Punctuation, ('#pop', 'value')),
		],
		'action': [
			include('comment'),
			(r'}', Punctuation, '#pop'),
			(r'(?s)(apply|apply_once)(\s*{)', bygroups(Keyword, Punctuation), '#push'),
			(r'(apply|apply_once)\s*', Keyword, 'apply_role'),
			(r'\b(%s)\b' % "|".join(actions), Keyword, 'command'),
		],
		'command': [
			include('comment'),
			(r';', Punctuation, '#pop'),
			(r'}', Punctuation, '#pop:2'),
			(r'[\w:.-]+', Name),
			(r'=+', Punctuation, 'value'),
			(r'\|+', Punctuation),
			(r'(?=[\'"])', Text, 'interp-string'),
		],
		'apply_role': [
			include('comment'),
			(r'[^{]+{', Text, ('#pop', 'action')),
		],
		'apply': [
			include('command'),
		],
		'type': [
			include('comment'),
			(r']', Punctuation, '#pop'),
			(r'0x[0-9a-fA-F]+\s*', Name),
			(r'(level|resolution)(\s+)([\d-]+)', bygroups(Keyword, Punctuation, Literal)),
			(r'(default_name)(=|\s+)', bygroups(Keyword, Text), 'string'),
			(r'(road_class|road_speed)([\s=]+)([\d-]+)', bygroups(Keyword, Punctuation, Literal)),
			(r'(continue|with_actions|withactions|propogate|no_propogate|copy|oneway|access)', Keyword),
		],
		'string': [
			include('comment'),
			(r'(?s)"[^"]*"', String.Double, '#pop'),
			(r"(?s)'[^']*'", String.Single, '#pop'),
		],
		'interp-string': [
			include('comment'),
			(r'"', String, ('#pop', 'interp-string-d')),
			(r"'", String, ('#pop', 'interp-string-s')),
		],
		'interp-string-c': [
			(r'[^\'"\$]+', String),
			(r'\${[^}]+}', String.Interpol),
			(r'\$\([^)]+\)', String.Interpol),
			(r'\$', String),
			(r'[\'"]', String),
		],
		'interp-string-d': [
			(r'"', String, '#pop'),
			include('interp-string-c'),
		],
		'interp-string-s': [
			(r"'", String, '#pop'),
			include('interp-string-c'),
		],
		'value': [
			include('string'),
			(r'[\w:\.-]+', String, '#pop'),
			(r'\*', Literal, '#pop'),
			(r'\$[\w:-]+', Name.Attribute, '#pop'),
			(r'\${[\w:-]+}', Name.Attribute, '#pop'),
		],
		'comment': [
			(r'\s+', Text),
			(r'#.*\n', Comment),
		],
	}
