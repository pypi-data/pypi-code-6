import dm.cli.admin
import os.path
import sys
import commands

# Todo: Rename the model objects nicely, then bubble the names up.

class AdministrationUtility(dm.cli.admin.AdministrationUtility):

    # todo: Do something with this thing.
    servicePathEnvironVariableName = 'QUANTHOME'

    def handleNullArgs(self):
        self.runScript()

    def buildApplication(self):
        import quant.soleInstance
        self.appInstance = quant.soleInstance.application

    def constructSystemDictionary(self):
        from quant.dictionary import SystemDictionary
        return SystemDictionary()

    def backupSystemService(self):
        import quant.soleInstance
        commandSet = quant.soleInstance.application.commands
        backupCommandName = 'Backup'
        backupCommand = commandSet[backupCommandName](self.args[0])
        backupCommand.execute()

    def takeDatabaseAction(self, actionName):
        from quant.utils.db import Database
        db = Database()
        actionMethod = getattr(db, actionName)
        actionMethod()

    def getSystemName(self):
        return "Quant"
        
    def getSystemVersion(self):
        import quant
        return quant.__version__
        
    def createAboutMessage(self):
        systemName = self.getSystemName()
        systemVersion = self.getSystemVersion()
        aboutMessage = \
'''This is %s version %s.

Copyright the Appropriate Software Foundation. Quant is open-source
software licensed under the GPL v2.0. See COPYING for details.
''' % (systemName, systemVersion)
        return aboutMessage


class UtilityRunner(dm.cli.admin.UtilityRunner):

    systemName = 'quant'
    servicePathEnvironVariableName = 'QUANTHOME'
    utilityClass = AdministrationUtility
    usage  = """Usage: %prog [options] [command]

Administer a Quant service, including its domain objects. 

Can be run in three modes:
   1. single command: run the command quantd and exit (Default)
   2. interactive (use the "--interactive" option)
   3. scripted commands, either write a file of commands and run it with
      quant --script path, or write a file of commands, put the shebang
      #!/usr/bin/env quant at the top, and make it executable.

To obtain information about the commands available run the "help" command.

Domain objects (e.g. persons, projects, etc) are administered by starting
a python shell from within interactive mode. Run "help shell" for more details.

"""

