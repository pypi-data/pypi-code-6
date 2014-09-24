from __future__ import unicode_literals

from pygments.token import Token

__all__ = (
    'LeftMargin',
    'LeftMarginWithLineNumbers',
)


class LeftMargin(object):
    def __init__(self, width=10, token=None):
        self.width = width
        self.token = token or Token.Layout.LeftMargin

    def write(self, cli, screen, line_number):
        screen.write_highlighted([
            (self.token, '.' * self.width)
        ])


class LeftMarginWithLineNumbers(LeftMargin):
    width = 10

    def write(self, cli, screen, line_number):
        screen.write_highlighted([
            (self.token, '%%%ii. ' % (self.width - 2) % (line_number + 1)),
        ])
