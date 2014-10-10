from nose.tools import eq_
from behave import given, then

from bdgt.models import Account
from bdgt.storage.database import session_scope
from bdgt.storage.gateway import save_object


@given('the following accounts')
def step_add_accounts(context):
    for row in context.table:
        account = Account(row['name'], row['number'])
        save_object(account)


@then('account "{account_name}" exists')
def step_account_exists(context, account_name):
    with session_scope() as session:
        count = session.query(Account).filter_by(name=account_name).count()
        eq_(count, 1)


@then('account "{account_name}" doesn\'t exist')
def step_account_doesnt_exist(context, account_name):
    with session_scope() as session:
        count = session.query(Account).filter_by(name=account_name).count()
        eq_(count, 0)
