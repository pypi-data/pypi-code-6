import argparse, json

from os.path import abspath
from os.path import isfile
from os.path import isdir
from os import walk
from indexer import index
from query import search

def checkValidity(name, _type):
	if _type == 'file':
		if isfile(name) == False:
			print 'Please give a file to index and nothing else !!'
			return (None, None)

	elif type == 'dir':
		if isdir(name) == False:
			print 'Please give a directory to index recursively and nothing else !!'
			return (None, None)

	try:
		tags = raw_input("Tags [separated by a space]: ")
		desc = raw_input("Description [short description]: ")
	except KeyboardInterrupt:
		print '\nExiting Gracefully...'
		return (None, None)

	return (tags, desc)
	

def main():
	parser = argparse.ArgumentParser()

	# Currently only optional argument support (later add optional arguments using subparsers)
	parser.add_argument("-f", "--filename", help="you want to index a new file.")
	parser.add_argument("-d", "--dirname", help="recursively add a tag and description to each file in directory.")
	parser.add_argument("-st", "--searchtags", help="search for a file based on tags", action="store_true")
	parser.add_argument("-sd", "--searchdescription", help="search for a file based on its description", action="store_true")
	parser.add_argument("-sn", "--searchname", help="search for a file based on its name", action="store_true")
	args = parser.parse_args()


	# if a file name is provided then index this file
	if args.filename:
		name = args.filename
		tags, desc = checkValidity(name, 'file')

		if (tags, desc) == (None, None):
			return

		doc = {
			'filename': abspath(name),
			'filepath': path,
			'tags': tags,
			'description': desc
		}
		index (doc)

	# if a directory is provided then recursively walk the directory
	if args.dirname:
		dirname = args.dirname
		tags, desc = checkValidity(dirname, 'dir')

		if (tags, desc) == (None, None):
			return

		for root, dir, files in walk(abspath(dirname)):
			for name in files:
				print 'Now indexing file: ', root + '/' + name
				doc = {
					'filename': name,
					'filepath': root + '/' + name,
					'tags': tags,
					'description': desc
				}

				index(doc)


	# if search on tags requested
	if args.searchtags:
		try:
			tags = raw_input('tags to be searched [space separated]: ')
		except KeyboardInterrupt:
			print '\nExiting Gracefully...'
			return

		search('tags:' + tags)


	# if search on description requested
	if args.searchdescription:
		try:
			desc = raw_input('rough description of file: ')
		except KeyboardInterrupt:
			print '\nExiting Gracefully...'
			return

		search('description:' + desc)


	# if search on name requested
	if args.searchname:
		try:
			name = raw_input('filename to be searched: ')
		except KeyboardInterrupt:
			print '\nExiting Gracefully...'
			return

		search('filename:' + name)


if __name__ == '__main__':
	main()
