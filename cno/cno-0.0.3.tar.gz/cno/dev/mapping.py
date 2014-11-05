from bioservices import Kegg, UniProt
import math


class GeneMapping(object):
    """General class to help map database identifiers to other databases


    Available mapping:

        * KEGG to Uniprot
        * Uniprot to KEGG

    works with dictionaries

        g = GeneMapping()
        # g.load() can load a dictionary that has been previously saved.
        g.build_kegg_unipr t2kegg_mapping()
        g.build_kegg_kegg2uniprot_mapping()
        g.save()


    """
    def __init__(self, organism="hsa"):
        self._organism = organism
        self.cache = {"hsa":{}}

        print("Initialisint KEGG and UniProt instances")
        self.kegg = Kegg(verbose=False)
        self.kegg.organism = organism
        self.uniprot = UniProt(verbose=False)
        self.cache = {"hsa":{}}

    def _get_organism(self):
        return self._organism
    def _set_organism(self, organism):
        self._organism = organism
        self.cache = {organism:{}}
    organism = property(_get_organism, _set_organism, 
        doc="R/W to organism")

    def build_kegg_uniprot2kegg_mapping(self):
        # build a dictionary with unitprot keys and list of KEGG identifiers.
        # Somehow, the conv function from uniprot to hsa and hsa to uniprot do not return the same
        # number of entries.... so for now, we retrieve both and reconstruct a dictionary
        # there are about 25000 uniprot identifiers for 18000 kegg id so this 
        # there are more values than keys
        print("Fetching the mapping from uniprot 2 kegg identifiers (KEGG web service)")
        if "kegg_kegg2uniprot" not in self.cache[self.organism].keys():
            self.cache[self.organism]["kegg_kegg2uniprot"] = self.kegg.conv("uniprot", self.organism)
        mapping1 = self.cache[self.organism]["kegg_kegg2uniprot"]

        print("Fetching the mapping from kegg 2 uniprot identifiers (KEGG web service)")
        if "kegg_uniprot2kegg" not in self.cache[self.organism].keys():
            self.cache[self.organism]["kegg_uniprot2kegg"] = self.kegg.conv(self.organism, "uniprot")
        mapping2 = self.cache[self.organism]["kegg_uniprot2kegg"]

        print("Building dictionary 1/2")
        # and combine them by using sets:
        mapping = dict([(k,set([v])) for k,v in mapping2.iteritems()])

        print("Building dictionary 2/2")    
        # the mapping2 is inversed as compared to mapping1
        for k,v in mapping1.iteritems():
            # note that we loop over values here
            mapping[v].add(k)

        return mapping

    def build_kegg_kegg2uniprot_mapping(self):
        print("Fetching the mapping from uniprot 2 kegg identifiers (KEGG web service)")
        if "kegg_kegg2uniprot" not in self.cache[self.organism].keys():
            self.cache["kegg_kegg2uniprot"] = self.kegg.conv("uniprot", self.organism)
        mapping1 = self.cache[self.organism]["kegg_kegg2uniprot"]

        print("Fetching the mapping from kegg 2 uniprot identifiers (KEGG web service)")
        if "kegg_uniprot2kegg" not in self.cache[self.organism].keys():
            self.cache["kegg_uniprot2kegg"] = self.kegg.conv(self.organism, "uniprot")
        mapping2 = self.cache[self.organism]["kegg_uniprot2kegg"]

        # build a new dictionary where values are transformed into set so that we can add more values
        print("Building dictionary 1/2")    
        mapping = dict([(k,set([v])) for k,v in mapping1.iteritems()])
        print("Building dictionary 2/2")    

        for k,v in mapping2.iteritems():
            mapping[v].add(k)

        return mapping


    def stats(self):
        from pylab import clf, plot, title, xlabel, ylabel, semilogy, grid
        mapu2k = self.build_kegg_uniprot2kegg_mapping()
        mapk2u = self.build_kegg_kegg2uniprot_mapping()

        lengths = set([len(v) for k,v in mapk2u.iteritems()])
        N = [len([1 for v in mapk2u.values() if len(v)==l]) for l in lengths]
        clf(); 
        semilogy(list(lengths), N, "o-", label="kegg 2 uniprot"); 

        lengths = set([len(v) for k,v in mapu2k.iteritems()])
        N = [len([1 for v in mapu2k.values() if len(v)==l]) for l in lengths]
        semilogy(list(lengths), N, "x-", label="uniprot 2 kegg"); 
        grid(True); 
        xlabel("Mapping ambiguity between KEGG and Uniprot mapping"); 
        ylabel(r"\#"); 
        title("Mapping of KEGG ids to Uniprot ids")

    def uniprot_mapk2u(self):
        """

        mapk2u_uni = m.uniprot_mapu2k()

        """
        # mapping from KEGG
        mapk2u = self.build_kegg_kegg2uniprot_mapping()

        uniprot_mapk2u = {}
        N = len(mapk2u.keys())
        dN = 1000
        if N<dN:
            n = 1
        else:
            n = int(math.ceil(N/float(dN)))

        print("Calling uniprot web services")
        for i in range(0, n):
            print("call %s of %s" % (i+1,n))
            if (i+1)*dN > N:
                res = self.uniprot.mapping(fr="KEGG_ID", to="ACC", 
                    query=" ".join([x for x in mapk2u.keys()[i*dN:]]))
                for k,v in res.iteritems():
                    uniprot_mapk2u[k] = v
            else:
                res = self.uniprot.mapping(fr="KEGG_ID", to="ACC", 
                            query=" ".join([x for x in mapk2u.keys()[i*dN:(i+1)*dN]]))
                for k,v in res.iteritems():
                    uniprot_mapk2u[k] = v
        return uniprot_mapk2u

    def uniprot_mapu2k(self):
        """

        mapk2u_uni = m.uniprot_mapu2k()

        """
        # mapping from KEGG
        mapu2k = self.build_kegg_uniprot2kegg_mapping()

        uniprot_mapu2k = {}
        N = len(mapu2k.keys())
        dN = 1000
        if N<dN:
            n = 1
        else:
            n = int(math.ceil(N/float(dN)))

        print("Calling uniprot web services")
        for i in range(0, n):
            print("call %s of %s" % (i+1,n))
            if (i+1)*dN > N:
                res = self.uniprot.mapping(fr="ACC", to="KEGG_ID",
                        query=" ".join([x[3:] for x in mapu2k.keys()[i*dN:]]))
                for k,v in res.iteritems():
                    uniprot_mapu2k[k] = v
            else:
                res = self.uniprot.mapping(fr="ACC", to="KEGG_ID", 
                        query=" ".join([x[3:] for x in mapu2k.keys()[i*dN:(i+1)*dN]]))
                for k,v in res.iteritems():
                    uniprot_mapu2k[k] = v
        return uniprot_mapu2k


    def checking_kegg_vs_uni(self):
        """the id not found in both

        """
        mapk2u_uni = self.uniprot_mapk2u()
        mapu2k_uni = self.uniprot_mapu2k()
        mapk2u = self.build_kegg_kegg2uniprot_mapping()
        mapu2k = self.build_kegg_uniprot2kegg_mapping()
        print("identifiers not found in uniprot mapping tool")
        [k for k in mapk2u.keys() if k not in mapk2u_uni.keys()]
        print("identifiers not found in uniprot mapping tool")

        keys = ["up:"+k for k in mapu2k_uni.keys()]
        [k for k in mapu2k.keys() if k not in keys]


    def save(self):
        import pickle
        fh = open("/home/cokelaer/mapping.dat", "w")
        pickle.dump(self.cache, fh)
        fh.close()

    def load(self):
        import pickle
        fh = open("/home/cokelaer/mapping.dat", "r")
        data = pickle.load(fh)
        self.cache = data
        fh.close()




