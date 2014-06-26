#/usr/bin/env python

#Lipid-converter.py
#Copyright (C) 2014 Per Larsson Peter Kasson 

#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Library General Public
#License as published by the Free Software Foundation; either
#version 2 of the License, or (at your option) any later version.

#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Library General Public License for more details.

#You should have received a copy of the GNU Library General Public
#License along with this library; if not, write to the
#Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
#Boston, MA  02110-1301, USA.

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

def conv(struct,ffin,lin,lout,n,asymmetry):
    c = convert()
    c.read_conversions()
    new_struct = c.do(struct,ffin,lin,lout,n,asymmetry)
    return new_struct

