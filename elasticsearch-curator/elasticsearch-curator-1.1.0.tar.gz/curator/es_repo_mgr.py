#!/usr/bin/env python

import sys
import time
import logging
from datetime import timedelta

import elasticsearch

try:
    from logging import NullHandler
except ImportError:
    from logging import Handler

    class NullHandler(Handler):
        def emit(self, record):
            pass

__version__ = '1.1.0'

# Elasticsearch versions supported
version_max  = (2, 0, 0)
version_min = (1, 0, 0)

logger = logging.getLogger(__name__)

DEFAULT_ARGS = {
    'host': 'localhost',
    'url_prefix': '',
    'port': 9200,
    'ssl': False,
    'timeout': 30,
    'dry_run': False,
    'debug': False,
    'log_level': 'INFO',
}

def make_parser():
    """ Creates an ArgumentParser to parse the command line options. """
    help_desc = 'Repository manager for Elasticsearch Curator.'
    try:
        import argparse
        parser = argparse.ArgumentParser(description=help_desc)
        parser.add_argument('-v', '--version', action='version', version='%(prog)s '+__version__)
    except ImportError:
        print('{0} requires module argparse.  Try: pip install argparse'.format(sys.argv[0]))
        sys.exit(1)
    parser.add_argument('--host', help='Elasticsearch host. Default: localhost', default=DEFAULT_ARGS['host'])
    parser.add_argument('--url_prefix', help='Elasticsearch http url prefix. Default: none', default=DEFAULT_ARGS['url_prefix'])
    parser.add_argument('--port', help='Elasticsearch port. Default: 9200', default=DEFAULT_ARGS['port'], type=int)
    parser.add_argument('--ssl', help='Connect to Elasticsearch through SSL. Default: false', action='store_true', default=DEFAULT_ARGS['ssl'])
    parser.add_argument('-t', '--timeout', help='Connection timeout in seconds. Default: 30', default=DEFAULT_ARGS['timeout'], type=int)
    parser.add_argument('-n', '--dry-run', action='store_true', help='If true, does not perform any changes to the Elasticsearch indices.',
                    default=DEFAULT_ARGS['dry_run'])
    parser.add_argument('-D', '--debug', dest='debug', action='store_true', help='Debug mode', default=DEFAULT_ARGS['debug'])
    parser.add_argument('--loglevel', dest='log_level', action='store', help='Log level', default=DEFAULT_ARGS['log_level'], type=str)
    parser.add_argument('-l', '--logfile', dest='log_file', help='log file', type=str)

    # Command sub_parsers
    subparsers = parser.add_subparsers(title='Commands', dest='command', description='Select one of the following commands:',
                    help='Run: ' + sys.argv[0] + ' COMMAND --help for command-specific help.')

    # 'fs' Repository creation
    parser_fs = subparsers.add_parser('create_fs', help='Create an "fs" type repository')
    parser_fs.set_defaults(func=_create_repository, repo_type='fs')
    parser_fs.add_argument('-r', '--repository', dest='repository', required=True, help='Repository name', type=str)
    parser_fs.add_argument('--location', dest='location', action='store', type=str, required=True,
                    help='Shared file-system location. Must match remote path, & be accessible to all master & data nodes')
    parser_fs.add_argument('--disable-compression', dest='compress', action='store_false', default=True,
                    help='Disable compression (enabled by default)')
    parser_fs.add_argument('--concurrent_streams', dest='concurrent_streams', action='store', type=int, default=None,
                        help='Number of streams (per node) preforming snapshot. Default: 5')
    parser_fs.add_argument('--chunk_size', dest='chunk_size', action='store', type=str, default=None,
                        help='Chunk size, e.g. 1g, 10m, 5k. Default is unbounded.')
    parser_fs.add_argument('--max_restore_bytes_per_sec', dest='max_restore_bytes_per_sec', action='store', type=str, default=None,
                        help='Throttles per node restore rate (per second). Default: 20mb')
    parser_fs.add_argument('--max_snapshot_bytes_per_sec', dest='max_snapshot_bytes_per_sec', action='store', type=str, default=None,
                        help='Throttles per node snapshot rate (per second). Default: 20mb')

    # 's3' Repository creation
    parser_s3 = subparsers.add_parser('create_s3', help='Create an \'s3\' type repository')
    parser_s3.set_defaults(func=_create_repository, repo_type='s3')
    parser_s3.add_argument('-r', '--repository', dest='repository', required=True, help='Repository name', type=str)
    parser_s3.add_argument('--bucket', dest='bucket', action='store', type=str, required=True,
                        help='S3 bucket name')
    parser_s3.add_argument('--region', dest='region', action='store', type=str, default=None,
                        help='S3 region. Defaults to US Standard')
    parser_s3.add_argument('--base_path', dest='base_path', action='store', type=str, default=None,
                        help='S3 base path. Defaults to root directory.')
    parser_s3.add_argument('--access_key', dest='access_key', action='store', type=str, default=None,
                        help='S3 access key. Defaults to value of cloud.aws.access_key')
    parser_s3.add_argument('--secret_key', dest='secret_key', action='store', type=str, default=None,
                        help='S3 secret key. Defaults to value of cloud.aws.secret_key')
    parser_s3.add_argument('--disable-compression', dest='compress', action='store_false', default=True,
                        help='Disable compression (enabled by default)')
    parser_s3.add_argument('--concurrent_streams', dest='concurrent_streams', action='store', type=int, default=None,
                        help='Number of streams (per node) preforming snapshot. Default: 5')
    parser_s3.add_argument('--chunk_size', dest='chunk_size', action='store', type=str, default=None,
                        help='Chunk size, e.g. 1g, 10m, 5k. Default is unbounded.')
    parser_s3.add_argument('--max_restore_bytes_per_sec', dest='max_restore_bytes_per_sec', action='store', type=str, default=None,
                    help='Throttles per node restore rate (per second). Default: 20mb')
    parser_s3.add_argument('--max_snapshot_bytes_per_sec', dest='max_snapshot_bytes_per_sec', action='store', type=str, default=None,
                        help='Throttles per node snapshot rate (per second). Default: 20mb')

    # Delete repository
    parser_delete = subparsers.add_parser('delete', help='Delete named repository')
    parser_delete.set_defaults(func=_delete_repository)
    parser_delete.add_argument('-r', '--repository', dest='repository', required=True, help='Repository name', type=str)


        # Show registered repositories
    parser_show = subparsers.add_parser('show', help='Show all registered repositories')
    parser_show.set_defaults(func=show)

    return parser


