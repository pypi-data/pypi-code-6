import logging

logger = logging.getLogger(__name__)


def save_instance(session, instance):
    """
    Save an instance of a model object.
    If we already have staged changes, commit them first and then save.
    """
    created = instance.id is None
    success = False
    try:
        session.merge(instance)
        session.commit()
        success = True
    except Exception:
        logger.exception("Exception while attempting to save an instance.")
        session.rollback()
        created = False

    if not success:
        logger.error("Failed to save instance! TODO PRINT ME SOME MORE INFO")

    return success, created


def query(session, model, **kwargs):
    try:
        if len(kwargs.keys()):
            return session.query(model).filter_by(**kwargs).all()
        else:
            return session.query(model).all()
    except:
        session.expunge()
        raise


def get(session, model, **kwargs):
    results = query(session, model, **kwargs)
    if len(results) > 1:
        raise Exception("Query for: '%s' returned more than 1 result!")
    if len(results):
        return results[0]
    return None