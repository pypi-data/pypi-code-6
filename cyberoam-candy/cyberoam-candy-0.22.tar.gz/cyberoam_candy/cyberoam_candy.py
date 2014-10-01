#!/usr/bin/python
from xml.dom.minidom import parseString
from datetime import datetime
import urllib2, urllib
import sys
import time
import base64
import getpass
import os

def login(url,username,password):

    cyberoamAddress = url
    data = {"mode":"191","username":username,"password":password,"a":(str)((int)(time.time() * 1000))}
    try:
        print "Sending login request..."
        myfile = urllib2.urlopen(cyberoamAddress + "/httpclient.html", urllib.urlencode(data) , timeout=3)
    except IOError:
        return "Error: Could not connect to server"
    data = myfile.read()
    #print "=========== this is html ================\n",data
    myfile.close()
    dom = parseString(data)
    xmlTag = dom.getElementsByTagName('message')[0].toxml()
    #print "=========== this is xml tag ============\n ",xmlTag
    message = xmlTag.replace('<message>', '').replace('</message>', '').replace('<message/>', '')
    #print "========== msg is =============\n ",message
    
    #xmlTag = dom.getElementsByTagName('status')[0].toxml()
    #status = xmlTag.replace('<status>', '').replace('</status>', '')
    #print "=========== status is ============ \n ",status

    return message

def logout(url,username,password):

    cyberoamAddress = url
    data = {"mode":"193","username":username,"a":(str)((int)(time.time() * 1000))}

    try:
        print("Sending logout request...")
        myfile = urllib2.urlopen(cyberoamAddress + "/httpclient.html", urllib.urlencode(data), timeout=3)
    except IOError:
        return "Error:  Could not connect to server"
    data = myfile.read()
    myfile.close()
    dom = parseString(data)
    xmlTag = dom.getElementsByTagName('message')[0].toxml()
    message = xmlTag.replace('<message>', '').replace('</message>', '')
    #print "============ message is ============== \n",message
    return message

def main(argv):
    #check for cases in the string.
    #add file not found exceptions.
    #add no argument given exception.

    if(len(argv)==2):
        print "Cyberoam Client Login Tool"

        db_config = []
        for line in open("config_file"):
            line = line.strip()
            db_config.append(line)

        server_url = db_config[0]
        if(argv[1]=="login"):
            users = []
            passwd = []

            for i in range(1,len(db_config)):
                user,password = db_config[i].split(':')
                users.insert(i-1,user)
                passwd.insert(i-1,password)


            for i in range(0,len(users)):
                return_message = login(server_url,str(users[i]),str(passwd[i]))
                if("Make sure your password is correct" in return_message):
                    print "Username :",users[i]," password is different than given in the config file. Please update it."
                    print "Trying for a new ID."
                elif("Could not connect to server" in return_message):
                    print "\nCould not connect to server. Program will exit. Please try again when you're connected."
                    time.sleep(2)
                    sys.exit()
                elif("exceeded" in return_message):
                    print "Data exceeded. Moving to the next username, password."
                elif("successfully logged in" in return_message):
                    print "Logged in successfully."
                    current_id_file = open("currently_using","w")
                    current_id_file.write("Currently Using ID & Password\nID:"+users[i]+"\nPassword:"+passwd[i]+"\nLogged in at : "+str(time.time())+"\nThis file will automatically delete on logout.")
                    time.sleep(2)
                    sys.exit()

            if(i==len(users)-1):
                print "Sorry. None of the IDs worked out, it seems. You should look out for better friends."

        elif(argv[1]=="logout"):
            arr = []
            for line in open("currently_using"):
                line = line.strip()         #to delete the "\n" appended at the end of every line.
                arr.append(line)

            userid = arr[1].split(':')
            passwd = arr[2].split(':')
            print "Currently, you were using\nUsername: ",userid[1],"\n\nNow logging out."

            return_msg = logout(server_url,userid[1],passwd[1])

            if("Could not connect to server" in return_msg):
                print "\nCould not connect to server. Program will exit. Please try again when you're connected."
                time.sleep(2)
                sys.exit()
            elif("successfully logged off" in return_msg):
                print "Logged out successfully. Deleting file."
                ## if file exists, delete it ##
                if os.path.isfile("currently_using"):
                        os.remove("currently_using")
                sys.exit()

    else:
        print "Incorrect input. \n\nFormat to run the file : python cyberoamcandy.py <option>\noption = login/logout"


if(len(sys.argv)>1):
    main(sys.argv)