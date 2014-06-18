#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Permet la gestion d'un fichier verrou
Permet par exemple de controler l'unicité d'un process 
ou d'y mettre fin 
"""

__author__ = "Fabrice Romand"
__copyright__ = "Copyleft 2010, Fabrice Romand"
__credits__ = [ "Fabrice Romand" ]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Fabrice Romand"
__email__ = "fabrom@jability.org"
__status__ = "Development"

from pathfinder import get_current_script_path

import atexit
import logging
import os

log = logging.getLogger('jabilitypyup.lockflag')

class lockFlag:
    """Classe de gestion d'un fichier verrou"""

    def __init__(self, flagname=u"pid", flagext=u"lock", flagdir=None):
        """Initialisation de l'indicateur avec
        ''flagdir'': le chemin ou est stocké l'état de l'indicateur
        ''flagname'': le nom du fichier indicateur
        ''flagext'': l'extension du fichier indicateur
        """
        self.fullpath = None
        self.path = flagdir
        self.name = flagname
        self.ext = flagext
        self.pid = os.getpid()
        
        if self.path == None:
            self.path = os.getcwd()
        
        self.fullpath = os.path.abspath(os.path.join(self.path,self.name + "." + self.ext))   
    
    def create(self):
        if not self.exists():
            try:
                ff = open(self.fullpath, "w")
                ff.write(str(self.pid))
                ff.close()
            except Exception:
                log.error("Cannot create lock file %s" % (self.fullpath))
                log.exception("")
                return False
            atexit.register(self.delete)
            return True
        return False
    
    def exists(self):
        """Contrôle l'existence de l'indicateur"""
        if os.path.exists(self.fullpath):
            return True
        return False
        
    def delete(self):
        """Suppression du fichier indicateur"""
        try:
            if self.exists():
                os.remove(self.fullpath)
        except Exception:
            log.error("Cannot delete lock file %s" % (self.fullpath))
            log.exception("")
            return False
        return True