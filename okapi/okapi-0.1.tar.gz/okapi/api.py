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
	Make sure to discuss the schema.
	Make neccessary adjustments to make best schema
	Have a base schema in place. Could definitely add/remove as neccessary
"""

# database connection
# already created in this case or can create one like following line
#client = create_client('localhost',27017)

# database name 
db = client.okapi

"""
TODO:
	Depends on how we want to calculate the time to
	receieve the request form Home Depots API.
	There are several choices. 
	Time.time, Time.clock, and a class from request called elapsed
	I have a test file that makes it seem that time.clock is fastest but is it most accurate?!?
	I have used time.clock for now
"""

# calls requests of request library while storing info about api call into mongo db
def request(method, url, project_name, **kwargs):

	start = time.clock()
	res = requests.request(method, url, **kwargs)
	end = time.clock()

	collection = db.project_name
	
	data = {'time':(end-start),
			'project_name':project_name,
			'status_code':res.status_code,
			'url':res.url,
			'request_method':method
	}

	datas = db.datas
	data_id = datas.insert(data)

	return res

# calls get method of request library while storing info about api call into mongo db
def get(url, project_name,  **kwargs):

	start = time.clock()
	res = requests.get(url, **kwargs)
	end = time.clock()

	collection = db.project_name

	data = {'time':(end-start),
		   	'project_name':project_name,
		   	'status_code':res.status_code,
		   	'url':res.url,
		   	'request_method':'GET'
	}

	datas = db.datas
	data_id = datas.insert(data)

	return res

# calls delete method of request library while storing info about api call into mongo db
def delete(url, project_name, **kwargs):

	start = time.clock()
	res = requests.delete(url, **kwargs)
	end = time.clock()

	collection = db.project_name

	data = {'time':(end-start),
		   	'project_name':project_name,
		   	'status_code':res.status_code,
		   	'url':res.url,
		   	'request_method':'DELETE'
	}

	datas = db.datas
	data_id = datas.insert(data)

	return res

# calls post method of request library while storing info about api call into mongo db
def post(url, project_name, **kwargs):

	start = time.clock()
	res = requests.post(url, **kwargs)
	end = time.clock()

	collection = db.project_name

	data = {'time':(end-start),
		   	'project_name':project_name,
		   	'status_code':res.status_code,
		   	'url':res.url,
		   	'request_method':'POST'
	}

	datas = db.datas
	data_id = datas.insert(data)

	return res

# calls put method of request library while storing info about api call into mongo db
def put(url, project_name, **kwargs):

	start = time.clock()
	res = requests.put(url, **kwargs)
	end = time.clock()

	db = okapi
	collection = db.project_name

	data = {'time':(end-start),
		   	'project_name':project_name,
		   	'status_code':res.status_code,
		   	'url':res.url,
		   	'request_method':'PUT'
	}

	datas = db.datas
	data_id = datas.insert(data)

	return res
