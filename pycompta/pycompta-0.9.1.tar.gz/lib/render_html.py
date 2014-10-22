# -*- coding: utf-8 -*-

"""
Render xml to html
"""

DOCTYPE = u'''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0//EN">'''
HEADER = u'''<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<link rel="stylesheet" type="text/css" href="http://intranet.logilab.fr/css/intranet.css">
<script language="javascript" type="text/javascript" src="http://intranet.logilab.fr/lib/mochikit/1.4/MochiKit.js"></script>
<title>%(title)s</title>
<script language="javascript">
    function toggleVisible(id) {
      elt = document.getElementById(id);
      if (elt.style.display == 'block') { elt.style.display = 'none' }
      else { elt.style.display = 'block' };
    }
</script>
</head>
<body><h1>%(title)s</h1><div>%(breadcrumbs)s</div>'''
FOOTER = u'''</body></html>'''
TRHIGHLIGHT = u'''<tr onmouseover="addElementClass(this, 'highlighted');" ''' \
    '''onmouseout="removeElementClass(this, 'highlighted')">'''

SOCIETE = '%soc%'

# FIXME: move javascript to lib ?

def fmc(compte, key, empty_if_zero=True):
    return format_montant(compte.get(key), empty_if_zero)

def format_montant(montant, empty_if_zero=True, separator='&nbsp;'):
    assert isinstance(montant, int) or isinstance(montant, str), type(montant)
    if empty_if_zero and not int(montant):
        return ''
    if isinstance(montant, int):
        montant = '%i' % montant
    if len(montant) == 1:
        return '0,0%s' % montant
    elif len(montant) == 2:
        return '0,%s' % montant
    else:
        r = ','+montant[-2:]
        montant = montant[:-2]
        sep = ''
        while montant:
            r = montant[-3:] + sep + r
            montant = montant[:-3]
            sep = separator
        return r

def _breadcrumbs(items):
    txt = []
    for url, label in items:
        if url:
            txt.append(u'<a href="%s">%s</a>' % (url, label))
        else:
            txt.append(label)
    return u' > '.join(txt)

def breadcrumbs(tree, label):
    items = [('../', u'comptabilité'),
             ('pilote.html', get_exercice(tree)),
             (None, label)]
    return _breadcrumbs(items)

def get_exercice(tree):
    debut = tree.get('debut')[:4]
    fin =  tree.get('fin')[:4]
    if debut == fin:
        return debut
    else:
        return u'%s-%s' % (debut,fin)

def write_journal(out, journal, planc):
    jnl = journal.getroot()
    out.write(DOCTYPE)
    title = u'Comptabilité %s -- Journal du %s au %s' % (SOCIETE, jnl.get('debut'), jnl.get('fin'))
    out.write(HEADER % {'title':title,'breadcrumbs':breadcrumbs(jnl,'journal')})
    out.write(u'''
        <table align="center" width="100%" class="pycompta">
        <thead><tr>
        <th>Date</th>
        <th>N° Compte</th>
        <th width="50%">Compte</th>
        <th>Débit</th>
        <th>Crédit</th>
        </tr></thead>
        <tbody>
        ''')
    ecritures = [(ecr.get('date'), ecr) for ecr in journal.findall('ecriture')]
    ecritures.sort()
    ecritures.reverse()
    for pos, (date, ecriture) in enumerate(ecritures):
        rowcolor = (pos % 2) and 'rowlight' or 'rowdark'
        out.write(u'''<tr class="%s" valign="top">
            <td align="center"><a name="%s">%s</a></td>
            <td></td><td></td><td></td><td></td></tr>
            ''' % (rowcolor, ecriture.get('e_num'), ecriture.get('date')))
        for cpt, debit in sorted([(deb.get('compte'), deb) for deb in ecriture.findall('debit')]):
            out.write(u'''<tr class="%s" valign="top">
                <td></td>
                <td align="left"><a href="grand-livre.html#compte%s">%s</a></td>
                <td>%s</td>
                <td align="right">%s</td>
                <td></td>
                </tr>
                ''' % (rowcolor, cpt, cpt, planc.get(cpt), fmc(debit, 'montant')))
        for cpt, credit in sorted([(cred.get('compte'), cred) for cred in ecriture.findall('credit')]):
            out.write(u'''<tr class="%s" valign="top">
                <td></td>
                <td align="right"><a href="grand-livre.html#compte%s">%s</a></td>
                <td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s</td>
                <td></td>
                <td align="right">%s</td>
                </tr>
                ''' % (rowcolor, cpt, cpt, planc.get(cpt), fmc(credit, 'montant')))
        txt = u''
        if ecriture.get('ref'):
            txt += u'Cf %s <br />' % ecriture.get('ref')
        for reg in ecriture.findall('reglement'):
            txt += u'Réglement %s %s <br />' % (reg.get('type',''), reg.text)
        txt += u'<em>%s</em>' % ecriture.findtext('libelle')
        out.write(u'''<tr class="%s">
            <td></td> <td></td> <td>%s</td> <td></td> <td></td>
            </tr>''' % (rowcolor, txt))
    out.write(u'''</tbody>
        <tfoot><tr>
        <td colspan="2"></td>
        <td><b>TOTAUX</b></td>
        <td align="right"><b>%s</b></td>
        <td align="right"><b>%s</b></td>
        </tr></tfoot>
        </table>
        ''' % (fmc(jnl, 'debit'), fmc(jnl, 'credit')))
    out.write(FOOTER)

