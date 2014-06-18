import sys
import csv
import itertools

import wbcontractawards.download as d
import wbcontractawards.parse as p

def contracts():
    for os in itertools.count(0, 10):
        response = d.search(os)
        contract_urls = p.search(response)
        if [] == contract_urls:
            break
        for url in contract_urls:
            response = d.get(url)
            try:
                yield p.contract(response)
            except:
                sys.stderr.write('Error at %s\n' % url)
                raise

def cli():
    writer = csv.writer(sys.stdout)
    writer.writerow(['contract','bidder','status','amount','currency'])
    for contract in contracts():
        if contract != None:
            for bid in contract['bids']:
                row = [
                    contract['url'],
                    bid.get('bidder.name'),
                    bid.get('status'),
                    bid.get('opening.price.amount'),
                    bid.get('opening.price.currency'),
                ]
                writer.writerow(row)
