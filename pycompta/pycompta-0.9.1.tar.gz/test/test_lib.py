# -*- coding: utf-8 -*-

"""
PyCompta

Ce module rassemble les tests unitaires.
"""

__revision__ = "$Id: test_lib.py,v 1.14 2006-04-23 13:58:49 nico Exp $"

import sys
from cStringIO import StringIO
from logilab.common import testlib

from pycompta import DEBUT, FIN, Date
from pycompta import version as VERSION
from pycompta.lib import entities, visitors, xmlreader, definitions, diagrams
from pycompta.lib.comptas import Comptabilite

#from aspects.weaver import weaver
#from aspects.lib.contracts import ContractAspect
#weaver.weave_module(entities,ContractAspect)

def _mk_e1() :
    """
    Ecriture au premier janvier 2002, apport de 100 EUR de capital
    """
    e = entities.Ecriture(Date(2002,1,1))
    e.libelle = 'ecriture 1'
    e.add_credit(u'101',10000)
    e.add_debit(u'20',10000)
    return e

def _mk_e2() :
    """
    Ecriture au 20 janvier 2002, ???
    """
    e = entities.Ecriture(Date(2002,1,20))
    e.libelle = 'ecriture 2'
    e.add_credit(u'20',20000)
    e.add_debit(u'30',20000)
    return e

def _mk_e3() :
    """
    Ecriture au 21 janvier 2002, ???
    """
    e = entities.Ecriture(Date(2002,1,21))
    e.libelle = 'ecriture 3'
    e.add_credit(u'30',30000)
    e.add_credit(u'35',20000)
    e.add_debit(u'40',50000)
    return e

def _mk_e4() :
    """
    Ecriture au 25 janvier 2002, ???
    """
    e = entities.Ecriture(Date(2002,1,25))
    e.libelle = 'ecriture 4'
    e.add_credit(u'707',30000)
    e.add_debit(u'607',20000)
    return e

def _mk_i() :
    """
    Immobilisation au premier janvier 2002, ???
    """
    i = entities.Immobilisation(u'ecriture 1', Date(2002,1,1), None, 24, u'20', 10000)
    return i

# MONTANT #####################################################################

class MontantTC(testlib.TestCase) :
    """Tests pour lecture montants"""

    def test(self) :
        """tout"""
        self.assertEqual( xmlreader._montant('100'), 10000 )
        self.assertEqual( xmlreader._montant('100.45'), 10045 )
        self.assertEqual( xmlreader._montant('100,45'), 10045 )
        self.assertEqual( xmlreader._montant('100,4'), 10040 )

# ECRITURE #####################################################################

class EcritureTC(testlib.TestCase) :
    """Tests pour écriture comptable"""

    def setUp(self) :
        """une écriture au premier janvier 2002"""
        self.e = entities.Ecriture(Date(2002,1,1))

    def test_add_credit_1(self) :
        """ajout credit"""
        self.e.add_credit(u'101',10000)
        self.assertEqual( self.e.credits, [ ('101', 10000) ] )

    def test_add_debit_1(self) :
        """ajout debit"""
        self.e.add_debit(u'101',10000)
        self.assertEqual( self.e.debits, [ ('101', 10000) ] )

    def test_est_equilibre(self) :
        """verifie écriture équilibrée"""
        self.e.add_credit(u'101', 10000)
        self.e.add_debit(u'11', 10000)
        self.failUnless( self.e.est_equilibre() )

    def test_est_equilibre2(self) :
        """vérifie écriture pas équilibrée"""
        self.e.add_credit(u'101', 10000)
        self.e.add_debit(u'11', 10100)
        self.failIf( self.e.est_equilibre() )

    def test_entre(self) :
        """comparaison de dates"""
        self.failUnless( self.e.entre(Date(2002,1,1), Date(2002,1,2)) )
        self.failUnless( self.e.entre(Date(2002,1,1), Date(2002,12,31)) )
        self.failIf( self.e.entre(Date(2002,1,2), Date(2002,12,31)) )
        self.failUnless( self.e.entre(DEBUT, Date(2002,12,31)) )
        self.failUnless( self.e.entre(Date(2001,12,31),FIN) )

    def test_inclure(self) :
        self.e.add_credit(u'101', 10000)
        self.e.add_debit(u'11', 10000)
        d = entities.Ecriture(Date(2002,2,1))
        d.add_credit(u'101', 20000)
        d.add_debit(u'11', 20000)
        self.e.inclure(d)
        self.assertEqual( self.e.credits, [ ('101', 30000) ] )
        self.assertEqual( self.e.debits, [ ('11', 30000) ] )

