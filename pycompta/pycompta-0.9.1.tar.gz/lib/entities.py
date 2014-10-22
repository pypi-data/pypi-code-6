# -*- coding: utf-8 -*-

"""
PyCompta

Ce module définit les entités manipulées en comptabilité : écritures, journal,
compte, grand-livre, balance, compte-résultat, bilan, amortissement,
immobilisations.
"""

__revision__ = "$Id: entities.py,v 1.36 2006-04-23 13:59:33 nico Exp $"

import types
import logging

from pycompta import L1, DEBUT #, FIN
from pycompta import RelativeDateTime, DateTimeType
from pycompta.lib import definitions

# ECRITURES ####################################################################

class ExceptionEcriture(Exception):
    """Ecriture a un probleme: est pas equilibree"""

class Ecriture(object):
    """
    Une écriture comptable en partie double
    """

    def __init__(self, date) :
        """
        --pre:
        type(date) is DateTimeType
        """
        self.date = date
        self.libelle = u''
        self.reference = None
        self.reglement = None
        self.refs = []
        self.credits = []
        self.debits = []
        self.num = 0
        self.analyse = {}
        self.type = None

    def add_credit(self, compte, montant) :
        """
        ajout d'une ligne crédit

        -- pre:
        type(compte) is types.UnicodeType
        type(montant) is types.IntType
        montant > 0
        """
        self.credits.append( (compte, montant) )

    def add_debit(self, compte, montant) :
        """
        ajout d'une ligne débit

        --pre:
        type(compte) is types.UnicodeType
        type(montant) is types.IntType
        montant > 0
        """
        self.debits.append( (compte, montant) )

    def _get_totaux(self) :
        """
        renvoie la somme des credits et la somme des débits
        """
        import operator
        total_c = reduce(operator.add, [m for c, m in self.credits], 0)
        total_d = reduce(operator.add, [m for d, m in self.debits], 0)
        return total_c, total_d

    def est_equilibre(self) :
        """
        renvoie vrai si la somme des credits est egale à la somme des débits
        """
        total_c, total_d = self._get_totaux()
        return total_c == total_d

    def __repr__(self) :
        total_c, total_d = self._get_totaux()
        r = u"%i %s ---%s---\n CREDIT %s\n DEBIT  %s\n"\
            u"TOTAUX CREDIT %i DEBIT %i" \
            % (self.num, self.date.date, self.libelle,
               str(self.credits), str(self.debits),
               total_c, total_d)
        return r.encode(L1)

    def entre(self, debut, fin) :
        """
        renvoie vrai si date de l'écriture est entre debut et fin

        --pre:
        type(debut) is DateTimeType
        type(fin) is DateTimeType
        """
        return debut <= self.date <= fin

    def inclure(self, ecriture) :
        """
        Ajoute aux crédits et débits ceux de l'écriture donnée en argument
        """
        credits = dict(self.credits)
        for c, m in ecriture.credits :
            credits[c] = credits.get(c,0) + m
        self.credits = credits.items()
        self.credits.sort()
        debits = dict(self.debits)
        for c, m in ecriture.debits :
            debits[c] = debits.get(c,0) + m
        self.debits = debits.items()
        self.debits.sort()

    def montants_positifs(self):
        for compte, montant in self.credits:
            if montant < 0:
                return False
        for compte, montant in self.debits:
            if montant < 0:
                return False
        return True

# JOURNAL ######################################################################

