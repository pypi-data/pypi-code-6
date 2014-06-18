#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module d'extraction des messages significatifs des journaux d'activité
et envoi par email de l'extraction
"""

__author__ = "Fabrice Romand"
__copyright__ = "Copyleft 2009, Fabrice Romand"
__credits__ = [ "Fabrice Romand" ]
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Fabrice Romand"
__email__ = "fabrom@jability.org"
__status__ = "Development"


import os
import filescollector
import logging
import time

import pysendmail
import toolbox
import sys

log = logging.getLogger('jabilitypyup.logreporter')

class logReporter:
    """
    Classe d'extraction des messages significatifs des journaux d'activité
    et envoi par email de l'extraction
    """
    def __init__(self,   logspath=u".",
                         fromdate=u"19800101",
                         logsfilter=r"^.*\.log$",
                         logdateformat=u"%Y%m%d",
                         logdatepos=1,
                         loglevels = (u"CRITICAL",u"ERROR",u"WARNING"),
                         loglevelpos=3,
                         charset = 'UTF-8'):
        """
        ''logspath'': chemin des journaux à analyser
        ''fromdate'': date de début des entrées à analyser (format %Y%m%d)
        ''logsfilter'': expr. régulière de collecter des fichiers journaux
        ''logdateformat'': format des dates dans les journaux
        ''logdatepos'': position de la date dans une entrée de journal
        ''loglevels'': liste des niveaux à rapporter
        ''loglevelpos'': position du niveau dans une entrée de journal
        ''charset'': encodage des journaux
        """
        self.logdir = os.path.abspath(logspath)
        self.logdateformat = logdateformat
        self.logdatepos = logdatepos
        self.loglevelpos = loglevelpos
        self.loglevels = loglevels
        self.logsfilter = logsfilter
        self.fromdate = time.mktime(time.strptime(fromdate, logdateformat))
        self.extractedlines = list()
        self.charset = charset
        if self.charset == None:
            self.charset = toolbox.get_stream_encoding(sys.stdout)
            
    def extract(self):
        """ Analyse des logs
        Renvoie la liste des lignes sélectionnées
        """

        reslines = list()

        fc = filescollector.FilesCollector()
        fc.setSourceDir(self.logdir)
        fc.setFileFilter(self.logsfilter)
        files = fc.run(True)
        log.debug("%d log file(s) find" % (len(files)))

        for file in files:
            if os.path.getmtime(file) < self.fromdate:
                log.debug(u"%s too old : ignored" % (os.path.basename(file)))
                continue
            try:
                tfl = open(file, "r")
                lines = tfl.readlines()
                tfl.close()
            except OSError:
                log.debug(u"Can't read %s : ignored" % (os.path.basename(file)))
                reslines.append(u"** Cannot read log '%s'" % (file))
                continue
            numline = 0
            for line in lines:
                numline += 1
                sline = line.split()
                if len(sline) >= self.loglevelpos and \
                    len(sline) >= self.logdatepos:
                    try:
                        dline = time.mktime(time.strptime(sline[self.logdatepos-1],
                                                          self.logdateformat))
                        if dline >= self.fromdate:
                            if sline[self.loglevelpos-1] in self.loglevels:
                                reslines.append(line.decode(self.charset))
                    except Exception:
                        log.debug(u"Can't read %s line %d : ignored" % (os.path.basename(file), numline))
                        reslines.append(u"** Bad file format '%s' line %d" % (file, numline))
                        continue
                else:
                    log.debug(u"Bad file format %s line %d : ignored" % (os.path.basename(file), numline))
                    reslines.append(u"** Bad file format '%s' line %d" % (file, numline))
                    continue

        self.extractedlines = reslines
        log.debug("%d lines to report" % (len(self.extractedlines)))
        return reslines


    def email_report(self, mfrom, mto, msubject, msmtpserver='localhost'):
        """Envoi du rapport par email
        ''mfrom'': adresse mail de l'expéditeur
        ''mto'': liste des destinataires
        ''msubject'': sujet du mail à envoyer
        ''msmtpserver'': adresse du serveur SMTP
        
        Voir jabilipyup.pysendmail.send() pour les codes renvoyés. 
        """

        mbody = u"logs directory : " + self.logdir + u"\n"

        slevels = u""
        for level in self.loglevels:
            slevels += level + u" "
        mbody += u"required level(s) : " + slevels + u"\n\n"

        for line in self.extractedlines:
            mbody += line

        return pysendmail.send(mfrom, mto, msubject,
                               mbody, list(), msmtpserver)