# JOURNAL ######################################################################

class JournalTC(testlib.TestCase) :
    """Tests pour journal comptable"""

    def setUp(self) :
        """les écritures 1 et 2"""
        self.e1 = _mk_e1()
        self.e2 = _mk_e2()

    def test_tri(self) :
        """vérifie tri des écritures"""
        self.journal = entities.Journal([self.e1, self.e2])
        self.assertEqual(self.journal.ecritures, [self.e1, self.e2])

        self.journal = entities.Journal([self.e2, self.e1])
        self.assertEqual(self.journal.ecritures, [self.e1, self.e2])

    def test_get_ecriture(self) :
        """vérifie numérotation des écritures"""
        self.journal = entities.Journal([self.e1, self.e2])
        self.assertEqual(self.journal.get_ecriture(1), self.e1)
        self.assertEqual(self.journal.get_ecriture(2), self.e2)

class VisitorsJournalTC(testlib.TestCase) :
    """Tests visiteurs du journal"""

    def setUp(self) :
        self.journal = entities.Journal([_mk_e1(), _mk_e2()])

    def test_ecriture_xml(self) :
        """écriture du journal en XML"""
        buf = StringIO()
        visitors.write_journal(buf, self.journal, Date(2002,1,1), Date(2002,1,1))


# COMPTE #######################################################################

class CompteTC(testlib.TestCase) :
    """Tests pour compte"""

    def setUp(self):
        """les écritures 1 et 2, le journal et le compte 101"""
        self.e1 = _mk_e1()
        self.e2 = _mk_e2()
        self.journal = entities.Journal([self.e1, self.e2])
        self.c = entities.Compte('101', self.journal)

    def test_add_credit(self) :
        """crédite compte"""
        self.c.add_credit( self.e1, 10000 )
        self.assertEqual(self.c.credits, [(1,10000)])

    def test_add_debit(self) :
        """débite compte"""
        self.c.add_debit( self.e1, 10000 )
        self.assertEqual(self.c.debits, [(1,10000)])

    def test_get_credits_1(self) :
        """liste des opérations au crédit"""
        self.c.add_credit( self.e1, 10000 )
        self.assertEqual(self.c.get_credits(DEBUT,FIN), [(1,10000)])

    def test_get_credits_2(self) :
        """liste des opérations au crédit, avec date"""
        self.c.add_credit( self.e1, 10000 )
        self.assertEqual(self.c.get_credits(Date(2002,1,1),FIN), [(1,10000)])
        self.assertEqual(self.c.get_credits(DEBUT,Date(2002,2,1)), [(1,10000)])
        self.assertEqual(self.c.get_credits(Date(2002,2,1),FIN), [])

    def test_get_debits_1(self) :
        """liste des opérations au débit"""
        self.c.add_debit( self.e1, 10000 )
        self.assertEqual(self.c.get_debits(DEBUT,FIN), [(1,10000)])

    def test_get_debits_2(self) :
        """liste des opérations au débit, avec date"""
        self.c.add_debit( self.e1, 10000 )
        self.assertEqual(self.c.get_debits(Date(2002,2,1),FIN), [])

    def test_get_solde(self) :
        """calcul du solde (crédit,débit)"""
        self.c.add_debit( self.e1, 10000 )
        self.assertEqual(self.c.get_solde(DEBUT,FIN), (0, 10000))
        self.c.add_credit( self.e2, 20000 )
        self.assertEqual(self.c.get_solde(DEBUT,FIN), (20000, 10000))

    def test_get_mouvements(self) :
        """renvoie écritures triées par date"""
        self.c.add_debit( self.e1, 10000 )
        self.c.add_credit( self.e2, 20000 )
        res = [(self.e1.date, 0, 10000, self.e1), (self.e2.date, 20000, 0, self.e2)]
        self.assertEqual(self.c.get_mouvements(), res)

    def test_get_mouvements2(self) :
        """renvoie écritures triées par date -- ré-ordonne"""
        e1 = _mk_e1()
        e2 = _mk_e2()
        journal = entities.Journal([e2, e1])
        c = entities.Compte('101', journal)
        c.add_credit( self.e2, 20000 )
        c.add_debit( self.e1, 10000 )
        res = [(e1.date, 0, 10000, e1), (e2.date, 20000, 0, e2)]
        self.assertEqual(c.get_mouvements(), res)


