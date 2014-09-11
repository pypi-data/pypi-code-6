#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Lime
# @Date:   2014-09-11 17:12:11
# @Last Modified by:   Lime
# @Last Modified time: 2014-09-11 19:28:40

'''
Find domain names related with the given ip(s).

Usage:
    reverseip ip(s)

Examples:
    reverseip 1.1.1.1
    reverseip 1.1.1.1 1.1.1.2 1.1.1.3
'''

import sys
import urllib
import urllib2
import gevent

from bs4 import BeautifulSoup


class ReverseIP(object):
    URL = 'http://reverseip.domaintools.com/search/'

    def __init__(self, ip_list):
        self.ip_list = ip_list

    def parse_ip(self, ip):
        url = '%s?%s' % (self.URL, urllib.urlencode({'q': ip}))
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html)

        domain_list = soup.find_all(name='span', title=ip)

        print 'There are %s domains for %s' % (len(domain_list), ip)
        for index, domain in enumerate(domain_list):
            print '%s. %s' % (index + 1, domain.string)
        print

    def parse_all(self):
        tasks = [gevent.spawn(self.parse_ip, ip) for ip in self.ip_list]
        gevent.joinall(tasks)


def main():
    if len(sys.argv) < 2:
        print __doc__
        exit()

    reverseip = ReverseIP(sys.argv[1: ])
    reverseip.parse_all()


if __name__ == '__main__':
    main()
