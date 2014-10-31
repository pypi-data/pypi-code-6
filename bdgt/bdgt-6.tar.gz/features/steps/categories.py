from nose.tools import eq_
from behave import given, then

from bdgt.models import Category, Transaction
from bdgt.storage.database import session_scope
from bdgt.storage.gateway import save_object


@given('the following categories')
def step_add_categories(context):
    """
    Add categories from a table in the format given below

    | name |
    | cat1 |
    """
    for row in context.table:
        cat = Category(row['name'])
        save_object(cat)


@then('category "{category_name}" exists')
def step_category_exists(context, category_name):
    with session_scope() as session:
        count = session.query(Category).filter_by(name=category_name).count()
        eq_(count, 1)


@then('category "{category_name}" has {num_txs:n} transactions')
def step_num_txs_in_category(context, category_name, num_txs):
    with session_scope() as session:
        count = session.query(Transaction) \
                       .filter(Transaction.category.has(name=category_name)) \
                       .count()
        eq_(count, num_txs)


@then('"{category_name}" has {num_budget_items:n} budget items')
def step_num_budget_items_in_category(context, category_name,
                                      num_budget_items):
    with session_scope() as session:
        category = session.query(Category).filter_by(name=category_name).one()
        eq_(num_budget_items, len(category.budget_items))
