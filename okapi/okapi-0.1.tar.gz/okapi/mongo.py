"""
okapi.mongo
~~~~~~~~~
Creates a mongo client (as of right now)
"""

# necessary libraries and modules for this script
import requests
import pymongo

from pymongo import MongoClient 

client = MongoClient()

# allows user to set the host and port to create MongoClient
def create_client(host, port):
	client = MongoClient(host,port)	
	return client