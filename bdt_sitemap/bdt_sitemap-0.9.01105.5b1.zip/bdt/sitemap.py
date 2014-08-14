#! /usr/bin/env python
# -*- coding: utf-8 -*-

#BDT Sitemap Generator
#By Daniel Tadeuszow
#2014-08-13
#License: AGPL3+


import os, sys, datetime
from urllib2 import urlopen, URLError, HTTPError
from urllib import pathname2url
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET


emod_time=datetime.date(1990,01,01)

#Reinitialize emod_time, when working in a new directory
def init_emod_time():
	global emod_time
	emod_time=datetime.date(1990,01,01)
	

#Compare modified time to emod_time,
#if it is more recent, then set it as emod_time
def compare_emod_time(newtime):
	global emod_time
	if emod_time<newtime:
		emod_time=newtime
	

def create_sitemap(domain, site_dir, ignorelist=[]):
	
	global emod_time
	
	#This is a template sitemap.xml file
	sitemap_index= "<sitemapindex xmlns='http://www.sitemaps.org/schemas/sitemap/0.9'></sitemapindex>"
		
	#This is a template sitemap for each page and directory
	empty_record= "<sitemap><loc></loc><lastmod></lastmod></sitemap>"
	
	#Use Python's handy 'os.walk' function to traverse the entire website
	for root, dirs, files in os.walk(os.path.abspath(site_dir), topdown=False):
		
		#initialize skip flags
		skipdir=False
		
		#If current path contains an ignored term,
		for term in ignorelist:
			if term in root.replace(site_dir, ""):
				
				#Set the 'skipdir' flag
				skipdir=True
				break
				
		#If the flag was triggered, skip this directory
		if skipdir: break
		
		
		
		#Otherwise, continue
		#Announce current dir
		#print "Mapping: " + root
		#TODO: Verbose flag
		
		#Create a new XML object from the template above
		sitemap_index_element=ET.fromstring(sitemap_index)
		
		#Reinitialize directory emod_time
		init_emod_time()
		
		#For every file,
		for name in files:
			
			#Initialize item skip flag
			skipitem=False
			
			#If current name contains an ignored term, skip it
			for term in ignorelist:
				if term in name:
					skipitem=True
			if skipitem: continue
			
			#Create an empty page record
			record=ET.fromstring(empty_record)
			
			#Create absolute filepath
			curfile_path=os.path.join(root, name)
			
			#Set location url:
			#1.) Take the absolute path of the current file,
			#2.) remove from it the location of the local website folder,
			#3.) convert filesystem path into url path
			record.find("loc").text=pathname2url(curfile_path.replace(site_dir,""))
			
			#Set date modified:
			#1.) Get the date modified timestamp for the current file,
			#2.) Convert it to W3 date format, year-month-day as xxxx-xx-xx, where x's are numerals
			lastmod=datetime.date.fromtimestamp(os.stat(curfile_path).st_mtime)
			record.find("lastmod").text=lastmod.__str__()
			
			#See if it's the most recently modified time in this directory
			compare_emod_time(lastmod)
			
			#If the file ends with 'html':
			if name.endswith("html"):
				
				#Open the HTML file as an Element object
				htmlsoup=BeautifulSoup(open(curfile_path))
				
				#For every meta tag...
				for meta in htmlsoup.find_all("meta"):
					
					metatag_name=meta.get("name")
					if metatag_name != None:
						
						#Add a record to the sitemap
						ET.SubElement(record, meta.get("name"))
						
						#And record that metadata
						record.find(meta.get("name")).text=meta.get("content")
						
						#^This catch-all solution is useful for javascript
						#It enables it to learn about other pages on a site without fetching the html for each
						
						
			#Add to sitemap
			sitemap_index_element.append(record)
			
		#!!!
		#The section cheats a bit! In a good way I believe!
		#Notice that we're python walking from bottom up...
		#This means that whenever we work on a directory,
		#All the directories belowe have already been completed.
		#If an index.html file exists in this directory,
		#We can just copy the sitemap for it, for the whole dir!
		#!!!
		#For every directory,
		for name in dirs:
			
			#Initialize item skip flag
			skipitem=False
			
			#If current name contains an ignored term, skip it
			for term in ignorelist:
				if term in name:
					skipitem=True
			if skipitem: continue
			
			#Create an empty page record
			record=ET.fromstring(empty_record)
			
			#Create absolute filepath
			curdir_path=os.path.join(root, name)
			
			#Assuming an index.html file exists, this would be its path
			index_path=os.path.join(curdir_path, "index.html")
			
			#Set the location, using the same technique as used for files
			record.find("loc").text=pathname2url(curdir_path.replace(site_dir,""))
			
			#Find the last modified time of the directory's children, as recorded in the emod_time tag,
			#set that as the directory's lastmod time in the parent directory's sitemap
			record.find("lastmod").text=ET.parse(os.path.join(curdir_path, "sitemap.xml")).getroot().find("lastmod").text
			
			#See if it's the most recently modified time in this directory
			compare_emod_time(lastmod)
			
			#Record complete, add to sitemap
			sitemap_index_element.append(record)
			
		#Create a lastmod tag for the entire directory and set it to emod_time.
		#With every sitemap, I save a tag recording the earliest mtime of all its children
		#This ensures that all the lastmod times are correct in parent directory sitemaps
		sitemap_index_element.append(ET.Element("lastmod"))
		sitemap_index_element.find("lastmod").text=emod_time.__str__()
		
		#Save the complete sitemap to sitemap.xml
		#Since 'fromstring' creates an element object, not elementtree,
		#We must then parse the tree from the element object to use the write function
		ET.ElementTree(sitemap_index_element).write(os.path.join(root, 'sitemap.xml'), encoding="UTF-8", xml_declaration=True, )
	
	print "All sitemaps successfully generated."