def write_grandlivre(out, glivre, planc):
    glnode = glivre.getroot()
    out.write(DOCTYPE)
    title = u'Comptabilité %s -- Grand Livre du %s au %s' % (
        SOCIETE, glnode.get('debut'), glnode.get('fin'))
    out.write(HEADER % {'title':title,'breadcrumbs': breadcrumbs(glnode,'grand livre')})
    out.write(u'<p>Comptes')
    for compte in glivre.findall('compte'):
        out.write(u'<a href="#compte%s" title="%s">%s</a> - '
                  % (compte.get('num'), planc.get(compte.get('num'),u''), compte.get('num')))
    out.write(u'</p>')
    for compte in glivre.findall('compte'):
        out.write(u'''<hr>
        <a name="compte%s"></a><h2>Compte %s - %s</h2>
        <table border="0" width="100%%" align="center">
        ''' % (compte.get('num'), compte.get('num'), planc.get(compte.get('num'),u'')))
        if int(compte.get('report-solde')) < 0:
            out.write(u'<tr><td colspan="2" align="left"><b>Report débit %s</b></td></tr>'
                      % fmc(compte, 'report-solde'))
        elif int(compte.get('report-solde')) > 0:
            out.write(u'<tr><td colspan="2" align="right"><b>Report crédit %s</b></td></tr>'
                      % fmc(compte, 'report-solde'))
        out.write(u'''
        <tr valign="top">
        <td width="50%%">
            <table border="0" align="center" width="100%%" cellpadding="2"><tr>
            <td width="15%%"></td>
            <td width="70%%"><i>Total Débits</i></td>
            <td width="15%%" align="right"><i>%s</i></td>
            </tr></table>
        </td>
        <td width="50%%">
            <table border="0" align="center" width="100%%" cellpadding="2"><tr>
            <td width="15%%"></td>
            <td width="70%%"><i>Total Crédits</i></td>
            <td width="15%%" align="right"><i>%s</i></td>
            </tr></table>
        </td>
        </tr>''' % (fmc(compte, 'var-debit', False), fmc(compte, 'var-credit', False)))
        if int(compte.get('solde')) < 0:
            out.write(u'<tr><td colspan="2" align="left"><b>COMPTE DEBITEUR %s</b></td></tr>'
                      % fmc(compte, 'solde'))
        elif int(compte.get('solde')) > 0:
            out.write(u'<tr><td colspan="2" align="right"><b>COMPTE CREDITEUR %s</b></td></tr>'
                      % fmc(compte, 'solde'))
        out.write(u'</table>')
    out.write(u'''<hr>
        <table border="0" width="100%%><tr>
        <td align="left"><b>%s</b></td>
        <td><b>TOTAUX</b></td>
        <td align="right"><b>%s</b></td>
        </tr></table>''' % (fmc(glnode, 'debit'), fmc(glnode, 'credit')))
    out.write(FOOTER)

