#Lipid-converter.py                                                            #Copyright (C) 2014 Per Larsson Peter Kasson 

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

import os
import glob
import re
from structure import Protein
from forcefields import ff_transformations
import aux

import sys

regexp = re.compile('^ *\[ *(.*) *\]')

class transform():
    def __init__(self):
        self.transforms = {}
        
    def read_transforms(self):
        for ff in ff_transformations:
            
            fn = ""

            try:
                path = os.path.dirname(__file__)
                path = os.path.join(path,ff,'transforms.top')
                fn = open(path,'r')
            except:
                print "Could not open transform file for %s"%ff
            
            transf = []
            hyd = []
            ffout = ""
            lipid = ""

            for line in fn:
                l = line.strip()
                
                if l.startswith("["):
                    d = re.findall(regexp,l)[0].strip().lower()
                    
                    # If we get to end of an entry, store it
                    if d=='end':
                        
                        # Create a new dict for this entry
                        m = {}
                        m['transf']=transf
                        if hyd:
                            m['hyd']=hyd
                        
                            # Add this combination of lipid, ff and ffout
                            # as a tuple key
                        self.transforms[lipid,ff,ffout]=m
                        
                        # Reset these two
                        transf = []
                        hyd = []

                    continue

                if not l:
                    continue

                elif d == 'atoms':
                    transf.append(l.split())
                    
                elif d == 'hydrogens':
                    hyd.append(l.split())

                elif d == 'molecule':
                    lipid = l.split()[0]

                elif d =='target':
                    ffout = l.split()[0]

    def do(self,prot,ffin,ffout):

        new = Protein()
        #print self.transforms['POPC','lipid11','charmm36']
        #sys.exit()
        
        for resnum in prot.get_residues():
            residue = prot.get_residue_data(resnum)
            
            print "converting residue %d"%resnum
            try:
                if ffin == 'lipid11':
                    lipid = prot.get_canonical_residue_name(residue)
                else:
                    lipid = residue[0][1]
                    
                transf_atoms = self.transforms[lipid,ffin,ffout]['transf']
                try:
                    hyd = self.transforms[lipid,ffin,ffout]['hyd']
                except KeyError:
                    hyd = ""
            except:
                print "No transformation from %s to %s for residue %s %d found"%(ffin,ffout,lipid,resnum)
                sys.exit()
                
            # Do the transformation
            transformed = self.transform_residue(residue,transf_atoms,ffin,ffout,lipid)
            #print transformed
            #new.add_residue_data(transformed)
            #new.write('test.pdb')
            #sys.exit()
            #print hyd
            #sys.exit()
            if hyd:
                transformed = self.build_atoms(transformed,hyd)
            
            #print transformed
            #sys.exit()
            # Add the result to a new protein
            new.add_residue_data(transformed)
            #new.write('test.pdb')
            #print new.atname
            #print new.coord
            #sys.exit()
        return new
            
    def transform_residue(self,residue,transf_atoms,ffin,ffout,lipid):
        out = []
        #print transf_atoms
        for i in range(len(residue)):
            #print residue
            #sys.exit()
            ain = residue[i][0]
            resn_in = residue[i][1]
            
            #print resn_in
            #sys.exit()
            
            # Amber/lipids11 is a special case in that we also
            # need to change (and later sort on) the residue name
            # as well                                              
            # note that in this case the transf_atom structure       
            # from read_tranforms() will contain the new residue     
            # name as well in the [2]-column                         
            # this pertains to when the ffout==lipid11            
            if ffin == 'lipid11':
                for j in range(len(transf_atoms)):
                    if ( (ain == transf_atoms[j][0]) and
                         (resn_in == transf_atoms[j][2]) ):
                        aout = transf_atoms[j][1]
                        resn = lipid
                        
                        resi = residue[i][2]
                        coords = residue[i][3]
                        out.append((aout,resn,resi,coords))
                        break
            elif ffout=='lipid11':
                for j in range(len(transf_atoms)):
                    
                    if(ain == transf_atoms[j][0]):
                        aout = transf_atoms[j][1]
                        resn = transf_atoms[j][2]
                        
                        resi = residue[i][2]
                        coords = residue[i][3]
                        out.append((aout,resn,resi,coords))
                        break
            else:
                for j in range(len(transf_atoms)):
                    
                    if(ain == transf_atoms[j][0]):
                        aout = transf_atoms[j][1]
                        resn = lipid
                        
                        resi = residue[i][2]
                        coords = residue[i][3]
                        out.append((aout,resn,resi,coords))
                        break
        return out

    def build_atoms(self,residue,hyd):
        
        for i in range(len(hyd)):
            
            # Get the data for building atoms
            name,suffix,ai,aj,ak = hyd[i]
            
            # Number of atoms to build is based on the length of the
            # suffix string
            num = len(suffix)
            
            xai = aux.get_xyz_coords(residue,ai)
            xaj = aux.get_xyz_coords(residue,aj)
            xak = aux.get_xyz_coords(residue,ak)

            pos   = aux.get_pos_in_list(residue,ai)
            resn  = aux.get_resn(residue,ai)
            resi  = aux.get_resi(residue,ai)

            if num==1:
                x1 = aux.one_single_atom(xai,xaj,xak)
                x1_name = name
                residue.insert(pos+1,(x1_name,resn,resi,(x1[0],x1[1],x1[2])))

            elif num==2:
                x1,x2 = aux.two_atoms(xai,xaj,xak)
                x1_name = name+suffix[0]
                x2_name = name+suffix[1]
                residue.insert(pos+1,(x1_name,resn,resi,(x1[0],x1[1],x1[2])))
                residue.insert(pos+2,(x2_name,resn,resi,(x2[0],x2[1],x2[2])))

            elif num==3:
                x1,x2,x3 = aux.three_atoms(xai,xaj,xak)
                x1_name = name+suffix[0]
                x2_name = name+suffix[1]
                x3_name = name+suffix[2]
                residue.insert(pos+1,(x1_name,resn,resi,(x1[0],x1[1],x1[2])))
                residue.insert(pos+2,(x2_name,resn,resi,(x2[0],x2[1],x2[2])))
                residue.insert(pos+2,(x3_name,resn,resi,(x3[0],x3[1],x3[2])))
            else:
                print "Need to specify either 1,2 or 3 hydrogens to construct around central atom %s"%ai
                print "Currently it is %d"%num
                print "Bailing out..."
                
                sys.exit()
        #print residue
        return residue
        

    
    
