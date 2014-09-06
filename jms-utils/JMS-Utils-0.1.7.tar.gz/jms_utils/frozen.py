import os
import sys

FROZEN = getattr(sys, u'frozen', False)


def cwd():
    if FROZEN:  # pragma: no cover
        # we are running in a |PyInstaller| bundle
        cwd_ = os.path.dirname(sys.argv[0])
    else:
        # we are running in a normal Python environment
        cwd_ = os.getcwd()
    return cwd_
