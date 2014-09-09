#TODO 
from __future__ import print_function
import os
import sys
import logging
import argparse
from  bam2x import IO,TableIO,DBI
from bam2x.Struct import binindex
from bam2x.Tools import compatible_with_transcript
def help():
    return "compare RNA Seq bam with Gene annotations, remove the low score (<20 ) and reads from gene"
def set_parser(parser):
    #parser.add_argument("-m",type=str,choices=("seq","cDNA","cdna","cds","utr5","utr3"),dest="method")
    parser.add_argument("-a","--bed",type=str,dest="bed",help="gene annotations bed12 file")
    parser.add_argument("-s","--strand",type=str,dest="strand",choices=("read1","read2"),default="read2",help="paired end RNA seq strand, default:%(default)s")
    
    
def run(args):
    SCORE_THRESHOLD=20
    logging.basicConfig(level=logging.INFO)
    out=IO.fopen(args.output,"w")
    logging.info("reading annotation into data structure")
    binindex_db=binindex(TableIO.parse(args.bed,"bed12"))
    logging.info("done.")
    mapped_reads_count=0
    compatible_reads_count=0
    overlap_not_compatible_reads_count=0
    no_overlap_reads_count=0
    spliced_reads_count=0
    for count,i in enumerate(TableIO.parse(args.input,"bam2bed12",strand=args.strand)):
        overlap_gene=False
        compatible_gene=False
        mapped_reads_count+=1
        if count%1000==0:
            print("M: {mapped}    \t  C: {compatible}  \t  O: {overlap}   \tN: {no_overlap}   \tS: {spliced}                               ".format(mapped=mapped_reads_count,compatible=compatible_reads_count,overlap=overlap_not_compatible_reads_count,no_overlap=no_overlap_reads_count,spliced=spliced_reads_count),file=sys.stderr,end="\r")
        if i.score<SCORE_THRESHOLD:
            continue
        if i.blockCount>1:
            spliced_reads_count+=1
        for j in binindex_db.query(i):
            overlap_gene=True
            if compatible_with_transcript(i,j):
                compatible_gene=True
                break
        if compatible_gene:
            compatible_reads_count+=1
            continue
        elif overlap_gene:
            overlap_not_compatible_reads_count+=1
            print(i,file=out)
        else:
            no_overlap_reads_count+=1
            print(i,file=out)
    print("M: {mapped}    \t  C: {compatible}  \t  O: {overlap}   \tN: {no_overlap}   \tS: {spliced}                               ".format(mapped=mapped_reads_count,compatible=compatible_reads_count,overlap=overlap_not_compatible_reads_count,no_overlap=no_overlap_reads_count,spliced=spliced_reads_count))








if __name__=="__main__":
    from bam2x.IO import parser_factory
    p=parser_factory(description=help())
    set_parser(p)
    if len(sys.argv)==1:
        print(p.print_help())
        exit(0)
    run(p.parse_args())