# VUE COMPTES ##################################################################

class VueComptesTC(testlib.TestCase) :
    """Tests pour grand livre"""

    def setUp(self):
        """les écritres 1,2 et 3, le journal, le grand livre"""
        self.e1 = _mk_e1()
        self.e2 = _mk_e2()
        self.e3 = _mk_e3()
        self.journal = entities.Journal([self.e1, self.e2, self.e3])
        self.glivre = entities.GrandLivre(self.journal)

    def test_c101(self) :
        """un seul crédit"""
        vc = self.glivre.get_vue_comptes(DEBUT,FIN, ['101'])
        self.assertEqual(vc.solde_debut, (0,0))
        self.assertEqual(vc.variations, (10000,0))
        self.assertEqual(vc.solde_fin, (10000,0))
        self.assertEqual(vc.total_debut, 0)
        self.assertEqual(vc.total_variations, 10000)
        self.assertEqual(vc.total_fin, 10000)

    def test_c4(self) :
        """un seul débit"""
        vc = self.glivre.get_vue_comptes(DEBUT,FIN, ['40'])
        self.assertEqual(vc.solde_debut, (0,0))
        self.assertEqual(vc.variations, (0,50000))
        self.assertEqual(vc.solde_fin, (0,50000))
        self.assertEqual(vc.total_debut, 0)
        self.assertEqual(vc.total_variations, -50000)
        self.assertEqual(vc.total_fin, -50000)

    def test_c2(self) :
        """un débit un crédit"""
        vc = self.glivre.get_vue_comptes(DEBUT,FIN, ['20'])
        self.assertEqual(vc.solde_debut, (0,0))
        self.assertEqual(vc.variations, (20000,10000))
        self.assertEqual(vc.solde_fin, (20000,10000))
        self.assertEqual(vc.total_debut, 0)
        self.assertEqual(vc.total_variations, 10000)
        self.assertEqual(vc.total_fin, 10000)

    def test_c2b(self) :
        """un débit un crédit et une date"""
        vc = self.glivre.get_vue_comptes(Date(2002,1,19),FIN, ['20'])
        self.assertEqual(vc.solde_debut, (0,10000))
        self.assertEqual(vc.variations, (20000,0))
        self.assertEqual(vc.solde_fin, (20000,10000))
        self.assertEqual(vc.total_debut, -10000)
        self.assertEqual(vc.total_variations, 20000)
        self.assertEqual(vc.total_fin, 10000)

    def test_c3(self) :
        """plusieurs comptes"""
        vc = self.glivre.get_vue_comptes(DEBUT,FIN, ['30','35'])
        self.assertEqual(vc.solde_debut, (0,0))
        self.assertEqual(vc.variations, (50000,20000))
        self.assertEqual(vc.solde_fin, (50000,20000))
        self.assertEqual(vc.total_debut, 0)
        self.assertEqual(vc.total_variations, 30000)
        self.assertEqual(vc.total_fin, 30000)

    def test_c3b(self) :
        """plusieurs comptes et une date"""
        vc = self.glivre.get_vue_comptes(Date(2002,1,21),FIN, ['30','35'])
        self.assertEqual(vc.solde_debut, (0,20000))
        self.assertEqual(vc.variations, (50000,0))
        self.assertEqual(vc.solde_fin, (50000,20000))
        self.assertEqual(vc.total_debut, -20000)
        self.assertEqual(vc.total_variations, 50000)
        self.assertEqual(vc.total_fin, 30000)

# GRAND LIVRE ##################################################################

