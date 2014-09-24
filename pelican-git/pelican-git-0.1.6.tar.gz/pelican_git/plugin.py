#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Git embedding plugin for Pelican
=================================

This plugin allows you to embbed `git` file into your posts.

"""

from __future__ import unicode_literals
import os, re, logging, hashlib, codecs, copy
from bs4 import BeautifulSoup
import collections
import jinja2
import requests
g_jinja2 = jinja2.Environment(loader=jinja2.PackageLoader('pelican_git', 'templates'))

logger = logging.getLogger(__name__)
git_regex = re.compile(r'(\[git:repo\=([^,]+)(:?,file\=([^,]+))(:?,branch\=([^,]+))?(:?,hash\=([^,]+))?\])')

gist_template = """<div class="gist">
    {{code}}
</div>"""

GIT_TEMPLATE = 'git.jinja.html'


def git_url(repo, filename, branch="master", hash=None):
    url = "https://github.com/{}/blob/{}{}/{}".format(repo, "" if hash else branch, "" if not hash else hash, filename)
    return url


def cache_filename(base, repo, filename, branch="master", hash=None):
    h = hashlib.md5()
    h.update(str(repo).encode())
    h.update(str(filename).encode())
    if hash is not None:
        h.update(hash.encode())
    else:
        h.update(branch.encode())
    return os.path.join(base, '{}.cache'.format(h.hexdigest()))


def get_cache(base, repo, filename, branch="master", hash=None):
    cache_file = cache_filename(base, repo, filename, branch="master", hash=None)
    if not os.path.exists(cache_file):
        return None
    with codecs.open(cache_file, 'rb') as f:
        return f.read().decode('utf-8')


def set_cache(base, repo, filename, branch="master", hash=None, body=""):
    with codecs.open(cache_filename(base, repo, filename, branch, hash), 'wb') as f:
        f.write(body.encode('utf-8'))


def fetch_git(repo, filename, branch="master", hash=None):
    """Fetch a gist and return the contents as a string."""
    url = git_url(repo, filename, branch, hash)
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('Got a bad status looking up gist.')
    body = response.text
    if not body:
        raise Exception('Unable to get the gist contents.')

    return body


def setup_git(pelican):
    """Setup the default settings."""
    pelican.settings.setdefault('GIT_CACHE_ENABLED', False)
    pelican.settings.setdefault('GIT_CACHE_LOCATION',
                                '/tmp/git-cache')

    # Make sure the cache directory exists
    cache_base = pelican.settings.get('GIT_CACHE_LOCATION')
    if not os.path.exists(cache_base):
        os.makedirs(cache_base)


def get_body(res):
    soup = BeautifulSoup(res)
    body = soup.find('div', 'file')
    del body.contents[1]
    return body.prettify()


def replace_git_url(generator):
    """Replace gist tags in the article content."""
    template = g_jinja2.get_template(GIT_TEMPLATE)

    should_cache = generator.context.get('GIT_CACHE_ENABLED')
    cache_location = generator.context.get('GIT_CACHE_LOCATION')

    for article in generator.articles:
        for match in git_regex.findall(article._content):
            params = collections.defaultdict(str)
            repo = match[1]
            filename = match[3]
            branch = match[5]
            hash = match[7]

            params['repo'] = match[1]
            params['filename'] = match[3]
            if match[5]:
                params['branch'] = match[5]
            if match[7]:
                params['hash'] = match[7]

            logger.info('[git]: Found repo {}, filename {}, branch {} and hash {}'.format(repo, filename, branch, hash))
            logger.info('[git]: {}'.format(params))

            body = None if not should_cache else get_cache(cache_location, **params)

            # Fetch the git
            if not body:
                logger.info('[git]: Git did not exist in cache, fetching...')
                response = fetch_git(**params)

                if should_cache:
                    logger.info('[git]: Saving git to cache...')
                    body = get_body(response)
                    cache_params = copy.copy(params)
                    cache_params['body'] = body
                    set_cache(cache_location, **cache_params)
            else:
                logger.info('[git]: Found git in cache.')

            # Create a context to render with
            context = generator.context.copy()
            context.update({
                'code': body,
                'footer': 'full',
                'base': 'https://github.com/minhhh/pelican-git',
                'filename': filename,
                'url': git_url(**params)
            })
            replacement = template.render(context)
            article._content = article._content.replace(match[0], replacement)


def register():
    """Plugin registration."""
    from pelican import signals

    signals.initialized.connect(setup_git)

    signals.article_generator_finalized.connect(replace_git_url)
