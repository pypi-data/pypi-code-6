import clr

clr.AddReference('System.Data')

from System.Data.SqlClient import SqlConnection
from cursor import Cursor

class Connection(object):
    """ The sqlnet Database Conection Object. """

    from sqlnet_exceptions import Warning, Error, InterfaceError,\
        DataError, DatabaseError, OperationalError, IntegrityError,\
        InternalError, NotSupportedError, ProgrammingError

    def __init__(self, *args, **kwargs):
        """ Initialise from arguments given. """
        self.connection = self.create_connection(*args, **kwargs)
        self.connection.Open()

        # Immediately create a new transaction.
        self.transaction = self.connection.BeginTransaction()

    def cursor(self):
        """ Create a cursor """
        return Cursor(self.connection, self.transaction)
    
    def create_connection(*args, **kwargs):
        """ Create a database connection based on arguments. """
        connection_string = ""

        # Parse host param
        host = kwargs.get('host', None)
        if host != None:
            connection_string += "Server={host};".format(host=host)

        # Parse database params.
        database = kwargs.get('db', None)
        if database != None:
            connection_string += "Database={database};".format(
                database=database
            )

        trusted_connection = kwargs.get('trusted_connection', False)
        connection_string +=\
            "Trusted_Connection={trusted_connection};".format(
                trusted_connection=trusted_connection
            )

        return SqlConnection(connection_string)

    # TODO: This should be fleshed out so that we can quickly parse params.
    def parse_param(self, param_name):
        pass

    def close(self):
        """ Closes self.connection. """
        self.connection.Close()

    def commit(self):
        """ Commit all Cursors to database. """
        # Commit the current transaction on the connection.
        self.transaction.Commit()

        # Create new transaction because each transaction can
        # only be used once.
        self.transaction = self.connection.BeginTransaction()

    def rollback(self):
        """ Roll back the transaction. """
        self.transaction.Rollback()

        # Create new transaction because each transaction can
        # only be used once.
        self.transaction = self.connection.BeginTransaction()

