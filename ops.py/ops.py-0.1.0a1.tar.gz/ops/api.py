import json
import urllib2
import urllib
from compound import *
from target import *


class API:

  def __init__(self, app_id, app_key):
    self.app_id = app_id
    self.app_key = app_key
    self.base_url = "https://beta.openphacts.org/1.4/"


  def getCompoundInfo(self, uri):
    uri_encoded = urllib.quote_plus(uri)
    #print uri_encoded
    url_str = self.base_url+ "compound?app_id=" + self.app_id + "&app_key=" + self.app_key + "&uri="+ uri_encoded + "&_format=json"
    #print url_str
    results = json.load(urllib2.urlopen(url_str))
    return results


  def getTargetInfo(self, uri):
    uri_encoded = urllib.quote_plus(uri)
    url_str = self.base_url+ "target?app_id=" + self.app_id + "&app_key=" + self.app_key + "&uri="+ uri_encoded + "&_format=json"
    #print url_str
    results = json.load(urllib2.urlopen(url_str))
    return results


  def getCompoundPharmacology(self, uri):
     uri_encoded = urllib.quote_plus(uri)
     page_num = "1"
     url_str = self.base_url+ "compound/pharmacology/pages?app_id=" + self.app_id + "&app_key=" + self.app_key + "&uri="+ uri_encoded + "&_page="+ page_num +"&_format=json"
     for x in self.getCompoundPharmacologyIter(url_str):
       yield x

  def getCompoundPharmacologyIter(self, url_str):
     results = json.load(urllib2.urlopen(url_str))
     items = results['result']['items']

     for item in items:
          yield item

     if "next" in results['result']:
        url_str_next = results['result']['next']
        for x in self.getCompoundPharmacologyIter(url_str_next):
          yield x

  def getTargetPharmacology(self, uri):
     uri_encoded = urllib.quote_plus(uri)
     page_num = "1"
     url_str = self.base_url+ "target/pharmacology/pages?app_id=" + self.app_id + "&app_key=" + self.app_key + "&uri="+ uri_encoded + "&_page="+ page_num +"&_format=json"
     for x in self.getCompoundPharmacologyIter(url_str):
       yield x

  def getTargetPharmacologyIter(self, url_str):
     results = json.load(urllib2.urlopen(url_str))
     items = results['result']['items']

     for item in items:
          yield item

     if "next" in results['result']:
        url_str_next = results['result']['next']
        for x in self.getTargetPharmacology(url_str_next):
          yield x
