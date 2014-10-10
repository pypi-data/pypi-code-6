import calendar
import datetime
import logging
from collections import defaultdict
from StringIO import StringIO

import asciitable
from sqlalchemy.orm.exc import NoResultFound

from bdgt.models import BudgetItem, Category
from bdgt.storage.gateway import session_scope


_log = logging.getLogger(__name__)


class CmdSet(object):
    def __init__(self, category_name, period, amount):
        self.category_name = category_name
        self.period = period
        self.amount = amount

    def __call__(self):
        # Get the category if it already exists, or create a new one.
        with session_scope() as session:
            try:
                category = session.query(Category) \
                                  .filter_by(name=self.category_name) \
                                  .one()
            except NoResultFound:
                raise ValueError("{} not found".format(self.category_name))

            budget_item = BudgetItem(datetime.datetime.now().date(),
                                     self.period, self.amount)
            category.budget_items.append(budget_item)

            session.add(category)

        return 'Budget for "{}" is set to {} per {}'.format(self.category_name,
                                                            self.amount,
                                                            self.period)


class CmdStatus(object):
    def __init__(self, month, year):
        self.month = month
        self.year = year

    def __call__(self):
        # Get the category if it already exists, or create a new one.
        with session_scope() as session:
            categories = session.query(Category) \
                                .order_by(Category.name) \
                                .all()

        output = defaultdict(list)
        for category in categories:
            # If the category doesn't have a budget set, skip it.
            if category.budget_items is None or category.budget_items == []:
                continue

            txs = category.transactions

            # Remove income transactions and transactions outside the date
            # range.
            (_, num_days) = calendar.monthrange(self.year, self.month)
            beg_date = datetime.date(self.year, self.month, 1)
            end_date = beg_date + datetime.timedelta(days=num_days)
            txs = filter(lambda x: x.is_debit(), txs)
            txs = filter(lambda x: x.is_in_period(beg_date, end_date), txs)

            # Get the budget item for this category
            budget_item = category.budget_items[-1]

            # Get the total spent for this category
            # Only include debit transactions, which have a negative amount
            spent = sum([abs(tx.amount) for tx in txs], 0)
            rem = budget_item.amount - spent

            # Calculate percentage of budget
            spent_pct = (spent / budget_item.amount) * 100.0
            rem_pct = (rem / budget_item.amount) * 100.0

            # Add data to output dict
            output['category'].append(category.name)
            output['budget'].append("{:.2f}".format(budget_item.amount))
            output['spent'].append("{:.2f} ({:.0f}%)".format(spent,
                                                             spent_pct))
            output['remaining'].append("{:.2f} ({:.0f}%)".format(rem,
                                                                 rem_pct))
            output['transactions'].append(len(txs))

        if not output:
            return "No budget set"

        output_io = StringIO()
        asciitable.write(output, output_io,
                         Writer=asciitable.FixedWidth,
                         names=['category', 'budget', 'spent', 'remaining',
                                'transactions'],)

        return output_io.getvalue()
