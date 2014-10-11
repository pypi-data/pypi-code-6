#! /usr/bin/env python
# -*- coding: utf-8 -*-

#8chan thread archiver
#By Daniel Tadeuszow
#2014-10-10
#License: AGPL3+

import os, sys, time
from urllib2 import urlopen, URLError, HTTPError
from bs4 import BeautifulSoup

#most of the dlfile function written by by dcolish
#http://stackoverflow.com/questions/4028697/how-do-i-download-a-zip-file-in-python-using-urllib2

#'setdefaultencoding' trick by drstrangelove with cosmetic edits by Eric Fortin
#As used in my if __name__ == main
#This resolves some encoding errors encountered by beautiful soup


def dlfile(url, path, filename, skip_if_exists=False):
	#Prepare the path
	if not os.path.exists(path):
		os.makedirs(path)
	
	# Open our local file for writing
	#with open(os.path.basename(url), "wb") as local_file:
	
	#Parse local filename
	if filename==None:
		filename=os.path.basename(url)
	#filepath=os.path.join(path, filename + os.path.splitext(url)[1])
	filepath=os.path.join(path, filename)
	
	#Skip downloading if the file exists
	if skip_if_exists and os.path.isfile(filepath):
		#print "file exists"
		return
	
	#print filepath
	
	# Open the url
	try:
		f = urlopen(url)
		#print "downloading " + url
		
		#Create a temporary version, so that when we save the file to disk we have no risk of a partially downloaded file
		#TODO: Consider not doing this for webms, since they may be of a much larger size than images
		temp_storage=f.read()
		
		#Save the file to disk
		with open(filepath, "wb") as local_file:
			local_file.write(temp_storage)
	
	#handle errors ()
	except HTTPError, e:
			print "HTTP Error:", e.code, url
	except URLError, e:
			print "URL Error:", e.reason, url


def thread_dl(url, path_pre, filename):
	#Download the page
	try:
		#Download the webpage and parse it nicely
		#dl_page= urlopen(url, "page.html")
		dl_page= urlopen(url)
		#Check for redirect
		
		#IMPORTANT
		
		page_contents= dl_page.read()
		#print "page fetched"
	#If it fails though, then skip the rest of the chapter(s)
	except:
		print "The site appears to be down, oh well!"
		
		#Quit the function early, but not the whole script
		return
	
	#Prepare the soup
	thread_soup= BeautifulSoup(page_contents)
	
	#Parse the thread ID
	thread_id=os.path.basename(url).replace('.html', '')
	
	#TODO: Make board parsing *not* bullshit
	board=os.path.split(os.path.split(os.path.split(url)[0])[0])[1]
	
	
	#And change the path so that all data for this thread will be saved in a subdirectory matching the board and thread id
	path= path_pre+'/'+board+'/'+thread_id
	
	
	#Prepare the path
	if not os.path.exists(path):
		os.makedirs(path+'/thumb')
	
	#Dirty, but makes sure the directory exists
	time.sleep(2)
	
	
	#
	#Fix the javascript links
	#
	for link_node in thread_soup.find_all('script'):
		if link_node.get('src') != None:
			link_node['src']= 'https://8chan.co'+link_node.get('src')
	
	
	#
	#PARSE MEDIA LinKS
	#
	
	#TODO: replace "/v/thumb" with "thumb" in the html
	#
	thumb_list= []
	
	for link_node in thread_soup.find_all('img'):
		link= link_node.get('src')
		if link==None: continue
		elif link.find("thumb") != -1:
			link_node['href']='thumb/'+link[8+len(board):]
			link_node['src']='thumb/'+link[8+len(board):]
			thumb_list.append(link[8+len(board):])
	
	
	img_list= []
	
	#TODO: replace "/v/src/" with "" in the html because I want images to ALWAYS be in the same directory as the thread
	#^The above option should be a flag so that the babbies don't cry
	#
	#TODO: flag to use original filename instead
	#span class="postfilename" title="originaltitle.jpg"
	for link_node in thread_soup.find_all('a'):
		link= link_node.get('href')
		if link==None: continue
		elif link.find("/"+board+"/src") != -1:
			link_node['href']=link[6+len(board):]
			if link.find("player") != -1: continue
			img_list.append(link[6+len(board):])
		#HOWEVER, since post quotes are in 'a' tags as well... fix them here in the same loop
		elif link.find("/"+board+"/res") != -1:
			if link_node.get('href') != None:
				link_node['href']= 'https://8chan.co'+link_node.get('href')
	
	#
	#DOWNLOAD MEDIA
	#
	
	#dl all thumbs
	for link in thumb_list:
		#print "getting thumbnail:", link
		dlfile("https://8chan.co/"+board+"/thumb/"+link, path+"/thumb", None, skip_if_exists=True)
	
	#Download all the images
	for link in img_list:
		#print "getting image:", link
		dlfile("https://8chan.co/"+board+"/src/"+link, path, None, skip_if_exists=True)
	#
	
	
	
	with open(os.path.join(path, filename + os.path.splitext(url)[1]), "wb") as local_file:
		local_file.write(thread_soup.prettify(formatter="html"))


def dl8chan2():
	#
	reload(sys)
	sys.setdefaultencoding("utf-8")
	#
	thread_link=raw_input("Please enter the url for the thread you wish to archive:")
	thread_dl(thread_link, os.getcwd(), "thread")

