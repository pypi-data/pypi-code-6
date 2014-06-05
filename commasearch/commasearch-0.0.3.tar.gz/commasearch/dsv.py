'''
Why am I not writing this in Haskell!?
'''
import csv
import re
from urllib.parse import urlsplit
from io import StringIO
from logging import getLogger
from functools import partial

import special_snowflake
from thready import threaded
import requests

from commasearch.util import traceback, column_combinations

logger = getLogger('commasearch')

def download(func, db, url:str):
    if url not in db.errors:
        fp = retrieve_csv(url)
        if fp == None:
            db.errors[url] = True
            logger.error('Could not load %s' % (url))
        else:
            result = func(db, fp, url)
            fp.close()
            return result
   
def _index(db, fp, url:str):
    '''
    Index a CSV file.
    '''
    # Dialect of the CSV file
    dialect = guess_dialect(fp)
    
    # Find the unique keys.
    indices = unique_keys(fp, dialect)
    
    # Get the hashes of all the values.
    many_args = distinct_values(fp, dialect, indices)

    # Save them to the database threaded because it might go faster.
    def save_values(args):
        index, values = args
        db.values(index)[url] = values
    threaded(many_args.items(), save_values, max_queue = 0)

    # Wait until the end to save indices because that's the way that
    # completeness is checked.
    db.indices[url] = indices


def _search(db, fp, search_url:str):
    '''
    Search for table.
    '''

    # Index the file first.
    if search_url not in db.indices:
        raise ValueError('The table must be indexed before you can search it. (%s)' % search_url)

    # Dialect of the CSV file
    dialect = guess_dialect(fp)

    # Then grab column combinations.
    colnames = get_colnames(fp, dialect)
    indices = list(column_combinations(colnames))

    # Then look for things that have high overlap.
    index_search_values = distinct_values(fp, dialect, indices)
    for i, search_values in index_search_values.items():
        for (result_path, result_values) in db.values(i).items():
            yield {
                'index': i,
                'overlap':len(search_values.intersection(result_values)),
                'path': result_path,
                'nrow': len(result_values)
            }

index = partial(download, _index)
search = partial(download, _search)


# Utilities follow.

def get_colnames(fp, dialect) -> list:
    pos = fp.tell()
    reader = csv.reader(fp, dialect = dialect)
    result = next(reader)
    fp.seek(pos)
    return result

def guess_dialect(fp):
    'Guess the dialect of a CSV file.'
    pos = fp.tell()
    try:
        dialect = csv.Sniffer().sniff(fp.read(1024))
    except csv.Error:
        dialect = 'excel' # the default
    fp.seek(pos)
    return dialect

def http_transporter(url):
    try:
        response = requests.get(url)
    except Exception as e:  
        logger.error('Error downloading %s:\n%s' % (url,traceback()))
    else:
        if response.ok:
            return StringIO(response.text)
        else:
            logger.error('Status %d at %s' % (response.status_code, url))

def gettransporters():
    t = {
        'file': lambda url: open(re.sub(r'^file://', '', url), 'r'),
        'http': http_transporter,
    }
    t['https'] = t['http']
    return t

def retrieve_csv(url:str, transporters = gettransporters()):
    def other(scheme):
        raise ValueError('The %s:// scheme is not supported' % scheme)
    return transporters.get(urlsplit(url).scheme, other)(url)

def unique_keys(fp, dialect) -> set:
    '''
    Find the unique keys in a dataset.
    '''
    pos = fp.tell()
    result = special_snowflake.fromcsv(fp, dialect = dialect)
    fp.seek(pos)
    return result

def distinct_values(fp, dialect, indices) -> dict:
    '''
    Find the distinct values of an index in a csv file.
    '''
    result = {index: set() for index in indices}
    pos = fp.tell()
    reader = csv.DictReader(fp, dialect = dialect)
    for row in reader:
        for index in indices:
            result[index].add(hash(tuple(row[column] for column in index)))
    fp.seek(pos)
    return result
