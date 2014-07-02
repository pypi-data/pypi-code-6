from __future__ import print_function
import os
import sys
import logging
import argparse
from  bam2x import IO,TableIO,DBI
from bam2x.Tools import _translate_to_meta,merge_bed
def help():
    return "merged spliced bed ( Result from clean_reads )"
def set_parser(parser):
    #parser.add_argument("-m",type=str,choices=("seq","cDNA","cdna","cds","utr5","utr3"),dest="method")
    parser.add_argument("--gap",type=int,dest="gap",default=200)
    
def nh(bed): 
    '''
    Return 1.0/NH ( number of hits )  
    '''
    x=float(bed.itemRgb.split(",")[0])
    if x==0.0: x=1.0
    return 1.0/x
    
def run(args):
    def process():
        if len(buff)==1: return 0
        meta=buff[0]
        score=0.0
        score=nh(buff[0])
        for i in buff[1:]:
            meta=merge_bed(meta,i,"group_"+str(group_id))
            score+=nh(i)
        meta=meta._replace(score=score)

        print("META\t{meta}".format(meta=meta),file=out)
        for i in buff:
            print("READ\t{read}".format(read=_translate_to_meta(meta,i)),file=out)
        return 1
    GAP=args.gap
    fin=IO.fopen(args.input,"r")
    out=IO.fopen(args.output,"w")
    iterator=TableIO.parse(fin,"bed12")
    last=iterator.next()
    last_stop=last.stop
    group_id=0
    buff=[last]
    last_chr=last.chr
    for i in iterator:
        if i.chr!=last_chr or i.start-last_stop > GAP:
            group_id+=process()
            buff=[i]
            last_chr=i.chr
            last_stop=i.stop
        else:
            buff.append(i)
            if i.stop>last_stop:
                last_stop=i.stop
    process()
        

    
    
    
        

if __name__=="__main__":
    from bam2x.IO import parser_factory
    p=parser_factory(description=help())
    set_parser(p)
    if len(sys.argv)==1:
        print(p.print_help())
        exit(0)
    run(p.parse_args())







