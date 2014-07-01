from __future__ import unicode_literals

from sqlalchemy import engine_from_config, MetaData
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


metadata = MetaData()


def init(settings):
    if 'db.engine' not in settings:
        settings['db.engine'] = (
            engine_from_config(settings, 'sqlalchemy.')
        )

    if 'session' not in settings:
        settings['session'] = scoped_session(sessionmaker(
            bind=settings['db.engine'],
        ))
    return settings
