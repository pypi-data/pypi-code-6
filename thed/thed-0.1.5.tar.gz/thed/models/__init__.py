from __future__ import unicode_literals
import inspect

from sqlalchemy.ext.declarative import api, declarative_base
from sqlalchemy.orm.exc import DetachedInstanceError

from thed.db import metadata


class Model(object):

    @classmethod
    def __declare_last__(cls):
        for base_cls in inspect.getmro(cls):
            if '_register_' in base_cls.__dict__:
                base_cls._register_(cls)
        return cls

    def __init__(self, **kwargs):
        """
        Initializes a model by invoking the _declarative_constructor
        in SQLAlchemy. We do this for full control over construction
        of an object
        """
        api._declarative_constructor(self, **kwargs)

    def __repr__(self):
        cols = self.__mapper__.c.keys()
        class_name = self.__class__.__name__
        try:
            items = ', '.join([
                '%s=%s' % (col, repr(getattr(self, col))) for col in cols
            ])
        except DetachedInstanceError:
            items = '<detached>'
        return '%s(%s)' % (class_name, items)


DBModel = declarative_base(
    cls=Model,
    constructor=None,
    metadata=metadata,
)


def init(settings):
    DBModel.query = settings['session']
    return settings
