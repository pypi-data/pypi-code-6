import os, datetime
import argparse

import lxml.html
from picklecache import cache
import requests
import pickle_warehouse, pickle_warehouse.serializers

DIR = os.path.join('~','.scarsdale-trustees')

@cache(os.path.join(DIR, 'index'))
def download_index(_):
    url = 'http://www.scarsdale.com/Home/BoardofTrustees/BoardofTrusteesAgendasMinutes.aspx'
    return requests.get(url)

def parse_index(response):
    html = lxml.html.fromstring(response.text)
    html.make_links_absolute(response.url)
    yield from html.xpath('//td[@class="PanesTD"]//a[contains(@href,"/Link")]')

def download_document(directory, anchor):
    w = pickle_warehouse.Warehouse(directory,
                                   serializer = pickle_warehouse.serializers.identity)
    url = anchor.xpath('@href')[0]
    text = anchor.xpath('text()')[0]
    if text not in w:
        w[text + '.pdf'] = requests.get(url).content

argparser = argparse.ArgumentParser()
argparser.add_argument('directory', default = '.',
                       help = 'Directory to download files to')

def main():
    args = argparser.parse_args()

    datestamp = datetime.date.today().isoformat()
    response = download_index(datestamp)
    for anchor in parse_index(response):
        download_document(args.directory, anchor)
