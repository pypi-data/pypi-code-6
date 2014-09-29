# -*- coding: UTF-8 -*-

"""
Get pollution info in Île-de-France from http://www.airparif.asso.fr/
"""

from bs4 import BeautifulSoup

try:
    from urllib import urlopen
except ImportError:
    from urllib.request import urlopen  # Python 3

BASEURL = 'http://www.airparif.asso.fr/'


def get_indices():
    """
    Return a list of 3 integers representing EU indices for yesterday, today
    and tomorrow.
    """
    doc = BeautifulSoup(urlopen(BASEURL))

    divs = doc.select('.indices_txt')
    if not divs:
        return None

    sibling = divs[1].nextSibling
    if not sibling:
        return None

    data = sibling.nextSibling
    if not data:
        return None

    # the indices are in an HTML comment
    data = BeautifulSoup(data)

    divs = data.select('.selected')
    return map(lambda d: int(d.text), divs)