def write_balance(out, glivre, planc):
    glnode = glivre.getroot()
    out.write(DOCTYPE)
    title = u'Comptabilité %s -- Balance du %s au %s' % (
        SOCIETE, glnode.get('debut'), glnode.get('fin'))
    out.write(HEADER % {'title':title,'breadcrumbs': breadcrumbs(glnode,'balance')})
    out.write(u'''
<table width="100%" align="center" cellpadding="3" class="pycompta">
<thead>
<tr>
<th colspan="2" rowspan="2">Compte</th>
<th colspan="2">Report</th>
<th colspan="2">Période</th>
<th colspan="2">Solde</th>
</tr>
<tr>
<th>Débit</th>
<th>Crédit</th>
<th>Débit</th>
<th>Crédit</th>
<th>Débit</th>
<th>Crédit</th>
</tr>
</thead>
<tbody>
''')
    for compte in glivre.findall('compte'):
        total = int(compte.get('solde'))
        out.write(u'''
        <tr onmouseover="addElementClass(this, \'highlighted\');" onmouseout="removeElementClass(this, \'highlighted\')" class="rowlight">
        <td><a href="grand-livre.html#compte%s">%s</a></td>
        <td>%s</td>
        <td align="right">%s</td>
        <td align="right">%s</td>
        <td align="right">%s</td>
        <td align="right">%s</td>
        <td align="right">%s</td>
        <td align="right">%s</td>
        </tr>
        ''' % (compte.get('num'), compte.get('num'), planc.get(compte.get('num'), u''),
               fmc(compte, 'report-debit'), fmc(compte, 'report-credit'),
               fmc(compte, 'var-debit'), fmc(compte, 'var-credit'),
               format_montant(max(-total,0)), format_montant(max(total,0))
               ))
    out.write(u'''
    <tr>
    <td><b>TOTAUX</b></td>
    <td> </td>
    <td align="right"><b>%s</b></td>
    <td align="right"><b>%s</b></td>
    <td align="right"><b>%s</b></td>
    <td align="right"><b>%s</b></td>
    <td align="right"><b>%s</b></td>
    <td align="right"><b>%s</b></td>
    </tr>
    ''' % (fmc(glnode, 'report-debit'), fmc(glnode, 'report-credit'),
           fmc(glnode, 'var-debit'), fmc(glnode, 'var-credit'),
           fmc(glnode, 'debit'), fmc(glnode, 'credit')
           ))
    out.write(u'</tbody></table>')
    out.write(FOOTER)

def depth_style(depth, msg, has_child=True):
    if depth == 0 and has_child:
        return u'''<b>%s</b>''' % msg
    elif depth == 1 and has_child:
        return u'''<i>%s</i>''' % msg
    else:
        return u'''%s''' % msg

def write_decompte_poste(out, poste, planc):
    out.write(u'''<a onclick="javascript:toggleVisible('%s')">%s</a>''' \
                  % (poste.get('id'), poste.get('nom')))
    out.write(u'''<div align="right" style="display: none" id="%s">
        <table border="1" style="border-collapse: collapse">''' % poste.get('id'))
    out.write(u'''<thead><tr><th>compte</th><th>crédit</th><th>débit</th></tr></thead>''')
    for compte in poste.findall('compte'):
        out.write(u'''<tr><td>%s - %s</td><td>%s</td><td>%s</td></tr>''' % (
                compte.get('num'), planc.get(compte.get('num'),'error'),
                fmc(compte, 'credit'), fmc(compte, 'debit')))
    out.write(u'''</table></div>''')

