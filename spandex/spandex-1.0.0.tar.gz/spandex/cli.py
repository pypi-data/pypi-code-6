import argparse
import itertools
import json

import yaml

from spandex import client


def dump_attributes(attributes):
    for attribute, values in attributes.iteritems():
        if attribute[0] == '@':
            # skip meta attributes
            continue

        printed_attribute = False
        total_hits = sum(values.values())
        for value_hash, hits in values.iteritems():
            if hits > 1:
                if not printed_attribute:
                    print(attribute)
                    printed_attribute = True
                value = json.loads(value_hash)
                print('  %d%% %s' % (100.0 * hits / total_hits, value))
        if printed_attribute:
            print


def analyze_attributes(attributes):
    analysis = {}
    for attribute, values in attributes.iteritems():
        if attribute[0] == '@' or attribute == 'message':
            # skip meta attributes and raw messages
            continue

        analysis[attribute] = []

        total_hits = sum(values.values())
        for value_hash, hits in values.iteritems():
            value = json.loads(value_hash)
            analysis[attribute].append((100.0 * hits / total_hits, value))

        # sort by hit percentage
        analysis[attribute] = reversed(sorted(analysis[attribute],
                                       key=lambda x: x[0]))

    return analysis


def query(args):
    with open(args.query_file.name) as f:
        query_file = yaml.load(f.read())
        query = query_file['query']

    r = client.query(q=query, days=args.days)
    print('total hits: %s' % r['hits']['total'])

    attributes = {}
    for hit in r['hits']['hits']:
        for key, value in hit['_source'].iteritems():
            value_hash = json.dumps(value)
            attributes.setdefault(key, {}).setdefault(value_hash, 0)
            attributes[key][value_hash] += 1

    analysis = analyze_attributes(attributes)
    for attribute, results in analysis.iteritems():
        print(attribute)
        for percentage, value in itertools.islice(results, None, args.values):
            if isinstance(value, list):
                value = ' '.join(unicode(x) for x in value)
            print('  %d%% %s' % (percentage, value))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'query_file', type=argparse.FileType('r'),
        help='Path to an elastic-recheck YAML query file.')
    parser.add_argument(
        '--values', type=int, default=5,
        help='Maximum number of values to show for each attribute.')
    parser.add_argument(
        '--days', type=float, default=14,
        help='Timespan to query, in days (may be a decimal).')
    args = parser.parse_args()
    query(args)
