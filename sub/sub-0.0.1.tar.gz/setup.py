import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = 'sub',
    version = '0.0.1',
    author = 'Sartaj Singh',
    author_email = 'singhsartaj94@gmail.com',
    description = ('Simple Tool to download Subtitles.'),
    license = 'MIT',
    keywords = 'subtitles download movies tv shows',
    url = 'http://github.com/leosartaj/sub',
    packages=['sub'],
    scripts=['bin/sub'],
    long_description=read('README.md'),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
)
