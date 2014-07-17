# -*- coding: utf8 -*-
"""
Created on Sun Jun 29 03:15:20 2014
@author: Kyunghoon Kim
"""
import urllib
import urllib2
import json

def analyzer(s, securitycode, nounlist=[], comp=0):
    """
    Korean Morpheme Analyzer.
    Get the JSON type result using Web API
    The function name 'Umorpheme' is an abbreviation of UNIST_morpheme
    :param s: Input Sentence
    :param securitycode: Personal Verification Key
    :param nounlist: CUSTOM Noun list
    :param comp: Compound noun 1:True, 0:False
    :return: term order, data, feature
    at UNIST Mathematical Sciences 2014.
    """
    url = "http://newsjam.kr:8080/?securitycode=" # morpheme analyzer
    r = url+securitycode

    if nounlist != []:
        params = urllib.urlencode({'nounlist': nounlist, 's':s})
    else:
        params = None
    if comp != 0:
        r = r + "&comp="+str(comp)
    req = urllib2.Request(r, params)
    response = urllib2.urlopen(req)
    data = json.load(response)
    return data