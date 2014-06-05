# Experimental File

import argparse
import os, json
from elasticsearch import Elasticsearch
import uuid
from utils.querying import query
from utils.indexing import indexDoc

def main():
	parser = argparse.ArgumentParser()
	es = Elasticsearch()

	# Currently only optional argument support (later add optional arguments using subparsers)
	parser.add_argument("-f", "--filename", help="you want to index a new file")
	parser.add_argument("-st", "--searchtags", help="search for a file based on tags", action="store_true")
	parser.add_argument("-sd", "--searchdescription", help="search for a file based on its description", action="store_true")
	parser.add_argument("-sn", "--searchname", help="search for a file based on its name", action="store_true")

	args = parser.parse_args()

	if args.filename:
		name = args.filename

		if os.path.isfile(name) == False:
			print 'Needed a file'
			return

		tags = (raw_input("Tags [separated by a space]: ")).split(' ')
		desc = (raw_input("Description [short description]: "))
		path = os.getcwd() + '/' + args.filename

		doc = {
			"file": name,
			"path": path,
			"tags": tags,
			"description": desc
		}

		unique_id = str(uuid.uuid4())
		indexDoc(es, 'tagz', 'files', unique_id, doc)

	if args.searchtags:
		query(es, 'tags')

	if args.searchdescription:
		query(es, 'description')

	if args.searchname:
		query(es, 'name')


if __name__ == '__main__':
	main()
