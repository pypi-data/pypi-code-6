#!/usr/bin/env python
# Programmer : zhuxp
# Date: 
# Last-modified: 05-28-2014, 14:07:51 EDT
from __future__ import print_function
VERSION="0.1"
import os,sys,argparse
from bam2x.Annotation import BED12
from bam2x import TableIO,Tools
from bam2x import IO
import time
import multiprocessing as mp
def Main():
    print(rep([0,0,1,1,2,2]))

def rep(list):
    s=""
    last=list[0]
    step=0
    offset=0
    for i in list:
        if i!=last:
            s+="{offset},{value},{step}\n".format(offset=offset,value=last,step=step)
            last=i
            offset+=step
            step=1
        else:
            step+=1
    s+="{offset},{value},{step}".format(offset=offset,value=last,step=step)
    return s



    
if __name__=="__main__":
    Main()





