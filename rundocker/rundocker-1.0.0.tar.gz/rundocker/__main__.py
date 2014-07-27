#!/usr/bin/env python
import os
import sys
import logging
import subprocess

logger = logging.getLogger(__name__)

CIDFILE_DIR = os.environ.get('CIDFILE_DIR', '/var/run')
CIDFILE_SUFFIX = os.environ.get('CIDFILE_SUFFIX', '.cid')


def get_arg(args, prefix):
    """Get an argument by given prefix.

    """
    for arg in args:
        if arg.startswith(prefix):
            return arg[len(prefix):]


def read_content(filepath):
    with open(filepath, 'rt') as cfile:
        return cfile.read()


def main(args=None):
    logging.basicConfig(level=logging.INFO)
    if args is None:
        args = sys.argv[1:]

    cidfile = get_arg(args, '--cidfile=')
    name = get_arg(args, '--name=')
    if name is None:
        raise ValueError('You need to specify container name')
    if cidfile is None:
        cidfile = os.path.join(CIDFILE_DIR, name + CIDFILE_SUFFIX)
        logger.info('Use default CID path %s', cidfile)
        args.insert(0, '--cidfile={}'.format(cidfile))
    else:
        logger.info('Use given CID path %s', cidfile)

    if os.path.exists(cidfile):
        logging.info('CID file exists, ensure the old container is removed')
        cid = read_content(cidfile)
        subprocess.call(['docker', 'rm', '-f', cid])
        os.remove(cidfile)

    # TODO: handle other signals here?
    logging.info('Executing docker run %s', ' '.join(args))
    try:
        subprocess.check_call(['docker', 'run'] + args)
    except (SystemExit, KeyboardInterrupt):
        cid = read_content(cidfile)
        logging.info('Stopping docker container %s', cid)
        subprocess.check_call(['docker', 'stop', cid])

if __name__ == '__main__':
    main()
