from BCBio import GFF
from collections import defaultdict

gff_file = 'data/ref_GRCh37.p13_top_level.gff3'

gene2loc=defaultdict(dict) #geneId to TLS loc string
gene2tx = defaultdict(list) #list of tx for gene
tx2gene = defaultdict(dict) #map tx to geneID
tx2exon = defaultdict(list) #map exon locs to tx as a list
tx2cds = defaultdict(list) #map cds locs to tx as a list

def get_loc(seq, data):
    chr_name = chrid2name[seq]
    start = data.location.start
    stop = data.location.end
    loc = chr_name + ":" + str(start) + "-" + str(stop)
    return loc

geneIdsToGet = [i.strip() for i in open('genes.txt')]


chr_list = ['NC_000001.10'] #for testing
for c in chr_list:
    lim_info = dict(
            gff_id=[c]) #set gff limits
    print "Getting data for " + c
    with open(gff_file) as in_handle:
        for rec in GFF.parse(in_handle, limit_info=lim_info):
            seqID = rec.id
            geneID = ''
            for line in rec.features:
                if 'Dbxref' not in line.qualifiers:
                    pass 
                    #need to sort out what lines they are at some point
                else:
                    xref_str = line.qualifiers['Dbxref']
                    for xref in xref_str:
                        if xref.startswith('GeneID:'):
                            geneID = xref.split(':')[1]
                if geneID in geneIdsToGet:
                    #only keep data if in list of things to match
                    #print "Getting info for: " + geneID
                    gene_loc = get_loc(seqID, line)
                    gene2loc[geneID]=gene_loc
                    for info in line.sub_features:
                        if info.type == 'transcript' or info.type == 'mRNA' or info.type == 'primary_transcript':
                            txAcc = info.qualifiers['Name'][0]
                            #print txAcc
                            gene2tx[geneID].append(txAcc)
                            tx2gene[txAcc]=geneID
                            for detail in info.sub_features:
                                if detail.type == 'CDS':
                                    cds_loc = get_loc(seqID, detail)
                                    tx2cds[txAcc].append(cds_loc)
                                if detail.type == 'exon':
                                    exon_loc = get_loc(seqID, detail)
                                    tx2exon[txAcc].append(exon_loc)
                else:
                    pass
