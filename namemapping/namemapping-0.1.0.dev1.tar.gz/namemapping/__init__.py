import sys
import argparse
import urllib2
import oauth2 as oauth
import time
import httplib
import json
from urlparse import urlparse
from collections import defaultdict

url = "http://yboss.yahooapis.com/ysearch/web"
# READ IN YAHOO BOSS API CREDENTIAL FROM HIDDEN CONFIG FILE '.credential'
file_credential = open(".credential")
OAUTH_CONSUMER_KEY = file_credential.readline().strip()
OAUTH_CONSUMER_SECRET = file_credential.readline().strip()
file_credential.close()

parser = argparse.ArgumentParser(prog='PROG')
parser.add_argument('-i', '--input', default="input.txt", help="an input file which contains a list of company names that need to be grouped")
parser.add_argument('-o', '--output', default="output.txt", help="an output file where the mapping will go to")
parser.add_argument('-e', '--extra', default="electronics", help="a word(like 'electronics','components') that will help the match when the company name is too short")

args = parser.parse_args()

# Set HTTP to 1.0 protocol so it can avoid the server side error incomplete read
httplib.HTTPConnection._http_vsn = 10
httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'

def oauth_request(url, params, method="GET"):
    # Removed trailing commas here - they make a difference.
    params['oauth_version'] = "1.0" #,
    params['oauth_nonce'] = oauth.generate_nonce() #,
    params['oauth_timestamp'] = int(time.time())  # @UndefinedVariable
    consumer = oauth.Consumer(key=OAUTH_CONSUMER_KEY,
                              secret=OAUTH_CONSUMER_SECRET)
    params['oauth_consumer_key'] = consumer.key
    req = oauth.Request(method=method, url=url, parameters=params)
    req.sign_request(oauth.SignatureMethod_HMAC_SHA1(), consumer, None)
    return req

def yahoosearch(search_term):
    req = oauth_request(url, params={"q": search_term})
    req['q'] = req['q'].encode('utf8')
    req_url = req.to_url().replace('+', '%20')
    result = urllib2.urlopen(req_url)
    response = result.read()
    return response

def main():
    # HIT API AND STORE THE RAW RESPONSE
    inputfile = open(args.input, 'r')
    datafile = open('data.json', 'w')

    for line in inputfile.readlines():
        try:
            myinput = line.strip()
            if len(myinput) < 2:
                continue
            result = {}
            result['myinput'] = myinput
            if len(myinput) < 5:
                search_term = myinput + " " + args.extra
            else:
                search_term = myinput
            result['search_term'] = search_term
            result['response'] = json.loads(yahoosearch(search_term))
            print >>datafile, result
        except:
            print sys.exc_info()
    datafile.close()
    inputfile.close()

    # PARSE THE RAW RESPONSE AND DO THE WORK
    datafile = open('data.json', 'r')
    outputfile = open(args.output, 'w')

    mapping = defaultdict(list)
    for line in datafile.readlines():
        try:
            record = eval(line.strip())
            myinput = record['myinput']

            try:
                result = record['response']['bossresponse']['web']['results']
                urls = ['{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(elem['url'])) for elem in result]
                firsturl = urls[0]
                mapping[firsturl].append(myinput)
            except:
                pass
        except:
            pass

    for key in mapping.keys():
        print >>outputfile, chr(1).join([key, str(mapping[key])])
    datafile.close()
    outputfile.close()
