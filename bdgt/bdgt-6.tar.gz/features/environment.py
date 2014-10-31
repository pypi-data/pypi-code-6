import os
import shlex
import subprocess

from bdgt.storage.database import open_database, session_scope
from bdgt.models import Account, BudgetItem, Category, Transaction


TOP = os.path.join(os.path.dirname(__file__), "..")


class Command(object):
    COMMAND_MAP = {
        "bdgt": {
            "bin": os.path.normpath("{0}/bin/bdgt".format(TOP)),
        }
    }

    @classmethod
    def run(cls, cmd, args):
        cmd_split = shlex.split(cmd)
        given_cmd = cmd_split[0]
        if given_cmd in cls.COMMAND_MAP:
            if args is not None:
                for arg in reversed(args):
                    cmd_split.insert(1, arg)
            cmd_split[0] = cls.COMMAND_MAP[given_cmd]["bin"]

        try:
            output = subprocess.check_output(cmd_split)
            exit_code = 0
        except subprocess.CalledProcessError as e:
            output = e.output
            exit_code = e.returncode
        print output
        return exit_code, output


def before_tag(context, tag):
    if tag == 'database.none':
        context.db_location = None
    elif tag == 'database.default':
        context.db_location = 'sqlite:///test.db'
        open_database(context.db_location)


def after_tag(context, tag):
    if context.db_location is not None:
        if context.db_location.startswith('sqlite'):
            os.remove(context.db_location[10:])
        context.db_location = None


def before_scenario(context, scenario):
    if context.db_location is not None:
        # Ensure that the database is indeed empty
        with session_scope() as session:
            assert session.query(Account).count() == 0
            assert session.query(BudgetItem).count() == 0
            assert session.query(Category).count() == 0
            assert session.query(Transaction).count() == 0

    # Give the context a test_data_files list
    context.test_data_files = []


def after_scenario(context, scenario):
    if context.db_location is not None:
        # Clear all records from the database
        with session_scope() as session:
            session.query(Account).delete()
            session.query(BudgetItem).delete()
            session.query(Category).delete()
            session.query(Transaction).delete()

    for test_data_file in context.test_data_files:
        os.remove(test_data_file)


def before_all(context):
    # Add the command executor to the context so steps can execute commands via
    # subprocess.
    context.cmd_line = Command

    # Create .bdgt data folder
    data_dir = os.path.expanduser('~/.bdgt')
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)


def after_all(context):
    if os.path.exists('example.db'):
        os.remove('example.db')
