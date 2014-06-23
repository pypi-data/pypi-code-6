#/usr/bin/env python
import sys
import os
from structure import Protein
from transform import transform
from convert import convert
import argparse

def lipid_converter():
    # Use argparse to parse command line options
    parser = argparse.ArgumentParser(description='Lipid-converter')
    parser.add_argument('-f','--input',required=True)
    parser.add_argument('-o','--output',required=True)
    parser.add_argument('-mode','--mode',default='transform',help='Transform or Convert')
    parser.add_argument('-ffin','--ffin',default='berger',help='Source force field')
    parser.add_argument('-ffout','--ffout',default='charmm36',help='Target force field')
    parser.add_argument('-lin','--lin',help='Input lipid')
    parser.add_argument('-lout','--lout',help='Output lipid')
    parser.add_argument('-n','--n',help='Convert every n-th lipid')
    parser.add_argument('-canonical','--canonical',action='store_true',help='Canonical force field sorting of output')
    parser.add_argument('-longresnum','--longresnum',action='store_true',help='Assume long residues numbers in pdb file')
    
# Get the arguments
    args = parser.parse_args()

# Read in the input structure - pdb or gro based on file ending
    struct = Protein(args.input,args.longresnum,debug=0)

# Do conversion or transformation
    if args.mode == 'transform':
        t = transform()
        t.read_transforms()
        new_struct = t.do(struct,args.ffin,args.ffout)
    elif args.mode == 'convert':
        t = convert()
        t.read_conversions()
        new_struct = t.do(struct,args.ffin,args.lin,args.lout,args.n)
    else:
        print "Either transform or convert please...!"
        sys.exit()
        
# Does it make sense to sort here?
    if args.canonical:
        
        # If we are changing from one forcefield to another, we are
        # sorting according to the output ff
        if args.mode == 'transform':
            ff_sort = args.ffout
    
        # And similarily, if we are changing a lipid type within a forcefield,
        # we sort on this ff (ie the input ff)
        if args.mode == 'convert':
            ff_sort = args.ffin
        
        # We also need a special trick for amber/lipids11, since the residue
        # names are identical between different lipids (the plug-and-play
        # architecture differentiates between different lipid headgroups and
        # tails, so that different lipids with the same tails will have the same
        # residue names.
        # We therefore loop over the input structure and save an array with the
        # old residue names
        # Todo: work out something when going from an amber/lipid11 coordinate
        # file (probably some kind of third file with residue names)
        resmap = None    
        if ff_sort == 'lipid11':
            resmap = struct.get_resnames()
        
        new_struct = new_struct.sort(ff_sort,resmap)    

    # Write out result
    new_struct.write(args.output)
