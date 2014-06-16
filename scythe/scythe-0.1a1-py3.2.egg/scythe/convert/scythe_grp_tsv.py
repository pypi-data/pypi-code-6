#!/usr/bin/env python3
import sys
import getopt
VERB=True
#####################################
# last update 05/03/2013 by J. Mass #
# version = '0.1'                   #
#####################################

def usage():
    print ("""
    ###################################
    #  Scythe_ensemble2grp.py (v0.1)  #
    ###################################
    -s NUM, --species    number of species in infile
    -f INFILE, --file=INFILE
                   input format: SP0geneID0    ...    SPkgeneID0
                   first line is header

    -o OUTFILE, --output=OUTFILE    default: ENSEMBLE input.grp]
    -h, --help    prints this
    #----------------------------------#
    .grp format: GroupID\tgeneIDiSp1\tgeneIDjSp2\t...geneIDkSpn
    """)
    sys.exit(2)
###################################
outfile = None
ensemblMap = None
numSp=None
###################################
try:
    opts, args = getopt.gnu_getopt(sys.argv[1:], "f:ho:s:", ["file=","help", "output=", "species="])
except getopt.GetoptError as err:
    print (str(err))
    usage()
for o, a in opts:
    if o in ("-f", "--file"):
        ensemblMap = a
    elif o in ("-h", "--help"):
        usage()
    elif o in ("-s", "--species"):
        numSp = a
    elif o in ("-o", "--output"):
        outfile = a
    else:
        assert False, "unhandled option"

if not ensemblMap or not numSp:
    usage()
if not outfile:
        outfile = ensemblMap+".grp"
########################################
def printInfo(numSp, numLoc, outfile=outfile, verb=False):
    if verb:
        print("# Success\n# Formatted "+str(numSp)+" species and "+str(numLoc)+" geneIDs.")
       # print("# That's an average of "+pfloat(numTr/numLoc)+" Transcripts per Locus")
        print("# Saved to file "+outfile)


def readEnsemblMap(infile, outfile, numSp):
    seen = []
    many = set()
    one = set()
    seenDct={}
    result = ""
    id = 0
    inf = open(infile, "r")
    out = open(outfile,"w")
    for l in inf:
        if l.startswith("Ensembl "):
            continue
        #if (id == 0):
        #    id+=1
        #    continue
        l = l.rstrip("\n")
        tmp = l.split("\t")

        if (len(tmp)<2 or (len(tmp)>int(numSp))):
            print("Check your input file", infile)
            usage()
        tmp = [t for t in tmp if t !=""]
        if (len(tmp)<2):
            pass
            #print("no orthologs, skip "+" ".join(tmp))

        else:
            new = [t for t in tmp if t not in one]
            for n in new:
                one.add(n)
            if(len(new)<len(tmp)):
                pass
            else:
                seen.append("\t".join(new))

    inf.close()
    for l in seen:
        out.write(str(id)+"\t"+l+"\n")
        id+=1
    out.close()
    printInfo(verb=VERB,numLoc=id+1, numSp=numSp)
readEnsemblMap(ensemblMap, outfile, numSp)
