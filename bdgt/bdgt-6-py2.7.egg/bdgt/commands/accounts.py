from bdgt.storage.database import session_scope
from bdgt.storage.gateway import delete_object, save_object
from bdgt.models import Account


class CmdAddAccount(object):
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __call__(self):
        account = Account(self.name, self.number)
        save_object(account)
        return "Account '{}' created".format(self.name)


class CmdDeleteAccount(object):
    def __init__(self, name):
        self.name = name

    def __call__(self):
        with session_scope() as session:
            account = session.query(Account).filter_by(name=self.name).one()
        delete_object(account)
        return "Account '{}' deleted".format(self.name)


class CmdListAccounts(object):
    def __call__(self):
        with session_scope() as session:
            output = ""
            for account in session.query(Account).all():
                output += account.name + "\n"
            return output
