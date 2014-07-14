# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import argparse
import itertools
import json

import yaml

from spandex import client


LESS_THAN_USEFUL_ATTRIBUTES = [
    'build_master',
    'build_patchset',
    'build_ref',
    'build_short_uuid',
    'build_uuid',
    'error_pr',
    'host',
    'received_at',
    'type',
]


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
        if not args.verbose and attribute in LESS_THAN_USEFUL_ATTRIBUTES:
            # skip less-than-useful attributes to reduce noise in the report
            continue

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
    parser.add_argument(
        '--verbose', action='store_true',
        help='Report on additional query metadata.')
    args = parser.parse_args()
    query(args)