class Journal(object):
    """
    Journal des écritures comptables.

    XXXFIXME: utiliser un arbre binaire pour trouver rapidement les indices des
    dates dans la liste des écritures.
    """

    def __init__(self, ecritures, nom=None) :
        self.nom = nom
        self.ecritures = self._tri_num(ecritures)

    def _tri_num(self, ecritures) :
        """
        trie écritures par date, les numérote et renvoie le résultat.
        """
        ecritures_tri = [(e.date, e) for e in ecritures]
        ecritures_tri.sort()
        ecritures = []
        i = 1
        for date, e in ecritures_tri :
            e.num = i
            ecritures.append(e)
            i += 1
        return ecritures

    def _mk_cache(self) :
        """
        Construit un cache pour faciliter recherche par date.
        FIXME: fonctionne pas.
        """
        cache = {}
        d = ''
        last = ('', 0)
        for i in range(len(self.ecritures)) :
            e = self.ecritures[i]
            if d != e.date :
                last = (d, i)
                d = e.date
                cache[last[0]] = (last[1], i)
        return cache

    def get_ecriture(self, num) :
        """
        renvoie écriture de numéro num

        --pre:
        type(num) is types.IntType
        num > 0
        """
        return self.ecritures[num-1]

    def get_ecritures(self, debut, fin) :
        """
        renvoie écritures de la période

        --pre:
        type(debut) is DateTimeType
        type(fin) is DateTimeType
        """
        return [e for e in self.ecritures if e.entre(debut, fin)]

    def est_equilibre(self, debut, fin) :
        """
        renvoie vrai si toutes les écritures de la période sont équilibrées

        --pre:
        type(debut) is DateTimeType
        type(fin) is DateTimeType
        """
        for e in self.ecritures :
            if e.entre(debut, fin) and not e.est_equilibre() :
                return False
        return True

    def get_total(self, debut, fin) :
        """
        renvoie le total des crédits et débits de toutes les écritures

        --pre:
        type(debut) is DateTimeType
        type(fin) is DateTimeType
        """
        total_c, total_d = 0, 0
        for e in self.get_ecritures(debut, fin) :
            total_c += sum([m for c,m in e.credits])
            total_d += sum([m for c,m in e.debits])
        return total_c, total_d

# COMPTE #######################################################################

class Compte(object):
    """
    Compte du plan comptable
    """

    def __init__(self, num, journal) :
        """
        --pre:
        type(num) is types.IntType
        isinstance(journal,Journal)
        """
        self.num = num
        self.journal = journal
        self.credits = []
        self.debits = []

    def __repr__(self):
        return '<pycompta.Compte num="%s">' % self.num

    def add_credit(self, ecriture, montant) :
        """
        ajout d'une ligne de crédit

        --pre:
        isinstance(ecriture,Ecriture)
        type(montant) is types.IntType
        montant > 0
        """
        self.credits.append( (ecriture.num, montant) )

    def add_debit(self, ecriture, montant) :
        """
        ajoute d'une ligne de débit

        --pre:
        isinstance(ecriture,Ecriture)
        type(montant) is types.IntType
        montant > 0
        """
        self.debits.append( (ecriture.num, montant) )

    def _select(self, debut, fin, lignes) :
        """
        renvoie lignes de la liste dont date écriture est comprise entre bornes
        """
        return [(e_num,m) for e_num,m in lignes
                if self.journal.get_ecriture(e_num).entre(debut,fin)]

    def get_credits(self, debut, fin) :
        """
        renvoie liste lignes de crédit dont date est comprise entre bornes
        """
        return self._select(debut, fin, self.credits)

    def get_debits(self, debut, fin) :
        """
        renvoie liste lignes de débit dont date est comprise entre bornes
        """
        return self._select(debut, fin, self.debits)

    def get_solde(self, debut, fin) :
        """
        renvoie le couple (total crédit, total débit) pour les écritures
        de la période (début,fin)
        """
        total_c = sum([m for e_num,m in self.get_credits(debut,fin)])
        total_d = sum([m for e_num,m in self.get_debits(debut,fin)])
        return total_c, total_d

    def get_mouvements(self) :
        """
        renvoie une liste de triplets (date, credit, debit).
        """
        mov = []
        for (e_num, mont) in self.credits:
            d = self.journal.get_ecriture(e_num).date
            mov.append( (d, mont, 0, self.journal.get_ecriture(e_num)) )
        for (e_num, mont) in self.debits:
            d = self.journal.get_ecriture(e_num).date
            mov.append( (d, 0, mont, self.journal.get_ecriture(e_num)) )
        mov.sort()
        return mov

