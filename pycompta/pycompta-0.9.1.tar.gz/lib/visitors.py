# -*- coding: utf-8 -*-

"""
PyCompta

Ce module définit les visiteurs qui écrivent les entités manipulées dans des
fichiers XML.
"""

__revision__ = "$Id: visitors.py,v 1.34 2005-10-31 18:10:57 nico Exp $"

from pycompta import L1, version, DEBUT
from pycompta.lib import entities, definitions
from pycompta import DateTimeDelta, DateTimeType

def toxml(s) :
    """
    Transforme objet en chaîne prête à être écrite dans un fichier XML.
    (convertit date en chaîne, remplace & et < et encode résultat.
    """
    if type(s) is DateTimeType :
        s = s.date
    return s.encode(L1).replace('&','&amp;').replace('<','&lt;')

ENTETE = '<?xml version="1.0" encoding="%s"?>\n' \
         '<!-- pycompta version %s -->\n' % (L1, version)

# VUE COMPTES ##################################################################

def write_vue_comptes(out, glivre, vuc, detail=False) :
    for compte in vuc.comptes :
        vc = glivre.get_vue_comptes(vuc.debut, vuc.fin, [compte.num])
        out.write('<compte num="%s" '
                  'report-credit="%i" report-debit="%i" report-solde="%i" '
                  'var-credit="%i" var-debit="%i" var-solde="%i" '
                  'credit="%s" debit="%s" solde="%s"'
                  % ((compte.num,) + vc.solde_debut + (vc.total_debut,)
                     + vc.variations + (vc.total_variations,)
                     + vc.solde_fin + (vc.total_fin,)))
        if detail:
            out.write('>\n')
            for num, montant in compte.get_credits(vuc.debut, vuc.fin) :
                e = glivre.journal.get_ecriture(num)
                out.write('    <credit e_num="%i" date="%s" montant="%i">' \
                          '%s</credit>\n' % (num, e.date.date,
                                             montant,toxml(e.libelle)))
            for num, montant in compte.get_debits(vuc.debut, vuc.fin) :
                e = glivre.journal.get_ecriture(num)
                out.write('    <debit e_num="%i" date="%s" montant="%i">' \
                          '%s</debit>\n' % (num, e.date.date,
                                            montant, toxml(e.libelle)))
            out.write('</compte>\n')
        else:
            out.write('/>\n')

# IMMOBILISATIONS ##############################################################

def write_livre_immo(out, livre_immo, debut, fin) :
    """
    Ecrit la liste des immobilisations et amortissements dans un fichier XML
    """
    out.write(ENTETE)
    out.write('<immo-amort debut="%s" fin="%s" ' % (debut.date, fin.date))
    brut, amort = livre_immo.get_cumul(fin)
    out.write('montant-brut="%i" montant-amort="%i" montant-net="%i">\n' \
              % (brut, amort, brut-amort))
    for i in livre_immo.immobilisations :
        if i.entree > fin :
            continue
        amort = i.get_cumul_dotations(fin)
        sortie = i.sortie and i.sortie.date or '-'
        out.write('  <immo entree="%s" sortie="%s" duree="%i" compte="%s" '\
                  'montant-brut="%i" montant-amort="%i" montant-net="%i">'\
                  '%s</immo>\n' % (i.entree.date, sortie, i.duree, toxml(i.compte),
                                   i.montant, amort, i.montant-amort,
                                   toxml(i.libelle)))
    out.write('</immo-amort>\n')

def all_comptes(poste):
    id_poste, nom_poste, comptes_immo, comptes_amort, subdivisions_poste = poste
    for cnum, cond in comptes_immo:
        yield cnum
    for sub in subdivisions_poste:
        for cnum in all_comptes(sub):
            yield cnum