class GrandLivreTC(testlib.TestCase) :
    """Tests pour grand livre"""

    def setUp(self):
        """les écritres 1,2 et 3, le journal, le grand livre"""
        self.e1 = _mk_e1()
        self.e2 = _mk_e2()
        self.e3 = _mk_e3()
        self.journal = entities.Journal([self.e1, self.e2, self.e3])
        self.glivre = entities.GrandLivre(self.journal)

    def test_init(self) :
        """vérifie la création des comptes"""
        c = self.glivre.comptes.keys()
        c.sort()
        self.assertEqual(c, ['101','20','30','35','40'])

    def test_get_comptes(self) :
        """sélection des comptes"""
        c = [c_num for c_num,cpt in self.glivre.get_comptes()]
        self.assertEqual(c, ['101','20','30','35','40'])
        c = [c_num for c_num,cpt in self.glivre.get_comptes('1')]
        self.assertEqual(c, ['101'])
        c = [c_num for c_num,cpt in self.glivre.get_comptes('3')]
        self.assertEqual(c, ['30','35'])
        c = [c_num for c_num,cpt in self.glivre.get_comptes('4')]
        self.assertEqual(c, ['40'])
        c = [c_num for c_num,cpt in self.glivre.get_comptes('5')]
        self.assertEqual(c, [])

    def test_get_solde_comptes(self) :
        """calcul du solde des comptes"""
        gl = self.glivre
        self.assertEqual(gl.get_solde_comptes(DEBUT,FIN),      (80000,80000))
        self.assertEqual(gl.get_solde_comptes(DEBUT,FIN,'101'), (10000,0))
        self.assertEqual(gl.get_solde_comptes(DEBUT,FIN,'20'), (20000,10000))
        self.assertEqual(gl.get_solde_comptes(DEBUT,FIN,'30'), (30000,20000))
        self.assertEqual(gl.get_solde_comptes(DEBUT,FIN,'35'), (20000,0))
        self.assertEqual(gl.get_solde_comptes(DEBUT,FIN,'40'), (0,50000))
        self.assertEqual(gl.get_solde_comptes(DEBUT,FIN,'3'),  (50000,20000))

    def test_check(self):
        e = entities.Ecriture(Date(2002,1,25))
        e.libelle = 'ecriture 4'
        e.add_credit(u'10',30000)
        e.add_debit(u'20',20000)
        self.journal = entities.Journal([self.e1, self.e2, self.e3, e])
        self.glivre = entities.GrandLivre(self.journal)
        err = self.glivre.check()
        self.assertEqual(len(err), 1)

class VisitorsGrandLivre(testlib.TestCase) :
    """Tests pour visiteur du grand livre"""

    def setUp(self) :
        """l'écriture 1"""
        self.e1 = _mk_e1()

    def test_write_1(self):
        """écriture grand livre en XML"""
        expected = (
            '<?xml version="1.0" encoding="ISO-8859-1"?>\n'
            '<!-- pycompta version %s -->\n'
            '<grand-livre debut="2002-01-01" fin="2002-01-31" '
            'report-credit="0" report-debit="0" report-solde="0" '
            'var-credit="10000" var-debit="10000" var-solde="0" '
            'credit="10000" debit="10000" solde="0">\n'
            '<compte num="101" '
            'report-credit="0" report-debit="0" report-solde="0" '
            'var-credit="10000" var-debit="0" var-solde="10000" '
            'credit="10000" debit="0" solde="10000">\n'
            '    <credit e_num="1" date="2002-01-01" '
            'montant="10000">ecriture 1</credit>\n'
            '</compte>\n'
            '<compte num="20" '
            'report-credit="0" report-debit="0" report-solde="0" '
            'var-credit="0" var-debit="10000" var-solde="-10000" '
            'credit="0" debit="10000" solde="-10000">\n'
            '    <debit e_num="1" date="2002-01-01" '
            'montant="10000">ecriture 1</debit>\n'
            '</compte>\n'
            '</grand-livre>\n' % VERSION
            )
        self.journal = entities.Journal([self.e1])
        self.glivre = entities.GrandLivre(self.journal)
        out = StringIO()
        visitors.write_grand_livre(out, self.glivre,
                                   Date(2002,1,1), Date(2002,1,31))
        self.assertMultiLineEqual(expected, out.getvalue())

# BALANCE ######################################################################

