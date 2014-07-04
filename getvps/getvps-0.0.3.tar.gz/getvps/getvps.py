import requests
import sys
import time
import random
import re

class Query:
	def __init__(self, sleepTime=30, trycount=1):
		randVal = random.randint(0, 10000)
		user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.' + str(randVal)  +  '.52 Safari/537.36'

		url = 'https://noupload.com/'
		sess = requests.session()
		sess.headers.update({'User-Agent' : user_agent})
		
		r = sess.get(url)
		#print "Cookies"
		#print r.cookies
		#print "---------------------------------------------"
		#print r.text
		
		#print "============================================="
		
		time.sleep(5)

		# Check
		if 'PHPSESSID' not in r.cookies:
			# Error
			print 'Not Found Cookie["PHPSESSID"]'
			sys.exit()
		
		
		# Start
		url = 'https://noupload.com/create'
		
		params = {}
		cookie = {'PHPSESSID' : r.cookies['PHPSESSID']}
		sess.headers.update({'referer': 'https://noupload.com/'})
		sess.headers.update({'X-Requested-With': 'XMLHttpRequest'})
		#sess.headers.update({'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; rv:30.0) Gecko/20100101 Firefox/30.0'})
		sess.headers.update({'User-Agent' : user_agent})
	
		
		r2 = sess.post(url, cookies=cookie)
		
		
		#print r2.cookies
		#print "---------------------------------------------"
		#print r2.text
		#print "============================================="
		
		time.sleep(sleepTime)
		
		url = 'https://noupload.com/'
		
		cookie = {'PHPSESSID' : r.cookies['PHPSESSID'] }
		sess.headers.update({'User-Agent' : user_agent})
		#sess.headers.update({'referer': 'https://noupload.com/create'})
		r3 = sess.get(url, cookies=cookie)
		
		#print "---------------------------------------------"
		#print r3.cookies
		#print "============================================="
		#print r3.text

		# Parse
		rtrnParams = {}
		regex = re.compile('<h3>IP: <span class="label label-info">.+?</span></h3>')
		match = regex.search(r3.text)
		if match:
			ipPassStr = match.group()
			#print ipPassStr
			regex = re.compile('\d+?\.\d+?\.\d+?\.\d+')
			match = regex.search( ipPassStr ) 
			if match:
				#print "IP=OK"
				rtrnParams['ipAddr'] = match.group()
				#print rtrnParams['ipAddr']
			else:
				print "IP=NO"

			regex = re.compile('Username: <span class="label label-info">.+?</span>')
			match = regex.search( ipPassStr )
			if match:
				#print "UserName=OK"
				userName = match.group()
				#print userName
				userName = userName[41:]
				#userName = userName.strip('Username: <span class="label label-info">')
				userName = userName.strip('</span>')
				rtrnParams['userName'] = userName
				#print rtrnParams['userName']
			else:
				print "UserName=NO"

			regex = re.compile('Password: <span class="label label-info">.+?</span></h3>')
			match = regex.search( ipPassStr )
			if match:
				#print "Pass=OK"
				pswd = match.group()
				pswd = pswd[41:]
				pswd = pswd.strip('</span></h3>')
				rtrnParams['password'] = pswd
				#print rtrnParams['password']

			else:
				print "Pass=NO"

		else:
			print "Not Match!"
			
		
		#print rtrnParams
		self.params = rtrnParams
	
	def getData(self):
		return self.params
