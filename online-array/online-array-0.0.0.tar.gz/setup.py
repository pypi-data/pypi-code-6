import sys

from setuptools import setup

if sys.version_info < (2, 6):
    raise Exception('online-array requires Python 2.6 or higher.')

import online_array as distmeta

setup(
    name='online-array',
    version=distmeta.__version__,
    description='An array-like object that calls a function.',
    long_description=distmeta.__doc__,
    author=distmeta.__author__,
    author_email=distmeta.__contact__,
    url=distmeta.__homepage__,
    license='MIT License',
    platforms=['any'],
    packages=['online_array'],
    install_requires=[],
    entry_points = {
        },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        ],
    keywords='mathematics, numpy'
)
