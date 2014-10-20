from cssselect.xpath import HTMLTranslator
from lxml import etree
from pyquery import PyQuery
import os

__doc__ = """convenience wrapper around pyquery"""

# from wrappers.pq import PQ
def PQ(*args, **kw):
	"""wrapper for PyQuery to support mixed-case tag names"""
	if len(args) and isinstance(args[0], str) and os.path.isfile(args[0]):
		kw['filename'] = args[0]
		args = args[1:]
	dom = PyQuery(*args, css_translator=HTMLTranslator(xhtml=True), **kw)
	if 'keepns' in kw and kw['keepns']:
		return dom
	return dom.remove_namespaces()
