# -*- coding: utf-8 -*-

import os
import os.path as osp
import logging

from pycompta import absjoin, log
from pycompta import RelativeDateTime, Date
from pycompta.lib import visitors, diagrams, entities
from pycompta.lib.comptas import Comptabilite

XSLTPROC_CMD = 'xsltproc'
XSLDIR = absjoin(osp.dirname(__file__), '../xsl')
if not osp.exists(XSLDIR):
    XSLDIR = '/usr/share/pycompta/xsl'


def get_params(config):
    return [('societe.def', config.srcpath('societe.xml')),
            ('bilan.precedent', config.srcpath('bilan_precedent.xml')),
            ('cr.precedent', config.srcpath('compte-resultat_precedent.xml')),
            ]

def xslt(src, xsl, target, params=None) :
    """
    Fait appel à xsltproc pour exécuter une transformation XSLT
    """
    if params :
        params_str = ' '.join(['--stringparam %s %s'%param for param in params])
    else :
        params_str = ''
    cmd = '%s %s %s/%s %s > %s' \
          % (XSLTPROC_CMD, params_str, XSLDIR, xsl, src, target)
    logging.debug(cmd+'\n')
    os.system(cmd)

def output_report(config) :
    """
    Génère écriture report à partir de balance
    """
    log("Génération écriture report...")
    src = absjoin(config['repertoire_cible'], 'balance.xml')
    xsl = 'balance2report.xslt'
    target = absjoin(config['repertoire_cible'], 'ecritures-report.xml')
    xslt(src, xsl, target)
    log('OK\n')


def write_xml(config, compta, date_ext, debut, fin):
    """
    Ecrit tout en xml
    """
    cibles = compta.CIBLES
    chemins = [a for a,b in config.get_chemins(cibles, date_ext)]
    JO, GL, BA, CR, BI, IM, IB, JP, GP, BP, BJ, BG, CT, CP = chemins
    visitors.write_journal(file(JO+'xml','w'), compta.journal, debut, fin)
    visitors.write_grand_livre(file(GL+'xml','w'), compta.glivre, debut, fin)
    visitors.write_balance(file(BA+'xml','w'), compta.balance, debut, fin)
    if not isinstance(compta, Comptabilite):
        return
    visitors.write_compte_resultat(file(CR+'xml','w'), compta.resultat, compta.debut, fin)
    visitors.write_bilan(file(BI+'xml','w'), compta.bilan, compta.debut, fin)
    visitors.write_livre_immo(file(IM+'xml','w'), compta.livrimmo, debut, fin)
    visitors.write_bilan_immo(file(IB+'xml','w'), compta.resultat, debut, fin)
    if compta.paye:
        visitors.write_journal(file(JP+'xml','w'), compta.paye.journal, debut, fin)
        visitors.write_grand_livre(file(GP+'xml','w'), compta.paye.glivre, debut, fin)
        visitors.write_balance(file(BP+'xml','w'), compta.paye.balance, debut, fin)
    visitors.write_journal(file(BJ+'xml','w'), compta.banque_journal, debut, fin)
    visitors.write_grand_livre(file(BG+'xml','w'), compta.banque_glivre, debut, fin)
    for num, cpt in compta.glivre.get_comptes('5'):
        fname = CT.replace('.compte.', '.%s.compte.'%num)
        visitors.write_historique_comptes(file(fname+'xml','w'), compta.glivre, debut, fin, cpt.num)
    visitors.write_historique_comptes(file(CP+'xml','w'), compta.glivre, debut, fin, '7')


