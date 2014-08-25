import os
import commands

import dm.util.db
import dm.ioc

class Database(dm.util.db.Database):

    features = dm.ioc.features
        
    def _getSystemDictionary(self):
        import quant.dictionary 
        systemDictionary = quant.dictionary.SystemDictionary()
        return systemDictionary
            
    def init(self):
        """
        Initialise service database by creating initial domain object records.
        """
        import quant.soleInstance
        commandSet = quant.soleInstance.application.commands
        commandClass = commandSet['InitialiseDomainModel']
        initDomainModel = commandClass()
        initDomainModel.execute()

