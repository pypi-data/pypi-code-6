#!/usr/bin/env python
# -*- coding: utf-8 -*- 

execfile("header.py")

def design():
    #---------------------------------------------------------------------------
    # This script should define a Dseqrecord named seq
    
    from pydna import read
    from pydna import Dseqrecord
    from pydna import pcr

    from pYPKa import pYPKa

    from Bio.Restriction import AjiI
    
    enz = AjiI
    
    ins = read("SsXYL1.txt")
    
    fp = read('''
>pfw957
aaATGCCTTCTATTAAGTTGAA
''', ds=False)
    
    rp = read('''
>prv957
TTAGACGAAGATAGGAATCTT
''', ds=False)
    
    pYPKa_cut = pYPKa.linearize(enz)
    
    ins = pcr(fp, rp, ins)
    
    seq = (pYPKa_cut + ins).looped().synced("tcgcgcgtttcggtgatgacggtgaaaacctctg")

    # This script should define a Dseqrecord named seq
    #---------------------------------------------------------------------------
    assert isinstance(seq, Dseqrecord)
    return seq
    
execfile("footer.py")
