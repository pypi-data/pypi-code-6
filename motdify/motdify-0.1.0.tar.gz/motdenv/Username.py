import os, pwd

class Username:
    """ Returns the name of the user running this process """

    def getVariableTuple(self):

        return [('USERNAME', pwd.getpwuid(os.getuid())[0])]