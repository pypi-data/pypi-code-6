from bs4 import BeautifulSoup
import urllib2
from urlparse import urljoin

def getoutlinks(url, useragent='Python 2.7'):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', useragent)]    
    soup = BeautifulSoup(opener.open(url))
    outlinks = set()
    
    for a in soup.find_all('a'):
        try:
            #############################################
            # Filter:
            # 1. start with /, turn relative to absolute
            # 2. ditch if doesn't contain '://'
            #############################################
            link = a['href']
            if link.startswith('/'):
                link = urljoin(args.url, link)
            elif '://' not in link:
                continue
            outlinks.add(link)
        except:
            pass
    return sorted(list(outlinks))
