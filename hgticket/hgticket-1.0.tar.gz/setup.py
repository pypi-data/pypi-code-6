from setuptools import setup, find_packages

import os
lines = open(os.path.join(os.path.dirname(__file__), 'README')).read().strip().splitlines()

sdesc = lines[0]
ldesc = '\n'.join(lines[1:])

setup(name='hgticket',
    version='1.0',
    author='Eric Gazoni',
    author_email='eric.gazoni@adimian.com',
    description=sdesc,
    long_description=ldesc,
    py_modules=['hgticket'],
    license='MIT',
    zip_safe=True,
    url='http://bitbucket.org/adimian/hgticket',
    download_url='http://bitbucket.org/adimian/hgticket/downloads',
    keywords='mercurial hg scm jira ticket',
)
