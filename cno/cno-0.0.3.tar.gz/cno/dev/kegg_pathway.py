from bioservices import Kegg, UniProt, KeggParser
from cellnopt.core import CNOGraph
import os
import json
"""

import kegg_pathway
k = kegg_pathway.CNOGraphKegg()
k.build_whole_graph()

mapping_uniprot = u.mapping(fr="KEGG_ID", to="ID", query=" ".join(set(k.nodes1+k.nodes2)))
mapping_uniprot_hsa_up = dict([(k,v) for k,v in zip(mapping_uniprot[0::2], [x.split("_")[0] for x in mapping_uniprot[1::2]])])
k.mapping_uniprot_hsa_up = mapping_uniprot_hsa_up.copy()
k.convert2uniprot()

c = k.export2cnograph()
c.nodes()


"""



class PathwayScanner(object):
    def __init__(self):
        self.graph = CNOGraph()


class KEGGPathwayScanner(object):
    def __init__(self, organism='hsa'):
        self.graph = CNOGraph()
	    self.organism = organism

    def scan_all_pathways(self):
        k = Kegg()


class CNOGraphKegg(object):
    """Scans all KGML KEGG pathway and stores activations/inhibitions into a CNOGraph


    Reaction found wuth value --> (activation) and --| (inhibition) are stored.
    Others are ignored. Only entries with type "gene" are kept.
    Skipping compound.

    """
    def __init__(self):
        self.k = Kegg(verbose=False)
        self.parser = KeggParser(verbose=False)
        self.nodes1 = []
        self.nodes2 = []
        self.edges = []
        self.pathways = []
        self.links = []
        self.names = []
        self.gene_names = {}

    def build_whole_graph(self, organism = 'hsa', start=10, end=None):
        import time
        t1 = time.time()
        self.k.organism = organism
        if end == None:
            end = len(self.k.pathwayIds)
        for i, eid in enumerate(self.k.pathwayIds[start:end]):
            print("============================== Scanning eid: %s %s out of %s" % (eid, str(i+1), len(self.k.pathwayIds)))

            if os.path.isfile(eid + ".json"):
                kgml = json.loads(open(eid + ".json", "r").read())
            else:
                kgml = self.k.parse_kgml_pathway(eid)
                fh = open(eid+".json", "w")
                fh.write(json.dumps(kgml))
                fh.close()
            res = self.interpret_kgml(kgml, eid)
        t2 = time.time()
        print("Took %s seconds" % str(t2-t1))
        self._cleanup()

    def parse_all_pathways_with_get_and_save_to_json(self, organism="hsa"):
        self.k.organism = organism
        for i, eid in enumerate(self.k.pathwayIds):
            print("processing %s/%s" % (i+1, len(self.k.pathwayIds)))
            data = self.parser.get(eid)
            res = self.parser.parse(data)
            fh = open("kegg_pathway_get_" + eid+".json", "w")
            fh.write(json.dumps(res))
            fh.close()
        

    def export2cnograph(self):
        from cellnopt.core import CNOGraph
        c = CNOGraph()
        for n1,e,n2 in zip(self.nodes1, self.edges, self.nodes2):
            # the if below is a hack becaues a speces is ill ormed with a wierd
            # character
            c.add_edge(n1,n2,link=e)

        # remove kegg Ids that have not been found
        # remove kegg Ids that have not been found
        for n in c.nodes():
            if n.startswith("hsa"):
                c.remove_node(n)
        return c

    def _cleanup(self):
        # in rare occasion, there is a special character to get rid of
        # over hsa, this convert 1 entry that is written: hsa:xxxx\uff0bmmu:YYYY
        self.nodes1 = [x.split(u"\uff0b")[0] for x in self.nodes1]
        self.nodes2 = [x.split(u"\uff0b")[0] for x in self.nodes2]

    def mapping(self):
        # kegg mapping
        self.mapping_kegg_up_hsa = self.k.conv("hsa", "uniprot")
        self.mapping_kegg_hsa_up = dict([(v,k) for k,v in mapping.iteritems()])

        #uniprot mapping
        u = UniProt
        mapping_uniprot = u.mapping(fr="KEGG_ID", to="ID", query=" ".join(set(self.nodes1+self.nodes2)))
        self.mapping_uniprot_hsa_up = dict((k,v) for k,v in zip(mapping_uniprot[0::2], [x.split("_")[0] for x in mapping_uniprot[1::2]]))
        

    def convert2uniprot(self):
        for i,name in enumerate(self.nodes2):
            try:
                #self.nodes2[i] = self.mapping_hsa_up[name]
                self.nodes2[i] = self.mapping_uniprot_hsa_up[name]
            except: 
                if "up:" not in name:
                    print("skipped ", name)
        for i,name in enumerate(self.nodes1):
            try:
                self.nodes1[i] = self.mapping_uniprot_hsa_up[name]
            except: 
                if "up:" not in name:
                    print("skipped ", name)

    def _filter_entries(self, kgml):
        entries = kgml['entries']
        # filter to keep only genes
        entries = [x for x in entries if x['type'] == "gene"]
        print("Keeping %s gene entries out of %s" % (len(entries),len(kgml['entries'])))
        return entries

    def _filter_relations(self, kgml):
        relations = kgml['relations']
        N1 = len(relations)
        relations = [x for x in relations if x['value'] in ["-->", "--|"]]
        N2 = len(relations)
        print("Keeping %s relations with activation or inhibition (out of %s)" % (N2, N1))
        return relations

    def interpret_kgml(self, kgml, eid):
        entries = self._filter_entries(kgml)
        relations = self._filter_relations(kgml)

        self.skipped = 0
        for r in relations:
            entry1 = [x for x in entries if x['id'] == r['entry1']]
            if len(entry1) == 0:
                continue
            entry1 = entry1[0]
            entry2 = [x for x in entries if x['id'] == r['entry2']]
            if len(entry2) == 0:
                continue
            entry2 = entry2[0]
            name = r['name']
            link = r['link']
            value = r['value']

            #print(u1, u2Name)
            if value == "-->":
                for x in entry1['name'].split(" "):
                    for y in entry2['name'].split(" "):
                        self.nodes1.append(x)
                        self.nodes2.append(y)
                        self.edges.append("+")
                        self.pathways.append(eid)
                        self.links.append(link) # link name e.g., PPrel
                        self.names.append(name) # another link name e.g., activation
                        self.gene_names[x] = entry1['gene_names']
                        self.gene_names[y] = entry2['gene_names']


            elif value == "--|":
                for x in entry1['name'].split(" "):
                    for y in entry2['name'].split(" "):
                        self.nodes1.append(x)
                        self.nodes2.append(y)
                        self.edges.append("-")
                        self.pathways.append(eid)
                        self.links.append(link) # link name e.g., PPrel
                        self.names.append(name) # another link name e.g., activation
                        self.gene_names[x] = entry1['gene_names']
                        self.gene_names[y] = entry2['gene_names']

            else:
                self.skipped += 1
                #print("---skipping %s %s %s %s %s" % (entry1['name'], entry2['name'], name, link, value) )
        print("Skipped %s relations and kept %s" % (self.skipped, len(relations)-self.skipped))



