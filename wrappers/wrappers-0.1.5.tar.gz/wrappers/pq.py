from cssselect.xpath import HTMLTranslator
from lxml import etree
from pyquery import PyQuery

__doc__ = """convenience wrapper around pyquery"""

def PQ(*args, **kw):
	"""wrapper for PyQuery to support mixed-case tag names"""
	return PyQuery(*args, css_translator=HTMLTranslator(xhtml=True), **kw)
