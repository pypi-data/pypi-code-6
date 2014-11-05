from cellnopt.dev import sif2uniprot
from cellnopt.data import cnodata
import pickle


siffile = cnodata("PKN-ToyMMB.sif") # just to load something. specis are
                                    # overwritten in the test


var = sif2uniprot.SIF2UniProt("PKN-ExtLiverPCB.sif",reviewed_only=True)

class test_sif2uniprot(object):

    def __init__(self, reviewed_only=True):
        self.var = sif2uniprot.SIF2UniProt("PKN-ExtLiverPCB.sif",all_entries=var.all_entries.copy() )
        self.var.species = ["pip3",  "egfr", "akt", "traf2", "raf1", "map3k7",
            "jak1", "stat13", "igfr1", "gsk3", "stat1n", "hsp27"]

    def test_mapping(self):
        self.var.mapping()


        # checking the mapping
        solutions = {'akt': 'AKT1/AKT2/AKT3',
             'egfr': 'EGFR',
             'gsk3': 'GSK3A/GSK3B',
             'hsp27': 'HSPB1/HSPB3',
             'igfr1': 'IGFR1',
             'jak1': 'JAK1',
             'map3k7': 'M3K7',
             'pip3': 'pip3',
             'raf1': 'RAF1',
             'stat13': 'STAT1/STAT3',
             'stat1n': 'STAT1_n',
             'traf2': 'TRAF2'}
        assert len(solutions.keys()) == len(self.var.mapping_data.keys())

        for k,v in self.var.mapping_data.iteritems():
            if v != solutions[k]:
                raise ValueError("Expected mapping of %s should be %s. Foudn %s" % (k, solutions[k], v))


        def test_write(self):
            self.var.write("test.sif")

