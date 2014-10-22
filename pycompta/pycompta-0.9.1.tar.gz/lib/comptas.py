# -*- coding: utf-8 -*-

from pycompta import DEBUT #, FIN
from pycompta import DateTime, RelativeDateTime, DateTimeType
from pycompta.lib.entities import Ecriture, Journal, GrandLivre, Balance
from pycompta.lib.entities import CompteResultat, Bilan, LivreImmobilisations

class AbstractCompta(object):

    CIBLES = [('journal'               ,'journal'),
              ('grand-livre'           ,'grand-livre'),
              ('balance'               ,'balance'),
              ('compte-resultat'       ,'compte-resultat'),
              ('bilan'                 ,'bilan'),
              ('immo-amort'            ,'immo-amort'),
              ('bilan-immo'            ,'bilan-immo'),
              ('paye.journal'          ,'journal'),
              ('paye.grand-livre'      ,'grand-livre'),
              ('paye.balance'          ,'balance'),
              ('banque.journal'        ,'journal-banque'),
              ('banque.glivre'         ,'grand-livre'),
              ('tresorerie.compte'     ,'compte'),
              ('produits.compte'       ,'compte'),
              ]

    def get_cibles(self):
        return self.CIBLES

    def get_dates(self, debut=None) :
        """
        renvoie liste des dates de début à self.fin
        """
        dates = []
        date = debut or self.debut
        date += RelativeDateTime(day=1)
        fin = self.fin+RelativeDateTime(day=1)
        while date <= fin :
            dates.append(date)
            date += RelativeDateTime(months=+1, day=1)
        return dates

class SousComptabilite(AbstractCompta) :
    """
    Journal, livre et balance d'un sous-ensemble des écritures, par
    exemple sous-compta paye ou sous-compta clients.
    """
    def __init__(self, debut, fin, ecritures, nom="") :
        self.debut = debut
        self.fin = fin
        self.nom = nom
        self.journal = Journal(ecritures)
        self.glivre = GrandLivre(self.journal)
        self.balance = Balance(self.glivre)

    def get_cibles(self):
        return self.CIBLES[:3]

    def get_reports(self) :
        """
        renvoie des écritures reportant mensuellement les totaux des comptes
        """
        reports = []
        for date in self.get_dates() :
            fin = date+RelativeDateTime(day=-1)
            report = Ecriture(fin)
            report.libelle = 'Report %s %s-%s' % (self.nom, date.year, date.month)
            variations = self.balance.get_variations_comptes(date,fin)
            for c_num, total_c, total_d in variations :
                if total_c > total_d :
                    report.add_credit(c_num, total_c - total_d)
                elif total_c < total_d :
                    report.add_debit(c_num, total_d - total_c)
            reports.append(report)
        return reports

class Comptabilite(AbstractCompta) :
    """
    Regroupe les différents livres
    """

    def __init__(self, debut, fin, ecritures, immobilisations, sous_compta=None) :
        """
        --pre:
        type(debut) is DateTimeType
        type(fin) is DateTimeType
        """
        self.debut = debut
        self.fin = fin
        self.ecritures = ecritures

        self.paye = sous_compta
        if self.paye :
            report_paye = self.paye.get_reports()
        else:
            report_paye = []

        self.livrimmo = LivreImmobilisations(immobilisations)
        amort = self.livrimmo.get_amortissements(debut, fin)
        self.journal = Journal(ecritures+amort+report_paye)
        self.glivre = GrandLivre(self.journal)
        self.balance = Balance(self.glivre)
        self.resultat = CompteResultat(self.glivre)
        self.bilan = Bilan(self.resultat)

        if self.paye :
            toutes_ecritures = ecritures + self.paye.journal.ecritures
        else :
            toutes_ecritures = ecritures
        self.banque_journal = Journal( self.get_banque(toutes_ecritures) )
        self.banque_glivre = GrandLivre(self.banque_journal)

        self._cache = {}

    def get_cibles(self):
        if self.paye:
            return self.CIBLES
        else:
            cibles = self.CIBLES[:]
            del cibles[6:9]
            return cibles

    def get_banque(self, ecritures) :
        ecr_banque = []
        for e in ecritures :
            for c, m in e.credits + e.debits :
                if c.startswith('51211') :
                    ecr_banque.append(e)
                    break
        return ecr_banque

    def get_etat(self, date) :
        """
        renvoie état comptable à une date donnée
        --pre:
        type(date) is DateTimeType
        """

        if not self._cache.has_key(date.date) :
            date += RelativeDateTime(day=-1)
            p = {}
            p['annee'] = date.year
            p['mois'] = date.month
            brut, amort = self.livrimmo.get_cumul(date)
            p['immobilisations'] = brut-amort
            p['journal'] = self.journal.est_equilibre(DEBUT, date)
            p['glivre'] = self.glivre.est_equilibre(DEBUT, date)
            p['balance'] = self.balance.est_equilibre(DEBUT, date)
            p['resultat'] = self.resultat.get_resultat(DEBUT, date)
            p['bilan'] = self.bilan.get_bilan(DEBUT, date)
            total_c, total_d = self.glivre.get_solde_comptes(DEBUT, date, '5')
            p['tresorerie'] = total_d - total_c
            prev_month = date+RelativeDateTime(day=0) # last day of previous month
            cha, pro = self.resultat.get_resultat(DEBUT, prev_month)
            p['charges'] = p['resultat'][0] - cha
            p['produits'] = p['resultat'][1] - pro
            self._cache[date.date] = p
        return self._cache[date.date]

    def check(self):
        errors = []
        errors += self.glivre.check()
        errors += self.resultat.check()
        errors += self.bilan.check()
        return errors

