# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2014 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU Affero General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
#  more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################

"""
Database Stuff
"""

from sqlalchemy.orm import sessionmaker

from .util import get_default_engine


Session = sessionmaker()


def configure_session_factory(config, session_factory=None):
    """
    Configure a session factory using the provided settings.

    :param config: Object containing database configuration.

    :param session_factory: Optional session factory; if none is specified then
        :attr:`Session` will be assumed.
    """
    from .changes import record_changes

    if session_factory is None:
        session_factory = Session

    engine = get_default_engine(config)
    if engine:
        session_factory.configure(bind=engine)

    ignore_role_changes = config.getboolean(
        'rattail.db', 'changes.ignore_roles', default=True)

    if config.getboolean('rattail.db', 'changes.record'):
        record_changes(session_factory, ignore_role_changes)
