#!/usr/bin/env python
import sys
import logging
import subprocess

import docker

logger = logging.getLogger(__name__)


def get_arg(args, prefix):
    """Get an argument by given prefix.

    """
    for arg in args:
        if arg.startswith(prefix):
            return arg[len(prefix):]


def main(args=None):
    logging.basicConfig(level=logging.INFO)
    if args is None:
        args = sys.argv[1:]

    name = get_arg(args, '--name=')
    if name is None:
        raise ValueError('You need to specify container name')

    # wehter to force removing container even if it is running
    force_rm = False
    if '--force-rm' in args:
        force_rm = True
        args.remove('--force-rm')

    client = docker.Client()
    containers = client.containers(all=True)

    target_container = None
    for container in containers:
        if '/{}'.format(name) in container['Names']:
            target_container = container
            break
    if target_container is None:
        logger.info(
            'Cannot find existing container with the same name %s', name
        )
    else:
        status = target_container['Status']
        if not status or status.startswith('Exited'):
            logger.info('Remove dead container')
            subprocess.check_call(['docker', 'rm', name])
        elif not force_rm:
            logger.error(
                'Container with the same name %r is still running',
                name,
            )
            raise RuntimeError(
                'Container name {} conflicts with running one {}'
                .format(name, target_container['Id']),
            )
        else:
            logger.warn('Force removing running container')
            subprocess.check_call(['docker', 'rm', '-f', name])
    # TODO: handle other signals here?
    logging.info('Executing docker run %s', ' '.join(args))
    try:
        subprocess.check_call(['docker', 'run'] + args)
    except (SystemExit, KeyboardInterrupt):
        logging.info('Stopping docker container %s', name)
        subprocess.check_call(['docker', 'stop', name])

if __name__ == '__main__':
    main()
