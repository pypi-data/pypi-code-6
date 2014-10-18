import argparse
import logging
import os
import sys
from decimal import Decimal

import colorama

from bdgt import get_data_dir, get_version
from bdgt.commands.factory import CommandFactory
from bdgt.storage.database import open_database


_log = logging.getLogger(__name__)


def process_cmd(args):
    try:
        command = CommandFactory.create(args)
        output = command()
    except Exception as e:
        print "Error: {}".format(str(e))
        sys.exit(1)
    else:
        print output
        sys.exit(0)


def main():
    colorama.init()

    # Parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database',
                        help="The absolute path to the bdgt database. " +
                             "If not specified, ~/.bdgt/bdgt.db is used.")
    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(get_version()))
    subparsers = parser.add_subparsers(dest='command')

    # Account
    account_parser = subparsers.add_parser(
        'account',
        help="Manage accounts"
    )
    account_subparsers = account_parser.add_subparsers(dest='sub_command')
    account_add_parser = account_subparsers.add_parser(
        'add',
        help='Add an account'
    )
    account_add_parser.add_argument(
        'name', type=unicode,
        help="The name of the account, e.g: personal, savings."
    )
    account_add_parser.add_argument(
        'number', type=unicode,
        help="The account number for the account."
    )
    account_subparsers.add_parser(
        'list',
        help="List accounts"
    )
    account_delete_parser = account_subparsers.add_parser(
        'delete',
        help="Delete an account"
    )
    account_delete_parser.add_argument(
        'name', type=unicode,
        help="The name of the account, e.g: personal, savings."
    )

    # Import
    import_parser = subparsers.add_parser(
        'import',
        help="Import transactions"
    )
    import_parser.add_argument(
        '--commit',
        action='store_true',
        help='Commit the imported transactions immediately'
    )
    import_subparsers = import_parser.add_subparsers(dest='sub_command')
    import_file_parser = import_subparsers.add_parser(
        'file',
        help="Import transactions from a file"
    )
    import_file_parser.add_argument(
        'type_', type=unicode, choices=["csv-ing", "mt940", "ofx"],
        help="The type of the file being imported."
    )
    import_file_parser.add_argument(
        'file_',
        help="The path of the file to import."
    )
    import_subparsers.add_parser(
        'status',
        help="View the status of an import that's in progress"
    )
    import_add_parser = import_subparsers.add_parser(
        'add',
        help="Add parsed transactions to the staging area"
    )
    import_add_parser.add_argument(
        'transaction_ids', type=unicode,
        help="A comma-separated list of transaction id's. A range of id's " +
             "can be specified using '-'; e.g: 1,4,6-10,12"
    )
    import_remove_parser = import_subparsers.add_parser(
        'remove',
        help="Remove parsed transactions from the staging area"
    )
    import_remove_parser.add_argument(
        'transaction_ids', type=unicode,
        help="A comma-separated list of transaction id's. A range of id's " +
             "can be specified using '-'; e.g: 1,4,6-10,12"
    )
    import_subparsers.add_parser(
        'reset',
        help="Resets the import process."
    )
    import_subparsers.add_parser(
        'commit',
        help="Commit parsed transactions to the database."
    )
    import_set_parser = import_subparsers.add_parser(
        'set',
        help="Set the value of a field in a parsed transaction"
    )
    import_set_parser.add_argument(
        'field', type=unicode, choices=["account", "category"],
        help="The field of which the value is to be set."
    )
    import_set_parser.add_argument(
        'value', type=unicode,
        help="The value to set the field to."
    )
    import_set_parser.add_argument(
        'transaction_ids', type=unicode,
        help="A comma-separated list of transaction id's. A range of id's " +
             "can be specified using '-'; e.g: 1,4,6-10,12"
    )

    # TX
    tx_parser = subparsers.add_parser(
        'tx',
        help="Manage transactions"
    )
    tx_subparsers = tx_parser.add_subparsers(dest='sub_command')
    tx_list_parser = tx_subparsers.add_parser(
        'list',
        help="List transactions"
    )
    tx_list_parser.add_argument(
        'account_name', type=unicode,
        help="The name of the account, e.g: personal, savings."
    )
    tx_assign_parser = tx_subparsers.add_parser(
        'assign',
        help="Assign transactions to a category."
    )
    tx_assign_parser.add_argument(
        'category_name', type=unicode,
        help="The name of the category"
    )
    tx_assign_parser.add_argument(
        'transaction_ids', type=unicode,
        help="A comma-separated list of transaction id's. A range of id's " +
             "can be specified using '-'; e.g: 1,4,6-10,12"
    )
    tx_unassign_parser = tx_subparsers.add_parser(
        'unassign',
        help="Unassign a transaction from a category."
    )
    tx_unassign_parser.add_argument(
        'transaction_ids', type=unicode,
        help="A comma-separated list of transaction id's. A range of id's " +
             "can be specified using '-'; e.g: 1,4,6-10,12"
    )
    tx_reconcile_parser = tx_subparsers.add_parser(
        'reconcile',
        help="Mark transactions as reconciled."
    )
    tx_reconcile_parser.add_argument(
        'transaction_ids', type=unicode,
        help="A comma-separated list of transaction id's. A range of id's " +
             "can be specified using '-'; e.g: 1,4,6-10,12"
    )

    # Set
    set_parser = subparsers.add_parser(
        'set',
        help="Set a budget for a category."
    )
    set_parser.add_argument(
        'category_name', type=unicode,
        help="The name of the category"
    )
    set_parser.add_argument(
        'period', type=unicode, choices=["week", "month", "quarter", "year"],
        help="The period the spending limit applies to."
    )
    set_parser.add_argument(
        'amount', type=Decimal,
        help="The spending limit amount."
    )

    # TODO: Month must be between 1 and 12
    # TODO: Year must be 4 digits
    status_parser = subparsers.add_parser(
        'status',
        help="View the status of a budget for the given month and year."
    )
    status_parser.add_argument(
        'month', type=int,
    )
    status_parser.add_argument(
        'year', type=int
    )

    args = parser.parse_args()

    # Open database
    if args.database:
        open_database(args.database)
    else:
        bdgt_dir = get_data_dir()
        if not os.path.exists(bdgt_dir):
            os.makedirs(bdgt_dir)
        bdgt_db = os.path.join(bdgt_dir, "bdgt.db")
        open_database("sqlite:///{}".format(bdgt_db))

    # Process command
    process_cmd(args)
