from cellnopt.core import SIFReader
from bioservices import BioGRID
from easydev import Logging
from cellnopt.dev import SIF2UniProt


class DynamicPKN(object):
    """
        from cellnop.dev import dynamic_model
        s = dynamic_model.DynamicPKN()
        s.loadSIF("test.sif")

s.species.append("mapk9")
res = s.getAllInteractions(strict=False)
res2 = [x for x in res if x[0] in s.species and x[1] in s.species]
c = cellnopt.core.cnograph.CNOGraph()
for x,y in res2:
    c.add_edge(x,y, None, link="+")
c.plotdot()
c.plotdot()
res2 = [x for x in res if x[0] in s.species or x[1] in s.species]
len(Res2)
len(res2)
res2 = [x for x in res if x[0] in s.species and x[1] in s.species or x[1] in
s.species and x[0] in s.species]
len(res2)
c = cellnopt.core.cnograph.CNOGraph()
for x,y in res2:
    c.add_edge(x,y, None, link="+")
c.plotdot()
['AKT1',
 'EGF',
 'MAPK1',
 'hspb1',
 'MAPK8',
 'Map2k1',
 'NFKB1',
 'PIK3C2A',
 'RAF1',
 'KRAS',
 'TNF',
 'TRAF6',
 'JUN',
 'HSPB1',
 'RPS6KA1',
 'AKT2',
 'AKT3',
 'HSPB2',
 'RPS6KA2',
 'PIK3CA',
 'TRAF2',
 'EGFR',
 'RASA1',
 'mapk9',
 'hspb2',
 'MAPK3']


    """

    def __init__(self):
        self.species = None
        self.logging = Logging("INFO")
        self.logging.info("Initialisation. Can take a minute")
        self.biogrid = BioGRID("9606")
        self.interactions = self.biogrid.biogrid.interactors[:]

    def convert2UniProt(self):
        self.sif2uniprot = SIF2UniProt(reviewed_only=True)
        self.sif2uniprot.species = self.species[:]
        self.sif2uniprot.mapping()
        return self.sif2uniprot.mapping_data


    def loadSIF(self, filename):
        try:
            self.sif = SIFReader(filename)
        except:
            from cellnopt.data import cnodata
            self.sif = SIFReader(cnodata(filename))
        self.species = self.sif.specID[:]

    def getAllInteractions(self, strict=True):
        """Return interactions that contains any of the species from the SIF"""
        if self.sif == None:
            self.logging.error("First, you must load a SIF file")

        allInteractions = []
        for specy in self.species:
            if strict==True:
                interactions = [(x,y) for x,y in self.interactions if specy.lower() == x.lower() or specy.lower() == y.lower()]
            else:
                interactions = [(x,y) for x,y in self.interactions if specy.lower() in x.lower() or specy.lower() in y.lower()]
            if len(interactions)==0:
                print("Found no interactions for ", specy)
            else:
                print("Found %s interactions for %s" %(len(interactions), specy))
            allInteractions.extend(interactions)
        return allInteractions

    def getInteractions(self, specy1, specy2=None, strict=True):
        """Return interactions that contains specy1 and/or specy2"""
        specy1 = specy1.lower()
        if specy2!=None:
            specy2 = specy2.lower()
        else:
            specy2 = "XXXXXXXX"

        if strict==True:
            results = [(x,y) for x,y in self.interactions if specy1 == x.lower() or 
                specy1 == y.lower() or specy2 == x.lower() or specy2 == y.lower()]
        else:
            results = [(x,y) for x,y in self.interactions if specy1 in x.lower() or 
                specy1 in y.lower() or specy2 in x.lower() or specy2 in y.lower()]
        return results

    def search(self, specy, strict=True):
        if strict == True:
            found1 = [x[0] for x in self.interactions if x[0].lower()==specy.lower()]
            found2 = [x[1] for x in self.interactions if x[1].lower()==specy.lower()]
        else:
            found1 = [x[0] for x in self.interactions if specy.lower() in x[0].lower()]
            found2 = [x[1] for x in self.interactions if specy.lower() in x[1].lower()]
        found1.extend(found2)
        return found1
        





#len([(x,y) for x,y in b.biogrid.interactors if x.lower() in x.lower() in species
#or y.lower() in species])
