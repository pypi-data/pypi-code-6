import os


def get_version():
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, 'version.txt')
    return open(path).read().strip()

__version__ = get_version()