def write_poste_resultat(out, poste, planc, postes_prec, depth=0):
    out.write(TRHIGHLIGHT)
    out.write(u'''<td valign="top">''')
    nom = poste.get('nom')
    ident = poste.get('id')
    out.write(u'&#xA0;&#xA0;&#xA0;&#xA0;&#xA0;&#xA0;' * depth)
    subpostes = poste.findall('poste')
    if depth == 0:
        out.write(u'<b>%s</b>' % nom)
    elif subpostes:
        out.write(u'<i>%s</i>' % nom)
    else:
        write_decompte_poste(out, poste, planc)
    out.write(u'''</td><td valign="top" align="right">''')
    if subpostes:
        out.write('&#xA0;')
    elif depth == 0:
        out.write(u'''<b>%s</b>''' % fmc(poste, 'montant', False))
    else:
        out.write(fmc(poste,'montant', False))
    out.write(u'''</td><td valign="top" align="right">''')
    contenu = subpostes and '&#xA0;' or fmc(postes_prec[ident], 'montant', False)
    if depth == 0:
        out.write(u'''<b>%s</b>''' % contenu)
    else:
        out.write(contenu)
    out.write(u'</td></tr>')
    for sposte in subpostes:
        write_poste_resultat(out, sposte, planc, postes_prec, depth+1)
    if subpostes:
        out.write(u'''<tr><td align="right">''')
        txt = u'&#xA0;&#xA0;&#xA0;&#xA0;&#xA0;&#xA0;'*depth + u'Total %s' % poste.get('nom')
        out.write(depth_style(depth, txt))
        out.write(depth_style(depth, fmc(poste, 'montant', False)))
        out.write(u'''</td> <td align="right">''')
        out.write(depth_style(depth, fmc(postes_prec[ident], 'montant', False)))
        out.write(u'</td></tr>')

# FIXME: move lightgray below to css
def write_compte_resultat_total(out, title, new, old):
    out.write(u'''<tr bgcolor="lightgray">
        <td><b>%s</b></td>
        <td align="right"><b>%s</b></td>
        <td align="right"><b>%s</b></td>
        </tr>''' % (title, format_montant(new), format_montant(old)))

def write_compte_resultat(out, resultat, planc, cr_precedent):
    crnode = resultat.getroot()
    crnode_prec = cr_precedent.getroot()
    out.write(DOCTYPE)
    title = u'Comptabilité %s -- Compte résulat du %s au %s' % (
        SOCIETE, crnode.get('debut'), crnode.get('fin'))
    out.write(HEADER % {'title':title,'breadcrumbs': breadcrumbs(crnode,u'compte de résultat')})
    out.write(u'''<table class="pycompta" width="100%" align="center" cellpadding="3">
        <tr><td></td><th>N</th><th>N-1</th></tr>''')
    postes_prec = {}
    # produits
    pnode = crnode.find('produits')
    produits = dict([ (poste.get('id'), poste) for poste in pnode.findall('poste') ])
    pnode_prec = crnode_prec.find('produits')
    postes_prec.update( dict([ (poste.get('id'), poste) for poste in pnode_prec.findall('.//poste') ]) )
    # charges
    cnode = crnode.find('charges')
    charges = dict([ (poste.get('id'), poste) for poste in cnode.findall('poste') ])
    cnode_prec = crnode_prec.find('charges')
    postes_prec.update( dict([ (poste.get('id'), poste) for poste in cnode_prec.findall('.//poste') ]) )
    # resultat exploitation
    write_poste_resultat(out, produits['2.1'], planc, postes_prec)
    write_poste_resultat(out, charges['1.1'], planc, postes_prec)
    resultat_exploit = int(produits['2.1'].get('montant')) - int(charges['1.1'].get('montant'))
    resultat_exploit_prec = int(postes_prec['2.1'].get('montant')) - int(postes_prec['1.1'].get('montant'))
    write_compte_resultat_total(out, u"1- Résultat d'exploitation", resultat_exploit, resultat_exploit_prec)
    # resultat financier
    write_poste_resultat(out, produits['2.2'], planc, postes_prec)
    write_poste_resultat(out, charges['1.2'], planc, postes_prec)
    write_poste_resultat(out, produits['2.3'], planc, postes_prec)
    write_poste_resultat(out, charges['1.3'], planc, postes_prec)
    resultat_fin = int(produits['2.3'].get('montant')) - int(charges['1.3'].get('montant'))
    resultat_fin_prec = int(postes_prec['2.3'].get('montant')) - int(postes_prec['1.3'].get('montant'))
    write_compte_resultat_total(out, u"2- Résultat financier", resultat_fin, resultat_fin_prec)
    # resultat courant
    resultat_avimp = resultat_exploit + resultat_fin \
        + int(produits['2.2'].get('montant')) - int(charges['1.2'].get('montant'))
    resultat_avimp_prec = resultat_exploit_prec + resultat_fin_prec \
        + int(postes_prec['2.2'].get('montant')) - int(postes_prec['1.2'].get('montant'))
    write_compte_resultat_total(out, u"3- Résultat courant avant impôts", resultat_avimp, resultat_avimp_prec)
    # resultat exceptionnel
    write_poste_resultat(out, produits['2.4'], planc, postes_prec)
    write_poste_resultat(out, charges['1.4'], planc, postes_prec)
    resultat_excep = int(produits['2.4'].get('montant')) - int(charges['1.4'].get('montant'))
    resultat_excep_prec = int(postes_prec['2.4'].get('montant')) - int(postes_prec['1.4'].get('montant'))
    write_compte_resultat_total(out, u"4- Résultat exceptionnel", resultat_excep, resultat_excep_prec)
    # benefice ou perte
    write_poste_resultat(out, charges['1.5'], planc, postes_prec)
    write_poste_resultat(out, charges['1.6'], planc, postes_prec)
    out.write(u'''<tr><td>&#xA0;</td><td>&#xA0;</td><td>&#xA0;</td></tr>''')
    out.write(u'''<tr>
          <td align="right"><b>Total des produits</b></td>
          <td align="right"><b>%s</b></td>
          <td align="right"><b>%s</b></td>
        </tr>''' % (fmc(pnode, 'montant'), fmc(pnode_prec, 'montant')))
    out.write(u'''<tr>
          <td align="right"><b>Total des charges</b></td>
          <td align="right"><b>%s</b></td>
          <td align="right"><b>%s</b></td>
        </tr>''' % (fmc(cnode, 'montant'), fmc(cnode_prec, 'montant')))
    benef_perte = int(pnode.get('montant')) - int(cnode.get('montant'))
    benef_perte_prec = int(pnode_prec.get('montant')) - int(cnode_prec.get('montant'))
    write_compte_resultat_total(out, u"5- Bénéfice ou perte", benef_perte, benef_perte_prec)
    out.write(u'''</table>''')
    out.write(FOOTER)

