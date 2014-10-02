# -*- coding: utf-8 -*-
__author__ = 'massimo'

import re
import urlparse

regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  #domain...
        r'localhost|'  #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

url_in_text_regex = re.compile(
        r'(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  #domain...
        r'localhost|'  #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)', re.IGNORECASE)

link_regex = re.compile(r'(href|src)=[\'"]([^\'"]+)[\'"]', re.IGNORECASE)


def valid_url(text):
    return regex.match(text)


def pull_out_all_links(text):
    matches = link_regex.findall(text)
    return [match[1] for match in matches]
    # return url_in_text_regex.findall(text)


def urljoin(base, url):
    path = urlparse.urljoin(base, url)
    path = path.replace("../", "")
    return path