def _w_i(out, glivre, poste, debut, fin, mul) :
    """
    Fonction récursive appellée pour écrire postes du bilan d'immo
    """
    id_poste, nom_poste, comptes_immo, comptes_amort, subdivisions_poste = poste
    comptes = list(all_comptes(poste))
    vc = glivre.get_vue_comptes(debut, fin, comptes)
    out.write('<poste id="%s" nom="%s"' % (toxml(id_poste), toxml(nom_poste)))
    out.write(' report-solde="%i" solde="%i"' % (-1*vc.total_debut, -1*vc.total_fin))
    out.write(' var-credit="%i" var-debit="%i"' % (vc.variations))
    out.write('>\n')
    if subdivisions_poste :
        for n in subdivisions_poste :
            _w_i(out, glivre, n, debut, fin, mul)
    else:
        write_vue_comptes(out, glivre, vc)
    out.write('</poste>\n')

def write_bilan_immo(out, bimmo, debut, fin) :
    """
    Ecrit le bilan des immobilisations en XML.
    """
    out.write(ENTETE)
    out.write('<bilan-immo debut="%s" fin="%s" ' % (debut.date, fin.date))
    comptes = []
    for poste in definitions.IMMO_AMORT:
        comptes += list(all_comptes(poste))
    vc = bimmo.glivre.get_vue_comptes(debut, fin, comptes)
    out.write(' report-solde="%i" solde="%i"' % (-1*vc.total_debut, -1*vc.total_fin))
    out.write(' var-credit="%i" var-debit="%i"' % (vc.variations))
    out.write('>\n')
    for p in definitions.IMMO_AMORT :
        _w_i(out, bimmo.glivre, p, debut, fin, 1)
    out.write('</bilan-immo>\n')

# JOURNAL ######################################################################

def write_ecriture(out, ecriture, trf=lambda x:x):
    e = ecriture
    out.write('  <ecriture date="%s" e_num="%i">\n' % (e.date.date, e.num))
    out.write('    <libelle>%s</libelle>\n' % toxml(e.libelle))
    for c, m in e.credits :
        out.write('    <credit compte="%s" montant="%s"/>\n' %
                  (toxml(c), trf(m)))
    for c, m in e.debits :
        out.write('    <debit compte="%s" montant="%s"/>\n' %
                  (toxml(c), trf(m)))
    if e.reference :
        out.write('    <reference>%s</reference>\n' % toxml(e.reference))
    if e.reglement :
        out.write('    <reglement>%s</reglement>\n' % toxml(e.reglement))
    for r in e.refs :
        out.write('    <ref type="%s" id="%s">%s</ref>\n'
                  % tuple([toxml(rr) for rr in r]))
    out.write('  </ecriture>\n')

def write_journal(out, journal, debut, fin) :
    """
    Ecrit le journal en XML
    """
    out.write(ENTETE)
    out.write('<journal debut="%s" fin="%s" ' % (debut.date, fin.date))
    out.write('credit="%s" debit="%s">\n' % journal.get_total(debut, fin))
    for ecr in journal.get_ecritures(debut, fin) :
        write_ecriture(out, ecr)
    out.write('</journal>\n')

def write_ecritures(out, ecritures) :
    """
    Ecrit les ecritures en XML
    """
    out.write(ENTETE)
    out.write('<ecritures>')
    for ecr in ecritures:
        write_ecriture(out, ecr, lambda x: '%.2f'%(float(x)/100))
    out.write('</ecritures>\n')

# COMPTE ######################################################################

def write_historique_comptes(out, glivre, debut, fin, starts_with='') :
    """
    Ecrit l'historique d'un compte en XML
    """
    vc = glivre.get_vue_comptes(debut, fin, [starts_with])
    out.write(ENTETE)
    out.write('<compte num="%s" ' % starts_with)
    out.write('debut="%s" fin="%s" ' % (debut.date, fin.date))
    out.write('report-credit="%i" report-debit="%i" report-solde="%i" '
              'var-credit="%i" var-debit="%i" var-solde="%i" '
              'credit="%s" debit="%s" solde="%s"'
              % (vc.solde_debut + (vc.total_debut,)
                 + vc.variations + (vc.total_variations,)
                 + vc.solde_fin + (vc.total_fin,)))
    out.write('>\n')
    for date, credit, debit, solde, e in glivre.get_historique_comptes(debut, fin, starts_with) :
        out.write('  <mouvement date="%s" e_num="%i"' % (e.date.date, e.num))
        out.write(' credit="%s" debit="%s" solde="%s">\n' % (credit, debit, solde))
        out.write('    <libelle>%s</libelle>\n' % toxml(e.libelle))
        if e.reference :
            out.write('    <reference>%s</reference>\n' % toxml(e.reference))
        if e.reglement :
            out.write('    <reglement>%s</reglement>\n' % toxml(e.reglement))
        for r in e.refs :
            out.write('    <ref type="%s" id="%s">%s</ref>\n'
                      % tuple([toxml(rr) for rr in r]))
        out.write('  </mouvement>\n')
    out.write('</compte>\n')

