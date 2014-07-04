# -*- coding: utf-8 -*-
"""verschemes.postgresql module

The PostgreSQL versioning module implements standard
`PostgreSQL <http://www.postgresql.org/>`_
`versioning <http://www.postgresql.org/support/versioning/>`__.

"""

from verschemes import SegmentDefinition as _SegmentDefinition
from verschemes import Version as _Version


SEGMENTS = (MAJOR1, MAJOR2, MINOR) = range(3)


class PgMajorVersion(_Version):

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
        _SegmentDefinition(),
        _SegmentDefinition(),
    )

    @property
    def major_version(self):
        """Return a new `PgMajorVersion` with the object's values.

        This is mainly useful in subclasses.

        """
        return PgMajorVersion(self[MAJOR1], self[MAJOR2])


class PgVersion(PgMajorVersion):

    """A complete, specific PostgreSQL version.

    This version scheme has three segments that identify a specific release of
    PostgreSQL.

    """

    SEGMENT_DEFINITIONS = PgMajorVersion.SEGMENT_DEFINITIONS + (
        _SegmentDefinition(optional=True, default=0),
    )
