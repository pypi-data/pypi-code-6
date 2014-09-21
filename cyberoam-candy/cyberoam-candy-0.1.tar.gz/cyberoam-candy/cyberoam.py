#!/usr/bin/python
from xml.dom.minidom import parseString
from datetime import datetime
import urllib2, urllib
import sys
import time
import base64
import getpass

def login(url,username,password):

    cyberoamAddress = url
    data = {"mode":"191","username":username,"password":password,"a":(str)((int)(time.time() * 1000))}
    try:
        print "Sending login request..."
        myfile = urllib2.urlopen(cyberoamAddress + "/httpclient.html", urllib.urlencode(data) , timeout=3)
    except IOError:
        print("Error: Could not connect to server")
        return
    data = myfile.read()
    print "=========== this is html ================\n",data
    myfile.close()
    dom = parseString(data)
    xmlTag = dom.getElementsByTagName('message')[0].toxml()
    print "=========== this is xml tag ============\n ",xmlTag
    message = xmlTag.replace('<message>', '').replace('</message>', '').replace('<message/>', '')
    print "========== msg is =============\n ",message
    xmlTag = dom.getElementsByTagName('status')[0].toxml()
    status = xmlTag.replace('<status>', '').replace('</status>', '')
    print "=========== status is ============ \n ",status

    if status.lower() != 'live':
        print("Error: " + message)
        return

def logout(url,username,password):

    cyberoamAddress = url
    data = {"mode":"193","username":username,"a":(str)((int)(time.time() * 1000))}

    try:
        print("Sending logout request...")
        myfile = urllib2.urlopen(cyberoamAddress + "/httpclient.html", urllib.urlencode(data), timeout=3)
    except IOError:
        print("Error:  Could not connect to server")
        return
    data = myfile.read()
    myfile.close()
    dom = parseString(data)
    xmlTag = dom.getElementsByTagName('message')[0].toxml()
    message = xmlTag.replace('<message>', '').replace('</message>', '')
    print "============ message is ============== \n",message

def run():
    url = "https://10.1.0.10:8090"
    print "Cyberoam Client Login Tool"
    username = raw_input("Username : ")
    password = getpass.getpass("Password : ")
    print "1. to Login, 2. To logout. "
    opt = raw_input("\nEnter option:")
    while(1):
    	if int(opt) == 1:
    		login(url,username,password)
    		opt = raw_input("\nEnter option:")
    	elif int(opt) == 2:
    		logout(url,username,password)
    		opt = raw_input("\nEnter option:")
    	else:
    		break