class GraphFromKEGG(object):
    """Create a graph with relations involving a species

        g = GraphFromKEGG("ZAP70")
        g.get_pathways()
        g.get_relations_and_entries()
        c = g.get_cnograph()
        c.plotdot()

    species must be a uniprot name eg ZAP70, RASK not a gene name

    """
    def __init__(self, species="ZAP70", load=None):
        self.k = Kegg()
        self.species = species


        # we will need this so let us compute it. takes some tim
        print("initialisation. takes some time")
        if load==None:
            mapping = self.k.conv("hsa", "uniprot")
            self.uniprot_ids = mapping.keys()
            self.kegg_ids = mapping.values()
        else:
            self.load_conv(load)


        self.relations = []
        # search for pathways that contains a specy
        # must be a valid UniProt Accession entry

        # kegg the Kegg ID
        self.u = UniProt()

        #self.kegg_id = self.u.mapping(fr="ACC+ID", to="KEGG_ID", query="%s_HUMAN" % self.species)[3]
        #self.uniprot_id = self.uniprot_ids[self.kegg_ids.index(self.kegg_id)][3:]


        self.kegg_id = self.u.mapping(fr="ACC+ID", to="KEGG_ID", query="%s_HUMAN" % self.species)[species+"_HUMAN"]
        #self.uniprot_id = self.uniprot_ids[self.kegg_ids.index(self.kegg_id)][3:]
        entries = self.u.quick_search("%s+AND+organism:9606" % self.species, limit=1)

        self.gene_name = [x['Gene names'] for x in entries.values()][0].split(" ")[0]

    def save_conv(self, filename="mapping.dat"):
        import pickle
        d = {'uniprot_ids':self.uniprot_ids, 'kegg_ids':self.kegg_ids}
        pickle.dump(d, open(filename, "w"))

    def load_conv(self, filename="mapping.dat"):
        import pickle
        d = pickle.load(open(filename, "r"))
        self.uniprot_ids = d['uniprot_ids']
        self.kegg_ids = d['kegg_ids']

    def get_pathways(self):
        # should be the gene name
        self.pathways =  self.k.get_pathway_by_gene(self.gene_name, "hsa")

    def get_relations_and_entries(self):
        nodes1 = []
        nodes2 = []
        edges = []
        pathways = []
        names = []  
        links=[]
        values= []
        self.relations = []
        for pathway in self.pathways.keys():
            print("Get relations from %s" % pathway)
            try:
                res = self.k.parse_kgml_pathway(pathway)
            except:
                continue
            relations = res['relations']
            species = [x for x in res['entries'] if x['type'] ]
            #species = [x for x in res['entries'] if x['type']  == "gene"]
            print [x['name'] for x in species]

            # there should be one match only 
            eid = [x for x in species if self.kegg_id in x['name'].split(" ")][0]['id']
            relations_of_interest = [r for r in relations if r['entry1'] == eid or r['entry2']==eid]
            print("...Found %s " % len(relations_of_interest))

            for r in relations_of_interest:
                entry1 = r['entry1']
                entry2 = r['entry2']

                if [x for x in species if x['id'] == entry1][0]['type'] != "gene": continue
                if [x for x in species if x['id'] == entry2][0]['type'] != "gene": continue



                name = r['name']
                link = r['link']
                value = r['value']

                print("===")
                print(entry1, entry2,name,link,value)

                
                kegg_name1_all = [x for x in species if x['id'] == entry1][0]['name']
                kegg_name1 = kegg_name1_all.split(" ")[0]
                kegg_name2_all = [x for x in species if x['id'] == entry2][0]['name']
                kegg_name2 = kegg_name2_all.split(" ")[0]

                if kegg_name1 and kegg_name2:
                    #print(kegg_name1, kegg_name2)
                    u1 = self.uniprot_ids[self.kegg_ids.index(kegg_name1)]
                    u2 = self.uniprot_ids[self.kegg_ids.index(kegg_name2)]

                    self.relations.append({
                        'kegg_name1':kegg_name1,
                        'kegg_name2':kegg_name2,
                        'u1':u1,
                        'u2':u2,
                        'value':value,
                        'link':link,
                        'name':name,
                        'pathway': pathway
                    })

                    #print(u1, u2)
                    if value == "-->":
                        nodes1.append(u1)
                        nodes2.append(u2)
                        edges.append("+")
                        pathways.append(pathway)
                        links.append(link)
                        values.append(value)
                        names.append(name)
                    if value == "--|":
                        edges.append("-")
                        nodes1.append(u1)
                        nodes2.append(u2)
                        pathways.append(pathway)
                        links.append(link)
                        values.append(value)
                        names.append(name)
                    else:
                        print("skipping %s %s %s %s %s" % (u1, u2, name, link, value) )
                else:
                    print("gene to compound/map/pathway relation ignored.")
        # convert to uniprot and add yo cnogrtaph
        self.nodes1 = nodes1[:]
        self.nodes2 = nodes2[:]
        self.edges = edges[:]
        self.pathway = pathways[:]
        self.links = links[:]
        self.values = values[:]
        self.names = names[:]

    def get_cnograph(self):
        c = CNOGraph()
        nodes1 = self.u.mapping(fr="ACC+ID", to="ID", query=" ".join([x[3:] for x in self.nodes1]))
        nodes2 = self.u.mapping(fr="ACC+ID", to="ID", query=" ".join([x[3:] for x in self.nodes2]))

        mapping = {}

        del nodes1[0]
        del nodes1[0]
        del nodes2[0]
        del nodes2[0]
        uniprot_id1 = nodes1[1::2]
        uniprot_id2 = nodes2[1::2]
        uniprot_acc1 = nodes1[0::2]
        uniprot_acc2 = nodes2[0::2]
        for k,v in zip(uniprot_acc1, uniprot_id1):
            mapping[k] = v
        for k,v in zip(uniprot_acc2, uniprot_id2):
            mapping[k] = v
        print mapping
        for n1, n2,e,p,l,v,n in zip(self.nodes1, self.nodes2, self.edges, 
                self.pathways, self.links, self.values, self.names):
            print n1
            print n2
            c.add_edge(mapping[n1[3:]], mapping[n2[3:]], link=e, pathway=p, 
                value=v, names=n, linktype=l)
        return c