def output_xml(config, compta, compta_prev) :
    """
    Calcule compta et produit résultat en HTML et XML.
    """
    # dates
    dates_recap = compta.get_dates()
    if compta_prev :
        dates_prev = compta_prev.get_dates(compta.fin)
    else :
        dates_prev = []

    # params
    params = get_params(config)

    # copie les fichiers xml
    import shutil
    for key in ('societe.xml', 'bilan_precedent.xml',
                'compte-resultat_precedent.xml',
                'comptes-annuels.xml', 'plan-comptable.xml', ):
        shutil.copy(config.srcpath(key), config.destpath(key))

    # crée fichier récap
    write_xml(config, compta, '', compta.debut, compta.fin)
    if compta_prev:
        write_xml(config, compta_prev, '.prev', compta_prev.debut, compta_prev.fin)
    output_report(config)

    # état facturation
    xslt(config.destpath('journal.xml'),
         'journal2facturation.xslt',
         config.destpath('facturation.xml'),
         params)

    log("Fichiers mensuels...")
    # crée fichiers récap mensuels
    for date in dates_recap :
        write_xml(config, compta,
                  '.'+date.Format("%Y-%m"),
                  date+RelativeDateTime(day=1),
                  date+RelativeDateTime(day=-1))
        log('.'+date.Format("%Y-%m"))

    # crée fichiers prev mensuels
    for date in dates_prev :
        write_xml(config, compta_prev,
                  '.'+date.Format("%Y-%m")+'.prev',
                  date+RelativeDateTime(day=1),
                  date+RelativeDateTime(day=-1))
        log('.'+date.Format("%Y-%m"))
    log('. OK\n')

    # pilote
    dates_recap.reverse()
    dates_prev.reverse()
    log("Pilote...")
    visitors.write_pilote(file(config.destpath('pilote.xml'),'w'),
                          compta, dates_recap, compta_prev, dates_prev)
    log(" OK\n")

## RENDER ######################################################################

FOP_CMD = 'fop'

def fop(src, dest) :
    """
    Fait appel à FOP pour produire un doc PDF
    """
    cmd = '%s %s %s' % (FOP_CMD, src, dest)
    os.system(cmd)

CSV_XSL = {'balance': 'balance2csv.xslt',
           'grand-livre': 'grand-livre2csv.xslt',
            }

def write_csv(config, compta, date_ext, debut, fin):
    """
    Ecrit tout en csv
    """
    params = get_params(config)
    cibles = compta.get_cibles()
    for chemin, type_ in config.get_chemins(cibles, date_ext):
        if type_ in CSV_XSL:
            xslt(chemin+'xml', CSV_XSL[type_], chemin+'csv', params)

HTML_XSL = {'journal':'journal2html.xsl',
            'grand-livre': 'grand-livre2html.xsl',
            'balance': 'balance2html.xsl',
            'compte-resultat': 'compte-resultat-1col2html.xsl',
            'bilan': 'bilan2html.xsl',
            'immo-amort': 'immo2html.xsl',
            'bilan-immo': 'bilan-immo2html.xsl',
            'journal-banque': 'journal-banque2html.xsl',
            'compte': 'compte2html.xsl',
            }

def write_html(config, compta, date_ext, debut, fin):
    """
    Ecrit tout en html
    """
    params = get_params(config)
    # plan comptable
    xslt(config.destpath('plan-comptable.xml'), 'plan-comptable2html.xsl',
         config.destpath('plan-comptable.html'), params)
    # tout sauf tresorerie
    cibles = compta.get_cibles()
    for chemin, type_ in config.get_chemins(cibles, date_ext):
        if 'tresorerie' not in chemin:
            xslt(chemin+'xml', HTML_XSL[type_], chemin+'html', params)
    # tresorerie
    for num, cpt in compta.glivre.get_comptes('5'):
        xslt(config.destpath('tresorerie.%s.compte.xml' % num), 'compte2html.xsl',
             config.destpath('tresorerie.%s.compte.html' % num), params)
    for num, cpt in compta.glivre.get_comptes('5'):
        xslt(config.destpath('tresorerie.%s.compte.prev.xml' % num), 'compte2html.xsl',
             config.destpath('tresorerie.%s.compte.prev.html' % num), params)

FO_XSL = {'journal':'journal2fo.xsl',
          'grand-livre': 'grand-livre2fo.xsl',
          'balance': 'balance2fo.xsl',
          'compte-resultat': 'compte-resultat-1col2fo.xsl',
          'bilan': 'bilan2fo.xsl',
          'bilan-immo': 'bilan-immo2fo.xsl',
          'immo-amort': 'immo2fo.xsl',
          'journal-banque': 'journal-banque2fo.xsl',
          }

