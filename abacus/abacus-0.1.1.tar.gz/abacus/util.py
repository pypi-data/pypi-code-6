import re


def resturl(url):
    url = re.sub(r'/:id$', '(?:/(\d+))?$', url)
    url = re.sub(r'/:id', '/(\d+)', url)
    return url
