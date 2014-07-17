# -*- coding: utf-8 -*-

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from ..utils import align, alignments, get_ssl, color


VI_EMBED = '<iframe width="{width}" height="{height}" src="{uri}" \
        frameborder="{border}" style="display: block; margin: {align}" \
        class="video" webkitAllowFullScreen mozallowfullscreen \
        allowfullscreen </iframe>'


class Vimeo(Directive):

    """Vimeo directive for easy embedding (`:options:` are optional).

    .. code-block:: rst

        .. vimeo:: 6455561
            :align: center
            :height: 1280
            :width: 720
            :border: 1px
            :color: ffffff
            :nobyline:
            :noportrait:
            :notitle:
            :autoplay:
            :loop:
            :ssl:
    """

    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        'height': directives.length_or_unitless,
        'width': directives.length_or_unitless,
        'align': align,
        'border': directives.length_or_unitless,
        'color': color,
        'noportrait': directives.flag,
        'notitle': directives.flag,
        'nobyline': directives.flag,
        'autoplay': directives.flag,
        'loop': directives.flag,
        'ssl': directives.flag,
    }
    has_content = False

    def run(self):
        """Create the html code.

        :type return: list

        """

        self.options.setdefault('color', '00adef')

        protocol = ('https:/' if ('ssl' in self.options or get_ssl()) else
                    'http:/')
        hostname = '/'.join((protocol, 'player.vimeo.com/video',
                             self.arguments[0]))

        color = '?color={color}&'.format(color=self.options['color'])
        title = 'title=0&' if 'notitle' in self.options else ''
        portrait = 'portrait=0&' if 'noportrait' in self.options else ''
        byline = 'byline=0&' if 'nobyline' in self.options else ''
        autoplay = 'autoplay=1&' if 'autoplay' in self.options else ''
        loop = 'loop=1' if 'loop' in self.options else ''

        self.options['uri'] = ''.join((hostname, color, title, portrait,
                                       byline, autoplay, loop))
        self.options['align'] = alignments[self.options.get('align', 'center')]
        self.options.setdefault('width', '500px')
        self.options.setdefault('height', '281px')
        self.options.setdefault('border', '0')

        global VI_EMBED
        return [nodes.raw('', VI_EMBED.format(**self.options), format='html')]


NAME = {frozenset({'vimeo', 'vi'}): Vimeo}

DEFAULT_CONFIG = {'FORCE_SSL': False, 'FORCE_TLS': False}
