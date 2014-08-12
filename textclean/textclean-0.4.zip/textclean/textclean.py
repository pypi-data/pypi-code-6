import re
import imp
import HTMLParser
class textclean:
	def __init__(self):
		return None

	def clean(self,text):
		a = imp.find_module('textclean')
		fil = a[1]+'\\lookup.txt'
	 	lookup = open(fil).read().split('\n')
	 	text = HTMLParser.HTMLParser().unescape(text)
	 	for line in lookup:
	 		lin = line.split('|')
	 		text = re.sub(lin[2],lin[4],text)
	 	cleaned_text = text
	 	# cleaned_text = cleaned_text.decode('utf-8')
	 	cleaned_text = cleaned_text.encode('utf-8').decode('ascii', 'ignore')
	 	return cleaned_text.strip()

textclean = textclean()