class BalanceTC(testlib.TestCase) :
    """Tests pour balance comptable"""

    def setUp(self):
        """les écritures 1,2 et 3, le journal, le grand livre et la balance"""
        self.e1 = _mk_e1()
        self.e2 = _mk_e2()
        self.e3 = _mk_e3()
        self.journal = entities.Journal([self.e1, self.e2, self.e3])
        self.glivre = entities.GrandLivre(self.journal)
        self.balance = entities.Balance(self.glivre)

    def test_get_solde_comptes(self) :
        """calcul des soldes des comptes"""
        self.assertEqual( self.balance.get_solde_comptes(DEBUT,FIN),
                          [ ('101', 0,0, 10000, 0),
                            ('20',  0,0, 20000, 10000),
                            ('30',  0,0, 30000, 20000),
                            ('35',  0,0, 20000, 0),
                            ('40',  0,0, 0,     50000),
                            ])

    def test_get_total(self) :
        """calcul du total de la balance"""
        self.assertEqual( self.balance.get_total(DEBUT,FIN), (80000,80000) )

    def test_est_equilibre(self):
        """verifie équilibre de la balance"""
        self.failUnless( self.balance.est_equilibre(DEBUT,FIN) )

class VisitorsBalanceTC(testlib.TestCase) :
    """Tests visiteurs du journal"""

    def setUp(self) :
        self.journal = entities.Journal([_mk_e1(), _mk_e2()])
        self.glivre = entities.GrandLivre(self.journal)
        self.balance = entities.Balance(self.glivre)

    def test_ecriture_xml(self) :
        """écriture de la balance en XML"""
        buf = StringIO()
        visitors.write_balance(buf, self.balance, Date(2002,1,1), Date(2002,1,1))

# COMPTE RESULTAT ##############################################################

class CompteResultatTC(testlib.TestCase) :
    """Tests pour compte de résultat"""

    def setUp(self):
        """les écritures 1,2 et 3, le journal, le grand livre et le
        compte de résultat"""
        self.e1 = _mk_e1()
        self.e2 = _mk_e2()
        self.e3 = _mk_e3()
        self.e4 = _mk_e4()
        self.journal = entities.Journal([self.e1, self.e2, self.e3])
        self.glivre = entities.GrandLivre(self.journal)
        self.resultat = entities.CompteResultat(self.glivre)

    def test_get_total(self) :
        """calcul des totaux des postes"""
        r = self.resultat
        node = (u'1', u'Poste1', [(u'101', None)], [])
        self.assertEqual(r.get_total(DEBUT,FIN,node), 10000)
        node = (u'1', u'Poste1', [(u'101', 'C')], [])
        self.assertEqual(r.get_total(DEBUT,FIN,node), 10000)
        node = (u'1', u'Poste1', [(u'101', 'D')], [])
        self.assertEqual(r.get_total(DEBUT,FIN,node), 0)

        node = (u'3', u'Poste3', [(u'30', None),(u'35',None)], [])
        self.assertEqual(r.get_total(DEBUT,FIN,node), 30000)
        node = (u'3', u'Poste3', [(u'3', None)], [])
        self.assertEqual(r.get_total(DEBUT,FIN,node), 30000)

    def test_get_resultat(self) :
        """calcul du résultat"""
        self.e4 = _mk_e4()
        self.journal = entities.Journal([self.e4])
        self.glivre = entities.GrandLivre(self.journal)
        self.resultat = entities.CompteResultat(self.glivre)
        self.assertEqual(self.resultat.get_resultat(DEBUT,FIN), (20000,30000))

class VisitorsResultat(testlib.TestCase) :
    """Tests pour affichage du compte de résultat"""

    def setUp(self) :
        """l'écriture 4"""
        self.e4 = _mk_e4()

    def test_write_1(self):
        """écriture compte résultat en XML"""
        self.journal = entities.Journal([self.e4])
        self.glivre = entities.GrandLivre(self.journal)
        self.resultat = entities.CompteResultat(self.glivre)
        out = StringIO()
        visitors.write_compte_resultat(out, self.resultat,
                                       Date(2002,1,1), Date(2002,1,31))
        with file(self.datapath('compte-resultat.xml')) as stream:
            data = stream.read().replace('x.y.z', VERSION)
            expected = '\n'.join([line.strip() for line in data.splitlines()])
        result = '\n'.join([line.strip() for line in out.getvalue().splitlines()])
        self.assertMultiLineEqual(expected, result)


# BILAN ########################################################################

