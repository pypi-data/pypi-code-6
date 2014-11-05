"""Example showing how to construct a PKN from psicquic given only the input names"""



from cellopt.core import *

# mapping from cellnopt.de sif2uniprot
import sif2uniprot
s2u = sif2uniprot.SIF2UniProt(cnodata("PKN-ToyPB.sif"), all_entries=all_entries)
mapping = s2u.mapping()

mapping = {'akt': 'AKT1/AKT2/AKT3',
 'ap1': 'AP1S1/AP2S1',
 'cjun': 'JUN',
 'creb': 'CREB1/CREB3/CREB5',
 'egf': 'EGF',
 'egfr': 'EGFR',
 'erk': 'EPHB2',
 'ex': 'RX',
 'gsk3': 'GSK3A/GSK3B',
 'ikb': 'IKBA/IKBB/IKBD/IKBE/IKBZ',
 'ikk': 'IKKA/IKKB/IKKE',
 'jnk': 'MK08/MK09/MK10',
 'map3k1': 'M3K1',
 'map3k7': 'M3K7',
 'mek': 'MP2K1/MP2K2/MP2K3/MP2K4/MP2K5/MP2K6/MP2K7',
 'mkk4': 'MP2K4',
 'mkk7': 'MP2K7',
 'nfkb': 'NFKB1/NFKB2',
 'nik': 'M4K4/M3K14',
 'p38': 'p38',
 'p90rsk': 'KS6A1/KS6A2/KS6A3/KS6A6',
 'ph': 'PHB/PHS',
 'pi3k': '?pi3k',
 'rac': 'RAC1/RAC2/RAC3',
 'raf1': 'RAF1',
 'ras': 'RASE/RASH/RASK/RASM/RASN',
 'sos': 'SOST/SOS1/SOS2',
 'tnfa': 'TNFA',
 'tnfr': 'TNR1A/TNR1B/TNR3',
 'traf2': 'TRAF2'}

mapping['erk'] = 'MK03/MK01'
mapping['pi3k'] = 'P3C2A'




species = ["AKT1",'AKT2','AKT3', 'AP1S1','AP2S1', 'JUN', 'CREB1','CREB3','CREB5','EGF', 'EGFR', 'MK03',"MK01"
  'GSK3A','GSK3B',  'IKBA','IKBB','IKBD','IKBE','IKBZ',  'IKKA','IKKB','IKKE',
  'MK08','MK09','MK10',  'M3K1',  'M3K7',  'MP2K1','MP2K2','MP2K3','MP2K4','MP2K5','MP2K6','MP2K7',
  'MP2K4',  'MP2K7',  'NFKB1','NFKB2',  'M4K4','M3K14',
  'p38',  'KS6A1','KS6A2','KS6A3','KS6A6',  'PHB','PHS',
 "P3C2A", 'RAC1','RAC2','RAC3', 'RAF1','RASE','RASH','RASK','RASM','RASN','SOS1','SOS2',
 'TNFA', 'TNR1A','TNR1B', 'TRAF2']

# build a reverse mapping usefule for later on
reverse_mapping = {}
for specy in species:
    for k, v in mapping.iteritems():
        if specy in v:
            reverse_mapping[specy] = k

s = psicquic.AppsPPI()
#s.queryAll("EGF AND species:9606")
c = CNOGraph()

def add_interactions(c, interactions):
    for db in s.interactions.keys():
        print(db, len(s.interactions[db]))
        for interaction in s.interactions[db]:
            n1 = interaction[0].split("_")[0]
            n2 = interaction[1].split("_")[0]
            if n1 not in species or n2 not in species:
                continue
            if len(c.edges())>1 and (n1, n2) in c.edges():
                if db in c.edge[n1][n2]['psicquic_db']:
                    continue
                else:
                    c.edge[n1][n2]['psicquic_db'].append(db)
                    c.edge[n1][n2]['psicquic'] += 1
            else:
                c.add_edge(n1,n2, link="+")
                c.edge[n1][n2]['psicquic_db'] = [db]
                c.edge[n1][n2]['psicquic'] = 1

for specy in species:
    print(specy)
    s.queryAll("%s AND species:9606" % specy)
    add_interactions(c, s.interactions)
    print(len(c))

for edge in c.edges():
    c.edge[edge[0]][edge[1]]['label'] = "  %s" % c.edge[edge[0]][edge[1]]['psicquic']

c._stimuli = ["EGF", "TNFA"]
c._inhibitors = [ "P3C2A"]
c._signals = ["RAF1", "GSK3A", "GSK3B", "p38", "NFKB1", "NFKB2", "AP1S1","AP2S1", "MK01", "MK03"]


def selector(c, N=1):
    c2 = CNOGraph()
    for edge in c.edges():
        score = c.edge[edge[0]][edge[1]]['psicquic']
        if score>=N:
            e1 = reverse_mapping[edge[0]]
            e2 = reverse_mapping[edge[1]]
            c2.add_edge(e1, e2, link="+")
        c2._stimuli = ["egf", "tnfa"]
        c2._inhibitors = ["pi3k"]
        c2._signals = ["raf1", "gsk3", "p38", "nfkb", "ap1", "erk"]
        c2.add_edge("mkk4", "p38", link="+")
    return c2




