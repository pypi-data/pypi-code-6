import logging
import subprocess
from os.path import dirname, join

from vdt.versionplugin.hotfix.args import parse_version_extra_args


log = logging.getLogger(__name__)


def build_package(version):
    """
    In here should go code that runs you package building scripts.
    """
    args, extra_args = parse_version_extra_args(version.extra_args)

    log.debug("Building hotfix version {0}-{1} with fpm.".format(version, args.iteration))
    if args.input_type == 'python':
        cmd = [
        'fpm', 
            '-s', 'python',
            '--version=%s' % version,
            '--iteration=%s' % args.iteration,
            '--exclude=*.pyc',
            '--exclude=*.pyo',
            '--depends=python',
            '--category=python',
            '--before-remove=%s' % join(dirname(__file__), 'preremove.sh'),
            '--template-scripts',
            '--python-install-lib=/usr/lib/python2.7/dist-packages/',
        ] + extra_args + ['setup.py']
    else:
        cmd = [
            'fpm',
            '-s', args.input_type,
            '--version=%s' % version,
            '--iteration=%s' % args.iteration,
        ] + extra_args

    log.debug("Running command {0}".format(" ".join(cmd)))
    try:
        log.debug(subprocess.check_output(cmd))
        return 0
    except subprocess.CalledProcessError as e:
        log.error("Fpm failed with exit code %s" % e.returncode)
        log.error(e.output)

    return 1