class BilanTC(testlib.TestCase) :
    """Tests pour bilan comptable"""

    def setUp(self):
        """les écritures 1,2 et 3, le journal, le grand livre, le
        compte de résultat et le bilan"""
        self.e1 = _mk_e1()
        self.e2 = _mk_e2()
        self.e3 = _mk_e3()
        self.journal = entities.Journal([self.e1, self.e2, self.e3])
        self.glivre = entities.GrandLivre(self.journal)
        self.resultat = entities.CompteResultat(self.glivre)
        self.bilan = entities.Bilan(self.resultat)

    def test_get_soldes(self) :
        """calcul des soldes des postes"""
        b = self.bilan

        node = (u'1', u'Poste1', [(u'10', None)], [])
        self.assertEqual(b.get_solde_poste(DEBUT,FIN,node), 10000)
        node = (u'1', u'Poste1', [(u'101', None)], [])
        self.assertEqual(b.get_solde_poste(DEBUT,FIN,node), 10000)
        node = (u'1', u'Poste1', [(u'101', 'C')], [])
        self.assertEqual(b.get_solde_poste(DEBUT,FIN,node), 10000)
        node = (u'1', u'Poste1', [(u'101', 'D')], [])
        self.assertEqual(b.get_solde_poste(DEBUT,FIN,node), 0)

        node = (u'3', u'Poste3', [(u'30', None),(u'35',None)], [])
        self.assertEqual(b.get_solde_poste(DEBUT,FIN,node), 30000)
        node = (u'3', u'Poste3', [(u'3', None)], [])
        self.assertEqual(b.get_solde_poste(DEBUT,FIN,node), 30000)

    def test_get_bilan(self) :
        """calcul du total actif/passif"""
        self.assertEqual( self.bilan.get_bilan(DEBUT,FIN), (-30000,10000) )

    def test_check(self):
        err = self.bilan.check()
        self.assertEqual(len(err), 2)

class VisitorsBilan(testlib.TestCase) :
    """Tests pour affichage du bilan"""

    def setUp(self) :
        """les écritures 1,2 et 3, le journal, le grand livre, le
        compte de résultat et le bilan"""
        self.e1 = _mk_e1()
        self.e2 = _mk_e2()
        self.e3 = _mk_e3()
        self.journal = entities.Journal([self.e1, self.e2, self.e3])
        self.glivre = entities.GrandLivre(self.journal)
        self.resultat = entities.CompteResultat(self.glivre)
        self.bilan = entities.Bilan(self.resultat)

    def test_write_1(self):
        """écriture d'un bilan simple en XML"""
        out = StringIO()
        visitors.write_bilan(out, self.bilan, Date(2002,1,1), Date(2002,2,1))
        lines = out.getvalue().splitlines()
        #self.assertEqual( out.getvalue(), '')
        actif_found = 0
        passif_found = 0
        poste_found = 0
        for l in lines:
            l=l.strip()
            if l.find('<actif')>=0:
                self.assertEqual( l, '<actif montant="-30000">' )
                actif_found = 1
            if l.find('<poste') >= 0 and l.find("Stocks") >= 0 :
                self.assertEqual(l, '<poste id="3.2.1" nom="Stocks et en-cours"' \
                                    ' montant-brut="-30000" montant-amort="0"' \
                                    ' montant="-30000">' )
                poste_found=1
            if l.find('<passif') >= 0:
                self.assertEqual( l, '<passif montant="10000">' )
                passif_found = 1
        self.assertEqual(actif_found,1,
                         'Couldn''t find line: <actif montant="30000">')
        self.assertEqual(passif_found,1,
                         'Couldn''t find line: <passif montant="10000">')
        self.assertEqual(poste_found,1,
                         'Couldn''t find line: <poste nom="Stocks" montant="30000">')

class FlattenTC(testlib.TestCase) :
    """Tests pour lecture montants"""

    def test(self) :
        """tout"""
        comptes = list(entities.flatten_desc(definitions.ACTIF[0], True))
        self.assertEqual(len(comptes), 48)


# IMMOBILISATION ###############################################################

class ImmobilisationTC(testlib.TestCase) :
    """Tests pour immobilisation"""

    def test_get_dotations(self) :
        """calcul des dotations"""
        immo = entities.Immobilisation(u'a', Date(2002,1,1),None,3,u'101',3000)
        self.assertEqual( immo.get_dotations(),
                          [(Date(2002,1,-1),'101',1000),
                           (Date(2002,2,-1),'101',1000),
                           (Date(2002,3,-1),'101',1000)])
        immo = entities.Immobilisation(u'a', Date(2002,1,1),None,3,u'101',3001)
        self.assertEqual( immo.get_dotations(),
                          [(Date(2002,1,-1),'101',1000),
                           (Date(2002,2,-1),'101',1000),
                           (Date(2002,3,-1),'101',1001)])
        immo = entities.Immobilisation(u'a', Date(2002,1,1),None,3,u'101',3002)
        self.assertEqual( immo.get_dotations(),
                          [(Date(2002,1,-1),'101',1000),
                           (Date(2002,2,-1),'101',1000),
                           (Date(2002,3,-1),'101',1002)])

    def test_get_dotations_avec_sortie(self) :
        """calcul des dotations avec sortie"""
        immo = entities.Immobilisation(u'a', Date(2002,1,1),Date(2002,2,15),3,u'101',3000)
        self.assertEqual( immo.get_dotations(),
                          [(Date(2002,1,-1),'101',1000),
                           (Date(2002,2,-1),'101',2000)])

