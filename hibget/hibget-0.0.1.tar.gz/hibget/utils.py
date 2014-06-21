__author__ = "Joel Pedraza"
__copyright__ = "Copyright 2014, Joel Pedraza"
__license__ = "MIT"

from requests import RequestException
from humblebundle.exceptions import HumbleResponseException
from distutils.util import strtobool
from contextlib import contextmanager
import sys

@contextmanager
def smart_open(file, mode='r', **kwargs):
    if file != '-':
        with open(file, mode=mode, **kwargs) as fd:
            yield fd
    else:
        if 'b' in mode:
            yield sys.stdout.buffer
        else:
            yield sys.stdout


def root_cause(e):
    root = cause = e
    while cause is not None:
        root = cause
        cause = cause.__cause__ or cause.__context__
    return root


def format_error(e):
    if isinstance(e, RequestException) and not isinstance(e, HumbleResponseException):
        e = root_cause(e)
    if hasattr(e, 'strerror') and e.strerror:
        return e.strerror
    return str(e)


def input_yes_no(question, default=None, separator=": "):
    if default is None:
        yn = " [y/n]"
    elif default is True:
        yn = " [Y/n]"
    elif default is False:
        yn = " [y/N]"
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    prompt = "".join([question, yn, separator])

    while True:
        try:
            choice = input(prompt)
            if choice == '':
                if default is None:
                    raise ValueError
                else:
                    return default

            return strtobool(choice)
        except ValueError:
            print('Please respond with \'y\' or \'n\'.\n', file=sys.stderr)