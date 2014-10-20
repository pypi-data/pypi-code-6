
from distutils.core import setup


# This snippet is in public domain
# https://gist.github.com/techtonik/4066623/

def get_version(relpath):
    """Read version info from a file without importing it"""
    from os.path import dirname, join

    # Allow to use function interactively
    if '__file__' not in globals():
        root = '.'
    else:
        root = dirname(__file__)

    # The code below reads text file with unknown encoding in
    # in Python2/3 compatible way. Reading this text file
    # without specifying encoding will fail in Python 3 on some
    # systems (see http://goo.gl/5XmOH). Specifying encoding as
    # open() parameter is incompatible with Python 2

    # cp437 is the encoding without missing points, safe against:
    #   UnicodeDecodeError: 'charmap' codec can't decode byte ...

    for line in open(join(root, relpath), 'rb'):
        line = line.decode('cp437')
        if '__version__' in line:
            if '"' in line:
                # __version__ = "0.9"
                return line.split('"')[1]
            elif "'" in line:
                return line.split("'")[1]


def get_description(relpath):
    from os.path import dirname, join
    text = open(join(dirname(__file__), 'README.txt'), 'rb').read()
    return text.decode('utf-8')


# Distutils 'API' to ship test data along with hexdump.py
# http://stackoverflow.com/questions/1612733/including-non-python-files-with-setup-py
from distutils.command.install import INSTALL_SCHEMES
for scheme in INSTALL_SCHEMES.values():
  scheme['data'] = scheme['purelib']


setup(
    name='hexdump',
    version=get_version('hexdump.py'),
    author='anatoly techtonik <techtonik@gmail.com>',
    url='http://bitbucket.org/techtonik/hexdump/',

    description="view/edit your binary with any text editor",
    license="Public Domain",
    classifiers=[
        #'Environment :: Console',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        #'Topic :: Utilities',
    ],

    py_modules=['hexdump'],
    data_files=[('', ['hexfile.bin'])],

    long_description=get_description('README.txt'),
)
