from getout import getoutlinks
import argparse
import sys

def main():
    try:
        parser = argparse.ArgumentParser(description='Get Outlinks of a given URL')
        #################
        # Input:
        # 1. URL
        # 2. User-agent
        #################
        parser.add_argument('-u', '--url', \
                            help='a URL that extract outlinks from', \
                            default='http://datafireball.com')
        parser.add_argument('-a', '--useragent', \
                            help='the user agent in request header', \
                            default='Python 2.7')
        args = parser.parse_args()
        outlinks = getoutlinks(args.url, args.useragent)
        for outlink in outlinks:
            print outlink
    except:
        print >>sys.stderr, sys.exc_info()



