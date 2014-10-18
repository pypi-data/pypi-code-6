import logging

from bdgt.storage.database import session_scope


_log = logging.getLogger(__name__)


def save_object(object_):
    _log.info("Saving '{}'".format(type(object_)))
    with session_scope() as session:
        session.add(object_)


def save_objects(objects):
    _log.info("Saving '{}' object".format(len(objects)))
    with session_scope() as session:
        session.add_all(objects)


def delete_object(object_):
    _log.info("Deleting '{}' with id {}".format(type(object_), object_.id))
    with session_scope() as session:
        session.delete(object_)
