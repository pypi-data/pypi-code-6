import unittest

from taxonome import Name
from taxonome.taxa.name_selector import NameSelector, TerminalNameSelector

from .test_matching import VerboseTracker
from .test_taxa import AutoInput

class NameSelectorTestCase(unittest.TestCase):
    def setUp(self):
        self.liquorice = Name("Glycyrrhiza glabra", "L.")
        self.Gg1 = Gg1 = Name("Glycyrrhiza glandulifera", "Waldst. and Kit.")

        self.ch_liquorice = Name("Glycyrrhiza uralensis", "Fisch.")
        self.Gg2 = Gg2 = Name("Glycyrrhiza glandulifera", "Ledeb.")
        
        self.options = [(self.Gg1, self.liquorice, None),
                        (self.Gg2, self.ch_liquorice, None)]

        self.Gg_ambig = Name("Glycyrrhiza glandulifera", "")
        self.previous_choices = {repr(self.Gg_ambig): \
                ({(Gg1, self.liquorice), (Gg2, self.ch_liquorice)},
                 (Gg1, self.liquorice) )
            }
    
    def test_one_answer(self):
        ns = NameSelector(previous_choices={})
        option = (self.Gg1, self.liquorice, None)
        self.assertEqual(ns([option], self.Gg_ambig), option)
    
    def test_get_previous_choice(self):
        ns = NameSelector(previous_choices=self.previous_choices)

        self.assertEqual(ns(self.options, self.Gg_ambig), self.options[0])
    
    def test_store_user_choice(self):
        user_choices = {}
        ns = TerminalNameSelector(previous_choices=user_choices)
        with AutoInput("1"):
            res = ns(self.options, self.Gg_ambig)
        
        self.assertEqual(res, self.options[0])
        self.assertEqual(user_choices, self.previous_choices)
        
