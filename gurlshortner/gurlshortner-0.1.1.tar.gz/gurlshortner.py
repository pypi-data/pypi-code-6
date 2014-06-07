#!/usr/bin/env python
import urllib
import urllib2
import json

GURL = 'https://www.googleapis.com/urlshortener/v1/url'

def shorten(longurl):
	post_value = { "longUrl": longurl }
	req = urllib2.Request(GURL, json.dumps(post_value), headers={'Content-type': 'application/json'})
	response = urllib2.urlopen(req)
	return json.loads(response.read())

def longify(shorturl):
	response = urllib2.urlopen(GURL + "?shortUrl=" + shorturl)
	return json.loads(response.read())