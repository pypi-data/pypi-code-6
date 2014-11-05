from __future__ import print_function, with_statement
import sys
from cStringIO import StringIO
import struct
import functools

import jaraco.windows.clipboard as wclip

from lpaste.source import Source

def get_image():
	try:
		import Image
	except ImportError:
		print("PIL not available - image pasting disabled", file=sys.stderr)
		raise
	with wclip.context():
		result = wclip.GetClipboardData(wclip.CF_DIB)
	# construct a header (see http://en.wikipedia.org/wiki/BMP_file_format)
	offset = 54 # 14 byte BMP header + 40 byte DIB header
	header = 'BM'+struct.pack('<LLL', len(result), 0, offset)
	img_stream = StringIO(header+result)
	img = Image.open(img_stream)
	out_stream = StringIO()
	img.save(out_stream, format='jpeg')
	out_stream.seek(0)
	return out_stream, 'image/jpeg', 'image.jpeg'

def try_until_no_exception(*functions):
	for f in functions:
		exceptions = getattr(f, 'exceptions', [])
		try:
			return f()
		except exceptions:
			pass
	raise RuntimeError("No function succeeded")

def do_image():
	return Source.from_stream(*get_image())
def do_html():
	snippet = wclip.get_html()
	return Source.from_stream(StringIO(snippet.html), 'text/html',
		'snippet.html')
def do_text():
	code = wclip.get_unicode_text()
	src = Source(code=code)
	try:
		# see if the code can compile as Python
		compile(code, 'pasted_code.py', 'exec')
		src.format = 'python'
	except:
		pass # use default format
	return src

def get_source():
	"""
	Return lpaste.Source for the content on the clipboard
	"""
	# try getting an image or html over just text
	do_image.exceptions = (TypeError, ImportError)
	do_html.exceptions = (TypeError,)
	return try_until_no_exception(do_image, do_html, do_text)

set_text = wclip.set_text
