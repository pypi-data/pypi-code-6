# -*- coding: utf-8 -*-

"""
Utility functions.
"""

import os
import re
import sys
import yaml
import socket
import codecs
from datetime import datetime

from config import config
from term import get_terminal_size


def read_yaml_file(path):
    """
    Read YAML data from a file.
    """

    with codecs.open(path, "r", encoding='utf-8') as fp:
        return read_yaml(fp)


def read_yaml(fp):
    """
    Read YAML data from a stream.
    """

    return yaml.safe_load(fp)


def age(date, agoflag=True):
    """
    Return a human-readable in-the-past time string given a date.
    """

    return ago((datetime.now() - date).total_seconds(), agoflag)


def ago(counter, agoflag=True):
    """
    Return how long ago a number of seconds is.
    """

    counter = int(counter)
    if counter == 0:
        return "just now"

    for unit, count in (("second", 60),
                        ("minute", 60),
                        ("hour",   24),
                        ("day",     7),
                        ("week",    4),
                        ("month",  12),
                        ("year",    0)):
        if count > 0 and counter >= count * 2:
            counter /= count
        else:
            break

    return "%d %s%s%s" % (counter, unit,
                          "s" if counter > 1 else "",
                          " ago" if agoflag else "")


def extract_username(email):
    """
    Return a short user name given email text.
    """

    if '@' not in email:
        return email

    m = re.search('([A-Za-z0-9_.]+)@', email)
    if m:
        return m.group(1)

    return email


def default_name():
    """
    Return the default user name.
    """

    name = config.get('ui', 'name')
    if name:
        return name

    for var in "DITZUSER", "USER", "USERNAME":
        if var in os.environ:
            return os.environ[var]

    return "ditzuser"


def default_email():
    """
    Return the default email address.
    """

    email = config.get('ui', 'email')
    if email:
        return email

    for var in "DITZEMAIL", "EMAIL":
        if var in os.environ:
            return os.environ[var]

    return default_name() + '@' + hostname()


def hostname():
    """
    Return the host name.
    """

    name = config.get('ui', 'hostname')
    if name:
        return name

    for var in "DITZHOST", "HOSTNAME", "COMPUTERNAME":
        if var in os.environ:
            return os.environ[var]

    try:
        return socket.gethostname()
    except socket.error:
        return "UNKNOWN"


def terminal_size():
    """
    Return terminal size, or zero if stdout is not a tty.
    """

    if sys.stdout.isatty():
        return get_terminal_size()
    else:
        return (0, 0)


def print_columns(items, linelen=70, spacing=2):
    """
    Print a number of items in column format.
    """

    maxlen = max(len(text) for text in items)
    columns = max(linelen / (maxlen + spacing), 1)
    padding = " " * spacing

    count = 0
    while count < len(items):
        print items[count].ljust(maxlen) + padding,
        count += 1
        if count % columns == 0:
            print

    if count % columns != 0:
        print


def make_directory(path):
    """
    Create a directory if it doesn't exist.
    """

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as msg:
            raise DitzError(msg)


def check_value(name, value, choices):
    if value not in choices:
        raise ValueError("unknown %s: %s (one of %s expected)"
                         % (name, value, ", ".join(choices.keys())))


class DitzError(Exception):
    "A generic Ditz error."
