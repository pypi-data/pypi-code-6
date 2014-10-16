#!/usr/bin/env python3
"""Unicode numbers

Allows you to convert decimal, octal, hexadecimal, and binary numbers; Unicode character and block names; and HTML/XHTML character entity names and numbers into one another.

Reimplementation of the original unum Perl utility by Gisle Aas (https://www.fourmilab.ch/webtools/unum/).
"""

__version__ = '1.1'


import sys
import re
from collections import namedtuple
try:
	from unicodedata2 import category, name as unicode_name
except ImportError:
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