import os


_VERSION = '6'


def get_data_dir():
    home_path = os.path.expanduser('~')
    if home_path == '~':
        raise RuntimeError("Unable to determine user's home folder.")
    bdgt_dir = os.path.join(home_path, ".bdgt")
    return bdgt_dir


def get_version():
    return _VERSION
