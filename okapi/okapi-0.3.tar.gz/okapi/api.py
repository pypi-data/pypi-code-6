"""
okapi.api
~~~~~~~~~
This module implements the Requests API while storing valuable information into mongodb.  
"""

# necessary libraries and modules for this script
import requests
import pymongo
import mongo
import time

from mongo import * 
from pymongo import MongoClient 

"""
TODO:
	Depends on how we want to calculate the time to
	receieve the request form Home Depots API.
	There are several choices. 
	Time.time, Time.clock, and a class from request called elapsed
	I have a test file that makes it seem that time.clock is fastest but is it most accurate?!?
	I have used time.clock for now
"""

class api:
	
	# initialization of class api
	def __init__(self, project_name, host, port):
		self.host = host
		self.port = port
		self.project_name = project_name

	# calls requests of request library while storing info about api call into mongo db
	def request(self, method, url, **kwargs):

		start = time.clock()
		res = requests.request(method, url, **kwargs)
		end = time.clock()

		content = ''

		if not res.ok:
			content = res.content
		
		client = MongoClient(self.host,self.port)	
		db = client.okapi
		collection = db.project_name

		data = {'time':(end-start),
				'project_name':self.project_name,
				'status_code':res.status_code,
				'url':res.url,
				'request_method':method,
				'content':content
		}

		datas = db.datas
		data_id = datas.insert(data)

		return res

	# calls get method of request library while storing info about api call into mongo db
	def get(self, url, **kwargs):

		start = time.clock()
		res = requests.get(url, **kwargs)
		end = time.clock()

		content = ''

		if not res.ok:
			content = res.content

		client = MongoClient(self.host,self.port)	
		db = client.okapi
		collection = db.project_name

		data = {'time':(end-start),
			   	'project_name':self.project_name,
			   	'status_code':res.status_code,
			   	'url':res.url,
			   	'request_method':'GET',
			   	'content':content
		}

		datas = db.datas
		data_id = datas.insert(data)

		return res

	# calls delete method of request library while storing info about api call into mongo db
	def delete(self, url, **kwargs):

		start = time.clock()
		res = requests.delete(url, **kwargs)
		end = time.clock()

		content = ''

		if not res.ok:
			content = res.content

		client = MongoClient(self.host,self.port)	
		db = client.okapi
		collection = db.project_name

		data = {'time':(end-start),
			   	'project_name':self.project_name,
			   	'status_code':res.status_code,
			   	'url':res.url,
			   	'request_method':'DELETE',
			   	'content':content
		}

		datas = db.datas
		data_id = datas.insert(data)

		return res

	# calls post method of request library while storing info about api call into mongo db
	def post(self, url, **kwargs):

		start = time.clock()
		res = requests.post(url, **kwargs)
		end = time.clock()

		content = ''

		if not res.ok:
			content = res.content

		client = MongoClient(self.host,self.port)	
		db = client.okapi
		collection = db.project_name

		data = {'time':(end-start),
			   	'project_name':self.project_name,
			   	'status_code':res.status_code,
			   	'url':res.url,
			   	'request_method':'POST',
			   	'content':content
		}

		datas = db.datas
		data_id = datas.insert(data)

		return res

	# calls put method of request library while storing info about api call into mongo db
	def put(self, url, **kwargs):

		start = time.clock()
		res = requests.put(url, **kwargs)
		end = time.clock()

		content = ''

		if not res.ok:
			content = res.content

		client = MongoClient(self.host,self.port)	
		db = client.okapi
		collection = db.project_name

		data = {'time':(end-start),
			   	'project_name':self.project_name,
			   	'status_code':res.status_code,
			   	'url':res.url,
			   	'request_method':'PUT',
			   	'content':content
		}

		datas = db.datas
		data_id = datas.insert(data)

		return res
