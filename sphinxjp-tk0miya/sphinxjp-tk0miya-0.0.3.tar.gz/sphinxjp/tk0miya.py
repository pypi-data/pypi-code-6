# -*- coding: utf-8 -*-
"""
    sphinxjp.tk0miya
    ~~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2014 by WAKAYAMA Shirou
    :license: BSD, see LICENSE for details.
"""

import sys
import random


import flickr_api

from docutils import nodes, utils
from docutils.parsers.rst import directives
from sphinx.util.compat import Directive


FLICKR_IMAGE_TEMPLATE = '''
<img src="{0}" />
'''


class searchnode(nodes.General, nodes.Element):
    pass


def spec_size(argument):
    possible = ('square', 'large square', 'thumbnail', 'small',
                'small 320', 'medium', 'medium 640', 'medium 800',
                'large', 'original')

    return directives.choice(argument, possible)


class SearchDirective(Directive):

    has_content = False
    required_arguments = 1
    optional_arguments = 3
    option_spec = {
        'random': directives.flag,
        'size': spec_size,
        'license': directives.unchanged,
    }

    def run(self):
        env = self.state.document.settings.env
        api_key = env.config.flickr_api_key
        secret = env.config.flickr_secret

        if 'size' in self.options:
            size = self.options['size']
            size = size.capitalize()
        else:
            size = "Medium"

        if 'license' in self.options:
            license = self.options['license']
        else:
            license = "0"

        if api_key is None or secret is None:
            # TODO: how to use warning?
            env.warn(__name__, 'please set your api_key and secret in conf.py')
            return []

        node = searchnode(api_key=api_key,
                          secret=secret,
                          searchtags=" ".join(self.arguments),
                          random=('random' in self.options),
                          license=license,
                          size=size)
        return [node]


def visit_search_node(self, node):
    searchtags = node['searchtags']
    api_key = node['api_key']
    secret = node['secret']
    size = node['size']

    try:
        flickr_api.set_keys(api_key=api_key, api_secret=secret)

        photos = flickr_api.Photo.search(tags=searchtags)

        if node['random']:
            p = random.choice(photos)
        else:
            p = photos[0]

        url = p.getPhotoFile(size_label=size)
        html = FLICKR_IMAGE_TEMPLATE.format(url)
        self.body.append(html)

    except Exception, e:
        self.builder.warn('fail to load flickr. check api_key in your conf.py')
        raise nodes.SkipNode


def depart_search_node(self, node):
    pass


def setup(app):
    app.add_config_value('flickr_api_key', None, 'env')
    app.add_config_value('flickr_secret', None, 'env')

    app.add_node(searchnode, html=(visit_search_node, depart_search_node))

    app.add_directive('flickr-search', SearchDirective)
