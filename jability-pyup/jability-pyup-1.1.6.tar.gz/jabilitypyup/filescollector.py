#!/usr/bin/python
#-*- coding: utf-8 -*-

"""Module de collecte de fichiers dans un dossier donné. Les fichiers
sont sélectionnés grâce à une expression régulière.
"""

__author__ = "Fabrice Romand"
__copyright__ = "Copyleft 2008 - Fabrice Romand"
__credits__ = [ "Fabrice Romand" ]
__license__ = "GPL"
__version__ = "1.3"
__maintainer__ = "Fabrice Romand"
__email__ = "fabrom@jability.org"
__status__ = "Development"

import logging
import os
import re
import time

log = logging.getLogger('jabilitypyup.filescollector')

class FilesCollector:
    """Classe de collecte des fichiers à traiter"""

    def __init__(self):
        """Initialisation du collecteur"""
        self.setSourceDir()
        self.setFileFilter()
        self.setMinimumFileLastChangeAge()

    def setSourceDir(self,sourcedir=u'.'):
        """Initialisation du dossier source ''sourcedir''
        """
        self.sourcedir=sourcedir

    def setFileFilter(self,filefilter=r'^.*$'):
        """initialisation du filtre de sélection des fichiers
        ''filefilter'' est une expression régulière pour la sélection
        des fichiers à collecter.
        """
        self.filefilter=filefilter
        self.reFileFilter=re.compile(self.filefilter)

    def setMinimumFileLastChangeAge(self, mins=0):
        """Si l'âge d'un fichier est inférieur au délai exprimé en minutes,
            il est ignoré.
        """
        self.minimumFileAge = mins * 60

    def run(self,returnAbspath=False):
        """Collecte des fichiers à traiter.
        ''returnAbspath'': Vrai si les chemins renvoyés doivent être
            absolus - Faux par défaut.
        Renvoie une liste triée des fichiers trouvés"""
        self.files=[]

        nowctime = time.time()

        try:
            normpath=os.path.abspath(os.path.normpath(self.sourcedir))
            if not os.access(normpath, os.F_OK|os.R_OK):
                log.error(u"'%s' path not exists or not readable !" % (normpath))
                return self.files
            if not os.path.exists(normpath):
                log.error(u"'%s' path not exists !" % (normpath))
                return self.files
            if not os.path.isdir(normpath):
                log.error(u"'%s' is not a directory !" % (normpath))
                return self.files
            flist=os.listdir(normpath)
            for tfile in flist:
                absfile=os.path.join(normpath,tfile)
                if not os.access(absfile, os.F_OK|os.R_OK):
                    log.error(u"'%s' file not exists or not readable !" % (absfile))
                    continue
                if not os.path.isfile(absfile):
                    continue
                if self.reFileFilter.match(tfile) == None:
                    continue
                file_stats = os.stat(absfile).st_mtime
                if self.minimumFileAge > 0:
                    if nowctime - file_stats < self.minimumFileAge:
                        continue
                if returnAbspath:
                    self.files.append((absfile, file_stats))
                else:
                    self.files.append((tfile, file_stats))
        except:
            log.error(u"unknow error during collect from path '%s'" % (self.sourcedir))
            log.exception('')

        return [x[0] for x in self.files]

