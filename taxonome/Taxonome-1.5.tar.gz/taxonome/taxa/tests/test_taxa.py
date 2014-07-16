import builtins
import unittest
import warnings

import taxonome
from taxonome.taxa import name_selector
from taxonome.taxa.base import UncertainSpeciesError
from taxonome.taxa.author import Authority
from taxonome.taxa.name_selector import TryAnotherName
import taxonome.taxa.collection

from taxonome import Name, Taxon

class AutoInput:
    """Context manager to override the input() call. Will automatically
    return the given response."""
    def __init__(self, response=''):
        self.response = response
    
    def __enter__(self):
        self.saved_input = builtins.input
        def autoinput(prompt):
            return self.response
        builtins.input = autoinput
    
    def __exit__(self, exc_type, exc_value, traceback):
        builtins.input = self.saved_input

class HyacinthBeanTest(unittest.TestCase):
    def setUp(self):
        self.bean = taxonome.Taxon("Lablab purpureus", "(L.) Sweet")
        self.bean.othernames.add(Name("Dolichos lablab","L."))
        self.bean.othernames.add(Name("Lablab niger", "Medikus"))
        self.bean.othernames.add(Name("Vigna aristata", "Piper"))
        self.ts = taxonome.TaxonSet()
        self.ts.add(self.bean)
    
    def testSynonymy(self):
        assert self.bean.hasname("Dolichos lablab")
        assert self.bean.hasname(Name("Lablab niger", "Medikus"))
    
    def testShortauth(self):
        assert self.bean.name == Name("Lablab purpureus", "Sweet.")
        assert self.bean.name == Name("Lablab purpureus", "Sweet ex. Madeup")
        
    def testTSSynonymy(self):
        assert Name("Vigna aristata","Piper.") in self.ts
        assert self.ts["Lablab niger"]
    
    def testAccnameLookup(self):
        self.assertEqual(self.ts.get_by_accepted_name(Name("Lablab purpureus",
                                "(L.) Sweet")), self.bean)

    def test_get_by_id(self):
        name = Name("Dolichos lablab","L.")
        n, an, tid = self.ts.resolve_name(name)[0]
        self.assertEqual(self.ts.get_by_id(tid), self.bean)
    
    def test_non_auth_lookup(self):
        t1 = self.ts.select(Name("Dolichos lablab", "L."))
        self.assertIs(t1, self.bean)
        with self.assertRaises(KeyError):
            self.ts.select(Name("Dolichos lablab", "non L."))
        with self.assertRaises(KeyError):
            self.ts.select(Name("Dolichos lablab", "sensu non L."))
        with self.assertRaises(KeyError):
            self.ts.select(Name("Dolichos lablab", "auct. non L."))
        
        # Test selecting the other way round.
        ts2 = taxonome.TaxonSet()
        ts2.add(taxonome.Taxon("Dolichos lablab", "non L."))
        with self.assertRaises(KeyError):
            ts2.select(Name("Dolichos lablab", "L."))
        
        # This should succeed.
        ts2.select(Name("Dolichos lablab", "Vahl"), strict_authority=False)

class PoaTest(unittest.TestCase):
    def setUp(self):
        self.t1 = taxonome.Taxon("Poa annua", "L.")
        self.t2 = taxonome.Taxon("Poa infirma", "H. B. & K.")
        self.t2.othernames.add(Name("Poa annua", "Cham. & Schlecht."))
        self.ts = taxonome.TaxonSet()
        self.ts.add(self.t1)
        self.ts.add(self.t2)
        self.ts._nameselector = name_selector.TerminalNameSelector(previous_choices={})
    
    def testPreferAccName(self):
        # No authority: should pick accepted name without asking for input.
        with AutoInput("N"):
            t1 = self.ts.select("Poa annua")
        self.assertEqual(t1, self.t1)
        
        # With authority: should ask the user by default.
        with AutoInput("0"), self.assertRaisesRegex(KeyError, "0"):
            self.ts.select(Name("Poa annua", "Madeup"))
        
        # With authority: When requested, prefer the accepted name:
        with AutoInput("N"):
            t1a = self.ts.select(Name("Poa annua", "Madeup"), prefer_accepted='all')
        self.assertEqual(t1a, self.t1)
        
