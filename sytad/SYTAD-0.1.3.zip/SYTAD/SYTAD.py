
from html.parser import HTMLParser
import urllib.request
import urllib.parse
import pafy
import sys
import re
import string
import os

# Determine the OS and set the default path and pathDelminiter accordingly
is_android = False
if sys.platform.startswith('win32'):
	pathDelimiter = '\\'
	hr = '-------------------------------------------------------------------------------'
	stdDownloadFolder = os.path.expanduser('~')+'\Downloads\SYTAD'
elif sys.platform.startswith('linux'):
	pathDelimiter = '/'
	hr = '----------------------------------------------------------------------'
	is_android = 'ANDROID_STORAGE' in os.environ
	if is_android: # Returns true if system is android
		stdDownloadFolder = os.environ['EXTERNAL_STORAGE']+'/Download/SYTAD'
	else:
		stdDownloadFolder = os.path.expanduser('~')+'/Download/SYTAD'
	
class video:
	def __init__(self, input, noPrint = False):
		self.video = pafy.new(input)
		if not noPrint: print('Loading video: '+ignoreEncodingErrors(self.video.title))
		
	def download(self, folder="", fileType="m4a", printDest = True):
		fixedTitle = sanitizeFileName(self.video.title)
		if folder == "":
			folder = stdDownloadFolder
		elif type(folder) is not str:
			raise Exception("Invalid download folder")
		if not os.path.exists(folder):
			os.makedirs(folder)
		path = folder+pathDelimiter+ignoreEncodingErrors(fixedTitle)+'.'+fileType
		path = self.recursiveNameFix(path)
		print(hr)
		if printDest: print('Destination: "'+folder+'".')
		print('Downloading: "'+ignoreEncodingErrors(self.video.title)+'".')
		self.video.getbestaudio(fileType).download(path, quiet = is_android)
		print('')
	
	def recursiveNameFix(self, path, i = 1):
		if os.path.isfile(path):
			pathParts = path.split('.')
			rule = '^([\w\s\-\_\\\(\)\:\'])*(\([0-9]*\))$'
			m = re.search(rule, ignoreEncodingErrors(pathParts[-2]))
			if m:
				i = int(m.group(2)[1:-1])+1
				pathParts[-2] = m.group(0)[:-len(m.group(2))-1]
			pathParts[-2] += ' ('+str(i)+')'
			fixedPath = ''
			for x in pathParts:
				fixedPath += '.'+x
			fixedPath = fixedPath[1:]
			return self.recursiveNameFix(fixedPath, i+1)
		return path

class multipleVideos:
	
	def __init__(self, input):
		if type(input) is list or type(input) is tuple:
			
			# public properties
			self.videoIdList = list(input)
			self.videoList = list()
			
			print(hr)
			print('Processing video information from the given list:')
			
			i = 0
			for x in input:
				self.videoList.append(video(x, noPrint = True))
				print(str(i)+': '+ignoreEncodingErrors(self.videoList[-1].video.title))
				i += 1
		else:
			raise Exception("Invalid input to class multipleVideos")
	
	def downloadAll(self, folder = stdDownloadFolder, fileType = "m4a"):
		print(hr)
		print('Starting downloads.')
		print('Destination folder: '+folder)
		for x in self.videoList:
			x.download(folder, fileType, printDest = False)
		print(hr)
		print('Download complete.')
		

class playlist(multipleVideos):
	
	def __init__(self, input):
		self.playlistInfo = YouTubePlaylistHTMLParser(input)
		self.videoList = list()
		
		print(hr)
		print('Processing video information in playlist "'+ignoreEncodingErrors(self.playlistInfo.title)+'":')
		
		i = 0
		for x in self.playlistInfo.videoIdList:
			self.videoList.append(video(x, noPrint = True))
			print(str(i)+': '+ignoreEncodingErrors(self.videoList[-1].video.title))
			i += 1
	
