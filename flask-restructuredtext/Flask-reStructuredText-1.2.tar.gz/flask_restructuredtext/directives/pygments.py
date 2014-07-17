# -*- coding: utf-8 -*-

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from flask import current_app

from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter
from pygments.styles import get_all_styles

STYLE_NAMES = tuple(get_all_styles())


def styles(argument):
    return directives.choice(argument, STYLE_NAMES)


class Pygments(Directive):

    required_arguments = 0
    optional_arguments = 1
    option_spec = {
        'style': styles,
        'linenos': directives.flag,
        'linenostart': directives.nonnegative_int,
        'hl_lines': directives.positive_int_list,
    }
    has_content = True

    def run(self):

        lineos_test = 'linenos' in self.options

        self.options['linenos'] = 'inline' if lineos_test else False
        self.options.setdefault('linenostart', 1)
        self.options.setdefault('hl_lines', [])

        style_test = ('style' in self.options and
                      current_app.config['PYGMENTS_STYLE']
                      != self.options['style'])

        self.options['noclasses'] = True if style_test else False

        self.content = '\n'.join(self.content)

        if self.arguments:
            lexer = get_lexer_by_name(self.arguments[0])
        else:
            lexer = guess_lexer(self.content)

        html = highlight(self.content, lexer, HtmlFormatter(**self.options))

        return [nodes.raw('', html, format='html')]

NAME = {
    frozenset({'pygments', 'sourcecode', 'code', 'code-block'}): Pygments,
}

DEFAULT_CONFIG = {
    'PYGMENTS_STYLE': 'default',
}


def get_style_css(style):
    return HtmlFormatter(style=style).get_style_defs()

CONTEXT_PROCESSOR = {
    'get_style_css': get_style_css
}
