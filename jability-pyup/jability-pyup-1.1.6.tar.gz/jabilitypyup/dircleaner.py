#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module de nettoyage des fichiers d'un dossier
en conservant les fichiers les plus récents exprimés
en nombre de fichiers à conserver ou en nombre de jours.
Ne nettoie pas les sous-dossiers.
"""

__author__ = "Fabrice Romand"
__copyright__ = "Copyleft 2008 - Fabrice Romand"
__credits__ = [ "Fabrice Romand" ]
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Fabrice Romand"
__email__ = "fabrom@jability.org"
__status__ = "Development"

import logging
import operator
import os
import sys
import time

import filescollector

log = logging.getLogger('jabilitypyup.dircleaner')

class dirCleaner:
    """Classe de nettoyage des dossiers d'un fichier"""

    def __init__(self, dir2clean = "."):
        """''dir2clean'' est le dossier à nettoyer
        """
        self.setDir(dir2clean)
        self.setFilter()
        self.setCleanLastest()


    def setDir(self, dir2clean):
        """positionne le dossier à nettoyer.
        ''dir2clean'' est le dossier à nettoyer
        """
        self.dir = os.path.abspath(dir2clean)
        log.debug(u"set %s for cleaning" % (dir2clean))


    def setFilter(self, pattern = r'^.*$'):
        """définition du filtre (expression régulière).
        ''pattern'' est l'expression de régulière pour filtrage'"""
        self.filefilter = pattern
        log.debug(u"set filter '%s'" % (pattern))


    def setCleanLastest(self, lastest = True, qty = 0 ):
        """positionne le type de nettoyage :
        lastest = True ne conserve que les qty derniers fichiers
        si = False conserve les fichiers créés les qty derniers jours
        """
        self.lastest = lastest
        self.qty = qty
        log.debug(u"set cleaning method : Lastest: %r - Quantity: %d" % (lastest, qty))


    def filedelete(self, filepath):
        """Suppression du fichier ''filepath''"""
        if os.path.exists(filepath):
            # FIXME: for Windows !!! otherwise errno 13 en multithread
            testflag = True
            testcount = 0
            while testflag and testcount < 10:
                try:
                    os.remove(filepath)
                except OSError:
                    time.sleep(1)
                    testcount += 1
                    log.warning(u"cannot delete %s : retry #%d..." % (filepath, count))
                    log.exception('')
                    continue
                testflag = False
            if os.path.exists(filepath):
                log.error(u"cannot delete %s" % (filepath))
                return False
        return True


    def clean(self):
        """Effectue le nettoyage
        Renvoie le nb de fichiers supprimés
        """
        res = 0

        if not os.path.isdir(self.dir):
            log.error(u"directory not found (%s)" % (self.dir))
            return

        fcoll = filescollector.FilesCollector()
        fcoll.setSourceDir(self.dir)
        fcoll.setFileFilter(self.filefilter)
        fcoll.run(True)
        log.debug(u"%d file(s) found in directory to clean" % (len(fcoll.files)))

        fl2 = list()
        for file in fcoll.files:
            try:
                ftime = os.path.getmtime(file)
            except OSError :
                log.error("cannot get mtime for %s" % (file))
                log.exception('')
                continue
            fl2.append((ftime,file))
        fl2a = sorted(fl2, key = operator.itemgetter(0))

        if self.lastest:
            if self.qty>0:
                bfin = fl2a[:self.qty*-1]
            else:
                bfin = fl2a
            for file in bfin:
                if os.path.isfile(file[1]):
                    if self.filedelete(file[1]):
                        res += 1
                    else:
                        log.error(u"Can't delete file %s" % (file[1]))
        else:
            now = time.time() - self.qty * 86400
            for file in fl2a:
                if file[0] <= now and os.path.isfile(file[1]):
                    if self.filedelete(file[1]):
                        res += 1
                    else:
                        log.error(u"Can't delete file %s" % (file[1]))
                        
        log.debug(u"%d file(s) deleted" % (res))
        return res
