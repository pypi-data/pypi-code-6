import json

def printResults(listResults, what):
	if len(listResults):
		print '\nResults on ' + what + ' are: \n--------------------------------------------\n'

	for i in range(0, len(listResults)):
		ob = (listResults[i])['_source']

		print '*  File Name: ' + str(ob['file'])
		print '*  Description: ' + str(ob['description'])
		print '*  File Path: ' + str(ob['path'])
		print '*  File Tags: ' + str(ob['tags'])
		
		if i != len(listResults)-1:
			print '\n'		


def query(es, what):

	if what == 'tags':
		tags = raw_input("Enter tags to be searched [space separated]: ")
		doc = {
			"query": {
				"query_string": {
					"query": tags,
					"fields": ["tags"]
				}
			}
		}

		res = es.search(index='tagz', doc_type='files', body=doc)
		lst = (res['hits'])['hits']

		printResults(lst, what)

	elif what == 'name':
		name = raw_input("File name to be searched [with extension]: ")
		doc = {
			"query": {
				"query_string": {
					"query": name,
					"fields": ["file"]
				}
			}
		}

		res = es.search(index='tagz', doc_type='files', body=doc)
		lst = (res['hits'])['hits']

		printResults(lst, what)

	elif what == 'description':
		desc = raw_input("Rough description to be searched : ")
		doc = {
			"query": {
				"query_string": {
					"query": desc,
					"fields": ["description"]
				}
			}
		}

		res = es.search(index='tagz', doc_type='files', body=doc)
		lst = (res['hits'])['hits']

		printResults(lst, what)		