# VUE COMPTES ##################################################################

class VueComptes(object):
    """
    Synthèse de plusieurs comptes qui donne soldes debut, fin et variations
    """

    def __init__(self, num, debut, fin, comptes):
        self.num = tuple(num)
        self.debut = debut
        self.fin = fin
        self.comptes = comptes
        self._cache = {}

    def _solde(self, debut, fin):
        if (debut, fin) not in self._cache:
            total_c, total_d = 0,0
            for c in self.comptes:
                credit, debit = c.get_solde(debut,fin)
                total_c += credit
                total_d += debit
            self._cache[(debut,fin)] = (total_c, total_d)
        return self._cache[(debut,fin)]

    def get_solde_debut(self):
        return self._solde(DEBUT, self.debut-RelativeDateTime(days=1))
    solde_debut = property(get_solde_debut)

    def get_solde_fin(self):
        return self._solde(DEBUT, self.fin)
    solde_fin = property(get_solde_fin)

    def get_variations(self):
        return self._solde(self.debut, self.fin)
    variations = property(get_variations)

    def get_total_debut(self):
        tc,td = self.solde_debut
        return tc-td
    total_debut = property(get_total_debut)

    def get_total_fin(self):
        tc,td = self.solde_fin
        return tc-td
    total_fin = property(get_total_fin)

    def get_total_variations(self):
        tc,td = self.variations
        return tc-td
    total_variations = property(get_total_variations)

# GRAND LIVRE ##################################################################

class GrandLivre(object):
    """
    Grand Livre comptable qui regroupe tous les comptes
    """

    def __init__(self, journal) :
        self.journal = journal
        self.comptes = {}
        self._mk()
        self._cache = {}

    def _mk(self) :
        """crée les comptes à partir des écritures du journal"""
        self.comptes = {}
        for e in self.journal.ecritures :
            for c, m in e.credits :
                if not self.comptes.has_key(c) :
                    self.comptes[c] = Compte(c, self.journal)
                self.comptes[c].add_credit(e, m)
            for c, m in e.debits :
                if not self.comptes.has_key(c) :
                    self.comptes[c] = Compte(c, self.journal)
                self.comptes[c].add_debit(e, m)

    def check(self):
        errors = []
        keys = sorted(self.comptes.keys())
        for i, c_num in enumerate(keys):
            for other in keys[i+1:]:
                lmin = min(len(c_num), len(other))
                if c_num[:lmin] == other[:lmin]:
                    errors.append(u'comptes imbriqués %s %s' % (c_num, other))
        return errors

    def get_vue_comptes(self, debut, fin, startswith=()):
        if isinstance(startswith, list):
            startswith = tuple(startswith)
        assert isinstance(startswith, tuple)
        if (debut, fin, startswith) not in self._cache:
            if startswith:
                comptes = []
                for sw in startswith:
                    comptes += [ (c_num,c) for c_num, c in self.comptes.items()
                                 if c_num.startswith(sw) ]
            else:
                comptes = self.comptes.items()
            comptes.sort()
            vc = VueComptes(startswith, debut, fin, [c for c_num,c in comptes])
            self._cache[ (debut, fin, startswith) ] = vc
        return self._cache[ (debut, fin, startswith) ]

    def get_comptes(self, starts_with='') :
        """
        renvoie la liste triée par ordre alphanumérique des comptes dont le
        numéro commence par la chaîne starts_with
        """
        try:
            return self._cache[starts_with]
        except KeyError:
            pass
        comptes = [ (c_num,c) for c_num, c in self.comptes.items()
                    if c_num.startswith(starts_with) ]
        comptes.sort()
        self._cache[starts_with] = comptes
        return comptes

    def get_solde_comptes(self, debut, fin, starts_with='') :
        """
        renvoie le couple (total débits, total crédits) pour comptes désignés
        """
        try:
            return self._cache[ (debut,fin,starts_with) ]
        except KeyError:
            pass
        (total_c, total_d) = (0, 0)
        for c_num, c in self.get_comptes(starts_with) :
            tc, td = c.get_solde(debut, fin)
            total_c += tc
            total_d += td
        self._cache[ (debut,fin,starts_with) ] = (total_c, total_d)
        return total_c, total_d

    def est_equilibre(self, debut, fin) :
        """
        renvoie vrai si le total des credits est égal au total des débits
        """
        c, d = self.get_solde_comptes(debut, fin)
        return c == d

    def get_historique_comptes(self, debut, fin, starts_with='') :
        """
        renvoie la liste des quadruplets (date, credits, debits, solde)
        pour comptes désignés
        """
        # recupere mouvements sur comptes
        mouvements = []
        for cpt_num, cpt in self.get_comptes(starts_with):
            mouvements.extend( cpt.get_mouvements() )
        mouvements.sort()
        # calcule historique
        historique = []
        vc = self.get_vue_comptes(debut, fin, [starts_with])
        solde = vc.total_debut
        for date, debit, credit,e in mouvements:
            if debut <= date <= fin :
                solde = solde + debit - credit
                historique.append( (date, debit, credit, solde, e) )
        return historique

