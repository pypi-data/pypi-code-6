import xapian
import json
from os.path import expanduser

def printResults(listResults):
	if len(listResults):
		print '\nResults are: \n--------------------------------------------\n'

	for i in range(0, len(listResults)):
		ob = (listResults[i])

		print '*  File Name: ' + str(ob['filename'])
		print '*  Description: ' + str(ob['description'])
		print '*  File Path: ' + str(ob['filepath'])
		print '*  File Tags: ' + str(ob['tags'])
		
		if i != len(listResults)-1:
			print '\n'


def search(querystring):
	db_path = expanduser('~') + '/.ktagz_db'

	# Open the database we're going to search and set up the querystring.
	db = xapian.Database(db_path)


	# Set up a QueryParser with a stemmer
	queryparser = xapian.QueryParser()
	queryparser.set_stemmer(xapian.Stem('en'))
	queryparser.set_stemming_strategy(queryparser.STEM_SOME)
	queryparser.add_prefix("description", 'S')
	queryparser.add_prefix('tags', 'XD')
	queryparser.add_prefix('filename', 'XO')


	# Parse the query
	query = queryparser.parse_query(querystring)


	# Use an Enquire object on the database to run the query
	enquire = xapian.Enquire(db)
	enquire.set_query(query)	


	# And print out something about the matches
	matches = []
	for match in enquire.get_mset(0, 100):
		fields = json.loads(match.document.get_data())
		matches.append(fields)

	printResults(matches)


if __name__ == '__main__':
	querystring = 'tags:github python'
	search(querystring)
