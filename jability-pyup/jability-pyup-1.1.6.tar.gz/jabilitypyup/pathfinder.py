#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module de recherche des chemins primordiaux
"""

__author__ = "Fabrice Romand"
__copyright__ = "Copyleft 2008, Fabrice Romand"
__credits__ = [ "Fabrice Romand" ]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Fabrice Romand"
__email__ = "fabrom@jability.org"
__status__ = "Development"


import imp
import os.path
import platform
import sys


def get_current_script_path():
    """Permet d'obtenir le chemin absolu du script
    ou de l'executable courant"""
    if main_is_frozen():
        scriptpath = os.path.dirname(sys.executable)
    else:
        scriptpath = os.path.dirname(sys.argv[0])
    absscriptpath = os.path.abspath(scriptpath)
    return absscriptpath


def get_user_dir_path():
    """Obtenir le chemin absolu du répertoire
    de l'utilisateur courant"""
    pltfrm = platform.system()
    if pltfrm == 'Windows':
        if os.environ.has_key('HOMEDRIVE') and os.environ.has_key('HOMEPATH'):
            homedrive = os.environ['HOMEDRIVE']
            homepath = os.environ['HOMEPATH']
            return homedrive + homepath
    return os.path.abspath(os.path.expanduser('~'))


def get_system_conf_path():
    """Obtenir le chemin absolu du dossier
    de configuration du système
    - /etc sur plateforme Unix-like
    - %SYSTEMROOT% sous MS Windows
    - le répertoire courant si la plateforme n'a pas été
      identifiée ou si le dossier détecté n'existe pas
    """
    pltfrm = platform.system()
    if pltfrm == 'Windows':
        if os.environ.has_key('SYSTEMROOT'):
            sysdir = os.environ['SYSTEMROOT']
    elif pltfrm == 'Linux' or pltfrm == 'Unix':
        sysdir = os.sep + 'etc'
    else:
        sysdir = os.getcwd()
    abssysdir = os.path.abspath(sysdir)
    if not os.path.exists(abssysdir):
        abssysdir = os.path.abspath(os.getcwd())
    return abssysdir


def get_tmp_dir():
    """Renvoi le premier chemin de dossier temporaire trouvé"""
    import tempfile
    return tempfile.gettempdir()


def get_configuration_filepath(
                        appshortname = 'foo',
                        filename = 'main.conf',
                        curdirsearch = True,
                        userdirsearch = True,
                        sysdirsearch = True,
                        localconfdirname = 'conf',
                        userconfdirprefix = '.'
                        ):
    """Cherche le fichier ''filename'' dans les dossiers
    suivants (dans l'ordre) :
    - le dossier courant (si ''curdirsrch''=True)
    - le dossier courant + ''localconfdirname'' (si ''curdirsrch''=True)
    - le dossier de l'utilisateur (si ''usersrch''=True)
    - le dossier de l'utilisateur + ''userconfdirprefix'' + ''appshortname'' (si ''usersrch''=True)
    - le dossier de configuration du système (si ''sysdirsrch''=True)
    - le dossier de configuration du système + ''appshortname'' (si ''sysdirsrch''=True)
    - le dossier du script ou de l'exécutable courant
    - le dossier du script ou de l'exécutable courant + ''localconfdirname''

    Renvoie le chemin absolu du fichier trouvé ou None
    """

    if curdirsearch:
        # recherche dans le <dossier courant>/<filename>
        base_curdir = os.path.abspath(os.getcwd())
        confpath_cur = os.path.join(base_curdir, filename)
        if os.path.exists(confpath_cur):
            return confpath_cur
        # recherche dans <dossier courant>/<localconfdirname>/<filename>
        confpath_cur = os.path.join(    base_curdir,
                                        localconfdirname,
                                        filename)
        if os.path.exists(confpath_cur):
            return confpath_cur

    if userdirsearch:
        # recherche dans le dossier de l'utilisateur <userdir>/<filename>
        base_userdir = get_user_dir_path()
        confpath_user = os.path.join(   base_userdir,
                                        filename)
        if os.path.exists(confpath_user):
            return confpath_user
        # recherche dans le dossier <userdir>/<userconfdirprefix><appshortname>/<filename>
        confpath_user = os.path.join(   base_userdir,
                                        userconfdirprefix + appshortname,
                                        filename)
        if os.path.exists(confpath_user):
            return confpath_user

    if sysdirsearch:
        # recherche dans le dossier de conf. système <sys>/<filename>
        base_sysdir = get_system_conf_path()
        confpath_sys = os.path.join(base_sysdir, filename)
        if os.path.exists(confpath_sys):
            return confpath_sys
        # recherche dans le dossier de conf. système <sys>/<appshortname>/<filename>
        confpath_sys = os.path.join(    base_sysdir,
                                        appshortname,
                                        filename)
        if os.path.exists(confpath_sys):
            return confpath_sys

    # recherche dans le dossier du script courant <scriptdir>/<filename>
    base_dftdir = get_current_script_path()
    confpath_dft = os.path.join(base_dftdir, filename)
    if os.path.exists(confpath_dft):
        return confpath_dft
    # recherche dans le dossier du script courant <scriptdir>/<localconfdirname>/<filename>
    confpath_dft = os.path.join(base_dftdir, localconfdirname, filename)
    if os.path.exists(confpath_dft):
        return confpath_dft

    # Pas trouvé
    return None


def ensure_directories(dirlist):
    """Vérifier l'existence des dossiers de la liste fournie ''dirlist''.
    Création du dossier s'il n'existe pas.
    Lève une exception OSError si le chemin existe mais n'est pas un dossier."""
    for dir in dirlist:
        d = os.path.dirname(dir)
        if not os.path.exists(d):
            os.makedirs(d)
        if not os.path.isdir(d):
            raise OSError, "'%s' exists but is not a directory !" % (d)


def main_is_frozen():
    return (hasattr(sys, "frozen") or # new py2exe
            hasattr(sys, "importers") # old py2exe
            or imp.is_frozen("__main__")) # tools/freeze
