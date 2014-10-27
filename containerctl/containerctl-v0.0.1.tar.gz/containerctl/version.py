"""Container version detection."""
import locale
import os
import subprocess
from .errors import VersionError
from functools import cmp_to_key

default_version = 'latest'


def _script(container):
    """Return the version output by the container's version script."""
    cmd = os.path.join(container.path, 'version')
    if not os.path.isfile(cmd):
        return None
    if not os.access(cmd, os.X_OK):
        raise VersionError("version script not executable")

    env = os.environ.copy()
    env = env.update({
        'CONTAINER_PATH': container.path,
        'CONTAINER_NAME': container.name,
        'CONTAINER_USER': container.user,
    })

    try:
        out = subprocess.check_output(['bash', '-c', cmd], cwd=container.path, env=env)
        version = out.split('\n', 1)[0]
        return version or None
    except subprocess.CalledProcessError:
        raise VersionError("version script failed to execute")


def _git_tag(container):
    """Return the annotated git tag of the container's repo or a git hash if not tagged."""
    try:
        out = subprocess.check_output(['git', 'tag', '--points-at', 'HEAD'],
                                      cwd=container.path, universal_newlines=True)
        lines = sorted(out.split('\n'), key=cmp_to_key(locale.strcoll))
        if not lines or not lines[-1]:
            return None
        return lines[-1]
    except subprocess.CalledProcessError:
        return None


def _git_rev(container):
    """Return a version name containing the branch name and hash."""
    try:
        rev = subprocess.check_output(['git', 'rev-parse', '--verify', '--short', 'HEAD'],
                                      cwd=container.path, universal_newlines=True).strip()
        return 'rev-{}'.format(rev)
    except subprocess.CalledProcessError:
        return None


def detect(container):
    """
    Detect the container version. Three methods are used to determine the version. They are execute
    in order. The result from the first to succeed is returned. If all methods fail the default
    value of 'latest' is returned. The following methods are attempted:

    If an executable called 'version' exists in the container path its first line of output will be
    returned as the version. This step is skipped if the first line is a zero length string or the
    executable does not exist.

    If the container path is part of a git repository and the git command exists the annotated tag
    of the current commit is returned. If the current commit has more than one tag they are sorted
    suing a locale sensitive sort and the last item returned.

    If the current commit has no tag then the short form of the current git tag is appended to
    'rev-' to form a commit specific version. This step is skipped

    The git steps are skipped if git fails to execute.
    """
    detectors = (
        _script,
        _git_tag,
        _git_rev,
    )
    for detector in detectors:
        version = detector(container)
        if version is not None:
            return version
    return default_version
