import datetime

from behave import given

from bdgt.models import BudgetItem, Category
from bdgt.storage.database import session_scope


@given('the following budget items')
def step_add_categories(context):
    """
    Add budget items from a table in the format given below

    | category | period | amount |
    | cat1     | month  | 100.00 |
    """
    for row in context.table:
        with session_scope() as session:
            category = session.query(Category) \
                              .filter_by(name=row['category']) \
                              .one()
        budget_item = BudgetItem(datetime.datetime.now(), row['period'],
                                 row['amount'])

        category.budget_items.append(budget_item)
        session.add(category)
