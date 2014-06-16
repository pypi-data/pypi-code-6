#########################
# last update:
# Mon 07 Apr 2014 10:32:02 AM CEST
# [JMass]
########################
import sys
import getopt
from ..helpers import FastaParser
def usage():
    """Usage"""

    print("""

    usage:
    loc_ensembl_fasta.py -f file.fa

    options:
    -f, --fasta= STR      FASTA file
    [-o, --out= STR]      [optional] output filename
    or
    [-s, --species= STR]  [optional] species name
    -h, --help            prints this
    #######################
    # FASTA header example:
    >ENSBTAP00000055373 pep:known scaffold:UMD3.1:GJ059509.1:3535:6470:-1 gene:ENSBTAG00000047958 transcript:ENSBTAT00000064726 gene_biotype:protein_coding transcript_biotype:protein_coding
    #######################
    """)
    sys.exit(2)

class Pep(object):
    def __init__(self,pep,gene,length):
        self.gene = gene
        self.pep  = pep
        self.cds = None
        self.length = length
        self.isLongest = None

def prepareLocFromFasta(fasta, outpath, specname):
    genes = {}
    longest = {}

    if not os.path.isdir(outpath):
        os.makedirs(outpath)
    if not outpath:
        out = fasta+".loc"
    else:
        out = outpath+os.sep+specname+".loc"
    fp = FastaParser()
    out = open(out,'w')
    print(out)
    for i in fp.read_fasta(fasta):
        tmp = i[0].split(" ")
        geneid = [t for t in tmp if "gene:" in t]
        geneid = geneid[0].split("gene:")[-1]
        proteinid = tmp[0]
        protlen=len(i[1])
        peptide= Pep(proteinid,geneid,protlen)
        try:
            genes[geneid].append(peptide)
            if peptide.length > longest[geneid].length:
                longest[geneid].isLongest =False
                longest[geneid]=peptide
                peptide.isLongest = True
        except KeyError as e:
            genes[geneid] = [peptide]
            longest[geneid] = peptide
            peptide.isLongest=True
    for g in genes:
        print(g)
        firstcol = [w for w in genes[g] if w.isLongest==True ]
        restcol = [w for w in genes[g] if w.isLongest!=True ]
        s = firstcol[0].gene+"\t"+firstcol[0].pep+"\t"
        s+="\t".join([v.pep for v in restcol])
        s+="\n"
        out.write(s)
        print(s)
    out.close()
    print("done")
#######################
def main():
    infile = None
    outfile = None
    specname = None
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "f:o:s:ch",["fasta=","out=","species=","help"])
    except getopt.GetoptError as err:
        sys.stderr.write(str(err))
        usage()
    for o, a in opts:
        if o in ("-f", "--fasta"):
            infile = a
            outfile = a+".loc"
        elif o in ("-o", "--out"):
            outfile = a
        elif o in ("-s", "--species"):
            specname = a
            outfile = None
        elif o in ("-h", "--help"):
            usage()
        else:
            assert False, "unhandled option"

if __name__=="__main__":
    main()
