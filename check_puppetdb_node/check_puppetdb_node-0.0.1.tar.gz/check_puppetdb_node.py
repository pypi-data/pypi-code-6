#!/usr/bin/env python
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import sys
import optparse
import datetime
import pypuppetdb
import requests


def total_seconds(delta):
    return (delta.microseconds + (delta.seconds + delta.days * 24 * 3600) *
            10**6) / 10**6


def cmd():
    description = """
check_puppetdb_node uses PuppetDB to check for the status of a node. It uses
the pypuppetdb library in order to do so and can do so securely through the
use of SSL client certificates if needed or wanted.

We check how old the report is and based on the warning and critical
thresholds will react accordingly. If no report is present an UNKNOWN
state will be returned instead. If the report contains failed events,
regardless of further thresholds, the machine will be regarded as being in an
erroneous state and a CRITICAL will be returned.
"""
    parser = optparse.OptionParser(description=description)
    parser.add_option('-n', '--hostname', dest='hostname',
                      help='Hostname of the machine to check')
    parser.add_option('-c', '--critical', type='float', default=2,
                      help=('Amount of hours after which a node should be '
                            'considered CRITICAL, defaults to 2 hours'))
    parser.add_option('-w', '--warning', type='float', default=1,
                      help=('Amount of hours after which a node should be '
                            'considered in WARNING, defaults to 1 hour'))
    parser.add_option('-p', '--port', default=8080, type='int',
                      help='Port on which PuppetDB listens')
    parser.add_option('-s', '--server', default='localhost',
                      help='Hostname on which PuppetDB is reachable')
    parser.add_option('-t', '--timeout', default=10, type='int',
                      help='Timeout for PuppetDB requests')
    parser.add_option('--clientcert', default=None,
                      help='Path to client certificate for PuppetDB')
    parser.add_option('--clientkey', default=None,
                      help='Path to client key for PuppetDB')
    parser.add_option('--verify', default='yes',
                      help=('Verify the PuppetDB server certificate. This can '
                            'be either "yes", "no" or the path to the Puppet '
                            'CA public key'))
    (options, _) = parser.parse_args()

    if not options.hostname:
        parser.error('Must provide a hostname, see --help for instructions')
    return options


def get_node(hostname, puppetdb):
    try:
        node = puppetdb.node(hostname)
    except requests.exceptions.HTTPError:
        print('UNKNOWN - {0} is unknown to PuppetDB'.format(options.hostname))
        sys.exit(3)
    finally:
        return node


def node_status(hostname, puppetdb):
    latest_events = puppetdb._query('event-counts',
                                    query='["=","latest-report?",true]',
                                    summarize_by='certname')
    status = [s for s in latest_events if s['subject']['title'] == hostname]

    # When a run completes successfully but nothing happens the status
    # ends up being empty instead of contains all items but at a zero value
    if status:
        return status[0]
    else:
        return None


def time_elapsed(timestamp):
    now = datetime.datetime.utcnow()
    now = datetime.datetime.strptime(str(now), '%Y-%m-%d %H:%M:%S.%f').replace(
        tzinfo=pypuppetdb.utils.UTC())
    delta = now - timestamp
    delta_seconds = total_seconds(delta)
    return (delta, delta_seconds)


def main():
    options = cmd()

    if options.verify == 'yes':
        ssl_verify = True
    elif options.verify == 'no':
        ssl_verify = False
    else:
        ssl_verify = options.verify

    p = pypuppetdb.connect(host=options.server, port=options.port,
                           ssl_verify=ssl_verify, ssl_key=options.clientkey,
                           ssl_cert=options.clientcert,
                           timeout=options.timeout)

    node = get_node(options.hostname, p)

    if not node.report_timestamp:
        print("UNKNOWN - This machine hasn't checked in with us yet")
        sys.exit(3)

    critical_seconds = 60 * 60 * options.critical
    warning_seconds = 60 * 60 * options.warning
    (delta, delta_seconds) = time_elapsed(node.report_timestamp)

    status = node_status(options.hostname, p)
    if status is not None and status['failures'] > 0:
        print(('CRITICAL -  We have {0} failure(s). Last report was '
               '{1} ago'.format(status['failures'], delta)))
        sys.exit(2)
    elif delta_seconds < warning_seconds:
        print('OK - Last run happened {0} ago'.format(delta))
        sys.exit(0)
    elif warning_seconds <= delta_seconds < critical_seconds:
        print('WARNING - Last run happened {0} ago'.format(delta))
        sys.exit(1)
    elif delta_seconds >= critical_seconds:
        print('CRITICAL - Last run happened {0} ago'.format(delta))
        sys.exit(2)
    else:
        print("UNKNOWN - Something went wrong determining this node's state")
        sys.exit(3)


if __name__ == '__main__':
    main()