def show(client, **kwargs):
    for repository in sorted(get_repository(client, '_all').keys()):
        print('{0}'.format(repository))
    sys.exit(0)

def get_version(client):
    """Return ES version number as a tuple"""
    version = client.info()['version']['number']
    return tuple(map(int, version.split('.')))

def check_version(client):
    """Verify version is within acceptable range"""
    version_number = get_version(client)
    logger.debug('Detected Elasticsearch version {0}'.format(".".join(map(str,version_number))))
    if version_number >= version_max or version_number < version_min:
        print('Expected Elasticsearch version range > {0} < {1}'.format(".".join(map(str,version_min)),".".join(map(str,version_max))))
        print('ERROR: Incompatible with version {0} of Elasticsearch.  Exiting.'.format(".".join(map(str,version_number))))
        sys.exit(1)

def get_repository(client, repo_name):
    """Get Snapshot Repository information"""
    try:
        return client.snapshot.get_repository(repository=repo_name)
    except elasticsearch.NotFoundError as e:
        logger.info("Repository {0} not found.  Error: {1}".format(repo_name, e))
        return None

def _create_repository(client, dry_run=False, **kwargs):
    """Create repository with repo_name and body settings"""
    if not dry_run:
        try:
            repo_name = kwargs['repository']
            body = create_repo_body(**kwargs)
            result = get_repository(client, repo_name)
            if not result:
                client.snapshot.create_repository(repository=repo_name, body=body)
            elif result is not None and repo_name not in result and not kwargs['dry_run']:
                client.snapshot.create_repository(repository=repo_name, body=body)
            else:
                logger.error("Unable to create repository {0}.  A repository with that name already exists.".format(repo_name))
                sys.exit(0)
        except:
            logger.error("Unable to create repository {0}.  Check logs for more information.".format(repo_name))
            return False
        logger.info("Repository {0} creation initiated...".format(repo_name))
        test_result = get_repository(client, repo_name)
        if repo_name in test_result:
            logger.info("Repository {0} created successfully.".format(repo_name))
            return True
        else:
            logger.error("Repository {0} failed validation...".format(repo_name))
            return False
    else:
        logger.info("Would have attempted to create repository {}".format(kwargs['repository']))