# BALANCE ######################################################################

class Balance(object):
    """
    Balance comptable qui synthètise les soldes des comptes
    """

    def __init__(self, glivre) :
        self.glivre = glivre

    def get_solde_comptes(self, debut, fin) :
        """
        renvoie une liste de triplets (num_compte, (solde début), (solde fin))
        les soldes sont des couples (total crédit, total débit)
        """
        return [((c_num,)+c.get_solde(DEBUT,debut)+c.get_solde(DEBUT,fin))
                for c_num, c in self.glivre.get_comptes()]

    def get_total(self, debut, fin) :
        """
        renvoie le couple (total crédits, total débits)
        """
        return self.glivre.get_solde_comptes(debut, fin)

    def est_equilibre(self, debut, fin):
        """
        renvoie vrai si le total des credits est égal au total des débits
        """
        total_credits, total_debits = self.get_total(debut, fin)
        return total_credits == total_debits

    def get_variations_comptes(self, debut, fin) :
        """
        renvoie une liste de triplets (num_compte, total crédit, total débit)
        """
        return [(c_num,)+cpt.get_solde(debut,fin)
                for c_num, cpt in self.glivre.get_comptes()]

# COMPTE RESULTAT ##############################################################

class CompteResultat(object):
    """
    Compte de résultat qui regroupe par postes les charges et les produits
    """

    def __init__(self, glivre) :
        self.glivre = glivre

    def get_total(self, debut, fin, poste) :
        """
        renvoie le total d'un poste pour la période
        """
        id_poste, nom_poste, liste_comptes, subdivisions_poste = poste
        total = 0
        # cumule le total des comptes associé au poste (crédits-débits)
        for c_num, condition in liste_comptes :
            total_c, total_d = self.glivre.get_solde_comptes(debut, fin, c_num)
            if condition is None \
                   or (condition == 'C' and total_c > total_d) \
                   or (condition == 'D' and total_c < total_d) :
                total += total_c - total_d

        # cumule le total des sous-postes
        total += sum([self.get_total(debut, fin, sous_poste)
                      for sous_poste in subdivisions_poste])
        return total

    def get_resultat(self, debut, fin) :
        """
        renvoie le couple (total chargs, total produits)
        """
        charges = self.get_total(debut, fin, ('','',[],definitions.CHARGES))
        produits = self.get_total(debut, fin, ('','',[],definitions.PRODUITS))
        # assert charges <= 0, "Charges %d, Produits %d" % (charges,produits)
        return -charges, produits

    def check(self): # XXX FIXME
        errors = []
        comptes = set()
        for poste in definitions.CHARGES + definitions.PRODUITS:
            for c_num, c in flatten_desc(poste):
                comptes.add(c_num)
        for c_num in comptes:
            for num, c in self.glivre.get_comptes(c_num):
                c.tag_resultat = True
        for c in self.glivre.comptes.values():
            if not hasattr(c, 'tag_resultat') and (c.num.startswith(u'6')
                                                   or c.num.startswith(u'7')):
                errors.append('compte %s apparaitra pas dans compte resultat' % c.num)
        return errors

