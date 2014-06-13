


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

		self.author = Article.fromLink('issue-4/bubble').author
	
	def test_article_author_fields(self):
		"""
			Testing article author
		"""
		self.assertEqual(self.author.id,'charvi-aggarwal')
		self.assertEqual(self.author.name,'Charvi Aggarwal')
		self.assertEqual(self.author.image,'https://s3.amazonaws.com/mixture-mixed/2967/5505/assets/img/authors/charvi.png')
	
	def tearDown(self):
		httpretty.HTTPretty.disable()
	

if __name__ == '__main__':
	unittest.main()
