import datetime

from nose.tools import eq_

from bdgt.models import Account, Transaction


def test_is_debit():
    account = Account(u"test", u"12345")
    tx = Transaction(account, datetime.datetime.now(), u"desc", 10.0)
    eq_(tx.is_debit(), False)

    tx = Transaction(account, datetime.datetime.now(), u"desc", -10.0)
    eq_(tx.is_debit(), True)

    tx = Transaction(account, datetime.datetime.now(), u"desc", 0.0)
    eq_(tx.is_debit(), False)


def test_is_credit():
    account = Account(u"test", u"12345")
    tx = Transaction(account, datetime.datetime.now(), u"desc", 10.0)
    eq_(tx.is_credit(), True)

    tx = Transaction(account, datetime.datetime.now(), u"desc", -10.0)
    eq_(tx.is_credit(), False)

    tx = Transaction(account, datetime.datetime.now(), u"desc", 0.0)
    eq_(tx.is_credit(), False)


def test_is_in_period():
    account = Account(u"test", u"12345")
    tx = Transaction(account, datetime.date(1859, 11, 24),
                     u"on the origin of species", 13.90)
    eq_(tx.is_in_period(datetime.date(1859, 11, 1),
                        datetime.date(1859, 11, 30)), True)
    eq_(tx.is_in_period(datetime.date(1859, 10, 1),
                        datetime.date(1859, 11, 30)), True)
    eq_(tx.is_in_period(datetime.date(1859, 10, 1),
                        datetime.date(1859, 10, 30)), False)

    tx = Transaction(account, datetime.date(2000, 01, 01), u"desc", 13.90)
    eq_(tx.is_in_period(datetime.date(2000, 01, 1),
                        datetime.date(2000, 01, 31)), True)

    tx = Transaction(account, datetime.date(2000, 01, 31), u"desc", 13.90)
    eq_(tx.is_in_period(datetime.date(2000, 01, 1),
                        datetime.date(2000, 01, 31)), True)
