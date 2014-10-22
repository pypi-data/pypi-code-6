# -*- coding: utf-8 -*-

"""
PyCompta main program

Regroupe la gestion du fichier de configuration, la lecture des fichiers
d'écritures, le calcul de la comptabilité et l'écriture des fichiers HTML.
"""

import sys
import os
import os.path as osp
import optparse
import logging

if sys.stdout.isatty():
    from logilab.common.logging_ext import set_color_formatter
    set_color_formatter()

from pycompta import FIN, absjoin, log
from pycompta import RelativeDateTime, Date
from pycompta.lib import entities, xmlreader, render
from pycompta.lib.comptas import Comptabilite, SousComptabilite
from pycompta.lib.config import get_config

def make_date(s, day_in_month=1) :
    """renvoie objet date à partir de chaîne du type 200306"""
    return Date(int(s[:4]), int(s[4:]), day_in_month)

def read_ecritures(path_ecritures) :
    """
    Lire tous fichiers dans répertoire des écritures
    """
    ecritures = []
    for path in os.listdir(path_ecritures) :
        path = osp.join(path_ecritures, path)
        if osp.isfile(path) and path.endswith('.xml') :
            ecritures += xmlreader.get_ecritures(file(path))
    return ecritures

def check_ecritures(ecritures, debut, fin) :
    """
    vérifie que les écritures sont équilibrées
    """
    msg = []
    for ecrit in ecritures :
        if not ecrit.est_equilibre() :
            msg.append("Cette écriture n'est pas équilibrée\n%s" % ecrit)
        if not ecrit.montants_positifs() :
            msg.append("Cette écriture a des montants négatifs\n%s" % ecrit)
        if not ecrit.entre(debut, fin) and not (ecrit.type == 'report' and ecrit.date < debut):
            msg.append("Cette écriture a une date non comprise entre %s et %s\n%s"
                       % (debut, fin, ecrit))
    return msg

def mk_comptas(config, debut, fin, prev) :
    """
    Lit fichiers et calcule comptabilités
    """
    # comptabilité
    log("Comptabilité\n")
    log("   lecture fichiers...")
    ecritures = read_ecritures(config['repertoire_ecritures'])
    log(".")
    for msg in check_ecritures(ecritures, debut, fin+RelativeDateTime(days=+1)):
        logging.warning(msg)
    log(".")
    if osp.exists(config['repertoire_ecritures_paye']):
        ecritures_paye = read_ecritures(config['repertoire_ecritures_paye'])
        log(".")
        for msg in check_ecritures(ecritures_paye, debut, fin+RelativeDateTime(days=+1)):
            logging.warning(msg)
        log(".")
    else:
        ecritures_paye = None
    immo = xmlreader.get_immobilisations(file(config['immobilisations']))
    log(" OK (%s ecritures lues)\n" % (len(ecritures)+len(immo)))
    log("   calcul...")
    if ecritures_paye:
        compta_paye = SousComptabilite(debut, fin, ecritures_paye, 'Paye')
        compta = Comptabilite(debut, fin, ecritures, immo, compta_paye)
    else:
        compta = Comptabilite(debut, fin, ecritures, immo)
    log(" OK\n")

    # vérifie cohérence
    errors = compta.check()
    if errors:
        logging.error('\n'.join(errors))

    # comptabilité prévisionnelle
    if prev :
        log("Comptabilité prévisionnelle\n")
        log("   lecture fichiers...")
        if osp.exists(config['repertoire_ecritures_prev']):
            ecritures_prev = read_ecritures(config['repertoire_ecritures_prev'])
            log(".")
            for msg in check_ecritures(ecritures_prev, fin - RelativeDateTime(months=+1), FIN):
                logging.warning(msg)
            log(".")
        else:
            ecritures_prev = []
        if osp.exists(config['repertoire_ecritures_paye_prev']):
            ecritures_paye_prev = read_ecritures(config['repertoire_ecritures_paye_prev'])
            log(".")
            for msg in check_ecritures(ecritures_paye_prev, fin - RelativeDateTime(months=+1), FIN):
                logging.warning(msg)
            log(".")
        else:
            ecritures_paye_prev = []
        immo_prev = xmlreader.get_immobilisations(file(config['immobilisations_prev']))
        log(" OK\n")
        log("   calcul...")
        if ecritures_paye_prev:
            compta_paye_prev = SousComptabilite(debut, prev,
                                                ecritures_paye+ecritures_paye_prev)
            compta_prev = Comptabilite(debut, prev,
                                       ecritures+ecritures_prev,
                                       immo+immo_prev,
                                       compta_paye_prev)
        else:
            compta_prev = Comptabilite(debut, prev,
                                       ecritures+ecritures_prev,
                                       immo+immo_prev)
        log(" OK\n")
        errors = compta_prev.check()
        if errors:
            logging.error('\n'.join(errors))
    else :
        compta_prev = None

    return compta, compta_prev