def _delete_repository(client, repository=None, dry_run=False, **kwargs):
    if not dry_run:
        try:
            logger.info('Deleting repository {0}...'.format(repository))
            return client.snapshot.delete_repository(repository=repository)
        except elasticsearch.NotFoundError as e:
            logger.error("Error: {0}".format(e))
            return False
    else:
        logger.info("Would have attempted to delete repository {}".format(repository))

def create_repo_body(repo_type='fs',
                     compress=True, concurrent_streams=None, chunk_size=None, max_restore_bytes_per_sec=None, max_snapshot_bytes_per_sec=None,
                     location=None,
                     bucket=None, region=None, base_path=None, access_key=None, secret_key=None, **kwargs):
    """Create the request body for creating a repository"""
    argdict = locals()
    body = {}
    body['type'] = argdict['repo_type']
    body['settings'] = {}
    settings = []
    maybes   = ['compress', 'concurrent_streams', 'chunk_size', 'max_restore_bytes_per_sec', 'max_snapshot_bytes_per_sec']
    s3      = ['bucket', 'region', 'base_path', 'access_key', 'secret_key']

    settings += [i for i in maybes if argdict[i]]
    # Type 'fs'
    if argdict['repo_type'] == 'fs':
        settings.append('location')
    # Type 's3'
    if argdict['repo_type'] == 's3':
        settings += [i for i in s3 if argdict[i]]
    for k in settings:
        body['settings'][k] = argdict[k]
    return body

def main():
    start = time.time()

    parser = make_parser()
    arguments = parser.parse_args()

    # Do not log and force dry-run if we opt to show indices.
    if arguments.command == 'show':
        arguments.log_file = '/dev/null'
        arguments.dry_run = True

    # Setup logging
    if arguments.debug:
        numeric_log_level = logging.DEBUG
    else:
        numeric_log_level = getattr(logging, arguments.log_level.upper(), None)
        if not isinstance(numeric_log_level, int):
            raise ValueError('Invalid log level: %s' % arguments.log_level)

    logging.basicConfig(level=numeric_log_level,
                        format='%(asctime)s.%(msecs)03d %(levelname)-9s %(funcName)22s:%(lineno)-4d %(message)s',
                        datefmt="%Y-%m-%dT%H:%M:%S",
                        stream=open(arguments.log_file, 'a') if arguments.log_file else sys.stderr)
    logging.info("Job starting...")

    # Setting up NullHandler to handle nested elasticsearch.trace Logger instance in elasticsearch python client
    logging.getLogger('elasticsearch.trace').addHandler(NullHandler())

    if arguments.dry_run:
        logger.info('DRY RUN MODE.  No changes will be made.')

    client = elasticsearch.Elasticsearch(host=arguments.host, port=arguments.port, url_prefix=arguments.url_prefix, timeout=arguments.timeout, use_ssl=arguments.ssl)

    check_version(client)

    # Execute the command specified in the arguments
    argdict = arguments.__dict__
    logging.debug("argdict = {}".format(argdict))
    arguments.func(client, **argdict)
    
    logger.info('Done in {0}.'.format(timedelta(seconds=time.time()-start)))
    
if __name__ == '__main__':
    main()