class LiquoriceTestBase(unittest.TestCase):
    taxon_collection_class = taxonome.TaxonSet
    taxon_collection_args = ()
    
    def setUp(self):
        self.ts = self.taxon_collection_class(*self.taxon_collection_args)
        self.liquorice = Name("Glycyrrhiza glabra", "L.")
        liquorice_t = taxonome.Taxon(self.liquorice)
        liquorice_t.othernames.add(Name("Glycyrrhiza glandulifera", "Waldst. and Kit."))
        self.ts.add(liquorice_t)
        self.ch_liquorice = Name("Glycyrrhiza uralensis", "Fisch.")
        ch_liquorice_t = taxonome.Taxon(self.ch_liquorice)
        ch_liquorice_t.othernames.add(Name("Glycyrrhiza glandulifera", "Ledeb."))
        self.ts.add(ch_liquorice_t)

class LiquoriceTest(LiquoriceTestBase):
    def testHomonym(self):
        assert self.ts.select(Name("Glycyrrhiza glabra", "L.")).hasname(Name("Glycyrrhiza glandulifera", "Waldst. & Kit."))
        homonyms = self.ts.resolve_name("Glycyrrhiza glandulifera")
        self.assertEqual(len(homonyms), 2)
        assert homonyms[0][0].match_unqualified(homonyms[1][0])
        assert not homonyms[0][1].match_unqualified(homonyms[1][1])
        with AutoInput("1"):
            self.assertIn(self.ts.select("Glycyrrhiza glandulifera"), self.ts)
    
    def testFuzzyLookup(self):
        fuzzy_match = self.ts.select("Glycyrhiza glabra")
        assert self.liquorice.match_qualified(fuzzy_match.name), fuzzy_match
        with self.assertRaises(KeyError):
            self.ts.select("Glycyrrhiza echinata")
        
        fuzzy_matches = self.ts.fuzzy_resolve_name("Glycyrhiza glandulifera")
        self.assertEqual(len(fuzzy_matches), 2)
    
    def testUpgradeSubsp(self):
        n1 = Name("Glycyrrhiza glabra subsp. glabra")
        n2 = Name("Glycyrrhiza glabra var. glabra")
        n3 = Name("Glycyrrhiza glabra subsp. spammens")
        with self.assertRaises(KeyError):
            self.ts.select(n1, upgrade_subsp="none")
        match1 = self.ts.select(n1, upgrade_subsp="nominal")
        assert match1.name.match_qualified(self.liquorice), match1
        match2 = self.ts.select(n2, upgrade_subsp="nominal")
        assert match2.name.match_qualified(self.liquorice), match2
        with self.assertRaises(KeyError):
            self.ts.select(n3, upgrade_subsp="nominal")
        match3 = self.ts.select(n3, upgrade_subsp="all")
        assert match3.name.match_qualified(self.liquorice), match3
        
        n4 = Name.from_string("Glycyrrhiza glabra L. subsp. glabra")
        match4 = self.ts.select(n4, upgrade_subsp="nominal")
        assert match4.name.match_qualified(self.liquorice), match4


class RecordingNameSelector(name_selector.NameSelector):
    lastcall = None
    
    def __call__(self, name_options, name, *args, **kwargs):
        self.lastcall = name
        return super().__call__(name_options, name, *args, **kwargs)

class LiquoriceAmbigTest(LiquoriceTestBase):
    def test_ambig_tryagain(self):
        """issue #14 - if a replacement name results in an ambiguous match
        again, it will use the terminal name selector."""
        n1 = Name("Glycyrrhiza glandulifera", "Waldst. and Kit.")
        n2 = Name("Glycyrrhiza glandulifera", "Ledeb.")
        self.ts.add(taxonome.Taxon("Glycyrrhiza fabricata", "L."))
        self.ts.add(taxonome.Taxon("Glycyrrhiza fabricata", "Regel."))
        prev_choices = {repr("Glycyrrhiza glandulifera"):
            ({(n1, self.liquorice), (n2, self.ch_liquorice)}, TryAnotherName("Glycyrrhiza fabricata"))}
        ns = RecordingNameSelector(previous_choices=prev_choices)

        try:
            with warnings.catch_warnings():
                # The ambiguous name will issue a warning, which we can ignore
                warnings.simplefilter("ignore")
                self.ts.select("Glycyrrhiza glandulifera", nameselector=ns)
        except Exception:
            pass
        
        self.assertEqual(ns.lastcall, "Glycyrrhiza fabricata")

