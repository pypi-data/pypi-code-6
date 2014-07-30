# -*- coding: utf-8 -*-
"""verschemes.postgresql module

The PostgreSQL verschemes module implements standard
`PostgreSQL <http://www.postgresql.org/>`_
`versioning <http://www.postgresql.org/support/versioning/>`__.

"""

# Support Python 2 & 3.
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from verschemes.future import *

from verschemes import SegmentDefinition, Version


__all__ = []

__all__.extend(['SEGMENTS', 'MAJOR1', 'MAJOR2', 'MINOR'])
SEGMENTS = (MAJOR1, MAJOR2, MINOR) = tuple(range(3))


__all__.append('PgMajorVersion')
class PgMajorVersion(Version):

    """A major PostgreSQL version.

    This version scheme has two segments that identify the major PostgreSQL
    version, which includes new features and requires a dump/reload of the
    database or use of the pg_upgrade module.  It is the base for the more
    detailed PostgreSQL version classes and is mostly only useful itself for
    comparison.  For example:

    >>> pg83 = PgMajorVersion(8.3)
    >>> my_version = PgVersion('8.3.4')
    >>> assert(my_version.major_version == pg83)

    """

    SEGMENT_DEFINITIONS = (
        SegmentDefinition(
            name='major1',
        ),
        SegmentDefinition(
            name='major2',
        ),
    )

    @property
    def major_version(self):
        """Return a new `PgMajorVersion` with the object's values.

        This is mainly useful in subclasses.

        """
        return PgMajorVersion(self[MAJOR1], self[MAJOR2])


__all__.append('PgVersion')
class PgVersion(PgMajorVersion):

    """A complete, specific PostgreSQL version.

    This version scheme has three segments that identify a specific release of
    PostgreSQL.

    """

    SEGMENT_DEFINITIONS = PgMajorVersion.SEGMENT_DEFINITIONS + (
        SegmentDefinition(
            name='minor',
            optional=True,
            default=0,
        ),
    )
