'''
Created on 30 Aug 2014

@author: Robert Putt
'''

import requests
import json
import logging

class APIClient:
    '''
        Docstring to be added...
    '''

    def __init__(self,apikey):
        '''
            Creates new 0870Py API Client object. To instantiate please
            provide a valid API Key to authenticate against the lookup
            server. If you require an API Key please visit
            www.0870converter.co.uk/api.php to get started.

            Example usage:
                from Py0870.APIClient import APIClient
                lookupclient = APIClient('my_api_key')
        '''
        self.apikey = apikey

    def lookup(self,number):
        '''
            Looks up an alternative for an 0800, 0845 or 0870 number
            which is provided as the number param. Numbers should be
            provided as a string in the format 0800000000 without
            any spaces or other punctuation.
        '''
        api_result = requests.get('http://www.0870converter.co.uk/api/query.php?key=%s&number=%s' % (self.apikey,number))

        raw_result = json.loads(api_result.content)
        if raw_result['status'] == 200:
            logging.info("Py0870 >> Successfully looked up alternative number for %s." % number)
            return {'number':raw_result['number'],'altnumber':raw_result['alternative'],'name':raw_result['name']}
        elif raw_result['status'] == 403:
            logging.error("Py0870 >> Could not authenticate to API, Please check your API Key.")
            raise Exception("Could not authenticate to 0870 Converter API. Please check your API Key.")
        elif raw_result['status'] == 404:
            logging.warn("Py0870 >> Could not find alternative number for %s." % number)
            raise Exception("No alternatives could be found for this number.")