#The function called when run from the shell
def run_shell():
	
	#Save 'Help Notice' as a string
	help_notice="""
	Domain:		In url form, the domain name for which you're generating sitemaps
	LocalPath:	Path to the website directory as stored locally. WARNING: If this argument is not passed, current directory will be assumed! You will be asked if this was a mistake, and given a chance to exit, but that's all! You will end up with sitemap.xmls all over the place if you're not careful!
"""
	#TODO: make any additional arguments terms to use in the ignore list,
	#As sitemaps might not need to be generated for EVERY directory
	
	#Record length of args list
	#Note that current directory is passed as the first argument
	#We only care about the arguments passed by the user, so ignore it in arglength
	arglength=len(sys.argv)-1
	
	#Initialize web domain variable
	domain="http://www.nonsense.ru/"
	
	#Initialize working directory variable
	workdir=os.getcwd()
	
	#If no arguments have been passed,
	if arglength==0:
		
		#Inform the user and exit gracefully
		print "Insufficient arguments, please pass" + help_notice
		exit(1)
		
	#If arguments have been passed,
	elif arglength>0:
			
		#If the user has asked for help,
		if sys.argv[1].lower() in ["-h","-help","help"]:
			
			#Inform them on valid use and exit gracefully
			print help_notice
			exit(0)
		
		#If the arglist is too long,
		if arglength>2:
			
			#Let the user know and exit gracefully
			print "Too many arguments passed! Valid arguments are" + help_notice
			exit(1)
			
		#Assume the url is valid (TODO, use url validator when one is available)
		domain=sys.argv[1]
		
		#If only one argument was passed,
		if arglength==1:
			
			#Confirm that's okay with the user
			print "Only one argument passed!"
			print "Domain name set to:" + domain
			print "Working directory will be assumed to be current working directory, ie:" + os.getcwd()
			if raw_input("\nContinue?").lower() not in ['y','yes', 'yeah']:
				exit(1)
				
		#Otherwise, with exactly 2 arguments passed,
		else:
			
			#Assign the second argument as the working directory
			workdir=sys.argv[2]
			
			#Check if it's a valid path (exists and is a directory)
			if not (os.path.exists(workdir) or os.path.isdir(workdir)):
				
				#Then the path is broken! Inform user and exit gracefully
				print "The work directory you have passed is invalid! Check your second argument:" + help_notice
				exit(1)
				
	create_sitemap(domain, workdir, ['testing', 'sitemap.xml'])

