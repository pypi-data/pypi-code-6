#!/usr/bin/env python

import argparse
import lipid_converter

# Use argparse to parse command line options                                 
parser = argparse.ArgumentParser(description='Lipid-converter')
parser.add_argument('-f','--input',required=True)
parser.add_argument('-o','--output',required=True)
parser.add_argument('-mode','--mode',default='transform',help='Transform or \
Convert')
parser.add_argument('-ffin','--ffin',default='berger',help='Source force fie\
ld')
parser.add_argument('-ffout','--ffout',default='charmm36',help='Target force\
 field')
parser.add_argument('-lin','--lin',help='Input lipid')
parser.add_argument('-lout','--lout',help='Output lipid')
parser.add_argument('-n','--n',help='Convert every n-th lipid')
parser.add_argument('-canonical','--canonical',action='store_true',help='Can\
onical force field sorting of output')
parser.add_argument('-longresnum','--longresnum',action='store_true',help='A\
ssume long residues numbers in pdb file')

# Get the arguments                                                              
args = parser.parse_args()