# BILAN ########################################################################

class Bilan(object):
    """
    Bilan comptable qui regroupe par postes actif et passif
    """

    def __init__(self, resultat) :
        self.resultat = resultat

    def _get_solde_compte(self, debut, fin, cnum, condition) :
        """
        renvoie le solde d'un compte si condition est satisfaite
        """
        if condition is None:
            total_c, total_d = self.resultat.glivre.get_solde_comptes(debut,fin,cnum)
            total = total_c - total_d
        elif condition in 'CD':
            total = 0
            for c_num, c in self.resultat.glivre.get_comptes(cnum) :
                total_c, total_d = c.get_solde(debut, fin)
                if (condition == 'C' and total_c > total_d) \
                   or (condition == 'D' and total_c < total_d):
                    total += total_c - total_d
        else:
            raise Exception('Condition %s inconnue dans définition du bilan '
                            'pour compte %s' % (condition, cnum))
        return total

    def get_solde_compte_diff(self, debut, fin, poste) :
        """
        renvoie valeur brute, amort/depreciation pour un compte
        de l'actif
        """
        id_poste, nom, comptes_brut, comptes_amort, subdivisions_poste = poste
        total_brut, total_amort = 0, 0
        for cnum, cond in comptes_brut :
            total_brut += self._get_solde_compte(debut, fin, cnum, cond)
        for cnum, cond in comptes_amort :
            total_amort += self._get_solde_compte(debut, fin, cnum, cond)
        for sous_poste in subdivisions_poste :
            brut, amort = self.get_solde_compte_diff(debut, fin, sous_poste)
            total_brut += brut
            total_amort += amort
        return total_brut, total_amort

    def get_solde_poste(self, debut, fin, poste) :
        """
        renvoie le solde du poste pour la période (début,fin)
        """
        id_poste, nom, liste_comptes, subdivisions_poste = poste
        if nom == u"Résultat de l'exercice" :
            charges, produits = self.resultat.get_resultat(debut, fin)
            return produits-charges
        else :
            total = 0
            for cnum, cond in liste_comptes :
                total += self._get_solde_compte(debut, fin, cnum, cond)
            for sous_poste in subdivisions_poste :
                total += self.get_solde_poste(debut, fin, sous_poste)
            return total

    def get_bilan(self, debut, fin) :
        """
        renvoie couple des montants (actif, passif)
        """
        p_actif = ('', '', [], [], definitions.ACTIF)
        p_passif = ('', '', [], definitions.PASSIF)

        brut, amort = self.get_solde_compte_diff(debut, fin, p_actif)
        actif = brut + amort
        passif = self.get_solde_poste(debut, fin, p_passif)

        #assert actif >=0, \
        #       "le total de l'actif devrait être positif %d,%d"%(actif,passif)
        return (-actif, passif)

    def est_equilibre(self, debut, fin):
        """
        renvoie vrai si le total des crédits est égal au total des débits
        """
        actif, passif = self.get_bilan(debut, fin)
        return actif == passif

    def check(self):
        errors = []
        comptes = set()
        for poste in definitions.ACTIF:
            for c_num, c in flatten_desc(poste, True):
                comptes.add(c_num)
        for poste in definitions.PASSIF:
            for c_num, c in flatten_desc(poste):
                comptes.add(c_num)
        for c_num in comptes:
            for num, c in self.resultat.glivre.get_comptes(c_num):
                c.tag_bilan = True
        for c in self.resultat.glivre.comptes.values():
            if not hasattr(c, 'tag_bilan') and not (
                c.num.startswith(u'6') or c.num.startswith(u'7')
                or c.num.startswith(u'9') or c.num.startswith(u'28')):
                errors.append('compte %s apparaitra pas dans bilan' % c.num)
        return errors

