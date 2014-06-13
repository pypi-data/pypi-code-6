

from os import path
import sys
import unittest

from test_utils import get_content , PRESETS_DIR
from tz import TZ , Article

import httpretty

class TestGetArticles(unittest.TestCase):
	
	def setUp(self):
		httpretty.HTTPretty.enable()
		httpretty.register_uri(httpretty.HTTPretty.GET,'http://thezine.biz',body=get_content('index.html'))
	
		self.tz = TZ()
		self.articles = self.tz.get_articles(1)
		self.dummy_articles = [{'author': ' \xe2\x80\x94 Meghna Gulati', 'link': u'issue-1/editorial', 'title': u'The Editorial'}, {'author': ' \xe2\x80\x94 Tanya Dutta', 'link': u'issue-1/smiles-tears', 'title': u'Of Smiles and Tears'}, {'author': ' \xe2\x80\x94 Anirban Chattopadhyaya', 'link': u'issue-1/plato', 'title': u'Plato Speak'}, {'author': ' \xe2\x80\x94 Zaid Drabu', 'link': u'issue-1/slam', 'title': u'Slam!'}, {'author': ' \xe2\x80\x94 Prakriti Anand', 'link': u'issue-1/perspective', 'title': u'Perspective'}, {'author': ' \xe2\x80\x94 Meghna Gulati', 'link': u'issue-1/possible', 'title': u'I. M. Possible'}, {'author': ' \xe2\x80\x94 Rahat Chawla', 'link': u'issue-1/review', 'title': u'The Good & the Bad'}, {'author': ' \xe2\x80\x94 Yash Sharma', 'link': u'issue-1/travel', 'title': u'Travel'}, {'author': ' \xe2\x80\x94 Kanika Rana', 'link': u'issue-1/death', 'title': u'If I Could Save Time in a Bottle'}]
	
	def test_get_articles_constructor(self):
		"""
			Testing returned articles
		"""
		for i in range(0,len(self.articles)):
			self.assertEqual(self.articles[i]['author'],self.dummy_articles[i]['author'])
	
	def tearDown(self):
		httpretty.HTTPretty.disable()
	

if __name__ == '__main__':
	unittest.main()
