from nose.tools import eq_, with_setup
from sqlalchemy import create_engine

from bdgt.commands.categories import CmdAdd
from bdgt.models import Category
from bdgt.storage.database import Base, Session, session_scope


def setup():
    global engine
    engine = create_engine('sqlite://', echo=False)
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)


def teardown():
    engine.dispose()
    Session.remove()


@with_setup(setup, teardown)
def test_cmd_add():
    CmdAdd(u'category1')()
    with session_scope() as session:
        num = session.query(Category).filter_by(name=u"category1").count()
        eq_(num, 1)


@with_setup(setup, teardown)
def test_cmd_add_subcategory():
    CmdAdd(u'category1')()
    CmdAdd(u'category2', u'category1')()
    with session_scope() as session:
        category2 = session.query(Category).filter_by(name=u"category2").one()
        eq_(category2.parent.name, u'category1')
        category1 = session.query(Category).filter_by(name=u"category1").one()
        eq_(len(category1.subcategories), 1)
