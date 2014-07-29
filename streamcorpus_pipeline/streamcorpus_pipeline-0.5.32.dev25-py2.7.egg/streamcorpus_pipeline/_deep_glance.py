'''
'''
from __future__ import absolute_import, division, print_function
import csv
import itertools
import logging
import backports.lzma as lzma
import os
import pprint
import sys

from BeautifulSoup import UnicodeDammit

import streamcorpus
from streamcorpus_pipeline.stages import Configured

# Some of the fields in this TSV file are huge.
csv.field_size_limit(sys.maxsize)
logger = logging.getLogger(__name__)


def drop_nuls(fobj):
    for line in fobj:
        yield line.replace('\x00', '')


class deep_glance_reader(Configured):
    config_name = 'deep_glance_reader'

    def __init__(self, *args, **kwargs):
        super(deep_glance_reader, self).__init__(*args, **kwargs)

    def __call__(self, deep_glance_dir):
        deep_glance_dir = os.path.abspath(deep_glance_dir)
        logger.info('deep_glance_dir: %s' % deep_glance_dir)
        frecords = os.path.join(deep_glance_dir, 'docviewer-new-1000.tsv.xz')
        fmeta = os.path.join(deep_glance_dir, 'metadata-1000.tsv.xz')

        records = drop_nuls(lzma.open(frecords))
        metas = drop_nuls(lzma.open(fmeta))
        rdr_records = csv.DictReader(records, delimiter='\t')
        rdr_metas = csv.DictReader(metas, delimiter='\t')
        for meta, record in itertools.izip(rdr_metas, rdr_records):
            yield self._make_stream_item(meta, record)

    def _make_stream_item(self, meta, record):
        assert meta['sourceid'] == record['docid']
        article_time = zulu_from_glance_timestamp(meta['articledatetime'])
        abs_path = os.path.join('deep-glance', meta['sourceid'])

        si = streamcorpus.make_stream_item(article_time, abs_path)
        si.source = 'deep-glance'
        si.original_url = meta.get('url', None)

        si.body = streamcorpus.ContentItem()
        si.body.language = streamcorpus.Language(code='en', name='ENGLISH')
        si.body.encoding = 'utf-8'
        si.body.media_type = 'text/plain'
        si.body.clean_visible = force_unicode(record['body']).encode('utf-8')
        return si


def zulu_from_glance_timestamp(s):
    date, time = s.split('_')
    y, m, d = map(int, [date[0:4], date[4:6], date[6:8]])
    h, min, ss = map(int, time.split(':'))
    return '%d-%02d-%02dT%02d:%02d:%02d.0Z' % (y, m, d, h, min, ss)


def force_unicode(raw):
    converted = UnicodeDammit(raw)
    if not converted.unicode:
        return unicode(raw, 'utf8', errors='ignore')
    else:
        return converted.unicode


Stages = {
    'deep_glance_reader': deep_glance_reader,
}


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'deep_glance_tsv',
        help='Path to a Deep Glance TSV file.')
    args = parser.parse_args()

    pp = pprint.PrettyPrinter(indent=2)
    reader = Stages['deep_glance_reader']()
    for i, si in enumerate(reader(args.deep_glance_tsv)):
        pp.pprint(si)
        print('-' * 79)
        # print(len(si.body.raw), si.stream_id) 
