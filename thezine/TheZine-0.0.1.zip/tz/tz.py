
#!/usr/bin/env python

"""
The Zine API
Unofficial Python API for The Zine

@author Abhijeet Mohan
@email void.aby@gmail.com
"""


import requests
from bs4 import BeautifulSoup

from constants import BASE_URL, INTERVAL_BETWEEN_REQUESTS
from utils import get_soup , get_article_soup



class TZ(object):
    """
    The class that parses the TZ page, and builds up all articles
    """
	
	
    def __init__(self):
        pass
		
    def get_articles(self, issue=''):
        """
			Yields a list of articles from the given issue.
        """	
		
		
	soup = get_soup() # get soup of all articles 
	issues = soup.find_all('ul')
		
	# validating and assigning default value for issue
	if not type(issue) is int or issue < 0 :
		issue = 1
	if issue > len(issues):
		issue = len(issues)		
		
	# considering latest article is last element 		
	articles = issues[len(issues)-issue].find_all('a') 
	mArticles = []
	for article in articles:
		mArticle = {}
		mArticle['link'] = article.get('href')[1:]
		mArticle['title'] = article.find('li').contents[0].strip()
		mArticle['author'] = article.find('span').contents[0].encode('utf8')
		mArticles.append(mArticle)
	return mArticles
		
		
		
class Article(object):
	"""
		Represents an article of tz
	"""
		
	def __init__(self, id, title='', tagline='', body='' , issue ='', link='' ,author = ''):
			self.id= id
			self.title = title
			self.tagline = tagline
			self.body = body
			self.issue = issue
			self.link = link
			self.author = author
			
	@classmethod
	def fromLink(self, link):
		"""
			Factory Method. Fetches article data from given link and builds the object
		"""
		soup = get_article_soup(link)
		head = soup.find_all('article',class_='')[0]
		parts = link.split('/')
		id = '%s-%s'%(parts[0],parts[-1])
		issue = parts[0].split('-')[-1]
		
		#fetching head
		title = head.find("h1").contents[0] if head.find("h1") else ''
		tagline = head.find("h2").contents[0] if head.find("h2") else ''
		
		body = '' #fetching body
		if len(soup.find_all('article',class_='main-body')) > 0:
			body = soup.find_all('article',class_='main-body')[0].find(class_='inner')
			
		author =  '' #fetching author
		if len(soup.find_all('aside')) > 0:
				aside = soup.find_all('aside')[0] if soup.find_all('aside')[0] else ''
				author = Author.from_soup(aside)
		return Article(id=id,title=title,tagline=tagline,body=body,issue=issue,link='http://thezine.biz/%s'%link,author=author)
			
	def __repr__(self):
		return '<Article : {0},{1},{2},{3}>'.format(self.id, self.title, self.link , self.author.name)		
		
		

class Author(object):
	"""
		Represents an author of tz
	"""
	
	def __init__(self, name, image, contact):
		self.id = Author._get_id(name)
		self.name= name
		self.image = image
		self.contact = contact
		
	@classmethod
	def _get_id(self,name):
		if name:
			words = name.lower().split(' ')
			return '-'.join(words)
		else :
			return ''
			
	@classmethod
	def from_soup(self,soup):
		"""
			Factory Method. Fetches author data from given soup and builds the object
		"""	
		if soup is None or soup is '':
			return None
		else:	
			author_name = soup.find('em').contents[0].strip() if soup.find('em') else ''
			author_image = soup.find('img').get('src') if soup.find('img') else ''
			author_contact = Contact.from_soup(self,soup)
			return Author(author_name,author_image,author_contact)	
		
	def __repr__(self):
		return '<Author : {0} , {1}>'.format(self.id, self.name)

class Contact(object):
	"""
		Represents different type of contact information of the author
	"""
	def __init__(self, email, facebook, twitter,link):
		self.email = email
		self.facebook = facebook
		self.twitter = twitter
		self.link = link
		
	@classmethod
	def from_soup(self,author,soup):
		"""
			Factory Method. Fetches contact data from given soup and builds the object
		"""	
		email = soup.find('span',class_='icon icon-mail').findParent('a').get('href').split(':')[-1]  if soup.find('span',class_='icon icon-mail') else ''
		facebook = soup.find('span',class_='icon icon-facebook').findParent('a').get('href') if soup.find('span',class_='icon icon-facebook') else ''
		twitter = soup.find('span',class_='icon icon-twitter-3').findParent('a').get('href') if soup.find('span',class_='icon icon-twitter-3') else ''
		link = soup.find('span',class_='icon icon-link').findParent('a').get('href') if soup.find('span',class_='icon icon-link') else ''
		return Contact(email,facebook,twitter,link)
		
	def __repr__(self):
		return '<Contact : {0} , {1} , {2} ,{3}>'.format(self.email, self.facebook,self.twitter,self.link)		
	
					
if __name__ == '__main__':
	print TZ().get_articles()
