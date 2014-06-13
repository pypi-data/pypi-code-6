


from os import path
import sys
import unittest

from test_utils import get_content , PRESETS_DIR
from tz import TZ , Article

import httpretty

class TestArticleAuthor(unittest.TestCase):
	
	def setUp(self):
		httpretty.HTTPretty.enable()
		httpretty.register_uri(httpretty.HTTPretty.GET,'http://thezine.biz/issue-4/bubble',body=get_content('article.html'))

		self.contact = Article.fromLink('issue-4/bubble').author.contact
	
	def test_author_contacts_fields(self):
		"""
			Testing article author
		"""
		self.assertEqual(self.contact.email,'charviaggarwal97@gmail.com')
		self.assertEqual(self.contact.facebook,'https://www.facebook.com/charvi.aggarwal')
		self.assertEqual(self.contact.twitter,'')
		self.assertEqual(self.contact.link,'')
	
	def tearDown(self):
		httpretty.HTTPretty.disable()
	

if __name__ == '__main__':
	unittest.main()
