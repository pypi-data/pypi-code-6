# -*- coding: utf-8 -*-
#    Asymmetric Base Framework :: Jinja utils
#    Copyright (C) 2013-2014 Asymmetric Ventures Inc.
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
from __future__ import absolute_import, division, print_function, unicode_literals

import datetime
from decimal import Decimal
from django.utils import html as django_html_utils
from markupsafe import Markup
import unittest


class Test(unittest.TestCase):
	
	def _get_env(self):
		try:
			from django.apps import apps
			env = apps.get_app_config('asymm-jinja').get_env()
		except ImportError:
			from asymm_jinja.app_config import jinja_app
			env = jinja_app.get_env()
		return env
	
	def assertJinjaHtml(self, jinja, html, **kwargs):
		env = self._get_env()
		t = env.from_string(jinja)
		self.assertEqual(html, t.render(**kwargs))
	
	def test_getenv(self):
		self._get_env()
	
	def test_csrf_token(self):
		jinja = '{% csrf_token %}'
		html = '<input type="hidden" name="csrfmiddlewaretoken" value="VALUE" />'
		self.assertJinjaHtml(jinja, html, csrf_token = "VALUE")
	
	def test_cond_escape(self):
		m = Markup("&")
		
		self.assertEqual(django_html_utils.conditional_escape(m), "&")
		self.assertEqual(django_html_utils.conditional_escape("&"), "&amp;")
	
	def test_date_filter(self):
		jinja = '{{ d|date }}'
		html = '01/Feb/03 04:05AM'
		d = datetime.datetime(2003, 02, 01, 04, 05)
		self.assertJinjaHtml(jinja, html, d = d)
	
	def test_fmt_filter(self):
		jinja = '{{ t|fmt(1,2,3) }}'
		html = '2,1,3'
		t = '{1},{0},{2}'
		self.assertJinjaHtml(jinja, html, t = t)
	
	def test_current_filter(self):
		jinja = '{{ c|currency }}'
		html = '$1,234.57'
		c = Decimal('1234.567')
		self.assertJinjaHtml(jinja, html, c = c)
		
		c = float(1234.567)
		self.assertJinjaHtml(jinja, html, c = c)
		
		html = '$12,345.00'
		c = int(12345)
		self.assertJinjaHtml(jinja, html, c = c)
	
	def test_filter_filter(self):
		jinja = '{{ l|filter }}'
		html = '[1, 2, 3]'
		l = [None, 1, 2, None, 3, None]
		self.assertJinjaHtml(jinja, html, l = l)

if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
