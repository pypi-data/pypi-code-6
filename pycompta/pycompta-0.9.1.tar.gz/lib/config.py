# -*- coding: utf-8 -*-

import os
import os.path as osp
import UserDict

from pycompta import absjoin

DEFAULT_CONFIG = '/etc/pycompta/pycompta.conf'

class ConfigDict(UserDict.UserDict) :
    """Dictionnaire contenant paramètres du fichier de config"""

    def __init__(self, config_path) :
        UserDict.UserDict.__init__(self)
        self.config_path = osp.abspath(config_path)
        self.data = {'societe':'societe.xml',
                     'repertoire_ecritures':'ecritures',
                     'repertoire_ecritures_prev':'ecritures_prev',
                     'repertoire_ecritures_paye':'./paye/ecritures',
                     'repertoire_ecritures_paye_prev':'./paye/ecritures_prev',
                     'immobilisations':'livre-immo.xml',
                     'immobilisations_prev':'livre-immo.prev.xml',
                     'comptes.png':'comptes.png',
                     'tresorerie.png':'tresorerie.png',
                     }

    def normalize_paths(self) :
        """normalise tous les chemins supposés relatifs à répertoire
        du fichier de config
        """
        source = os.path.dirname(self.config_path)
        self.data['exercice'] = source
        for key in ['societe', 'immobilisations', 'immobilisations_prev'] :
            self.data[key] = absjoin(source, self.data[key])
        for key in ['repertoire_ecritures', 'repertoire_ecritures_prev',
                    'repertoire_ecritures_paye', 'repertoire_ecritures_paye_prev'] :
            self.data[key] = absjoin(source, self.data[key])
        dest = self.data['repertoire_cible']
        for key in ['comptes.png', 'tresorerie.png'] :
            self.data[key] = absjoin(dest, self.data[key])

    def get_chemins(self, cibles, ext='') :
        """
        renvoie chemin des fichiers, sans extension
        """
        chemins = []
        for filename, type_ in cibles:
            dst = self.destpath('%s%s.' % (filename, ext))
            chemins.append( (dst, type_) )
        return chemins

    def srcpath(self, filename=''):
        return absjoin(self.data['exercice'], filename)

    def destpath(self, filename=''):
        return absjoin(self.data['repertoire_cible'], filename)

    def chkpaths(self):
        for key in ['exercice', 'repertoire_cible']:
            if not osp.exists(self.data[key]):
                raise OSError('%s does not exist'%self.data[key])

def read_config(file) :
    """
    Lit le fichier de config et renvoie un dictionnaire
    """
    config = {}
    for line in file :
        line = line.strip()
        if line and not line[0] == '#' :
            key, val = [token.strip() for token in line.split('=')]
            config[key] = val
    return config

def get_config(datasrc, targetdir):
    config_path = osp.join(datasrc, 'config')
    config = ConfigDict(config_path)
    if os.path.isfile(DEFAULT_CONFIG) :
        config.update(read_config(file(DEFAULT_CONFIG)))
    config.update(read_config(file(config_path)))
    config['repertoire_cible'] = targetdir
    config.normalize_paths()
    return config
