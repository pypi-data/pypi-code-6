def duplicate(es, idx, otype, doc):
	path = doc['path']

	doc = {
		"query" : {
			"filtered" : { 
				"query" : {
					"match_all" : {} 
				},
				"filter" : {
					"term" : { 
						"path": path
					}
				}
			}
		}
	}

	res = es.search(index='tagz', doc_type='files', body=doc)
	lst = (res['hits'])['hits']

	if len(lst):
		return (True, (lst[0])['_id'])

	return False


def indexDoc(es, idx, otype, oid, doc):
	try:
		ret = duplicate(es, idx, otype, doc)

		if ret == False:
			res = es.index(index=idx, doc_type=otype, id=oid, body=doc)
			print 'Okay!! Indexed'

		else:
			resp = raw_input('This file is already indexed. Do you want to use the recent tags/description for this file. ? (y/n): ')

			if resp == 'y':
				res = es.index(index=idx, doc_type=otype, id=ret[1], body=doc)
				print 'Okay!! Indexed'

			else:
				return

	except:
		print 'Encountered error while indexing. Is ElasticSearch instance running ??'