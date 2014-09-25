from __future__ import print_function
import os
import sys
import logging
import argparse
from bam2x import TableIO,IO,DBI
from bam2x.Tools import seq_wrapper,rc
from random import random
def help():
    return "generate random fastq file"
def set_parser(parser):
    #parser.add_argument("-m",type=str,choices=("seq","cDNA","cdna","cds","utr5","utr3"),dest="method",default="seq")
    parser.add_argument("-g","--genome",type=str,dest="genome",help="chromsome.2bit file")
    parser.add_argument("-b","--bed_column_number",type=int,choices=[3,6,12],dest="bed_column_number",default=12) 
    parser.add_argument("-l","--length",type=int,dest="length",default=60) 
    parser.add_argument("--num",type=int,dest="number",default=100000) 
    
def run(args):
    bedformat="bed"+str(args.bed_column_number)
    dbi=DBI.init(args.genome,"genome")
    out1=IO.fopen(args.output+"_1.fq","w")
    out2=IO.fopen(args.output+"_2.fq","w")
    seqs=[dbi.query(i,method="cdna") for i in TableIO.parse(IO.fopen(args.input,"r"),bedformat)]
    size=len(seqs)
    i=0
    while i<args.number:
        k=int(random()*size)
        l=len(seqs[k])
        if l<args.length: continue
        start=int(random()*(l-args.length))
        length=int(args.length+(l-args.length)*random())
        stop=start+length
        if stop > l: continue
        a=seqs[k][start:start+args.length]
        b=seqs[k][stop-args.length:stop]
        b=rc(b)
        print("@r{i}_1".format(i=i),file=out1)
        print("{a}".format(a=a),file=out1)
        print("+",file=out1)
        print("".join(["I" for j in xrange(args.length)]),file=out1)
        print("@r{i}_2".format(i=i),file=out2)
        print("{b}".format(b=b),file=out2)
        print("+",file=out2)
        print("".join(["I" for j in xrange(args.length)]),file=out2)
        i+=1
        if (i%100==0) :
            print("generate {i} fq".format(i=i),end="\r",file=sys.stderr)



if __name__=="__main__":
    from bam2x.IO import parser_factory
    p=parser_factory(description=help())
    set_parser(p)
    if len(sys.argv)==1:
        print(p.print_help())
        exit(0)
    run(p.parse_args())

 
