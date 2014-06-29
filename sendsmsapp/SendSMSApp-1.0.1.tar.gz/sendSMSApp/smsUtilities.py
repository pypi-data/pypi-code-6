'''
Created on Jun 28, 2014

@author: bhavyaj
'''

import urllib2
import urllib
from urllib2 import Request

mashapeKey = "kTohWlRnqemshh6o3QAtcqTvHhI1p1ll7KcjsnAhnRwQXN4GUv"
url = "https://site2sms.p.mashape.com/index.php"

def sendSMS(username,passwd,message,phoneNumbers):
    """
    Currently only site2SMS is supported
    """
    sendSMSTOSite2SMS(username, passwd, message, phoneNumbers)
    

def sendSMSTOSite2SMS(username,passwd,message,phoneNumbers):
    parameters = dict()
    parameters['msg'] = message
    parameters['pwd'] = passwd
    parameters['uid'] = username
    
    numberChunks = getNumberChunks(phoneNumbers, 10)
    
    for numbers in numberChunks:
        parameters['phone'] = getFormattedNumbers(numbers)
        data = urllib.urlencode(parameters)
        
        request = Request(url)
        request.add_data(data)
        request.add_header("X-Mashape-Key", mashapeKey)
        
        urllib2.urlopen(request)
   
def getNumberChunks(numberList, limit):
    for i in xrange(0,len(numberList), limit):
        yield numberList[i:i+limit]

def getFormattedNumbers(numbersList):
    if numbersList == None:
        raise Exception('Numbers List is not set.')
    formattedString = "";
    for numbers in numbersList:
        formattedString += numbers
        formattedString += ";"
    return formattedString[:-1]
         
if __name__ == '__main__':
    sendSMS('9966610574','ericson58','testing','9966610574;9460612381')
    