class VisitorImmobilisations(testlib.TestCase) :
    """Tests pour affichage des immobilisations"""

    def setUp(self) :
        """une immobilisation"""
        self.immos = [entities.Immobilisation(u'a', Date(2002,1,1),None,3,u'101',3000)]

    def test_write_1(self):
        """écriture immobilisations en XML"""
        expected = (
            '<?xml version="1.0" encoding="ISO-8859-1"?>\n'
            '<!-- pycompta version %s -->\n'
            '<immo-amort debut="2002-01-01" fin="2002-01-31" '
            'montant-brut="3000" montant-amort="1000" '
            'montant-net="2000">\n'
            '  <immo entree="2002-01-01" sortie="-" duree="3" compte="101" '
            'montant-brut="3000" montant-amort="1000" '
            'montant-net="2000">a</immo>\n'
            '</immo-amort>\n' % VERSION
            )
        out = StringIO()
        lim = entities.LivreImmobilisations(self.immos)
        visitors.write_livre_immo(out, lim, Date(2002,1,1), Date(2002,1,31))
        self.assertMultiLineEqual(expected, out.getvalue())

class AmortissementTC(testlib.TestCase) :
    """Tests pour amortissements"""

    def test_get_amort(self) :
        """cacul amortissement"""
        immo1 = entities.Immobilisation(u'a', Date(2002,1,1),None,3,u'10',3000)
        immo2 = entities.Immobilisation(u'a', Date(2002,3,1),None,3,u'10',3000)
        li = entities.LivreImmobilisations([immo1,immo2])
        amort = li.get_amortissements( Date(2002,1,1), Date(2002,12,1) )
        # ecriture1
        self.assertEqual( amort[0].credits,[ ('180', 1000) ] )
        self.assertEqual( amort[0].debits, [ ('6811', 1000) ] )
        # ecriture2
        self.assertEqual( amort[1].credits,[ ('180', 1000) ] )
        self.assertEqual( amort[1].debits, [ ('6811', 1000) ] )
        # ecriture3
        self.assertEqual( amort[2].credits,[ ('180', 2000) ] )
        self.assertEqual( amort[2].debits, [ ('6811', 2000) ] )
        # ecriture4
        self.assertEqual( amort[3].credits,[ ('180', 1000) ] )
        self.assertEqual( amort[3].debits, [ ('6811', 1000) ] )
        # ecriture5
        self.assertEqual( amort[4].credits,[ ('180', 1000) ] )
        self.assertEqual( amort[4].debits, [ ('6811', 1000) ] )


# PILOTE #######################################################################

class ComptabiliteTC(testlib.TestCase) :
    """Test du pilote"""

    def setUp(self) :
        """les écritures 1, 2 et 3 et un pilote"""
        self.e1 = _mk_e1()
        self.e2 = _mk_e2()
        self.e3 = _mk_e3()
        self.i = _mk_i()
        self.pilote = Comptabilite(Date(2002,1,1), Date(2002,2,-1),
                                   [self.e1, self.e2, self.e3], [self.i])

    def test_get_etat(self) :
        """calcul de l'état au début deuxième mois"""
        self.assertEqual( self.pilote.get_etat( Date(2002,2,-1) ),
                          {'annee':2002, 'mois':2,
                           'journal':True, 'glivre':True, 'balance':True,
                           'resultat': (832,0), 'bilan': (-30000,9168),
                           'immobilisations': 9168,
                           'tresorerie':0, 'produits':0,
                           'charges':416, } )


    def test_get_dates(self) :
        self.compta = self.pilote
        self.compta.debut = Date(2003,10,1)
        self.compta.fin = Date(2003,12,31)
        d = self.compta.get_dates()
        self.assertEqual( d, [Date(2003,10,1), Date(2003,11,1), Date(2003,12,1)] )
        d = self.compta.get_dates(Date(2003,10,31))
        self.assertEqual( d, [Date(2003,10,1), Date(2003,11,1), Date(2003,12,1)] )