def write_fo(config, compta, date_ext, debut, fin):
    """
    Ecrit tout en pdf
    """
    params = get_params(config)
    cibles = compta.get_cibles()
    for chemin, type_ in config.get_chemins(cibles, date_ext):
        if type_ == 'compte':
            print 'write_fo ignoring', chemin
	else:
            xslt(chemin+'xml', FO_XSL[type_], chemin+'fo', params)
            log(".")

    # comptes annuels
    src = absjoin(config['exercice'], 'comptes-annuels.xml')
    dst = absjoin(config['repertoire_cible'], 'comptes-annuels.')
    if os.path.exists(src):
        os.system('cp %s %sxml' % (src, dst))
        xslt(dst+'xml', 'comptes-annuels2fo.xsl', dst+'fo', params)
        log('.')
    else:
        print 'write_fo ignoring', src

def render_fo(config, compta, compta_prev) :
    """
    Transforme compta XML en XSL:FO
    """
    log("Génération xsl:fo...")
    write_fo(config, compta, '', compta.debut, compta.fin)
    log('OK\n')

def render_pdf(config, compta, compta_prev) :
    """
    Transforme compta XML en PDF
    """
    log("Génération pdf...")
    cibles = compta.get_cibles()
    for chemin, type_ in config.get_chemins(cibles) :
        if type_ == 'compte':
            print 'render_pdf ignoring', chemin
	else:
            fop(chemin+'fo', chemin+'pdf')
            log(".")
    cpts_ann = absjoin(config['repertoire_cible'], 'comptes-annuels.')
    if os.path.exists(cpts_ann+'fo'):
        fop(cpts_ann+'fo', cpts_ann+'pdf')
        log('.')
    else:
        print 'render_pdf ignoring', cpts_ann
    log('OK\n')

def render_html(config, compta, compta_prev) :
    """
    Transforme compta XML en HTML
    """
    # dates
    dates_recap = compta.get_dates()
    if compta_prev :
        dates_prev = compta_prev.get_dates(compta.fin)
    else :
        dates_prev = []

    # params
    params = get_params(config)

    # crée diagramme
    if compta_prev :
        log("Génération diagramme (avec prévisions)...")
        diagrams.diagram(config['comptes.png'],
                         compta_prev, compta_prev.get_dates())
        diagrams.diagram_flot(config.destpath('diagram.html'),
                              compta_prev, compta_prev.get_dates())
        diagrams.diagram_tres(config['tresorerie.png'],
                              compta_prev, compta_prev.get_dates())
        diagrams.diagram_tres_flot(config.destpath('diagram_treso.html'),
                                   compta_prev, compta_prev.get_dates())
    else :
        log("Génération diagramme...")
        diagrams.diagram(config['comptes.png'],
                         compta, compta.get_dates())
        diagrams.diagram_flot(config.destpath('diagram.html'),
                              compta, compta.get_dates())
        diagrams.diagram_tres(config['tresorerie.png'],
                              compta, compta.get_dates())
        diagrams.diagram_tres_flot(config.destpath('diagram_treso.html'),
                                   compta, compta.get_dates())
    log("OK\n")

    log("Génération csv...")
    write_csv(config, compta, '', compta.debut, compta.fin)
    if compta_prev:
        write_csv(config, compta_prev, '.prev', compta_prev.debut, compta_prev.fin)

    log("OK\n")

    log("Génération html...")
    write_html(config, compta, '', compta.debut, compta.fin)
    if compta_prev:
        write_html(config, compta_prev, '.prev', compta_prev.debut, compta_prev.fin)

    xslt(config.destpath('facturation.xml'),
         'facturation2html.xsl',
         config.destpath('facturation.html'),
         params)

    xslt(config.destpath('pilote.xml'),
         'pilote2html.xsl',
         config.destpath('pilote.html'),
         params)

    for date in dates_recap :
        write_html(config, compta,
                   '.'+date.Format("%Y-%m"),
                   date+RelativeDateTime(day=1),
                   date+RelativeDateTime(day=-1))
        log('.'+date.Format("%Y-%m"))

    for date in dates_prev :
        write_html(config, compta_prev,
                   '.'+date.Format("%Y-%m")+'.prev',
                   date+RelativeDateTime(day=1),
                   date+RelativeDateTime(day=-1))
        log('.'+date.Format("%Y-%m"))
    log('. OK\n')
