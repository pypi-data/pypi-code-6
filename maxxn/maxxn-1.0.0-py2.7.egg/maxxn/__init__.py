#!/usr/bin/env python
#encoding:utf-8
import sys
import requests

from bs4 import BeautifulSoup


def main():
    url = sys.argv[1]
    locate = sys.argv[2]
    content = _get_page_content(url)
    print _get_sizzle_res(content,locate)


def _get_page_content(url):
    page = requests.get(url)
    return page.content


def _get_sizzle_res(content,locate):
    html = BeautifulSoup(content)
    return html.select(locate)


if __name__ == "__main__":
    main()
