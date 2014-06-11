# -*- coding: utf-8 -*-
"""
QUERY    Operations on queries
----------------------------------------
query LIST 
query sync .   
query sync ~/myfolder/  
query upload myfile.lql 
query upload myfile.lql  disabled=true
query delete name 

"""
import sys, json, datetime, time, os, logging, errno
import requests
from os.path import isfile, join
import tornado
from tornado.httpclient import HTTPClient
from colorama import init as coloramainit
from termcolor import colored

from config import options
from .input import InputHelper

log = logging.getLogger("lytics")

def upload_query(qrytext,qsargs=""):
    "Upload qry text"
    url = '%s/api/query?key=%s&%s' % (options.api, options.key,qsargs)

    if options.preview:
        log.warn("would have sent %s \n%s" % (url, qrytext))
        return

    log.debug("connecting to %s" % (url))
    headers = {'content-type': 'application/json'}
    log.debug("uploading qrytext = %s" %(qrytext))
    r = requests.post(url, data=qrytext, headers=headers)
    try:
        if r.status_code > 399:
            log.error("Could not complete request %s", r.text)
            sys.exit(1)
            return
        jsdata = json.loads(r.text)
        errors = []
        #print(json.dumps(jsdata, sort_keys=True, indent=2))
        if 'data' in jsdata:
            print(json.dumps(jsdata, sort_keys=True, indent=2))
            # for qry in jsdata['data']:
            #     if "status" in qry and qry['status'] == "error":
            #         errors.append(qry)
            #     elif 'text' in qry:
            #         print colored(qry['peg'] + "\n\n", 'green')
            # for err in errors:
            #     print colored("FAILED TO PARSE\n" + qry['text'] + "\n\n", 'red')
        else:
            print(json.dumps(jsdata, sort_keys=True, indent=2))
    except Exception, e:
        if options.traceback:
            raise
        log.error(e)
        sys.exit(1)

def sync_folder(cli,folder="",qsargs=""):
    """
    Sync folder of queries to api, looks for any files with .lql 
    """
    cwd = os.getcwd()
    folder = "%s/%s" % (cwd,folder)
    #print folder
    onlyfiles = [ f for f in os.listdir(folder) if isfile(join(folder,f)) ]
    for fileName in onlyfiles:
        if '.lql' in fileName:
            filepath = "%s/%s" % (folder, fileName)
            with open(filepath, 'r') as qf:
                data = qf.read()
                upload_query(data,qsargs)
    
def upload(cli,fileName="",qsargs=""):
    """
    Sync file lql to api, file must have .lql 
    """
    cwd = os.getcwd()
    filePath = "%s/%s" % (cwd,fileName)
    #print folder
    if isfile(filePath) and '.lql' in fileName:
        with open(filePath, 'r') as qf:
            data = qf.read()
            upload_query(data,qsargs)
    

def sync_file(cli):
    """
    Sync queries to lytics api from raw text files of .lql type 
    It assumes each query is seperated by at least one blank line
    """
    ih = InputHelper()
    ql = ih.parse()
    url = '%s/api/query?key=%s%s' % (options.api, options.key, ih.qs)

    log.debug("Syncing %s Queries " % (len(ql)))
    
    if options.preview:
        log.warn("would have sent %s" % (url))
        for q in ql:
            print(q[0] + "\n" + q[1])
        return

    payload = []
    for q in ql:
        payload.append({'peg': q[0] + q[1], "idx":0})
        #log.info(q)

    
    log.warn("connecting to %s" % (url))
    headers = {'content-type': 'application/json'}
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    try:
        jsdata = json.loads(r.text)
        errors = []
        #print(json.dumps(jsdata, sort_keys=True, indent=2))
        if 'data' in jsdata:
            for qry in jsdata['data']:
                if "status" in qry and qry['status'] == "error":
                    errors.append(qry)
                elif 'peg' in qry:
                    print colored(qry['peg'] + "\n\n", 'green')
            for err in errors:
                print colored("FAILED TO PARSE\n" + qry['peg'] + "\n\n", 'red')
        else:
            print(json.dumps(jsdata, sort_keys=True, indent=2))
    except Exception, e:
        if options.traceback:
            raise
        log.error(e)
        


def qry_list(cli):
    "Lists queries"
    url = '%s/api/query?key=%s' % (options.api, options.key)
    r = requests.get(url)
    if r.status_code < 400:
        data = json.loads(r.text)
        if 'data' in data:
            if isinstance(data['data'], list):
                for qry in data["data"]:
                    print colored(qry['text'] + "\n\n", 'green')
    else:
        print url
        print("ERROR %s" % (r.text))



