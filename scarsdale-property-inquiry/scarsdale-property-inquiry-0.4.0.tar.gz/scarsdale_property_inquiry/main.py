import sys
import json
import os
import functools

from jumble import jumble
import dataset
from pickle_warehouse import Warehouse

import scarsdale_property_inquiry.download as dl
import scarsdale_property_inquiry.read as read
import scarsdale_property_inquiry.schema as schema

readme = '''
This directory contains big stuff that was produced by the following program.
http://pypi.python.org/pypi/scarsdale-property-inquiry

info/
    This directory contains the HTML of the property inquiry pages.
    You might also see "info.tar.gz", which is just an archive of
    this directory.
requests/
    This directory contains pickled response objects from python-requests.
scarsdale-property-inquiry.db
    This is a sqlite3 database that provides structure to the stuff in
    the HTML files.
'''

def get_fs(root_dir = os.path.expanduser('~/dadawarehouse.thomaslevine.com/big/scarsdale-property-inquiry/')):
    html_dir = os.path.join(root_dir, 'info')
    warehouse = Warehouse(os.path.join(root_dir, 'requests'))
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
    with open(os.path.join(root_dir, 'README'), 'w') as fp:
        fp.write(readme)
    return root_dir, html_dir, warehouse

import argparse

def getparser(root_dir):
    default_url = 'sqlite:///' + os.path.join(root_dir, 'scarsdale-property-inquiry.db')
    description = 'Inquire about Scarsdale properties, and save results to a relational database.'
    example = '''For example:

    scarsdale-property-inquiry --database mysql+pymysql://tlevine:password@big.dada.pink/scarsdale
'''
    parser = argparse.ArgumentParser(description=description, epilog = example)
    parser.add_argument('--database', type=str, nargs = '?', default = default_url,
                        help='The database to save to')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--streets', action = 'store_true', default = False,
                               help='List all of the street names.')
    group.add_argument('--street', type=str, nargs = '?',
                       help='Get the houses on a street.')
    group.add_argument('--house', type=str, nargs = '?',
                       help='Get the information about a particular house.')
    return parser

def main():
    stdout = sys.stdout
    root_dir, html_dir, warehouse = get_fs()
    p = getparser(root_dir).parse_args()

    db = dataset.connect(p.database)
    db.query(schema.properties)
    if p.house != None:
        session, _ = dl.home(warehouse)
        result = house(html_dir, warehouse, db, session, p.house)
        generator = [] if result == None else [result]
    elif p.street != None:
        session, _ = dl.home(warehouse)
        generator = street(warehouse, session, p.street)
    elif p.streets:
        _, generator = dl.home(warehouse)
    else:
        generator = village(html_dir, warehouse, db)
    for row in generator:
        stdout.write(json.dumps(row) + '\n')

def village(html_dir, warehouse, db):
    session, street_ids = dl.home(warehouse)
    for future in jumble(functool.partial(street, warehouse, session), street_ids):
        session, house_ids = future.result()
        for future in jumble(functools.partial(house, html_dir, warehouse, db, session), house_ids):
            row = future.result()
            if row != None:
                yield row

def street(warehouse, session, street_id):
    _, house_ids = dl.street(warehouse, session, street_id)
    yield from house_ids

def house(html_dir, warehouse, db, session, house_id):
    text = dl.house(warehouse, session, house_id)
    with open(os.path.join(html_dir, house_id + '.html'), 'w') as fp:
        fp.write(text)
    bumpy_row = read.info(text)
    if bumpy_row != None:
        excemptions = bumpy_row.get('assessment_information', {}).get('excemptions', [])
        if excemptions != []:
            for excemption in excemptions:
                excemption['property_number'] = bumpy_row['property_information']['Property Number']
                db['excemptions'].upsert(excemption, ['property_number'])
        flat_row = read.flatten(bumpy_row)
        if flat_row != None and 'property_number' in flat_row:
            if '' in flat_row:
                del(flat_row[''])
            db['properties'].upsert(flat_row, ['property_number'])
        return flat_row
