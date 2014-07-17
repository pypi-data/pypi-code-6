# -*- coding: utf-8 -*-

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from ..utils import align, alignments, get_ssl


YT_EMBED = '<iframe width="{width}" height="{height}" src="{uri}" \
        frameborder="{border}" style="display: block; margin: {align}" \
        start="{start}" class="video" allowfullscreend></iframe>'


class Youtube(Directive):

    """YouTube directive for easy embedding (`:options:` are optional).

    .. code-block:: rst

        .. youtube:: ZPJlyRv_IGI
            :start: 34
            :align: center
            :height: 1280
            :width: 729
            :privacy:
            :ssl:
    """

    required_arguments = 1
    optional_arguments = 0
    option_spec = {
        'height': directives.length_or_unitless,
        'width': directives.length_or_percentage_or_unitless,
        'border': directives.length_or_unitless,
        'align': align,
        'start': int,
        'ssl': directives.flag,
        'privacy': directives.flag,
    }
    has_content = False

    def run(self):
        """Create the html code.

        :type return: list

        """

        protocol = ('https:/' if ('ssl' in self.options or get_ssl()) else
                    'http:/')
        hostname = ('www.youtube-nocookie.com' if 'privacy' in self.options
                    else 'www.youtube.com')

        uri = '/'.join((protocol, hostname, 'embed', self.arguments[0]))

        self.options['uri'] = uri
        self.options['align'] = alignments[self.options.get('align', 'center')]

        self.options.setdefault('width', '680px')
        self.options.setdefault('height', '382px')
        self.options.setdefault('border', 0)
        self.options.setdefault('start', 0)

        global YT_EMBED
        return [nodes.raw('', YT_EMBED.format(**self.options), format='html')]


NAME = {frozenset({'youtube', 'yt'}): Youtube}

DEFAULT_CONFIG = {'FORCE_SSL': False, 'FORCE_TLS': False}
