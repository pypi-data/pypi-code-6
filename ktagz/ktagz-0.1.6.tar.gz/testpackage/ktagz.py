import argparse
import os, json
from indexer import index
from query import search

def main():
	parser = argparse.ArgumentParser()

	# Currently only optional argument support (later add optional arguments using subparsers)
	parser.add_argument("-f", "--filename", help="you want to index a new file.")
	parser.add_argument("-st", "--searchtags", help="search for a file based on tags", action="store_true")
	parser.add_argument("-sd", "--searchdescription", help="search for a file based on its description", action="store_true")
	parser.add_argument("-sn", "--searchname", help="search for a file based on its name", action="store_true")
	args = parser.parse_args()


	# if a file name is provided then index this file
	if args.filename:
		name = args.filename
		if os.path.isfile(name) == False:
			print 'Needed a file'
			return

		tags = raw_input("Tags [separated by a space]: ")
		desc = raw_input("Description [short description]: ")
		path = os.getcwd() + '/' + args.filename

		doc = {
			"filename": name,
			"filepath": path,
			"tags": tags,
			"description": desc
		}
		index(doc)


	# if search on tags requested
	if args.searchtags:
		tags = raw_input('tags to be searched [space separated]: ')
		search('tags:' + tags)


	# if search on description requested
	if args.searchdescription:
		desc = raw_input('rough description of file: ')
		search('description:' + desc)


	# if search on name requested
	if args.searchname:
		name = raw_input('filename to be searched: ')
		search('filename:' + name)


if __name__ == '__main__':
	main()
