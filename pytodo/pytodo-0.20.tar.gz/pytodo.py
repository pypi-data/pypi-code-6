"""pytodo, a simple command line todo application

Usage:
  t  add <task>
  t  check <id>
  t  uncheck <id>
  t  clear
  t  ls [--all]
  t  -h | --help
  t  --version

Commands:
  add           Add a new task
  check         Check a new task as done
  uncheck       Uncheck a task as done
  clear         Refresh the database
  ls            List all tasks

Options:
  -h --help     Show this screen.
  --version     Show version.
  --all         List all tasks
"""
import sqlite3
import os
import datetime
from docopt import docopt
from termcolor import colored
from prettytable import PrettyTable

SMILEY = "\xF0\x9F\x98\x83"  # Smiley emoji
GRIN = "\xF0\x9F\x98\x81"  # Grin face emoji


def echo(msg, err=False):
    """
    A simple function for printing to terminal with colors and emoji's
    """
    if err:
        print colored(msg + " " + GRIN, "red")
    else:
        print colored(msg + " " + SMILEY, "cyan")


class Todo(object):

    def __init__(self):
        """
        Set up the db and docopt upon creation of object
        """
        # Create a path to store the database file
        db_path = os.path.expanduser("~/")
        self.db_path = db_path + "/" + ".t-db"
        self._init_db()
        self.arg = docopt(__doc__, version=0.20)

    def _init_db(self):
        self.db = sqlite3.connect(self.db_path)
        self.cursor = self.db.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS todo(id INTEGER PRIMARY KEY, task TEXT,
            done INT, date_added TEXT, date_completed TEXT)
            ''')
        self.db.commit()

    def run(self):
        """
        Parse the arg's using docopt and route to the respoctive methods
        """
        if self.arg['add']:
            self.add_task()
        elif self.arg['check']:
            self.check_task()
        elif self.arg['uncheck']:
            self.uncheck_task()
        elif self.arg['clear']:
            self.clear_task()
        else:
            if self.arg['--all']:
                self.list_task()
            else:
                self.list_pending_tasks()

    def _record_exists(self, id):
        """
        Checks if the record exists in the db
        """
        self.cursor.execute('''
            SELECT * FROM todo WHERE id=?
          ''', (id,))
        record = self.cursor.fetchone()
        if record is None:
            return False
        return True

    def add_task(self):
        """
        Add a task todo to the db
        """
        task = self.arg['<task>']
        date = datetime.datetime.now()
        date_now = "%s-%s-%s" % (date.day, date.month, date.year)
        self.cursor.execute('''
          INSERT INTO todo(task, done, date_added)
          VALUES (?, ?, ?)
        ''', (str(task), 0, date_now))
        self.db.commit()
        echo("The task has been been added to the list")

    def _is_done(self, id):
        self.cursor.execute('''
                SELECT done FROM todo WHERE id=?
            ''', (id,))
        record = self.cursor.fetchone()
        if record[0] == 0:
            return
        else:
            return True

    def check_task(self):
        """
        Mark a task as done
        """
        task_id = self.arg['<id>']
        date = datetime.datetime.now()
        date_now = "%s-%s-%s" % (date.day, date.month, date.year)
        if self._record_exists(task_id):
            if self._is_done(task_id):
                echo("The task is already done", err=True)
            else:
                self.cursor.execute('''
                    UPDATE todo SET done=?, date_completed=? WHERE Id=?
                ''', (1, date_now, int(task_id)))
                echo("Task %s has been marked as done" % str(task_id))
                self.db.commit()
        else:
            echo("Task %s doesn't even exist" % (str(task_id)), err=True)

    def uncheck_task(self):
        """
        Mark as done task as undone
        """
        task_id = self.arg['<id>']
        if self._record_exists(task_id):
            if self._is_done(task_id):
                self.cursor.execute('''
                    UPDATE todo SET done=? WHERE id=?
                  ''', (0, int(task_id)))
                echo("Task %s has been unchecked" % str(task_id))
                self.db.commit()
            else:
                echo("The task is already pending", err=True)
        else:
            echo("Task %s doesn't exist" % str(task_id), err=True)

    def list_task(self):
        """
        Display all tasks in a table
        """
        tab = PrettyTable(["Id", "Task Todo", "Done ?", "Date Added",
                          "Date Completed"])
        tab.align["Id"] = "l"
        tab.padding_width = 1
        self.cursor.execute('''
            SELECT id, task, done, date_added, date_completed FROM todo
          ''')
        records = self.cursor.fetchall()
        for each_record in records:
            if each_record[2] == 0:
                done = "Nop"
            else:
                done = "Yup"
            if each_record[4] is None:
                status = "Pending..."
            else:
                status = each_record[4]
            tab.add_row([each_record[0], each_record[1], done,
                        each_record[3], status])
        print tab

    def list_pending_tasks(self):
        """
        Display all pending tasks in a tabular form
        """
        tab = PrettyTable(["Id", "Task Todo", "Date Added"])
        tab.align["Id"] = "l"
        tab.padding_width = 1
        self.cursor.execute('''
            SELECT id, task, date_added FROM todo WHERE done=?
          ''', (int(0),))
        records = self.cursor.fetchall()
        for each_record in records:
            tab.add_row([each_record[0], each_record[1], each_record[2]])
        print tab

    def clear_task(self):
        """
        Delete the table to refresh the app
        """
        self.cursor.execute('''
            DROP TABLE todo
          ''')
        self.db.commit()

    def __del__(self):
        self.db.close()


def main():
    """
    Entry point for console script
    """
    app = Todo()
    app.run()
