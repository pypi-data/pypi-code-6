'''
File: __init__.py
Author: Rinat F Sabitov
Description: m3 license managements module
'''

import os
import subprocess

VERSION = (0, 0, 2)


def get_version(version=None):
    "Returns a PEP 386-compliant version number from VERSION."
    if version is None:
        version = VERSION
    else:
        assert len(version) == 5
        assert version[3] in ('alpha', 'beta', 'rc', 'final')

    parts = 2 if version[2] == 0 else 3
    main = '.'.join(str(x) for x in version[:parts])

    return str(main)


def get_hg_changeset():
    """Returns a numeric identifier of the latest hg changeset."""
    repo_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    hg_log = subprocess.Popen(
        'hg tip --template "{latesttagdistance}-{node|short}"',
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        shell=True, cwd=repo_dir, universal_newlines=True
    )
    return hg_log.communicate()[0]
