import clr

clr.AddReference('System.Data')

from System.Data.SqlClient import SqlCommand

class Cursor(object):
    """ Cursor object """

    def __init__(self, connection, transaction):
        """ Initialise, just save connection """
        self.connection = connection
        self.transaction = transaction


    def execute(self, sql):
        """ Prepare and execute a database query or command. """
        self.command = SqlCommand(sql, self.connection, self.transaction)
        self.go()

        return self

    def __iter__(self):
        """ Return an iterator """
        reader = self.command.ExecuteReader()
        while reader.Read():
            yield [reader.GetValue(ii) for ii in xrange(reader.FieldCount)]
        reader.Close()

    def go(self):
        """ Actually execute/commit cursor command to database. """
        self.command.ExecuteNonQuery()
