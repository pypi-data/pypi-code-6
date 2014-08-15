#/usr/bin/env python
#coding:utf8

import requests

class Yo(object):

    wayto = {
        'all':'http://api.justyo.co/yoall/',
        'user':'http://api.justyo.co/yo/',
        'subscribers':'http://api.justyo.co/subscribers_count/'
        }
    
    def __init__(self, api_key):
        self.api_key = api_key

    def all(self):
        data = {'api_token':self.api_key}
        print requests.post(self.wayto['all'], data=data).json()

    def user(self, username):
        data = {'api_token':self.api_key, 
                'username':username}
        print requests.post(self.wayto['user'], data=data).json()

    def subscribers(self):
        url = self.wayto['subscribers'] + '?api_token=%s' % self.api_key
        print requests.get(url).json()

