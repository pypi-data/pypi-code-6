# -*- coding: utf-8 -*-
"""versioning.xorg module

The X.org versioning module implements standard `X.org <http://www.x.org/>`_
`version number scheme
<http://www.x.org/wiki/Development/Documentation/VersionNumberScheme/>`_.

"""

from verschemes import SegmentDefinition as _SegmentDefinition
from verschemes import Version as _Version


SEGMENTS = (
    MAJOR,
    MINOR,
    PATCH,
    SNAPSHOT,
) = tuple(range(4))


class XorgVersion(_Version):

    SEGMENT_DEFINITIONS = (
        _SegmentDefinition(),  # MAJOR
        _SegmentDefinition(  # MINOR
            default=0,
        ),
        _SegmentDefinition(  # PATCH
            default=0,
        ),
        _SegmentDefinition(  # SNAPSHOT
            optional=True,
            default=0,
        ),
    )

    def __init__(self, major_or_string=None, minor=None, patch=None,
                 snapshot=None):
        _super = super(XorgVersion, self).__init__
        if minor is None and patch is None and snapshot is None:
            _super(major_or_string)
        else:
            _super(major_or_string, minor, patch, snapshot)

    @property
    def is_release(self):
        return self[SNAPSHOT] is None

# TODO: Add validation for 99 patch and 900+ snapshot.