def write_poste_bilan(out, poste, planc, postes_prec, depth=0):
    out.write(TRHIGHLIGHT)
    poste_actif = poste.get('montant-brut') and True or False
    subpostes = poste.findall('poste')
    # label
    if poste_actif:
        out.write(u'''<td valign="top">''')
    else:
        out.write(u'''<td valign="top" colspan="3">''')
    nom = poste.get('nom')
    ident = poste.get('id')
    out.write(u'''&#xA0;&#xA0;&#xA0;&#xA0;&#xA0;&#xA0;''' * depth)
    if subpostes:
        out.write(depth_style(depth, nom))
    else:
        write_decompte_poste(out, poste, planc)
    out.write(u'''</td>''')
    if subpostes:
        if poste_actif:
            out.write('<td></td><td></td>')
        out.write('<td bgcolor="lightgray"></td><td></td>')
        out.write('</tr>')
        for sposte in subpostes:
            write_poste_bilan(out, sposte, planc, postes_prec, depth+1)
        out.write(TRHIGHLIGHT)
        if poste_actif:
            out.write('<td>')
        else:
            out.write('<td colspan=3>')
        out.write(u'''&#xA0;&#xA0;&#xA0;&#xA0;&#xA0;&#xA0;'''*depth)
        out.write(depth_style(depth, 'Total'))
        out.write('</td>')
    if poste_actif:
        out.write('<td align="right">')
        out.write(depth_style(depth, fmc(poste, 'montant-brut', False), has_child=subpostes))
        out.write('</td>')
        out.write('<td align="right">')
        out.write(depth_style(depth, fmc(poste, 'montant-amort', False), has_child=subpostes))
        out.write('</td>')
    out.write('<td align="right" bgcolor="lightgray">')
    out.write(depth_style(depth, fmc(poste, 'montant', False), has_child=subpostes))
    out.write('</td>')
    out.write('<td align="right">')
    out.write(depth_style(depth, fmc(postes_prec[ident], 'montant', False), has_child=subpostes))
    out.write('</td>')
    out.write('</tr>')
    if depth == 0:
        out.write(u'''<tr><td colspan="3">&#xA0;</td>
            <td bgcolor="lightgray">&#xA0;</td>
            <td>&#xA0;</td>
            </tr>''')

