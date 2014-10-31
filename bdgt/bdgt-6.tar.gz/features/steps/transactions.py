import datetime

from behave import given, then
from nose.tools import eq_

from bdgt.models import Account, Category, Transaction
from bdgt.storage.database import session_scope
from bdgt.storage.gateway import save_object


@given('the following transactions')
def step_add_transactions(context):
    """
    Add transactions from a table in the format given below

    | account | date       | desc | amount | reconciled | category |
    | test    | 01-01-2014 |      | 100.0  | False      | cat1     |

    Where category is optional.
    """
    for row in context.table:
        with session_scope() as session:
            account = session.query(Account) \
                             .filter_by(name=row['account']) \
                             .one()
        tx = Transaction(account,
                         datetime.datetime.strptime(row['date_time'],
                                                    '%d-%m-%Y'),
                         row['desc'],
                         float(row['amount']),
                         True if row['reconciled'] == 'True' else False)

        if 'category' in row.as_dict():
            with session_scope() as session:
                category = session.query(Category) \
                                  .filter_by(name=row['category']) \
                                  .one()
            tx.category = category
        save_object(tx)


@then('account "{account_name}" has {count:n} unreconciled transactions')
def step_unreconciled_transactions(context, account_name, count):
    with session_scope() as session:
        account = session.query(Account).filter_by(name=account_name).one()
        unreconciled_count = 0
        for tx in account.transactions:
            if not tx.reconciled:
                unreconciled_count += 1
        eq_(count, unreconciled_count)
