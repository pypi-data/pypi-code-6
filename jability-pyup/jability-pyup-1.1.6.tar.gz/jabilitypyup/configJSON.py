#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module de gestion d'un fichier de configuration au format JSON
"""

__author__ = "Fabrice Romand"
__copyright__ = "Copyleft 2010, Fabrice Romand"
__credits__ = [ "Fabrice Romand" ]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Fabrice Romand"
__email__ = "fabrom@jability.org"
__status__ = "Development"

import json
import logging
import os.path

log = logging.getLogger('jabilitypyup.configJSON')

class ConfigJSON:
    """Classe de gestion d'un fichier de configuration au format JSON
    """

    def __init__(self,  filepath='foo.conf'):
        """''filepath'' est le chemin du fichier de configuration.
        """
        self.filepath = filepath
        self.confdict = None
        log.debug(u"init configJSON for file %s" % (self.filepath))

    def exists(self):
        """ Teste l'existence du fichier de configuration.
            Renvoie True si le fichier existe; False s'il n'existe pas
            ou s'il ne s'agit pas d'un fichier régulier.
        """
        if not self.filepath == None:
            if os.path.exists(self.filepath) and \
                os.path.isfile(self.filepath):
                return True
        log.debug(u"%s not found" % (self.filepath))
        return False

    def load(self):
        """ Chargement du fichier de configuration.
            Renvoie le dictionnaire correspond ou None si le chargement
            est impossible.
        """
        if self.exists():
            log.debug(u"loading existing configuration file %s..." % (self.filepath))
            fp = open(self.filepath, 'r')
            self.confdict = json.load(fp)
            fp.close()
            log.debug(u"configuration file %s loaded." % (self.filepath))
            if not self.confdict.has_key("__configJSON__"):
                self.confdict["__configJSON__"] = dict()
                self.confdict["__configJSON__"]["API"] = __version__ 
            if not self.confdict["__configJSON__"].has_key("__VERSION__"):
                self.confdict["__configJSON__"]["this"] = dict()
                self.confdict["__configJSON__"]["this"]["__VERSION__"] = u"0.1"
            self.version = self.confdict["__configJSON__"]["this"]["__VERSION__"]
        else:
            log.error(u"%s not found" % (self.filepath))
            self.confdict = None
            self.version = None
        return self.confdict

    def _exec_string(self, cmdstr="pass", valparam=None):
        log.debug('executing %s...' % (cmdstr))
        exec(cmdstr)
        
    def update(self, updjsonfile="confupd.json"):
        """Mise à jour de la configuration courante à partir du fichier de
        mise à jour nommé updjsonfile et se trouvant dans le même dossier

        Exemple:
        { <version>: {
            "+": {
                "foo": "dict()",
                "foo:foo2": (1,2,3), 
                "db:sql" : {
                    "odbc":"DSN=host;user=x;pwd=y",
                    "encoding":"cp1252"
                    },
                "db:mysql:host": "localhost",
                "db:mysql:port": 3600,
                  },
            "-": [
                "foo"
                ]
            }
         }
        }
        """
        fullupdfile = os.path.join(os.path.dirname(self.filepath), updjsonfile)
        if os.path.exists(fullupdfile):
            try:
                fp = open(fullupdfile, 'r')
                upddict = json.load(fp)
                fp.close()
                log.debug(u"update configuration file %s loaded." % (updjsonfile))
            except Exception:
                log.error(u"Cannot read update configuration file %s" % (fullupdfile))
                log.exception('')
                return
            try:
                versions = upddict.keys()
                versions.sort()
                log.debug('current version is %s' % (self.version))
                for version in versions:
                    log.debug('find %s version updates...' % (version))
                    if self.version >= version :
                        log.debug('too old, continue...')
                        continue
                    log.debug('updating to %s version...' % (version))
                    if upddict[version].has_key('+'):
                        p2add = upddict[version]['+']
                        for param in p2add.keys():
                            log.debug('  - adding param %s = %s...' % (param,str(upddict[version]['+'][param])))
                            parampaths = param.split(':')
                            indexstr = ""
                            pdict = self.confdict
                            for parampath in parampaths:
                                if not pdict.has_key(parampath):
                                    cmd = "self.confdict" + indexstr + "['%s']" % (parampath)
                                    self._exec_string(cmd + " = dict()")
                                indexstr = indexstr + '["%s"]' % (parampath)
                                pdict = pdict[parampath]
                            valparam = upddict[version]['+'][param]
                            cmd = "self.confdict" + indexstr + " = valparam"
                            self._exec_string(cmd, valparam)
                    if upddict[version].has_key('-'):
                        p2del = upddict[version]['-']
                        for param in p2del.keys():
                            log.debug('  - deleting param %s...' % (param))
                            parampaths = param.split(':')
                            indexstr = ""
                            pdict = self.confdict
                            for parampath in parampaths:
                                if not pdict.has_key(parampath):
                                    indexstr = ""
                                    break
                                indexstr = indexstr + '["%s"]' % (parampath)
                                pdict = pdict[parampath]
                            if not indexstr == "":
                                cmd = "del self.confdict" + indexstr 
                                exec(cmd)
                self.confdict["__configJSON__"]["this"]["__VERSION__"] = version
                log.info(u"configuration updated (%s -> %s)" % (self.version, version))
                self.version = version
            except Exception:
                log.error(u"Error during configuration update")
                log.exception('')
        
    def save(self, confdict=None, filepath=None):
        """ Sauvegarde de la configuration dans un fichier.
        ''confdict'' est le dictionnaire correspondant à la configuration.
        ''filepath'' est le chemin du fichier de sauvegarde.
        """
        if filepath == None:
            filepath = self.filepath
        if confdict == None:
            confdict = self.confdict
        log.debug(u"saving configuration file %s..." % (self.filepath))
        fp = open(filepath, 'w+')
        json.dump(confdict, fp, indent=4, sort_keys=True)
        fp.close()
        log.debug(u"configuration file %s saved." % (self.filepath))

