from sqlalchemy.orm.exc import NoResultFound

from bdgt.models import Category
from bdgt.storage.database import session_scope
from bdgt.storage.gateway import delete_object, save_object


class CmdAdd(object):
    def __init__(self, name, parent_name=None):
        self.name = name
        self.parent_name = parent_name

    def __call__(self):
        if self.parent_name is not None:
            with session_scope() as session:
                try:
                    parent = session.query(Category)\
                                    .filter_by(name=self.parent_name)\
                                    .one()
                except NoResultFound:
                    raise ValueError(
                        "Category '{}' does not exist.".format(
                            self.parent_name))
            assert parent is not None

            category = Category(self.name, parent)
            save_object(category)
            return "Subcategory '{}' created.".format(self.name)
        else:
            category = Category(self.name)
            save_object(category)
            return "Category '{}' created.".format(self.name)


class CmdDelete(object):
    def __init__(self, name):
        self.name = name

    def __call__(self):
        with session_scope() as session:
            try:
                category = session.query(Category)\
                                  .filter_by(name=self.name)\
                                  .one()
            except NoResultFound:
                raise ValueError(
                    "Category '{}' does not exist.".format(
                        self.name))
        delete_object(category)
        return "Category '{}' deleted.".format(self.name)


class CmdRename(object):
    def __init__(self, name, new_name):
        self.name = name
        self.new_name = new_name

    def __call__(self):
        with session_scope() as session:
            try:
                category = session.query(Category)\
                                  .filter_by(name=self.name)\
                                  .one()
            except NoResultFound:
                raise ValueError(
                    "Category '{}' does not exist.".format(
                        self.name))

        category.name = self.new_name
        save_object(category)
        return "Category '{}' renamed to '{}'.".format(self.name,
                                                       self.new_name)
