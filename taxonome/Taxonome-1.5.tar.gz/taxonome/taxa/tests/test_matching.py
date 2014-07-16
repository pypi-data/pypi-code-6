import unittest

from taxonome import Name, Taxon, TaxonSet
from taxonome.taxa import match_taxa
from taxonome.tracker import NoopTracker

class VerboseTracker(NoopTracker):
    def name_event(self, name, event):
        print("name event", name, event)
    
    def name_transform(self, name, newname, event, **kwargs):
        print("name transform", name, newname, event, kwargs)
    
    def start_taxon(self, taxon):
        print("start taxon", taxon)
    
    def reset(self):
        print("--RESET--")
    
    def unreadable_name(self, rawname, error):
        print("unreadable name", rawname, error)

class MatchingTest(unittest.TestCase):
    def test_crotalaria(self):
        target = TaxonSet()
        target.add(Taxon(Name("Crotalaria virgulata subsp. forbesii", "(Baker) Polhill")))
        target.add(Taxon(Name("Crotalaria virgulata subsp. grantiana", "(Harv.) Polhill")))
        tomatch = [Taxon(Name("Crotalaria virgulata subsp. forbesii")),
                   Taxon(Name("Crotalaria virgulata subsp. grantiana"))
                  ]
        res = match_taxa(tomatch, target, tracker=VerboseTracker())
        self.assertEqual(len(res), 2)