def flatten_desc(poste, actif=False):
    try:
        if actif:
            id_poste, nom, liste_comptes, liste_comptes_bis, subdivisions_poste = poste
        else:
            id_poste, nom, liste_comptes, subdivisions_poste = poste
            liste_comptes_bis = []
    except ValueError:
        raise ValueError(str(poste))

    if subdivisions_poste :
        for p in subdivisions_poste :
            for item in flatten_desc(p, actif):
                yield item
    else:
	for cnum, cond in liste_comptes :
            yield cnum, cond
        for cnum, cond in liste_comptes_bis :
            yield cnum, cond

# IMMOBILISATION ###############################################################

class Immobilisation(object):
    """
    Immobilisation (charge amortie sur un ou plusieurs exercices)
    """

    def __init__(self, libelle, entree, sortie, duree, compte, montant) :
        """
        --pre:
        type(libelle) is types.UnicodeType, type(libelle)
        type(date) is DateTimeType
        type(duree) is types.IntType
        type(compte) is types.UnicodeType
        type(montant) is types.IntType
        """
        self.libelle = libelle
        self.entree = entree
        self.sortie = sortie
        self.duree = duree
        self.compte = compte
        self.montant = montant
        self.groupe = ''

    def get_cumul_dotations(self, date) :
        """
        renvoie cumul des dotations à la date donnée
        """
        cumul = 0
        for date_dot, compte, montant in self.get_dotations() :
            if date_dot <= date :
                cumul += montant
            else :
                break
        return cumul

    def get_dotations(self) :
        """
        renvoie la liste des triplets (date,compte,montant) pour toutes les
        dotations à effectuer pour amortir l'immobilisation.
        """
        result = []
        amort = 0
        entree = self.entree
        mensuel = int(self.montant) / int(self.duree)
        for m in range(self.duree-1):
            date = self.entree + RelativeDateTime(months=+m,day=-1)
            if self.sortie and date >= self.sortie:
                result.append( (date, self.compte, int(self.montant)-amort) )
                break
            else:
                result.append( (date,self.compte,mensuel) )
                amort += mensuel
        else:
            date = self.entree + RelativeDateTime(months=+m+1, day=-1)
            result.append( (date, self.compte, int(self.montant)-amort) )
        return result

class LivreImmobilisations(object):
    """
    Livre des immobilisations.
    """

    def __init__(self, immo) :
        self.immobilisations = immo

    def get_amortissements(self, debut, fin) :
        """
        renvoie les écritures d'amortissement cumulant les dotations
        à effectuer dans la période.
        """
        dot = {}
        for i in self.immobilisations :
            for date, compte, montant in i.get_dotations() :
                if debut <= date <= fin:
                    key = (date,compte,i.groupe)
                    dot[key] = dot.get(key,0) + montant
        amort = dot.items()
        amort.sort()
        ecritures_amort = []
        for (date,c,groupe),m in amort :
            e = Ecriture(date+RelativeDateTime(day=-1))
            e.libelle = 'Dotations Amortissements %s'%groupe
            compte = str(c)
            compte = compte[0]+'8'+compte[1:] # 2183 -> 28183
            e.credits.append( (compte,m) )
            e.debits.append( ('6811',m) )
            e.groupe = groupe.upper()
            ecritures_amort.append(e)
        return ecritures_amort

    def get_cumul(self,date) :
        """
        renvoie le total brut des immobilisations et le cumul des
        amortissements à la date donnée
        """
        brut, amort = 0, 0
        for i in self.immobilisations :
            if i.entree <= date and (i.sortie is None or date <= i.sortie):
                brut += i.montant
                amort += i.get_cumul_dotations(date)
        return (brut, amort)


class BilanImmo(object):

    def __init__(self, glivre):
        self.glivre = glivre


