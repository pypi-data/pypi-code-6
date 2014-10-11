#!/usr/bin/env python3
"""ucnum argument...

The ucnum program is a command line utility which allows you to convert decimal, octal, hexadecimal, and binary numbers; Unicode character and block names; and HTML/XHTML character entity names and numbers into one another. It can be used as an on-line special character reference for Web authors.

This version is a (blind) reimplementation of the original unum Perl utility by Gisle Aas (https://www.fourmilab.ch/webtools/unum/) in Python. It was written because it will stay up-to-date via Python’s own unicodedata updates. It has a few minor discrepancies:

1. The octal syntax 077 is not accepted: Use 0o77 instead.
2. Character information tables also contain the unicode block.
3. The regular expression flavour is Python’s.
4. The HTML escapes argument form is not accepted yet (see “TODO”).
5. Name aliases (e.g. for control characters) are not supported yet.

Arguments
=========

The command line may contain any number of the following forms of I<argument>:

123

	Decimal number.

0o371

	Octal number preceded by “0o”.

0x1D351

	Hexadecimal number preceded by “0x”. Letters may be upper or
	lower case, but the “x” must be lower case.

0b110101

	Binary number.

b=block

	Unicode character blocks matching block are listed.
	The block specification may be a regular expression.
	For example, “b=greek” lists all Greek character blocks
	in Unicode.

c=char...

	The Unicode character codes for the characters “char...” are printed.
	If the first character is not a decimal digit and the second not an
	equal sign, the “c=” may be omitted.

h=entity

	List all HTML/XHTML character entities matching entity, which may
	be a regular expression. Matching is case-insensitive, so
	“h=alpha” finds both “&Alpha;” and “&alpha;”.

l=block

	List all Unicode blocks matching block and all characters
	within each block; “l=goth” lists the Gothic block
	and the 32 characters it contains.

n=name

	List all Unicode character whose names match name, which may be
	a regular expression. For example, “n=telephone” finds the five
	Unicode characters for telephone symbols.

TODO
====

The following argument form is not yet accepted:

'&#number;&#xhexnum;...'

	List the characters corresponding to the specified HTML/XHTML
	character entities, which may be given in either decimal or
	hexadecimal. Note that the “x” in XHTML entities must be lower case.
	On most Unix-like operating systems, you'll need to quote the argument
	so the ampersand, octothorpe, and semicolon aren't interpreted by the
	shell.

Output
======

For number or character arguments, the value(s) are listed in all of the input formats, save binary.

	Octal  Decimal   Hex   HTML  Character        Block  Unicode
	 0o46       38  0x26  &amp;          &  Basic Latin  AMPERSAND


If the terminal font cannot display the character being listed, the “Character” field will contain whatever default is shown in such circumstances. Control characters are shown as a Python hexadecimal escape.

Unicode blocks are listed as follows:

	  Start         End  Unicode Block
	 0x2460  -   0x24ff  Enclosed Alphanumerics
	0x1d400  -  0x1d7ff  Mathematical Alphanumeric Symbols
	0x1f100  -  0x1f1ff  Enclosed Alphanumeric Supplement
"""

__version__ = '1.0'


import sys
import re
from collections import namedtuple
from unicodedata import category, name as unicode_name
from html.entities import codepoint2name

from unicodeblocks import blocks, blockof

Info = namedtuple('Info', 'cp char html block name')
CHAR_HEADERS = 'Octal Decimal Hex HTML Character Block Unicode'.split()
BLOCK_HEADERS = ['Start', '', 'End', 'Unicode Block']

def asciitable(lol, header=None, aligns=None, pad='  '):
	maxs = [len(h) for h in header] if header else [0] * len(lol[0])
	if aligns is None:
		aligns = ['>'] * len(maxs)
		aligns[-1] = '<'
	
	for row in lol:
		maxs = [max(m, len(str(row[i]))) for i, m in enumerate(maxs)]
	
	fmt = pad.join(('{{:{align}{max}}}'.format(max=m, align=a) for m, a in zip(maxs, aligns)))
	
	if header:
		yield fmt.format(*header)
	
	for row in lol:
		yield fmt.format(*row)

def print_char_table(chars):
	infos = [infoline(ord(char)) for char in chars]
	for row in asciitable(infos, CHAR_HEADERS):
		print(row)

def print_block_table(filtered_blocks):
	rows = [(hex(block.start), '-', hex(block.end), block.name) for block in filtered_blocks]
	for row in asciitable(rows, BLOCK_HEADERS):
		print(row)

def get_info(cp):
	char = chr(cp)
	name = unicode_name(char, '')
	block = blockof(char)
	
	html_name = codepoint2name.get(cp)
	if html_name is not None:
		html = '&{};'.format(html_name)
	else:
		html = '&#{:x};'.format(cp)
	
	return Info(cp, char, html, block, name)

def infoline(cp):
	i = get_info(cp)
	char = i.char.encode('unicode_escape').decode() if category(i.char).startswith('C') else i.char
	return [oct(i.cp), i.cp, hex(i.cp), i.html, char, i.block.name, i.name]


### parsing


def find_blocks(block_pattern):
	return [block for block in blocks.values() if block_pattern.search(block.name)]


def block_parse(block_pattern):
	print_block_table(find_blocks(block_pattern))

def list_block_parse(block_pattern):
	for block in find_blocks(block_pattern):
		print_block_table([block])
		print_char_table(list(block))

def entity_parse(entity_pattern):
	chars = [chr(cp) for cp, name in codepoint2name.items() if entity_pattern.search(name)]
	print_char_table(chars)

def name_parse(name_pattern):
	print_char_table([chr(cp) for cp in range(sys.maxunicode + 1) if name_pattern.search(unicode_name(chr(cp), ''))])


def main(arg):
	try:
		cp = int(arg, 0)
		print_char_table([chr(cp)])
		return
	except ValueError:
		pass
	
	parsers = dict(b=block_parse, l=list_block_parse, h=entity_parse, n=name_parse)
	if arg[1] == '=':
		mode = arg[0]
		if mode in parsers:
			pat = re.compile(arg[2:], re.I)
			parsers[mode](pat)
			return
		elif mode == 'c':
			print_char_table(arg[2:])
			return
	
	print_char_table(arg)

if __name__ == '__main__':
	if len(sys.argv) < 2 or sys.argv[1] in {'-h', '--help'}:
		print(__doc__)
		sys.exit(0)
	
	for arg in sys.argv[1:]:
		main(arg)