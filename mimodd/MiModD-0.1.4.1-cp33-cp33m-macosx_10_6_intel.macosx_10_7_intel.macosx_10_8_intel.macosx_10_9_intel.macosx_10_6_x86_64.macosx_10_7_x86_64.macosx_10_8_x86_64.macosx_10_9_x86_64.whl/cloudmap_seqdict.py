import sys
from . import pyvcf

def cloudmap_seqdict_from_vcf (ifile, ofile = None):
    try:
        vcf = pyvcf.open(ifile)
        if not ofile:
            out = sys.stdout
        else:
            out = open(ofile, 'w')
        
        for ident, length in vcf.info.contigs.items():
                out.write ('{0}\t{1}\n'.format(ident, int(length)//10**6+1))
    finally:
        try:
            vcf.close()
        except:
            pass
        if out is not sys.stdout:
            try:
                out.close()
            except:
                pass
    
