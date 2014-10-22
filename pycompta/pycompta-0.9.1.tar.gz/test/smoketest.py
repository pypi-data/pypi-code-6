# -*- coding: iso-8859-1 -*-

"""
CAS PRATIQUE

Pour vérifier que tout est d'aplomb.
"""

import tempfile, os
import os.path as osp

from logilab.common import testlib

from pycompta import main, Date
from pycompta.lib import entities, xmlreader
from pycompta.lib.comptas import Comptabilite

import xml.etree.ElementTree as ET

class CasBrico(testlib.TestCase) :
    """
    exemple 'Le cas Brico' de 'Introduction à la comptabilité'
    """

    def setUp(self) :
        """les écritures et le pilote"""
        self.debut = Date(2002,1,1)
        self.fin = Date(2002,1,31)

        self.ecritures = []

        e = entities.Ecriture(Date(2002,1,1))
        e.libelle = u'Report exercice précédent'
        e.add_debit(u'2181',200000)
        e.add_debit(u'2154',50000)
        e.add_debit(u'512',43000)
        e.add_debit(u'530',3000)
        e.add_credit(u'101',195000)
        e.add_credit(u'164',42000)
        e.add_credit(u'401',54000)
        e.add_credit(u'447',5000)
        self.ecritures.append(e)

        # page ###

        e = entities.Ecriture(Date(2002,1,2))
        e.add_debit(u'607',65600)
        e.add_credit(u'401',65600)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,7))
        e.add_debit(u'512',8500)
        e.add_debit(u'530',21500)
        e.add_credit(u'707',30000)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,9))
        e.add_debit(u'164',8400)
        e.add_credit(u'512',8400)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,9))
        e.add_debit(u'661',4200)
        e.add_credit(u'512',4200)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,10))
        e.add_debit(u'2154',2500)
        e.add_credit(u'404',2500)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,14))
        e.add_debit(u'512',10000)
        e.add_debit(u'530',42000)
        e.add_credit(u'707',52000)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,16))
        e.add_debit(u'628',432)
        e.add_credit(u'530',432)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,16))
        e.add_debit(u'512',60000)
        e.add_credit(u'530',60000)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,18))
        e.add_debit(u'613',12000)
        e.add_credit(u'512',12000)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,20))
        e.add_debit(u'447',5000)
        e.add_credit(u'512',5000)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,21))
        e.add_debit(u'512',9000)
        e.add_debit(u'530',31000)
        e.add_credit(u'707',40000)
        self.ecritures.append(e)

        # page ###

        e = entities.Ecriture(Date(2002,1,23))
        e.add_debit(u'615',680)
        e.add_credit(u'512',680)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,26))
        e.add_debit(u'623',800)
        e.add_credit(u'512',800)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,28))
        e.add_debit(u'512',18500)
        e.add_debit(u'530',23500)
        e.add_credit(u'707',42000)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,30))
        e.add_debit(u'613',15000)
        e.add_credit(u'512',15000)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,30))
        e.add_debit(u'401',70000)
        e.add_credit(u'512',70000)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,31))
        e.add_debit(u'641',10500)
        e.add_credit(u'512',10500)
        self.ecritures.append(e)

        e = entities.Ecriture(Date(2002,1,31))
        e.add_debit(u'512',60000)
        e.add_credit(u'530',60000)
        self.ecritures.append(e)

        for e in self.ecritures:
            e.groupe = 'aaa'
        self.compta = Comptabilite(self.debut, self.fin, self.ecritures, [])

    def test_balance(self) :
        """vérifie balance à la fin de l'année"""
        BALANCE = {u'101': (     0, 195000,      0, 195000),
                   u'164': (  8400,  42000,      0,  33600),
                   u'2154':( 52500,      0,  52500,      0),
                   u'2181':(200000,      0, 200000,      0),
                   u'401': ( 70000, 119600,      0,  49600),
                   u'404': (     0,   2500,      0,   2500),
                   u'447': (  5000,   5000,      0,      0),
                   u'512': (209000, 126580,  82420,      0),
                   u'530': (121000, 120432,    568,      0),
                   u'607': ( 65600,      0,  65600,      0),
                   u'613': ( 27000,      0,  27000,      0),
                   u'615': (   680,      0,    680,      0),
                   u'623': (   800,      0,    800,      0),
                   u'628': (   432,      0,    432,      0),
                   u'641': ( 10500,      0,  10500,      0),
                   u'661': (  4200,      0,   4200,      0),
                   u'707': (     0, 164000,      0, 164000),
                   }
        soldes = self.compta.balance.get_solde_comptes(Date(2001,12,31),
                                                       self.fin)
        for cnum, rep_credit, rep_debit, credit, debit in soldes :
            t = (cnum, debit-rep_debit, credit-rep_credit)
            if debit > credit :
                t += (debit-credit,0)
            else :
                t += (0,credit-debit)
            self.assertEqual( (cnum,) + BALANCE[cnum], t )

    def test_resultat(self) :
        """vérifie résultat comptable"""
        self.assertEqual( self.compta.resultat.get_resultat(self.debut, self.fin),
                          (109212,164000) )

    def test_bilan(self) :
        """vérifie bilan"""
        self.assertEqual( self.compta.bilan.get_bilan(self.debut, self.fin),
                          (335488,335488) )

class CasBrico2(CasBrico) :
    """
    le même qui charge les données depuis XML
    """
    def skip_setUp(self): # XXXFIME: reactiver
        self.debut = Date(2002,1,1)
        self.fin = Date(2002,1,31)
        self.filepath = osp.join(osp.abspath(osp.dirname(__file__)),
                                 'data/casbrico/ecritures.xml')
        self.ecritures = xmlreader.get_ecritures(file(self.filepath))
        self.compta = Comptabilite(self.debut, self.fin, self.ecritures,[])

if __name__ == '__main__':
    testlib.unittest_main()