class VisitorsPiloteTC(testlib.TestCase) :
    """Tests visiteurs du pilote"""

    def setUp(self) :
        self.e1 = _mk_e1()
        self.e2 = _mk_e2()
        self.e3 = _mk_e3()
        self.i = _mk_i()
        self.pilote = Comptabilite(Date(2002,1,1), Date(2002,2,-1),
                                   [self.e1, self.e2, self.e3], [self.i])

    def test_ecriture_xml(self) :
        """écriture du pilote en XML"""
        buf = StringIO()
        dates = [Date(2002,1,1)]
        visitors.write_pilote(buf, self.pilote, dates, self.pilote, dates)


class DiagramTC(testlib.TestCase) :
    """Tests diagramme"""
    def setUp(self) :
        self.e1 = _mk_e1()
        self.e2 = _mk_e2()
        self.e3 = _mk_e3()
        self.i = _mk_i()
        self.pilote = Comptabilite(Date(2002,1,1), Date(2002,2,-1),
                                   [self.e1, self.e2, self.e3], [self.i])

    def test_diag_matplotlib(self) :
        """écriture du diagramme"""
        dates = [Date(2002,1,1), Date(2002,2,-1)]
        diagrams.diagram('/tmp/diag.png', self.pilote, dates)

    def test_diag_tres_matplotlib(self) :
        """écriture du diagramme tresorerie"""
        dates = [Date(2002,1,1), Date(2002,2,-1)]
        diagrams.diagram('/tmp/diag_tres.png', self.pilote, dates)

    def test_diag_flot(self) :
        """écriture du diagramme"""
        dates = [Date(2002,1,1), Date(2002,2,-1)]
        diagrams.diagram_flot('/tmp/diag.html', self.pilote, dates)

    def test_diag_tres_flot(self) :
        """écriture du diagramme tresorerie"""
        dates = [Date(2002,1,1), Date(2002,2,-1)]
        diagrams.diagram_flot('/tmp/diag_tres.html', self.pilote, dates)

# XML READER #################################################################

class XMLReaderTC(testlib.TestCase) :

    def test_ecritures(self) :
        """test lecture des fichiers XML d'écritures"""
        buf = StringIO("""<?xml version="1.0" encoding="iso-8859-1"?>
        <ecritures>
          <ecriture date="2002-01-01">
            <libelle>Bought an accounting tool</libelle>
            <debit compte="60" montant="80,40" />     <!-- spend -->
            <debit compte="40" montant="19,60" />     <!-- vat -->
            <credit  compte="50" montant="100,00" />  <!-- bank account -->
            <reglement type='CB'> credit card on Jan 1st 2002</reglement>
            <ref type='doc' id='facture-001'/>
            <reference>quelque chose</reference>
          </ecriture>
        </ecritures>
        """)
        ecr = xmlreader.get_ecritures(buf)
        self.assertEqual(len(ecr), 1)
        ecr = ecr[0]
        self.assertEqual(ecr.libelle, u'Bought an accounting tool')
        self.assertEqual(ecr.debits, [(u'60', 8040), (u'40', 1960)])
        self.assertEqual(ecr.credits, [(u'50', 10000)])

    def test_immobilisations(self) :
        """test lecture des fichiers XML d'immobilisations"""
        buf = StringIO("""<?xml version="1.0" encoding="ISO-8859-1"?>
        <immobilisations>
          <immobilisation entree="2003-01-01" duree="36"
                          compte="2183" montant="1000,00">
            <libelle>Ordinateur portable</libelle>
          </immobilisation>
        </immobilisations>""")
        imm = xmlreader.get_immobilisations(buf)
        self.assertEqual(len(imm), 1)
        imm = imm[0]
        self.assertEqual(imm.libelle, u'Ordinateur portable')
        #self.assertEqual(imm.date, u')
        self.assertEqual(imm.duree, 36)
        self.assertEqual(imm.compte, u'2183')
        self.assertEqual(imm.montant, 100000)

if __name__ == '__main__':
    testlib.unittest_main()