class YouTubePlaylistHTMLParser(HTMLParser):
	
	def __init__(self, input):
		
		# Runs the parent constructor
		HTMLParser.__init__(self)
		
		# Initialises "public" field variables
		self.title = ""
		self.id = ""
		self.videoIdList = list()
		self.videoTitleList = list()
		self.videoParserList = list()
		
		# Initialises "private" field variables
		self.nameDataImminent = False
		self.ownerDataImminent = False
		self.tempInfo = list()
		
		# Retrieves the html from the given input and feeds it to the html parser
		# The input can be either a YouTube playlist url or YouTube playlist id
		urlrule = "^(http[s]?://)www\.youtube\.([a-zA-Z]){2}([a-zA-Z])/[a-zA-Z0-9\_\-\\?\=\&]*$"
		idrule = "[a-zA-Z0-9\_]*"
		
		if re.match(urlrule, input) is not None:
			if '&app=mobile' not in input and '&app=desktop' not in input:
				input = input+'&app=desktop'
				query = urllib.parse.parse_qs(urllib.parse.urlparse(input).query)
			elif '&app=mobile' in input:
				input = input.replace('&app=mobile', '&app=desktop')
				query = urllib.parse.parse_qs(urllib.parse.urlparse(input).query)
			elif '&app=desktop' in input:
				query = urllib.parse.parse_qs(urllib.parse.urlparse(input).query)
			url = input
			self.id = query['list'][0]
		elif re.match(idrule, input) is not None:
			url = 'https://www.youtube.com/playlist?list='+input+'&app=desktop'
			self.id = input
		else :
			raise Exception("Invalid playlist url or id")
		
		
		localFilename, headers = urllib.request.urlretrieve(url)
		file = open(localFilename)
		html = file.read()
		if is_android: # I don't know why this is necessary, but it doesn't work on Android if I don't skip directly to the content
			substring = '<h1 class="pl-header-title">'
			skipToIndex = html.find(substring)
			html = html[skipToIndex:]
		self.feed(html)
	
	def handle_starttag(self, tag, attrs):
		if tag == 'tr':
			self.match = False
			for x in attrs:
				
				if x[0] == 'class' and 'pl-video' in x[1]: #check if the tr object is a match
					self.match = True
					
				if x[0] == 'data-video-id': #match id attribute and get id
					id = x[1]
					
				if x[0] == 'data-title': #match title attribute and get title
					title = x[1]
					
			if self.match:
				self.tempInfo = (id, title)
		
		if tag == "td":
			for x in attrs:
				if x[0] == 'class' and 'pl-video-owner' in x[1]: #match the owner td; if empty the file is deleted and shouldn't be included
					self.ownerDataImminent = True
					self.ownerDataEmpty = True
					
		#Check if name data is imminent
		if tag == 'h1':
			for x in attrs:
				if x[0] == 'class' and 'pl-header-title' in x[1]:
					self.nameDataImminent = True

	def handle_endtag(self, tag):
		if tag == 'tr' and self.match:
			self.videoIdList.append(self.tempInfo[0])
			self.videoTitleList.append(self.tempInfo[1])
			self.match = False
			
		# End of the name data
		if tag == 'h1' and self.nameDataImminent:
			self.nameDataImminent = False
		
		# End of the owner data
		if tag == 'td' and self.ownerDataImminent:
			self.ownerDataImminent = False
			if self.ownerDataEmpty:
				self.match = False
			
	def handle_data(self, data):
		# Save name data, if imminent
		if self.nameDataImminent:
			self.title = data.strip()
			
		if self.ownerDataImminent:
			self.ownerDataEmpty = False
			
def ignoreEncodingErrors(string, encoding = 'cp850'):
	return string.encode(encoding, 'ignore').decode(encoding, 'ignore')

def sanitizeFileName(input):
	valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
	return ''.join(c for c in input if c in valid_chars)

def openTui():
	
	print(hr)
	print('Welcome to the Android script of the Simple YouTubeAudioDownloader (SYTAD).')
	print(hr)
	
	inputType = ""
	while inputType != "p" and inputType != "v":
		print('Please indicate whether you want to download from a YouTube playlist (enter "p") or directly from a YouTube video (enter "v"):')
		inputType = input()
	
	if inputType == "p":
		print(hr)
		print('Please enter a YouTube playlist ID or URL:')
		plid = input()
		print(hr)
		v = playlist(plid)
		v.downloadAll()
		
	elif inputType == "v":
		print(hr)
		print('Please enter a YouTube video ID or URL:')
		viid = input()
		print(hr)
		v = video(viid)
		v.download()
		
	else:
		raise Exception("You somehow got past the input check without typing p or v, congratulations.")
	

def topLevel():
	args = sys.argv[1:]
	if not args:
		openTui()
	else:
		if '-p' in args or '-playlist' in args:
			if '-p' in args:
				skipIndex = args.index('-p')
			if '-playlist' in args:
				skipIndex = args.index('-playlist')
			x = skipIndex+1
			plid = args[x]
			
			p = playlist(plid)
			p.downloadAll()
			
		else:
			videos = multipleVideos(args)
			videos.downloadAll()	
	
if __name__ == "__main__":
	topLevel()
	
	
	
	
	