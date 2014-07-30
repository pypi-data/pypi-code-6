# -*- coding: utf-8 -*-
"""verschemes.pep440 module

The PEP 440 verschemes module implements standard
`PEP 440 <http://legacy.python.org/dev/peps/pep-0440/>`_
`public <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
versioning.  PEP 440
`local <http://legacy.python.org/dev/peps/pep-0440/#local-version-identifiers>`_
versions are not supported by this module; they are just public versions with a
hyphen and a numeric version (as implemented by the defaults in the base
`verschemes.Version` class) appended.

This implementation is limited to six release-number segments, which should
handle any reasonable scheme.

"""

# Support Python 2 & 3.
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from verschemes.future import *

from verschemes import SegmentDefinition, SegmentField, Version
from verschemes._types import int_empty_zero


__all__ = []

__all__.extend(['SEGMENTS', 'EPOCH', 'RELEASE1', 'RELEASE2', 'RELEASE3',
                'RELEASE4', 'RELEASE5', 'RELEASE6', 'PRE_RELEASE',
                'POST_RELEASE', 'DEVELOPMENT'])
SEGMENTS = (
    EPOCH,
    RELEASE1,
    RELEASE2,
    RELEASE3,
    RELEASE4,
    RELEASE5,
    RELEASE6,
    PRE_RELEASE,
    POST_RELEASE,
    DEVELOPMENT,
) = tuple(range(10))

__all__.append('RELEASE_SEGMENTS')
RELEASE_SEGMENTS = SEGMENTS[:PRE_RELEASE]

__all__.append('NONRELEASE_SEGMENTS')
NONRELEASE_SEGMENTS = SEGMENTS[PRE_RELEASE:]


def _pre_release_level_render(value):
    value = value.lower()
    if len(value) > 1:
        if value == 'rc':
            value = 'c'
        else:
            value = value[0]
    return value


__all__.append('Pep440Version')
class Pep440Version(Version):

    """A PEP 440 public version.

    The version scheme has an optional `epoch` segment followed by up to six
    release-number segments (named 'releaseX', where X is 1-6) followed by the
    optional `pre_release`, `post_release`, and `development` segments.

    `~verschemes.Version.SEGMENT_DEFINITIONS` contains the following named
    segments in order:

    * epoch: optional=True, default=0

    * release1: default=0, separator='!'

    * release2: optional=True, default=0

    * release3: optional=True, default=0

    * release4: optional=True, default=0

    * release5: optional=True, default=0

    * release6: optional=True, default=0

    * pre_release: optional=True, separator='', separator_re_pattern='[.-]?'
        * field 'level': type=str (case-insensitive input)
            * normal form 'a' accepts 'a' or 'alpha'
            * normal form 'b' accepts 'b' or 'beta'
            * normal form 'c' accepts 'c' or 'rc'
        * field 'serial': type=int_empty_zero, re_pattern='[0-9]*'

    * post_release: optional=True, separator='.post', separator_re_pattern='[.-]?post'
        * field: type=int_empty_zero, re_pattern='[0-9]*'

    * development: optional=True, separator='.dev', separator_re_pattern='[.-]?dev'
        * field: type=int_empty_zero, re_pattern='[0-9]*'

    """

    SEGMENT_DEFINITIONS = (
        SegmentDefinition(
            name='epoch',
            optional=True,
            default=0,
        ),
        SegmentDefinition(
            name='release1',
            default=0,
            separator='!',
        ),
        SegmentDefinition(
            name='release2',
            optional=True,
            default=0,
        ),
        SegmentDefinition(
            name='release3',
            optional=True,
            default=0,
        ),
        SegmentDefinition(
            name='release4',
            optional=True,
            default=0,
        ),
        SegmentDefinition(
            name='release5',
            optional=True,
            default=0,
        ),
        SegmentDefinition(
            name='release6',
            optional=True,
            default=0,
        ),
        SegmentDefinition(
            name='pre_release',
            optional=True,
            separator='',
            separator_re_pattern='[.-]?',
            fields=(
                SegmentField(
                    type=str,
                    name='level',
                    re_pattern=('[aAbBcC]|'
                                '[aA][lL][pP][hH][aA]|'
                                '[bB][eE][tT][aA]|'
                                '[rR][cC]'),
                    render=_pre_release_level_render
                ),
                SegmentField(
                    type=int_empty_zero,
                    name='serial',
                    re_pattern='[0-9]*',
                ),
            ),
        ),
        SegmentDefinition(
            name='post_release',
            optional=True,
            separator='.post',
            separator_re_pattern='[.-]?post',
            fields=(
                SegmentField(
                    type=int_empty_zero,
                    re_pattern='[0-9]*',
                ),
            ),
        ),
        SegmentDefinition(
            name='development',
            optional=True,
            separator='.dev',
            separator_re_pattern='[.-]?dev',
            fields=(
                SegmentField(
                    type=int_empty_zero,
                    re_pattern='[0-9]*',
                ),
            ),
        ),
    )

    @property
    def is_release(self):
        """Whether this version represents a final release.

        Return `True` if all of the 'pre_release', 'post_release', and
        'development' segments have no value.

        """
        return all(self[x] is None for x in NONRELEASE_SEGMENTS)

    def _render_exclude_defaults_callback(self, index, scope=None):
        if scope is None:
            scope = list(RELEASE_SEGMENTS)
            scope.remove(EPOCH)
        return super()._render_exclude_defaults_callback(index, scope)

    def _render_include_min_release_callback(self, index,
                                             min_release_segments):
        return RELEASE1 <= index < RELEASE1 + min_release_segments

    def render(self, exclude_defaults=True, include_callbacks=(),
               exclude_callbacks=(), min_release_segments=1):
        """Override to provide the `min_release_segments` option."""
        include_callbacks = list(include_callbacks)
        include_callbacks.append(
            (type(self)._render_include_min_release_callback,
             min_release_segments))
        return super().render(exclude_defaults, include_callbacks,
                              exclude_callbacks)