# GRAND LIVRE ##################################################################

def write_grand_livre(out, glivre, debut, fin) :
    """
    Ecrit le grand livre en XML.
    """
    out.write(ENTETE)
    out.write('<grand-livre debut="%s" fin="%s" ' % (debut.date, fin.date))
    vc = glivre.get_vue_comptes(debut, fin)
    out.write('report-credit="%i" report-debit="%i" report-solde="%i" '
              'var-credit="%i" var-debit="%i" var-solde="%i" '
              'credit="%s" debit="%s" solde="%s">\n'
              % (vc.solde_debut + (vc.total_debut,)
                 + vc.variations + (vc.total_variations,)
                 + vc.solde_fin + (vc.total_fin,)))
    write_vue_comptes(out, glivre, vc, True)
    out.write('</grand-livre>\n')

# BALANCE ######################################################################

def write_balance(out, balance, debut, fin) : # XXX deprecated by render_html
    """
    Ecrit la balance en XML.
    """
    out.write(ENTETE)
    out.write('<balance debut="%s" fin="%s">\n' % (debut.date, fin.date))
    for c_num, report_c, report_d, credit, debit \
            in balance.get_solde_comptes(debut, fin):
        out.write('  <compte numero="%s"'
                  ' report-credit="%s" report-debit="%s"'
                  ' credit="%s" debit="%s"/>\n'
                  % (toxml(c_num), report_c, report_d, credit, debit))
    out.write('</balance>\n')

# COMPTE RESULTAT ##############################################################

def _w_c_r(out, resultat, poste, debut, fin, mul) :
    """
    Fonction récursive appellée pour écrire postes du compte de résultat
    """
    id_poste, nom_poste, liste_comptes, subdivisions_poste = poste
    out.write('<poste id="%s" nom="%s"' % (toxml(id_poste), toxml(nom_poste)))
    out.write(' montant="%i"' % (mul*resultat.get_total(debut, fin, poste)))
    out.write('>\n')
    if subdivisions_poste :
        for n in subdivisions_poste :
            _w_c_r(out, resultat, n, debut, fin, mul)
    else :
	for cnum, cond in liste_comptes :
	    out.write('<compte num="%s" credit="%s" debit="%s" />\n' \
		      % ((cnum,) + resultat.glivre.get_solde_comptes(debut, fin, cnum)))
    out.write('</poste>\n')

def write_compte_resultat(out, resultat, debut, fin) :
    """
    Ecrit le compte de résultat en XML.
    """
    out.write(ENTETE)
    out.write('<compte-resultat debut="%s" fin="%s">\n' % (debut.date, fin.date))
    charges, produits = resultat.get_resultat(debut, fin)
    out.write('  <charges id="charges" montant="%s">\n' % charges)
    for p in definitions.CHARGES :
        _w_c_r(out, resultat, p, debut, fin, -1)
    out.write('  </charges>\n')
    out.write('  <produits id="produits" montant="%s">\n' % produits)
    for p in definitions.PRODUITS :
        _w_c_r(out, resultat, p, debut, fin, 1)
    out.write('  </produits>\n')
    out.write('</compte-resultat>\n')

# BILAN ########################################################################

