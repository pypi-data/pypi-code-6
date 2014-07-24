"""
Utilities that apply across a broad variety of categories.
"""

import core


class Id(core.Shader):
    """ Return the input unchanged.

    This DOES NOT make a copy of the input
    It is usually used a zero-cost placeholder.
    """

    def shade(self, grid):
        return grid


class EmptyList(object):
    """
    Utility that can be numerically indexed, but
    always returns None (no matter what index is passed).

    This is used as a stand-in for a list when doing co-iteration
    on other lists.
    """

    def __getitem__(self, idx):
        return None
