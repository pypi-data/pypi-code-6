#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Permet la gestion d'un indicateur temporel
Permet par exemple de savoir s'il faut lancer une tâche journalière
"""

__author__ = "Fabrice Romand"
__copyright__ = "Copyleft 2008, Fabrice Romand"
__credits__ = [ "Fabrice Romand" ]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Fabrice Romand"
__email__ = "fabrom@jability.org"
__status__ = "Development"


import os
import time

class timeFlag:
    """Classe de gestion d'un indicateur temporel"""

    def __init__(self, flagdir=u".", flagname=u"onedayflag", flagext=u"dat"):
        """Initialisation de l'indicateur avec
        ''flagdir'': le chemin ou est stocké l'état de l'indicateur
        ''flagname'': le nom du fichier indicateur
        ''flagext'': l'extension du fichier indicateur
        """
        self.fullpath = None
        self.path = flagdir
        self.name = flagname
        self.ext = flagext
        self.setDaily()
        self.value = self._now()
        self.setFormat()

    def setDaily(self):
        """Définit un indicateur journalier"""
        self.setFormat()

    def setMonthly(self):
        """Définit un indicateur mensuel"""
        self.setFormat("%Y%m")

    def setWeekly(self):
        """définit un indicateur hebdomadaire"""
        self.setFormat("%Y%U")

    def setFormat(self, format="%Y%m%d"):
        """Modifie le format de l'indicateur
        ''format'': format de l'indicateur temporel
        Par défaut, l'indicateur est journalier avec un format %Y%m%d
        pour un indicateur horaire, le format est "%Y%m%d%H"
        pour un mensuel, "%Y%m"
        pour un hebdo, "%Y%U"
        """
        self.format = format

    def getFormat(self):
        """Renvoie le format de l'indicateur"""
        return self.format

    def update(self):
        """met à jour l'indicateur"""
        self.value = self._now()
        ff = open(self._getpath(), "wb")
        ff.write(self.value)
        ff.close()

    def get(self):
        """Renvoie la valeur de l'indicateur
        """
        if not os.path.exists(self._getpath()):
            self.update()
        ff = open(self._getpath(), "rb")
        self.value = ff.read()
        ff.close()
        return self.value

    def isuptodate(self):
        """Renvoie vrai si l'indicateur est à jour
        """
        self.get()
        now = self._now()
        if self.value == now:
            return True
        return False

    def delete(self):
        """Suppression de l'indicateur"""
        try:
            os.remove(self._getpath())
        except OSError:
            pass

    def getdiff(self):
        """Renvoie la différence entre le flag et maintenant
        sous forme de tuple (day,hr,min,sec)"""
        self.get()
        try:
            ttime = time.mktime(time.strptime(self._now(), self.format)) - \
                    time.mktime(time.strptime(self.value, self.format))
        except ValueError:
            return (-1,-1,-1,-1)

        nd = 0
        nh = 0
        nm = 0
        ns = 0
        if int(ttime/86400) > 0:
            rt = u"%d" % (int(ttime/86400))
            nd = int(rt)
            ttime -= int(rt) * 86400
        if int(ttime/3600) > 0:
            rt = u"%d" % (int(ttime/3600))
            nh = int(rt)
            ttime -= int(rt) * 3600
        if int(ttime/60) > 0:
            rt = u"%d" % (int(ttime/60))
            nm = int(rt)
            ttime -= int(rt) * 60
        if ttime > 0:
            ns = int(ttime)

        return (nd, nh, nm, ns)

    def _now(self):
        """Renvoie la date/heure actuelle au format de l'indicateur"""
        return time.strftime(self.format)

    def _getpath(self):
        """Renvoie le chemin complet de l'indicateur"""
        if self.fullpath == None:
            self.fullpath = os.path.abspath(os.path.join(self.path,self.name + "." + self.ext))
        return self.fullpath
