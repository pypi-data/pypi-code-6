from hyperspace.html import HTMLPage
from hyperspace.hydra import HydraPage
from hyperspace.turtle import TurtlePage
import requests
import cgi


session = requests.Session()


def jump(url):
    response = session.get(url)
    mime = cgi.parse_header(response.headers['Content-Type'])
    return mime_to_page(mime[0], **mime[1])(response)


def send(url, data, _):
    response = session.post(url, data=data)
    if 'Location' in response.headers:
        return jump(response.headers['Location'])


def mime_to_page(mime, **kwargs):
    return {
        'text/html': HTMLPage,
        'application/ld+json': HydraPage,
        'text/turtle': TurtlePage,
    }[mime]

