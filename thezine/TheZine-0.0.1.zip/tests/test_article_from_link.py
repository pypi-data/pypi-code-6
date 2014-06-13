

from os import path
import sys
import unittest

from test_utils import get_content , PRESETS_DIR
from tz import TZ , Article

import httpretty

class TestArticleFromLink(unittest.TestCase):
	
	def setUp(self):
		httpretty.HTTPretty.enable()
		httpretty.register_uri(httpretty.HTTPretty.GET,'http://thezine.biz/issue-4/bubble',body=get_content('article.html'))
	
		self.article = Article.fromLink('issue-4/bubble')
	
	def test_article_from_link_constructor(self):
		"""
			Testing article factory method
		"""
		self.assertEqual(self.article.id,'issue-4-bubble')
		self.assertEqual(self.article.title,'Just Bubble Stuff.')
		self.assertEqual(self.article.tagline,'On Economics.')
		self.assertEqual(self.article.issue,'4')
		self.assertEqual(self.article.link,'http://thezine.biz/issue-4/bubble')
	
	def tearDown(self):
		httpretty.HTTPretty.disable()
	

if __name__ == '__main__':
	unittest.main()