class NameParseTest(unittest.TestCase):
    def test_parse_name(self):
        n = Name.from_string("Teramnus repens (Taub.)Baker f. ssp. gracilis (Chiov.)Verdc.")
        self.assertEqual(n.plain, "Teramnus repens subsp. gracilis")
        self.assertEqual(str(n.authority), "(Chiov.) Verdc.")
        parent = n.parent
        self.assertEqual(parent.plain, "Teramnus repens")
        # f. (filius, i.e. son) is ignored for now
        self.assertEqual(str(parent.authority), "(Taub.) Baker")
        
        # N.B. var without a .
        n = Name("Vigna radiata var sublobata", "(Roxb.) Verdc.")
        self.assertEqual(n.plain, "Vigna radiata var. sublobata")
        
        # Extra spaces
        n = Name("Vigna    radiata\tvar. \t sublobata")
        self.assertEqual(n.plain, "Vigna radiata var. sublobata")
    
    def test_subspecies(self):
        n = Name("Gorilla gorilla gorilla", "Savage, 1847")
        self.assertEqual(n.rank, "subspecies")
        self.assertEqual(n.parent.plain, "Gorilla gorilla")
        
        n = Name.from_string("Gorilla gorilla gorilla Savage, 1847")
        self.assertEqual(n.rank, "subspecies")
        self.assertEqual(n.parent.plain, "Gorilla gorilla")
        
        n = Name("Alloteropsis semialata subsp. eckloniana", "(Nees) Gibbs-Russ.")
        self.assertEqual(n.rank, "subspecies")
        self.assertEqual(n.parent.plain, "Alloteropsis semialata")
        
        n = Name.from_string("Alloteropsis semialata (R. Br.) Hitchc. subsp. eckloniana (Nees) Gibbs-Russ.")
        self.assertEqual(n.rank, "subspecies")
        self.assertEqual(n.parent.plain, "Alloteropsis semialata")
        self.assertEqual(str(n.parent.authority), "(R. Br.) Hitchc.")
        self.assertEqual(str(n.authority), "(Nees) Gibbs-Russ.")
        
    def test_forma(self):
        n = Name('Muhlenbergia mexicana f. ambigua')
        self.assertEqual(n.rank, 'form')
        self.assertEqual(n.parent.plain, 'Muhlenbergia mexicana')
        
        n = Name.from_string('Muhlenbergia mexicana L. f. ambigua Foo.')
        self.assertEqual(n.rank, 'form')
        self.assertEqual(n.parent.plain, 'Muhlenbergia mexicana')
        self.assertEqual(str(n.authority), "Foo.")
        self.assertEqual(str(n.parent.authority), "L.")
        
        n = Name('Muhlenbergia mexicana forma mexicana')
        self.assertEqual(n.rank, 'form')
        self.assertEqual(n.parent.plain, 'Muhlenbergia mexicana')
        
        n = Name.from_string('Muhlenbergia mexicana L. forma mexicana Bar.')
        self.assertEqual(n.rank, 'form')
        self.assertEqual(n.parent.plain, 'Muhlenbergia mexicana')
        self.assertEqual(str(n.authority), "Bar.")
        self.assertEqual(str(n.parent.authority), "L.")
        
        # With f. for filius
        n = Name.from_string('Crotalaria dolichonyx Baker f. & Martin')
        self.assertEqual(n.rank, 'species')
        self.assertEqual(n.plain, 'Crotalaria dolichonyx')
        self.assertEqual(n.authority, Authority('Baker f. & Martin'))
    
    def test_hybrid(self):
        names = [('X Achnella caduca', 'Achnella caduca', 'genus'),
                 ('x Achnella caduca', 'Achnella caduca', 'genus'),
                 ('× Achnella caduca', 'Achnella caduca', 'genus'),
                 ('×Achnella caduca', 'Achnella caduca', 'genus'),
                 ('Calammophila X baltica', 'Calammophila baltica', 'species'),
                 ('Calammophila x baltica', 'Calammophila baltica', 'species'),
                 ('Calammophila × baltica', 'Calammophila baltica', 'species'),
                 # Using the × symbol, we allow this without a space:
                 ('Lespedeza ×patentibicolor', 'Lespedeza patentibicolor', 'species'),
                ]
        
        for raw, plain, hybrid in names:
            print(raw)
            n = Name(raw)
            self.assertEqual(n.plain, plain)
            self.assertEqual(n.hybrid, hybrid)
            
            n = Name.from_string(raw + " Bloggs")
            self.assertEqual(n.plain, plain)
            self.assertEqual(str(n.authority), "Bloggs")
            self.assertEqual(n.hybrid, hybrid)
        
    def test_genus_name(self):
        n = Name("Alloteropsis", "Presl.")
        self.assertEqual(n.plain, "Alloteropsis")
        self.assertEqual(str(n.authority), "Presl.")
    
    def test_with_year(self):
        n = Name.from_string("Balaena mysticetus Linnaeus, 1758")
        self.assertEqual(n.plain, "Balaena mysticetus")
        self.assertEqual(n.authority.year, "1758")
        
        self.assertEqual(n, Name("Balaena mysticetus", "L."))
    
    def test_invalid_name(self):
        with self.assertRaises(UncertainSpeciesError):
            Name.from_string("Festuca ovina & rubra")
        
        with self.assertRaises(UncertainSpeciesError):
            Name.from_string("Festuca sp.")
        with self.assertRaises(UncertainSpeciesError):
            Name.from_string("Festuca spp.")
        
        with self.assertRaises(UncertainSpeciesError):
            Name("Brachiaria sp")
        with self.assertRaises(UncertainSpeciesError):
            Name("Brachiaria sp.")
        with self.assertRaises(UncertainSpeciesError):
            Name("Brachiaria spp")
        with self.assertRaises(UncertainSpeciesError):
            Name("Brachiaria spp.")
    
    def test_not_capitalised(self):
        n = Name.from_string("cynodon dactylon")
        self.assertEqual(n.plain, "Cynodon dactylon")
        n = Name("echinochloa haploclada", "")
        self.assertEqual(n.plain, "Echinochloa haploclada")
    
    def test_auth_noncapital(self):
        n = Name.from_string("Trifolium pauciflorum d'Urv.")
        self.assertEqual(n.plain, "Trifolium pauciflorum")
        self.assertEqual(str(n.authority), "d'Urv.")
        
        n = Name.from_string("Trifolium pauciflorum de Madeup")
        self.assertEqual(n.plain, "Trifolium pauciflorum")
        self.assertEqual(str(n.authority), "de Madeup")


class WheatTest(unittest.TestCase):
    """See bitbucket issue 18
    
    https://bitbucket.org/taxonome/taxonome/issue/18/automatic-choice-of-the-accepted-name
    """
    def setUp(self):
        self.ts = taxonome.TaxonSet()
        self.ts.add(Taxon(Name('Triticum dicoccoides', '(Körn. ex Asch. & Graebn.) Schweinf.')))
        
        tt = Taxon(Name('Triticum timopheevii', '(Zhuk.) Zhuk.'))
        tt.othernames.add(Name('Triticum dicoccoides', 'auct.'))
        self.ts.add(tt)

    def test_resolve_name(self):
        res1 = self.ts.resolve_name('Triticum dicoccoides')
        self.assertEqual(len(res1), 2)
        
        res2 = self.ts.resolve_name(Name('Triticum dicoccoides'))
        self.assertEqual(len(res2), 2)

    def test_select(self):
        td = self.ts.select(Name('Triticum dicoccoides'), prefer_accepted='noauth')
        self.assertEqual(td.name.plain, 'Triticum dicoccoides')
