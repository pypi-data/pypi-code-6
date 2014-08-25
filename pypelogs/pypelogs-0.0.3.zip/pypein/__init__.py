from wikip import WikipArticles, WikipGeo
from text import Text
from json_in import JSON
from mongodb import MongoDBGeo
from nginx import Nginx
from csv_in import CSVIn
from flickr import Flickr
from instagram_in import Instagram
from oracle import Oracle
from postgresql import Postgresql
from twitter import Twitter

CLASSES = {
    'csv':    CSVIn,
    'flickr': Flickr,
    'ig':     Instagram,
    'text':   Text,
    'json':   JSON,
    'nginx':  Nginx,
    'ora':    Oracle,
    'pgsql':  Postgresql,
    'twitter': Twitter,
    'wikip':  WikipArticles,
    'wikig':  WikipGeo,
    'mongeo': MongoDBGeo
}


def input_for(s):
    spec_args = s.split(':', 1)
    clz = CLASSES.get(spec_args[0])
    if not clz:
        raise ValueError("No such input type: %s", spec_args[0])
    return clz() if len(spec_args) == 1 else clz(spec_args[1])