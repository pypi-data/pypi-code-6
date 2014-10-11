

import os, sys, time
from urllib2 import urlopen, URLError, HTTPError
from bs4 import BeautifulSoup
import bdt.dl8chan

def b8():
	#
	reload(sys)
	sys.setdefaultencoding("utf-8")
	#
	thread_link=raw_input("Please enter the url for the thread you wish to archive:")
	bdt.dl8chan.thread_dl(thread_link, os.getcwd(), "thread")
