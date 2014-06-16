#!/usr/bin/env python
# -*- coding: utf-8 -*- 

execfile("header.py")


def design():
    #---------------------------------------------------------------------------
    # This script should define a Dseqrecord named seq
       
    from pydna import parse
    from pydna import pcr
    from pydna import Assembly
    from pydna import Dseqrecord
    
    
    (p577,
     p578,
     p775,
     p778) = parse('''>577          
                      gttctgatcctcgagcatcttaagaattc                                                                           
                      >578            
                      gttcttgtctcattgccacattcataagt
                      >775 
                      gcggccgctgacTTAAAT
                      >778 
                      ggtaaatccggatTAATTAA''', ds=False)
    
    from Bio.Restriction import EcoRV

    from pYPKpw import pYPKpw
    
    pYPKpw_lin = pYPKpw.linearize(EcoRV)
    
    from pYPK0_TEF1tp_SsXYL1_TDH3tp import pYPK0_TEF1tp_SsXYL1_TDH3tp as cas1
    from pYPK0_TDH3tp_SsXYL2_PGItp import pYPK0_TDH3tp_SsXYL2_PGItp as cas2
    from pYPK0_PGItp_ScXKS1_FBA1tp import pYPK0_PGItp_ScXKS1_FBA1tp as cas3
    from pYPK0_FBA1tp_ScTAL1_PDC1tp import pYPK0_FBA1tp_ScTAL1_PDC1tp as cas4
    cas1  = pcr( p577, p778, cas1)
    cas2  = pcr( p775, p778, cas2)
    cas3  = pcr( p775, p778, cas3)
    cas4 = pcr( p775, p578, cas4)    
    
    asm = Assembly((pYPKpw_lin, cas1,cas2,cas3,cas4))

    print asm.analyze_overlaps(limit=167-47-10)

    print asm.create_graph()

    print asm.assemble_circular_from_graph()

    seq = asm.circular_products[0]
    
    print seq.small_fig()
            
    seq = seq.synced("tcgcgcgtttcggtgatgacggtgaaaacctctg")     
    
    # This script should define a Dseqrecord named seq
    #---------------------------------------------------------------------------
    assert isinstance(seq, Dseqrecord)
    return seq
    
execfile("footer.py")
    


