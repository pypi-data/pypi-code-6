# -*- coding: utf-8 -*-
"""
Test pelican-git
=================

Unit testing for pelican_git

"""

from __future__ import unicode_literals
import os, sys, re

from pelican_git import plugin as gitplugin
from mock import patch
import requests.models
from bs4 import BeautifulSoup

TEST_REPO = 'minhhh/wiki'
TEST_FILENAME = 'sample.md'
TEST_BRANCH = 'develop'
TEST_HASH = '08dab572cd'
# https://github.com/minhhh/wiki/blob/master/sample.md
# https://github.com/minhhh/wiki/blob/08dab572cd/sample.md
# https://raw.githubusercontent.com/minhhh/wiki/08dab572cdb5085f252baba51e55904c5381d86d/sample.md
# https://raw.githubusercontent.com/minhhh/wiki/master/sample.md

def test_git_url():
    repo = TEST_REPO
    filename = TEST_FILENAME
    hash = TEST_HASH

    # Test without a branch or hash
    url = gitplugin.git_url(**{'repo': TEST_REPO, 'filename': filename})
    assert filename in url

    # Test with a branch
    url = gitplugin.git_url(**{'repo': TEST_REPO, 'filename': filename, 'branch': 'develop'})
    assert url.endswith(filename)
    assert 'develop' in url

    # Test with a hash
    url = gitplugin.git_url(**{'repo': TEST_REPO, 'filename': filename, 'hash': hash})
    assert url.endswith(filename)
    assert hash in url


def test_cache_filename():
    repo = TEST_REPO
    filename = TEST_FILENAME
    path_base = '/tmp'

    # Test without a branch
    path = gitplugin.cache_filename(path_base, repo, filename)
    assert path.startswith(path_base)
    assert path.endswith('.cache')

    # Test with branch
    path = gitplugin.cache_filename(path_base, repo, filename, 'develop')
    assert path.startswith(path_base)
    assert path.endswith('.cache')


def test_set_get_cache():
    repo = TEST_REPO
    filename = TEST_FILENAME
    path_base = '/tmp'
    body = """Some gist body"""

    # Make sure there is no cache
    for f in (gitplugin.cache_filename(path_base, repo, filename), ):
        if os.path.exists(f):
            os.remove(f)

    # Get an empty cache
    cache_file = gitplugin.get_cache(path_base, repo, filename)
    assert cache_file is None

    # Set a cache file
    gitplugin.set_cache(path_base, repo, filename, body=body)

    # Fetch the same file
    cached = gitplugin.get_cache(path_base, repo, filename)
    assert cached == body

def test_regex():
    content = '[git:repo=minhhh/wiki,file=sample.md]'

    matches = gitplugin.git_regex.findall(content)
    match = matches[0]
    assert match[1] == 'minhhh/wiki'
    assert match[3] == 'sample.md'


def test_fetch_git():
    """Ensure fetch_gist returns the response content as a string."""
    repo = TEST_REPO
    filename = TEST_FILENAME
    CODE_BODY = "code"
    with patch('requests.get') as get:
        return_response = requests.models.Response()
        return_response.status_code = 200
        return_response._content= CODE_BODY.encode()
        get.return_value = return_response
        assert gitplugin.fetch_git(repo, filename) == CODE_BODY

def test_fetch_git_sample():
    """Ensure fetch_gist returns the response content as a string."""
    repo = TEST_REPO
    filename = TEST_FILENAME

    response = gitplugin.fetch_git(repo, filename)
    soup = BeautifulSoup(response)
    res = soup.find('div', 'file')
    assert res is not None
