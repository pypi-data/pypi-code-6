"""
Configurable dictionary of attributes of the system.

"""

import os
import sys
import dm.dictionary
from quant.dictionarywords import *
import quant

class SystemDictionary(dm.dictionary.SystemDictionary):
    
    def getSystemName(self):
        return 'quant'

    def getSystemVersion(self):
        return quant.__version__

    def setDefaultWords(self):
        super(SystemDictionary, self).setDefaultWords()
        self[PLUGIN_PACKAGE_NAME] = 'quant.plugin'
        self[INIT_STOP_VISITOR_REGISTRATION] = ''
        self[AC_SKIP_ROLE_INFERENCE] = ''
        self[INITIAL_PERSON_ROLE] = 'Developer'
        self[PROVISIONS_DIR_PATH] = '/tmp/%s-provisions' % self[SYSTEM_NAME]
        self[TRAC_PATH] = '' # By default, go with shipped system configurations.
        self[DOJO_PATH] = '/usr/share/dojo'
        self[DOJO_PREFIX] = '/dojo'
        self[DISTINGUISH_MODE] = 'auto'

