from nose.tools import eq_, with_setup
from sqlalchemy import create_engine

from bdgt.commands.accounts import (CmdAddAccount, CmdDeleteAccount,
                                    CmdListAccounts)
from bdgt.models import Account
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
def test_cmd_add_account():
    CmdAddAccount(u'test', u'987654321')()
    with session_scope() as session:
        num = session.query(Account).filter_by(name=u"test").count()
        eq_(num, 1)


@with_setup(setup, teardown)
def test_cmd_delete_account():
    CmdAddAccount(u'test', u'987654321')()
    CmdDeleteAccount(u'test')()
    with session_scope() as session:
        num = session.query(Account).filter_by(name=u"test").count()
        eq_(num, 0)


@with_setup(setup, teardown)
def test_cmd_list_accounts():
    CmdAddAccount(u'test1', u'987654321')()
    CmdAddAccount(u'test2', u'876543219')()
    CmdAddAccount(u'test3', u'765432198')()
    output = CmdListAccounts()()
    eq_(output, 'test1\ntest2\ntest3\n')
