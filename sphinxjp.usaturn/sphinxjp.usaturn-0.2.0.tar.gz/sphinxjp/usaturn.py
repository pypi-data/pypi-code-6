# -*- coding: utf-8 -*-

import os
from types import MethodType
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from sphinx.application import Sphinx
from sphinx.util.osutil import copyfile

USATURN_CSS = 'usaturn.css'


def html_visit_character_icon(self, node):
    self.body.append(self.starttag(node, 'div', CLASS='icon'))
    self.body.append(self.starttag(node, 'img', src=node['image_url'], empty=True))
    self.body.append('<br />')
    self.body.append(self.starttag(node, 'div', CLASS='name'))
    self.body.append(node.get('name') or '')
    self.body.append('</div>\n')
    self.body.append('</div>\n')


def html_visit_character_admonition(self, node):
    self.body.append(self.starttag(node, 'div', CLASS='admonition character-admonition'))
    if node['align'] != 'right':
        html_visit_character_icon(self, node)

    self.body.append(self.starttag(node, 'div', CLASS='message-box ' + node['align']))
    self.body.append(self.starttag(node, 'div', CLASS='message'))


def html_depart_character_admonition(self, node):
    self.body.append('</div>\n')
    self.body.append('</div>\n')
    if node['align'] == 'right':
        html_visit_character_icon(self, node)

    self.body.append('</div>\n')


class character_admonition(nodes.Admonition, nodes.Element):
    pass


def on_builder_inited(app):
    app.add_stylesheet(USATURN_CSS)


def on_build_finished(app, exception):
    if app.builder.name != 'html' or exception:
        return

    app.info('Copying requirements stylesheet... ', nonl=True)
    dest = os.path.join(app.builder.outdir, '_static', USATURN_CSS)
    source = os.path.join(os.path.abspath(os.path.dirname(__file__)), USATURN_CSS)
    copyfile(source, dest)
    app.info('done')


def add_character_admonition(self, name, image_url, label=''):
    def align(argument):
        return directives.choice(argument, ('left', 'right'))

    class CharacterAdmonition(BaseAdmonition):
        node_class = character_admonition
        option_spec = {'class': directives.class_option,
                       'name': directives.unchanged,
                       'align': align}

        def run(self):
            ret = super(CharacterAdmonition, self).run()
            ret[0]['image_url'] = image_url
            ret[0]['name'] = label
            ret[0]['align'] = self.options.get('align', 'left')
            return ret

    self.add_directive(name, CharacterAdmonition)


def setup(app):
    app.add_character_admonition = MethodType(add_character_admonition, app, Sphinx)

    app.add_node(character_admonition,
                 html=(html_visit_character_admonition, html_depart_character_admonition))
    app.connect('builder-inited', on_builder_inited)
    app.connect('build-finished', on_build_finished)

    app.add_character_admonition('usaturn',
                                 'https://pbs.twimg.com/profile_images/1365715199/md_400x400.png',
                                 u'うさたーん')
