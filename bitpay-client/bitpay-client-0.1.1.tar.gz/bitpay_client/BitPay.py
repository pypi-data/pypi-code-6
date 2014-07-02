"""
Permission is hereby granted to any person obtaining a copy of this software
and associated documentation for use and/or modification in association with
the bitpay.com service.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

Bitcoin Python payment library using the bitpay.com service.
Version 1.0
"""

import bp_options
import os
import time
import json
import base64
from hashlib import sha256
import hmac
import binascii
import urllib2
import urllib

#print bp_options.bpOptions
class API(object):
    #code
    def __init__(self,
        
        # Please look carefully through these options and adjust according to your installation.  
        # Alternatively, most of these options can be dynamically set upon calling the functions in bp_lib.
        
        # REQUIRED Api key you created at bitpay.com
        # example: bpOptions['apiKey'] = 'L21K5IIUG3IN2J3';
        apiKey = '',
        
        # whether to verify POS data by hashing above api key.  If set to false, you should
        # have some way of verifying that callback data comes from bitpay.com
        # note: this option can only be changed here.  It cannot be set dynamically. 
        verifyPos = 'true',
        
        # email where invoice update notifications should be sent
        notificationEmail = '',
        
        # url where bit-pay server should send update notifications.  See API doc for more details.
        # example: $bpNotificationUrl = 'http:#www.example.com/callback.php';
        notificationURL = '',
        
        # url where the customer should be directed to after paying for the order
        # example: $bpNotificationUrl = 'http:#www.example.com/confirmation.php';
        redirectURL = '',
        
        # This is the currency used for the price setting.  A list of other pricing
        # currencies supported is found at bitpay.com
        currency = 'BTC',
        
        # Indicates whether anything is to be shipped with
        # the order (if false, the buyer will be informed that nothing is
        # to be shipped)
        physical = 'true',
        
        # If set to false, then notificaitions are only
        # sent when an invoice is confirmed (according the the
        # transactionSpeed setting). If set to true, then a notification
        # will be sent on every status change
        fullNotifications = 'true',
        
        # transaction speed: low/medium/high.   See API docs for more details.
        transactionSpeed = 'low', 
        
        # Logfile for use by the self.Log function.  Note: ensure the web server process has write access
        # to this file and/or directory!
        logFile = '/bplog.log',
        
        # Change to 'true' if you would like automatic logging of invoices and errors.
        # Otherwise you will have to call the self.Log function manually to log any information.
        useLogging = False,
        ):
        #set vars
        #for kw,arg in kwargs.iteritems():
        #    setattr(self, kw, arg)
        self.apiKey = apiKey;
        self.verifyPos = verifyPos;
        self.notificationEmail = notificationEmail;
        self.notificationURL = notificationURL;
        self.redirectURL = redirectURL;
        self.currency = currency;
        self.physical = physical;
        self.fullNotifications = fullNotifications;
        self.transactionSpeed = transactionSpeed;
        self.logFile = logFile;
        self.useLogging = useLogging;
        
    def log(self, contents):
        """
        Writes contents to a log file specified in the bp_options file or, if missing,
        defaults to a standard filename of 'bplog.log'.
        
        @param mixed contents
        @return
        """
        if self.logFile != "":
            file = os.path.realpath( os.path.dirname( __file__ )) + self.logFile
        else:
            # Fallback to using a default logfile name in case the variable is
            # missing or not set.
            file = os.path.realpath( os.path.dirname( __file__ ) ) + '/bplog.log'
            
        with open(file, "a") as log_file:
            log_file.write(time.strftime('%m-%d %H:%M:%S') + ": ")
            log_file.write(json.dumps(contents) + "\n")
    
    def curl(self, url, apiKey, post = False):
        global response
        """
        Handles post/get to BitPay via curl.
        
        @param string url, string apiKey, boolean post
        @return mixed response
        """
        response = ""
        if url.strip() != '' and apiKey.strip() != '':
        
            cookie_handler= urllib2.HTTPCookieProcessor()
            redirect_handler= urllib2.HTTPRedirectHandler()
            opener = urllib2.build_opener(redirect_handler, cookie_handler)
    
            uname = base64.b64encode(apiKey)
    
            opener.addheaders = [
                ('Content-Type', 'application/json'),
                ('Authorization', 'Basic ' + uname),
                ('X-BitPay-Plugin-Info', 'pythonlib1.1'),
            ] 
    
            if post:
                responseString = opener.open(url, urllib.urlencode(json.loads(post))).read()
            else:
                responseString = opener.open(url).read()
    
            try:
                response = json.loads(responseString)
            except ValueError:
                response = {
                    "error": responseString
                }
                if self.useLogging:
                    self.log('Error: ' . responseString)
                    
        return response
    
    
    def createInvoice(self, orderId, price, posData, options = {}):
        """
            Creates BitPay invoice via self.curl.
            
            @param string orderId, string price, string posData, array options
            @return array response
        """
        # orderId: Used to display an orderID to the buyer. In the account summary view, this value is used to
        # identify a ledger entry if present. Maximum length is 100 characters.
        #
        # price: by default, price is expressed in the currency you set in bp_options.php.  The currency can be
        # changed in options.
        #
        # posData: this field is included in status updates or requests to get an invoice.  It is intended to be used by
        # the merchant to uniquely identify an order associated with an invoice in their system.  Aside from that, Bit-Pay does
        # not use the data in this field.  The data in this field can be anything that is meaningful to the merchant.
        # Maximum length is 100 characters.
        #
        # Note:  Using the posData hash option will APPEND the hash to the posData field and could push you over the 100
        #        character limit.
        #
        #
        # options keys can include any of:
        #	'itemDesc', 'itemCode', 'notificationEmail', 'notificationURL', 'redirectURL', 'apiKey'
        #	'currency', 'physical', 'fullNotifications', 'transactionSpeed', 'buyerName',
        #	'buyerAddress1', 'buyerAddress2', 'buyerCity', 'buyerState', 'buyerZip', 'buyerEmail', 'buyerPhone'
        #
        # If a given option is not provided here, the value of that option will default to what is found in bp_options.php
        # (see api documentation for information on these options).
    
        options = dict(bp_options.bpOptions.items() + options.items()) # options override any options found in bp_options.php
        pos = {
            "posData": posData
        }
    
        if self.verifyPos:
            pos['hash'] = self.hash(str(posData), options['apiKey']);
    
        options['posData'] = json.dumps(pos);
    
        if len(options['posData']) > 100:
            return {
                "error": "posData > 100 character limit. Are you using the posData hash?"
            }
    
        options['orderID'] = orderId;
        options['price'] = price;
    
        postOptions = ['orderID', 'itemDesc', 'itemCode', 'notificationEmail', 'notificationURL', 'redirectURL', 
                             'posData', 'price', 'currency', 'physical', 'fullNotifications', 'transactionSpeed', 'buyerName', 
                             'buyerAddress1', 'buyerAddress2', 'buyerCity', 'buyerState', 'buyerZip', 'buyerEmail', 'buyerPhone'];
               
        """                       
        postOptions = ['orderID', 'itemDesc', 'itemCode', 'notificationEmail', 'notificationURL', 'redirectURL', 
                             'posData', 'price', 'currency', 'physical', 'fullNotifications', 'transactionSpeed', 'buyerName', 
                             'buyerAddress1', 'buyerAddress2', 'buyerCity', 'buyerState', 'buyerZip', 'buyerEmail', 'buyerPhone',
                             'pluginName', 'pluginVersion', 'serverInfo', 'serverVersion', 'addPluginInfo'];
        """
        # Usage information for support purposes. Do not modify.
        #postOptions['pluginName']    = 'Python Library';
        #postOptions['pluginVersion'] = '1.0';
        #postOptions['serverInfo']    = htmlentities(_SERVER['SERVER_SIGNATURE'], ENT_QUOTES);
        #postOptions['serverVersion'] = htmlentities(_SERVER['SERVER_SOFTWARE'], ENT_QUOTES);
        #postOptions['addPluginInfo'] = htmlentities(_SERVER['SCRIPT_FILENAME'], ENT_QUOTES);
    
        for o in postOptions:
            if o in options:
                pos[o] = options[o]
    
        pos = json.dumps(pos);
    
        response = self.curl('https://bitpay.com/api/invoice/', options['apiKey'], pos);
    
        if self.useLogging:
            self.log('Create Invoice: ')
            self.log(pos)
            self.log('Response: ')
            self.log(response)
    
        return response
    
    def verifyNotification(self, apiKey = False):
        """
        Call from your notification handler to convert _POST data to an object containing invoice data
        
        @param boolean apiKey
        @return mixed json
        """
    
        if not apiKey:
            apiKey = self.apiKey
    
        post = {} #how you get this post body data depends on what HTTP server you are using - SimpleHTTPServer, Flask, Bottle, Django, etc.
    
        if not post:
            return 'No post data'
    
        jsondata = json.loads(post)
    
        if 'posData' not in jsondata:
          return 'no posData'
    
        posData = json.loads(jsondata['posData'])
    
        if self.verifyPos and posData['hash'] != self.hash(str(posData['posData']), apiKey):
            return 'authentication failed (bad hash)'
    
        jsondata['posData'] = posData['posData']
    
        return jsondata
    
    def getInvoice(self, invoiceId, apiKey=False):
        """
        Retrieves an invoice from BitPay.  options can include 'apiKey'
        
        @param string invoiceId, boolean apiKey
        @return mixed json
        """
    
        if not apiKey:
          apiKey = self.apiKey
    
        response = self.curl('https://bitpay.com/api/invoice/'+invoiceId, apiKey)
    
        response['posData'] = json.loads(response['posData'])
        response['posData'] = response['posData']['posData']
    
        return response
    
    def hash(self, data, key):
        """
        Generates a base64 encoded keyed hash.
        
        @param string data, string key
        @return string hmac
        """
        
        hashed = hmac.new(key, data, sha256)
        return binascii.b2a_base64(hashed.digest())[:-1]
    
    def decodeResponse(self, response):
        """
        Decodes JSON response and returns
        associative array.
        
        @param string response
        @return array arrResponse
        """
      
        if response == "" or response is None:
          return 'Error: decodeResponse expects a string parameter.';
    
        return json.loads(response)
