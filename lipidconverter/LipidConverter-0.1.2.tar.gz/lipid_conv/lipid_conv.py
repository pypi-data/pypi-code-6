#/usr/bin/env python
import sys
import os
from structure import Protein
from transform import transform
from convert import convert

def read_input(input,longresnum,debug=0):
    # Read in the input structure - pdb or gro based on file ending
    struct = Protein(input,longresnum,debug=0)
    return struct

def transf(struct,ffin,ffout):
    t = transform()
    t.read_transforms()
    new_struct = t.do(struct,ffin,ffout)
    return new_struct

def conv(struct,ffin,lin,lout,n):
    c = convert()
    c.read_conversions()
    new_struct = c.do(struct,ffin,lin,lout,n)
    return new_struct

