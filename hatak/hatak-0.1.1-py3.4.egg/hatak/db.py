from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import AbstractConcreteBase

DeclatativeBase = declarative_base()


def get_or_create(model, session, **kwargs):
    try:
        return session.query(model).filter_by(**kwargs).one()
    except NoResultFound:
        created = model(**kwargs)
        try:
            session.add(created)
            session.commit()
            return created
        except IntegrityError:
            session.rollback()
            return session.query(model).filter_by(**kwargs).one()


class Base(AbstractConcreteBase, DeclatativeBase):

    @classmethod
    def get_or_create(cls, *args, **kwargs):
        return get_or_create(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = None

    def assign_request(self, request):
        self.request = request
        self.registry = request.registry
