#!/usr/bin/env python

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
import gflags
import lipid_conv.lipid_conv as lipid_conv

# Use gflags to parse command line options                                 
FLAGS = gflags.FLAGS

gflags.DEFINE_string('mode','transform',
                     'Do transformation or conversion')

gflags.DEFINE_string('f','conf.pdb',
                     'Input pdb structure')
gflags.DEFINE_string('o','out.pdb',
                     'Output pdb structure')

gflags.DEFINE_string('ffin', 'berger',
                     'source force field')
gflags.DEFINE_string('ffout', 'charmm36',
                     'target force field')

gflags.DEFINE_string('lin', 'POPC',
                     'input lipid')
gflags.DEFINE_string('lout', 'POPG',
                     'output lipid')
gflags.DEFINE_integer('n', 1,
                      'Convert every n-th lipid')

gflags.DEFINE_bool('canonical',False,
                   'Turn on canonical sorting')
gflags.DEFINE_bool('asymmetry',False,
                   'Generate an asymmetric bilayer with --mode convert')
gflags.DEFINE_bool('longresnum',False,
                   'Assume 5-digit residue numbers in pdb-files')

# Get the arguments
argv = FLAGS(sys.argv)

# Read in the input structure - pdb or gro based on file ending 
struct = lipid_conv.read_input(input=FLAGS.f,
                               longresnum=FLAGS.longresnum,
                               debug=0)

# Do conversion or transformations
if FLAGS.mode == 'transform':
    new_struct = lipid_conv.transf(struct=struct,
                                   ffin=FLAGS.ffin,
                                   ffout=FLAGS.ffout)
elif FLAGS.mode == 'convert':
    new_struct = lipid_conv.conv(struct=struct,
                                 ffin=FLAGS.ffin,
                                 lin=FLAGS.lin,
                                 lout=FLAGS.lout,
                                 n = FLAGS.n,
                                 asymmetry = FLAGS.asymmetry)
else:
    print "Either transform or convert please...!"
    sys.exit()
        
if FLAGS.canonical:
    # If we are changing from one forcefield to another, we are              
    # sorting according to the output ff                                     
    if FLAGS.mode == 'transform':
        ff_sort = FLAGS.ffout
        
    # And similarily, if we are changing a lipid type within a forcefield,   
    # we sort on this ff (ie the input ff)                                   
    if FLAGS.mode == 'convert':
        ff_sort = FLAGS.ffin
        
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
new_struct.write(FLAGS.output)
