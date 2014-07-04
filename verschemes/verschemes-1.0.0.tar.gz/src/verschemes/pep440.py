# -*- coding: utf-8 -*-
"""verschemes.pep440 module

The PEP 440 versioning module implements standard
`PEP 440 <http://legacy.python.org/dev/peps/pep-0440/>`_
`public <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
versioning.  PEP 440
`local <http://legacy.python.org/dev/peps/pep-0440/#local-version-identifiers>`_
versions are not supported by this module; they are just public versions with a
hyphen and a numeric version (as implemented by the defaults in the base
`verschemes.Version` class) appended.

"""

from verschemes import SegmentDefinition as _SegmentDefinition
from verschemes import SegmentField as _SegmentField
from verschemes import Version as _Version


RELEASE_SEGMENTS = (
    EPOCH,
    RELEASE1,
    RELEASE2,
    RELEASE3,
    RELEASE4,
    RELEASE5,
    RELEASE6
) = tuple(range(7))

NONRELEASE_SEGMENTS = (
    PRE_RELEASE,
    POST_RELEASE,
    DEVELOPMENT
) = tuple(range(-3, 0))

SEGMENTS = RELEASE_SEGMENTS + NONRELEASE_SEGMENTS


class Pep440Version(_Version):

    SEGMENT_DEFINITIONS = (
        _SegmentDefinition(  # EPOCH
            optional=True,
            default=0,
        ),
        _SegmentDefinition(  # RELEASE1
            default=0,
            separator=':',
        ),
        _SegmentDefinition(  # RELEASE2
            optional=True,
            default=0,
        ),
        _SegmentDefinition(  # RELEASE3
            optional=True,
            default=0,
        ),
        _SegmentDefinition(  # RELEASE4
            optional=True,
            default=0,
        ),
        _SegmentDefinition(  # RELEASE5
            optional=True,
            default=0,
        ),
        _SegmentDefinition(  # RELEASE6
            optional=True,
            default=0,
        ),
        _SegmentDefinition(  # PRE_RELEASE
            optional=True,
            separator='',
            fields=(
                _SegmentField(
                    type=str,
                    name='level',
                    re_pattern='[abc]|rc',
                ),
                _SegmentField(
                    name='serial',
                ),
            ),
        ),
        _SegmentDefinition(  # POST_RELEASE
            optional=True,
            separator='.post',
        ),
        _SegmentDefinition(  # DEVELOPMENT
            optional=True,
            separator='.dev',
        ),
    )

    def __init__(self, epoch_or_string=None, release1=None, release2=None,
                 release3=None, release4=None, release5=None, release6=None,
                 pre_release=None, post_release=None, development=None):
        _super = super(Pep440Version, self).__init__
        if (release1 is None and release2 is None and release3 is None and
            release4 is None and release5 is None and release6 is None and
            pre_release is None and post_release is None and
            development is None):
            _super(epoch_or_string)
        else:
            _super(epoch_or_string, release1, release2, release3, release4,
                   release5, release6, pre_release, post_release, development)

    @property
    def is_release(self):
        return all([self[x] is None for x in NONRELEASE_SEGMENTS])

    def _render_exclude_defaults_callback(self, index, scope=None):
        if scope is None:
            scope = list(RELEASE_SEGMENTS)
            scope.remove(EPOCH)
        return (super(Pep440Version, self)
                ._render_exclude_defaults_callback(index, scope))

    def _render_include_min_release_callback(self, index,
                                             min_release_segments):
        return RELEASE1 <= index < RELEASE1 + min_release_segments
        # if segment_index < RELEASE1 or segment_index > min_release_segments:
        #     return False
        # segment = self.segments[segment_index]
        # return segment.definition.optional and segment._value is None

    def render(self, exclude_defaults=True, include_callbacks=(),
               exclude_callbacks=(), min_release_segments=1):
        include_callbacks = list(include_callbacks)
        include_callbacks.append((self._render_include_min_release_callback,
                                  min_release_segments))
        return super(Pep440Version, self).render(exclude_defaults,
                                                 include_callbacks,
                                                 exclude_callbacks)
