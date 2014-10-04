import os
from setuptools import setup

setup(
    name = 'knurko',
    version = '0.1',
    description = 'Select a frame from a video file.',
    author = 'Thomas Levine',
    author_email = '_@thomaslevine.com',
    url = 'http://small.dada.pink/knurko',
    license = 'AGPL',
    scripts = [os.path.join('bin', 'knurko')],
    packages = ['knurko'],
    tests_require = [
        'nose>=1.3.4',
    ],
)
