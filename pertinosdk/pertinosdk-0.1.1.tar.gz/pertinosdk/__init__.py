'''
Created on Aug 11, 2014

@author: lwoydziak
@author: shankins

'''
import requests
from json import dumps
import json


class QueryBuilder(object):
    '''
    Build a :py:filter closure to filter a list based on fields and values.
    '''
    def __init__(self, field):
        self.__field = field
    
    def contains(self, desired):
        '''Return the filter closure fully constructed.'''
        field = self.__field
        def aFilter(testDictionary):
            return (desired in testDictionary[field])
        return aFilter

def where(field):
    """:py:QueryBuilder factory seeding it with the field you wish to filter on."""
    return QueryBuilder(field)

class PertinoSdk(object):
    '''
    Encapsulation of the Publicly available API.
    As of now you can:
    - List organizations you belong to :py:listOrgs
    - List devices in an organization :py:listDevices
    - Delete devices from an organization :py:deleteFrom
    '''
    API_KEY = '993e79924d5b6346fe62a5cf62183bc5'

    USER_QUERY='?user_key=' + API_KEY
    BASE_URL='http://api.labs.pertino.com:5000'
    BASE_PATH='/api/v0-alpha'
    ORGS_PATH='/orgs'
    DEVICES_PATH='/devices'


    def __init__(self, username, password, requestsObject=None):
        self.__username = username
        self.__password = password
        self.requests = requests if not requestsObject else requestsObject

    def listOrgs(self, closure=lambda x: True):
        """
        :param closure: optional filter of the results :py:QueryBuilder
        :returns: a list of organizations (as dictionaries) you belong to.
        :raises: HTTP errors
        """
        url = self.BASE_URL+self.BASE_PATH+self.ORGS_PATH+self.USER_QUERY
        response = self.requests.get(url, auth=(self.__username, self.__password))
        response.raise_for_status()
        return list(filter(closure, response.json()["orgs"]))

    def listDevicesIn(self, organization, closure=lambda x: True):
        """
        :param closure: optional filter of the results :py:QueryBuilder
        :returns: a list of devices (as dictionaries) in organization
        :raises: HTTP errors
        """
        url = self.BASE_URL+self.BASE_PATH+self.ORGS_PATH+"/"+ str(organization["id"]) + self.DEVICES_PATH+self.USER_QUERY
        response = self.requests.get(url, auth=(self.__username, self.__password))
        response.raise_for_status()
        return list(filter(closure, response.json()["devices"]))

    def deleteFrom(self, organization, devices):
        """
        Deletes all devices in a list.
        :raises: HTTP errors
        """
        for device in devices:
            url = self.BASE_URL+self.BASE_PATH+self.ORGS_PATH+"/"+ str(organization["id"]) + self.DEVICES_PATH+ "/" + str(device["id"]) + self.USER_QUERY
            response = self.requests.delete(url, auth=(self.__username, self.__password))
            response.raise_for_status()

    

