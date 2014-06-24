#!/usr/bin/env python
import argparse
import lipid_conv.lipid_conv as lipid_conv

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
parser.add_argument('-asymmetry','--asymmetry',action='store_true',help='Treat each leaflet separately for mode convert. See docs/asymmetry for detailed usage')

# Get the arguments
args = parser.parse_args()

# Read in the input structure - pdb or gro based on file ending 
struct = lipid_conv.read_input(input=args.input,
                               longresnum=args.longresnum,
                               debug=0)

# Do conversion or transformations
if args.mode == 'transform':
    new_struct = lipid_conv.transf(struct=struct,
                                   ffin=args.ffin,
                                   ffout=args.ffout)
elif args.mode == 'convert':
    new_struct = lipid_conv.conv(struct=struct,
                                 ffin=args.ffin,
                                 lin=args.lin,
                                 lout=args.lout,
                                 n = args.n,
                                 asymmetry = args.asymmetry)
else:
    print "Either transform or convert please...!"
    sys.exit()
        
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