def write_bilan(out, bilan, planc, bilan_precedent):
    bnode = bilan.getroot()
    bnode_prec = bilan_precedent.getroot()
    out.write(DOCTYPE)
    title = u'Comptabilité %s -- Bilan au %s' % (SOCIETE, bnode.get('fin'))
    out.write(HEADER % {'title':title,'breadcrumbs': breadcrumbs(bnode,'bilan')})
    out.write(u'''<table class="pycompta" align="center">''')
    postes_prec = {}
    # prépare actif
    pnode = bnode.find('.//actif')
    pnode_prec = bnode_prec.find('.//actif')
    postes_prec.update( dict([ (poste.get('id'), poste) for poste in pnode_prec.findall('.//poste') ]) )
    # prépare passif
    cnode = bnode.find('.//passif')
    cnode_prec = bnode_prec.find('.//passif')
    postes_prec.update( dict([ (poste.get('id'), poste) for poste in cnode_prec.findall('.//poste') ]) )
    # écrit actif
    out.write(u''' <tr><th colspan="5" bgcolor="lightgray">Actif</th></tr>
              <tr><td>&#xA0;</td>
		<td align="center">Brut</td>
		<td align="center">Amort/Prov</td>
		<td align="center" bgcolor="lightgray"><b>Net N</b></td>
		<td align="center"><b>Net N-1</b></td>
              </tr>''')
    for poste in pnode.findall('poste'):
        write_poste_bilan(out, poste, planc, postes_prec)
    out.write(u'''<tr><td colspan="3"><b>Total général</b></td>
                <td align="right" bgcolor="lightgray"><b>%s</b></td>
                <td align="right"><b>%s</b></td>
              </tr>''' % (fmc(pnode, 'montant', False),
                          fmc(pnode_prec, 'montant', False)))
    # écrit passif
    out.write(u'''<tr><th colspan="5" bgcolor="lightgray">Passif</th></tr>
              <tr>
                <td colspan="3">&#xA0;</td>
                <td align="center" bgcolor="lightgray"><b>N</b></td>
                <td align="center"><b>N-1</b></td>
              </tr>''')
    for poste in cnode.findall('poste'):
        write_poste_bilan(out, poste, planc, postes_prec)
    out.write(u'''<tr><td colspan="3"><b>Total général</b></td>
                <td align="right" bgcolor="lightgray"><b>%s</b></td>
                <td align="right"><b>%s</b></td>
              </tr>''' % (fmc(cnode, 'montant', False),
                          fmc(cnode_prec, 'montant', False)))
    out.write(u'''</table>''')
    out.write(FOOTER)

def write_tva(out, glivre, planc):
    glnode = glivre.getroot()
    out.write(DOCTYPE)
    title = u'Comptabilité %s -- Rapprochement TVA du %s au %s' % (
        SOCIETE, glnode.get('debut'), glnode.get('fin'))
    out.write(HEADER % {'title':title,'breadcrumbs': breadcrumbs(glnode,'tva')})
    out.write(u'<br /><table class="pycompta" align="center">')
    out.write(u'<tr><th>Date</th><th>Libellé</th><th>TVA</th><th>HT estimé</th></tr>')
    total_ht = 0
    total_tva = 0
    for compte in glivre.findall('compte'):
        if compte.get('num') != '44571':
            continue
        for credit in compte.findall('credit'):
            ht_estime = int(float(credit.get('montant'))/.196)
            total_ht += ht_estime
            total_tva += int(credit.get('montant'))
            out.write(u'<tr><td>%s</td><td>%s</td><td align="right">%s</td><td align="right">%s</td></tr>'
                      % (credit.get('date'), credit.text, fmc(credit, 'montant', False),
                         format_montant(str(ht_estime), False)))
    out.write(u'<tr><td> </td><td align="right"><b>Total HT</b></td>'
              u'<td align="right"><b>%s</b></td><td align="right"><b>%s</b></td></tr>'
              % (format_montant(total_tva, False), format_montant(total_ht, False)))
    out.write(u'</table>')
    out.write(FOOTER)
