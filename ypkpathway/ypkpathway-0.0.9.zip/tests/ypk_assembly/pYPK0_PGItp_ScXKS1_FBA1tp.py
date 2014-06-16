#!/usr/bin/env python
# -*- coding: utf-8 -*- 

execfile("header.py")

def design():
    #---------------------------------------------------------------------------
    # This script should define a Dseqrecord named seq
    
    from pydna import pcr
    from pydna import parse
    from pydna import Genbank
    from pydna import Assembly
    from pydna import Dseqrecord
    
    p577,p578,p468,p467,p567,p568 =    parse('''>577        
                                                gttctgatcctcgagcatcttaagaattc                                                
                                                >578          
                                                gttcttgtctcattgccacattcataagt
                                                >468
                                                gtcgaggaacgccaggttgcccact
                                                >467 
                                                ATTTAAatcctgatgcgtttgtctgcacaga
                                                >567
                                                GTcggctgcaggtcactagtgag
                                                >568
                                                GTGCcatctgtgcagacaaacg''')
                                                
    from Bio.Restriction import ZraI, AjiI, EcoRV
    
    from pYPKpw import pYPKpw
    
    pYPKpw_lin = pYPKpw.linearize(EcoRV)
    
    from pYPKa_Z_PGItp import pYPKa_Z_PGItp as first
    from pYPKa_A_ScXKS1 import pYPKa_A_ScXKS1 as middle
    from pYPKa_E_FBA1tp import pYPKa_E_FBA1tp as last                                                                               

    first  = pcr( p577, p567, first)
    middle = pcr( p468, p467, middle)
    last   = pcr( p568, p578, last)
    
    asm = Assembly((pYPKpw_lin, first, middle, last))
    
    print asm.analyze_overlaps(limit=31)

    print asm.create_graph()

    print asm.assemble_circular_from_graph()

    seq = asm.circular_products[0]
    
    seq=seq.synced("tcgcgcgtttcggtgatgacggtgaaaacctctg")

    # This script should define a Dseqrecord named seq
    #---------------------------------------------------------------------------
    assert isinstance(seq, Dseqrecord)
    return seq

execfile("footer.py")