## MAIN ########################################################################

def mk_optparser():
    usage = "usage: %prog [options] <source> <target>"
    parser = optparse.OptionParser(usage)
    parser.add_option('--xml', action='store_true', default=True,
                      help=u'écrit la compta en XML [defaut]')
    parser.add_option('--no-xml', action='store_false', dest='xml',
                      help=u'ne pas regénérer le XML')
    parser.add_option('--html', action='store_true', default=True,
                      help=u'transforme le XML en HTML [défaut]')
    parser.add_option('--no-html', action='store_false', dest='html',
                      help=u'ne pas regénérer le HTML')
    parser.add_option('--fo', action='store_true', default=None,
                      help=u'transforme le XML en XSL:FO')
    parser.add_option('--no-fo', action='store_false', dest='fo',
                      help=u'ne pas regénérer le XSL:FO')
    parser.add_option('--pdf', action='store_true', default=False,
                      help=u'transforme le XSL:FO en PDF [implique --fo]')
    parser.add_option('--debug', action='store_true', default=False,
                      help=u"affiche messages de debug")
    parser.add_option('--no-prev', action='store_true', default=False, dest='no_prev',
                      help=u"ignore les prévisions si il y en a")
    parser.add_option('--profile', action='store_true', default=False,
                      help=u"run and print profiling information")
    return parser

def run_standard(config, debut, fin, prev, options):
    try:
        compta, compta_prev = mk_comptas(config, debut, fin, prev)
        if options.no_prev:
            compta_prev = None
    except entities.ExceptionEcriture, exc:
        msg = "Erreur ecriture: %s\n" % str(exc)
        log(msg+str(exc)+'\n')
        return 1
    job = (config, compta, compta_prev)

    if options.xml :
        render.output_xml(*job)
    if options.html :
        render.render_html(*job)
    if options.fo or (options.pdf and options.fo is None) :
        render.render_fo(*job)
    if options.pdf :
        render.render_pdf(*job)

def run(args):
    """
    Programme principal
    """
    # parse command-line
    parser = mk_optparser()
    options, args = parser.parse_args(args)

    if options.debug:
        logging.getLogger().setLevel(level=logging.DEBUG)

    if not (1 <= len(args) <= 2):
        parser.error('invalid number of arguments')

    datasrc = osp.abspath(args[0])
    if len(args) > 1:
        targetdir = args[1]
    else:
        targetdir = '.'
    targetdir = osp.abspath(targetdir)

    # get config
    try:
        config = get_config(datasrc, targetdir)
        config.chkpaths()
    except IOError, e:
        logging.error("%s '%s'" % (e.strerror, e.filename))
        return 1
    except OSError, e:
        logging.error("Aborting: %s" % e)
        return 1

    # chemins des commandes
    if 'xsltproc' in config :
        render.XSLTPROC_CMD = config['xsltproc']
    if 'fop' in config :
        render.FOP_CMD = config['fop']

    # dates
    debut = make_date(config['debut'])
    fin = make_date(config['fin'], -1)
    if config.has_key('fin_prev') :
        prev = make_date(config['fin_prev'], -1)
    else :
        prev = None

    # run
    if options.profile:
        log('*** profiled run ***\n')
        from hotshot import Profile, stats
        prof = Profile('stones.prof')
        prof.runcall(run_standard, config, debut, fin, prev, options)
        prof.close()
        stats = stats.load('stones.prof')
        stats.sort_stats('time', 'calls')
        stats.print_stats(30)
    else:
        return run_standard(config, debut, fin, prev, options)

