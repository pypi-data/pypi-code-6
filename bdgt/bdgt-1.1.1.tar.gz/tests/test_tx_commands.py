import datetime

from nose.tools import eq_, with_setup
from sqlalchemy import create_engine

from bdgt.commands.transactions import CmdAssignTx
from bdgt.models import Account, Transaction, Category
from bdgt.storage.database import Base, Session, session_scope
from bdgt.storage.gateway import save_object


def setup():
    global engine
    engine = create_engine('sqlite://', echo=False)
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)


def teardown():
    engine.dispose()
    Session.remove()


def test_cmd_assign_tx_parse_tx_ids():
    cmd = CmdAssignTx(u'cat1', u'1,2,3')
    eq_(cmd.tx_ids, [1, 2, 3])


def test_cmd_assign_tx_parse_tx_ids_range():
    cmd = CmdAssignTx(u'cat1', u'10-15')
    eq_(cmd.tx_ids, [10, 11, 12, 13, 14, 15])


def test_cmd_assign_tx_parse_tx_ids_mixture():
    cmd = CmdAssignTx(u'cat1', u'1,3,7,10-15,9')
    eq_(cmd.tx_ids, [1, 3, 7, 9, 10, 11, 12, 13, 14, 15])


def test_cmd_assign_tx_parse_tx_ids_mixture_remove_duplicates():
    cmd = CmdAssignTx(u'cat1', u'1,3,3,10-15,11,1')
    eq_(cmd.tx_ids, [1, 3, 10, 11, 12, 13, 14, 15])


@with_setup(setup, teardown)
def test_cmd_assign_tx_similar_category():
    account = Account(u'test', u'12345')
    save_object(account)
    save_object(Category(u'cat1'))
    save_object(Transaction(account,
                            datetime.datetime.now().date(), u'desc', 1.0))

    CmdAssignTx(u'Cat1', '1')()

    with session_scope() as session:
        count = session.query(Category).count()
        eq_(count, 1)
