#!/usr/bin/env python
#coding: utf-8

import httplib
from extract import extract, extract_all

def get_response(host,url,method="GET"):
    conn = httplib.HTTPConnection(host)
    conn.request(method,url)
    r = conn.getresponse()
    data = r.read()
    conn.close()
    return data

def last():
    home = get_response(host="opslinux.com",url="/")
    content = extract_all('<article>','</article>',home)
    for item in content:
        title_html = extract('<a href="','</a>',item)
        title = title_html.split('">')
        print "标题: %s \n地址: %s\n" % (title[1],title[0])

def all():
    archives = get_response(host="opslinux.com",url="/archives.html")
    content = extract_all('<article>','</article>',archives)
    for item in content:
        title_html = extract('<a href="','</a>',item)
        title = title_html.split('">')
        print "标题: %s \n地址: %s\n" % (title[1],title[0])