def _w_b_actif(out, bilan, poste, debut, fin, mul) :
    """
    Fonction récursive appellée pour écrire actif du bilan
    """
    id_poste, nom, comptes_brut, comptes_amort, subdivisions_poste = poste
    out.write('<poste id="%s" nom="%s"' % (toxml(id_poste), toxml(nom)))
    brut, amort = bilan.get_solde_compte_diff(debut, fin, poste)
    out.write(' montant-brut="%i" montant-amort="%i" montant="%i"' %
              (mul*brut, (-1)*mul*amort, mul*(brut+amort)))
    out.write('>\n')
    if subdivisions_poste :
        for n in subdivisions_poste :
            _w_b_actif(out, bilan, n, debut, fin, mul)
    else :
	for cnum, cond in comptes_brut+comptes_amort :
	    out.write('<compte num="%s" credit="%s" debit="%s" cond="%s" />\n' \
		      % ((cnum,) + bilan.resultat.glivre.get_solde_comptes(debut, fin, cnum) +
                         (cond or '',)))
    out.write('</poste>\n')

def _w_b_passif(out, bilan, poste, debut, fin, mul) :
    """
    Fonction récursive appellée pour écrire postes du bilan
    """
    id_poste, nom, comptes, subdivisions_poste = poste
    out.write('<poste id="%s" nom="%s"' % (toxml(id_poste), toxml(nom)))
    out.write(' montant="%i"' % (mul*bilan.get_solde_poste(debut, fin, poste)))
    out.write('>\n')
    if subdivisions_poste :
        for n in subdivisions_poste :
            _w_b_passif(out, bilan, n, debut, fin, mul)
    else:
	for cnum, cond in comptes :
	    out.write('<compte num="%s" credit="%s" debit="%s" cond="%s" />\n' \
		      % ((cnum,) + bilan.resultat.glivre.get_solde_comptes(debut, fin, cnum) +
                         (cond or '',)))
    out.write('</poste>\n')


def write_bilan(out, bilan, debut, fin) :
    """
    Ecrit le bilan en XML.
    """
    out.write(ENTETE)
    out.write('<bilan debut="%s" fin="%s">\n' % (debut.date, fin.date))
    actif, passif = bilan.get_bilan(DEBUT, fin) # XXX was debut
    out.write('  <actif montant="%s">\n' % actif)
    for n in definitions.ACTIF :
        _w_b_actif(out, bilan, n, DEBUT, fin, -1) # XXX
    out.write('  </actif>\n')
    out.write('  <passif montant="%s">\n' % passif)
    for n in definitions.PASSIF :
        _w_b_passif(out, bilan, n, DEBUT, fin, 1)
    out.write('  </passif>\n')
    out.write('</bilan>\n')

# PILOTE #######################################################################

def _write_pilote(out, compta, dates):
    for etat in [compta.get_etat(date) for date in dates]:
        out.write('<mensualite mois="%(mois)s" annee="%(annee)s"'
                  ' balance="%(balance)s"' % etat)
        out.write(' compte-resultat-charges="%i" compte-resultat-produits="%i"'
                  % etat['resultat'])
        out.write(' bilan-actif="%i" bilan-passif="%i"' % etat['bilan'])
        out.write(' tresorerie="%i"' % etat['tresorerie'])
        out.write(' produits="%i"' % etat['produits'])
        out.write(' charges="%i"' % etat['charges'])
        out.write(' immobilisations="%i"/>\n' % etat['immobilisations'])

def write_pilote(out, compta, dates_recap, compta_prev, dates_prev):
    """
    Ecrit le pilote en XML.
    """

    out.write(ENTETE)
    out.write('<pilote>\n<previsions>\n')
    _write_pilote(out, compta_prev, dates_prev)
    out.write('\n</previsions>\n<recapitulatif>\n')
    _write_pilote(out, compta, dates_recap)
    out.write('\n</recapitulatif>\n')
    out.write('<tresorerie>')
    for num, cpt in compta.glivre.get_comptes('5'):
        out.write('<compte num="%s"/>' % num)
    out.write('</tresorerie>\n')
    out.write('</pilote>\n')

