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

import math
import numpy as np

try:    
    import networkx as NX
    have_networkx = True
except ImportError:
    print "Could not import networkx - will disable asymmetric"
    print "bilayer opertations"
    have_networkx = False
    
distH = 0.1
alphaH = np.arccos(-1/3.0)
s6 = 0.5 * np.sqrt(3.0)

accepted_p_atoms = {'P','P8'}

def setup(xAI,xAJ,xAK):
    rij = 0.0
    ra = 0.0
    
    sij = []
    sb = []
    sa = []
    
    for i in range(3):
        xd = xAJ[i]
        sij.append(xAI[i]-xd)
        sb.append(xd-xAK[i])
        rij+=np.square(sij[i])
        #print rij
    rij = np.sqrt(rij)
    #print sij
    
    sa.append(sij[1]*sb[2]-sij[2]*sb[1])
    sa.append(sij[2]*sb[0]-sij[0]*sb[2])
    sa.append(sij[0]*sb[1]-sij[1]*sb[0])
    #print sa
    #import sys
    #sys.exit()
    for i in range(3):
        sij[i]=sij[i]/rij
        ra+=np.square(sa[i])
    
    ra = np.sqrt(ra)
    #print "ra=",ra
    #import sys
    #sys.exit()
    for i in range(3):
        sa[i]=sa[i]/ra
    
    # Important to remember to reset sb here
    sb = []
    sb.append(sa[1]*sij[2]-sa[2]*sij[1])
    sb.append(sa[2]*sij[0]-sa[0]*sij[2])
    sb.append(sa[0]*sij[1]-sa[1]*sij[0])
    
    #print "sb=",sb
    #import sys
    #sys.exit()
    return sa,sb,sij

def one_single_atom(xAI,xAJ,xAK):
    
    xH1 = []
    #xAI=[-0.0677, -0.123, -0.0491]
    #xAJ=[-0.0001,0.0064,-0.0491]
    #xAK=[0.1499,-0.011,-0.0491]
    #print xAI
    #print xAJ
    #print xAK
    sa,sb,sij = setup(xAI,xAJ,xAK)
    
    for i in range(3):
        xH1.append(xAI[i]+distH*np.sin(alphaH)*sb[i]-distH*np.cos(alphaH)*sij[i])
    
    return xH1

def two_atoms(xAI,xAJ,xAK):
    r1 = []
    r2 = []
    r2 = []
    
    xH1 = []
    xH2 = []
    
    for i in range(3):
        r1.append(xAI[i]-0.5*(xAJ[i]+xAK[i]))
        
    b = np.linalg.norm(r1)
    r2 = np.subtract(xAI,xAJ)
    r3 = np.subtract(xAI,xAK)
    r4 = np.cross(r2,r3)
    n  = np.linalg.norm(r4)
    
    for i in range(3):
        xH1.append(xAI[i]+distH*(np.cos(alphaH/2.0*r1[i]/b+np.sin(alphaH/2.0)*r4[i]/n)))
        xH2.append(xAI[i]+distH*(np.cos(alphaH/2.0*r1[i]/b-np.sin(alphaH/2.0)*r4[i]/n)))
        
    return xH1, xH2

def three_atoms(xAI,xAJ,xAK):
    xH1 = []
    xH2 = []
    xH3 = []
    
    sa,sb,sij = setup(xAI,xAJ,xAK)
    
    for i in range(3):
        xH1.append(xAI[i]+distH*np.sin(alphaH)*sb[i]-distH*np.cos(alphaH)*sij[i])
        
        xH2.append(xAI[i]-
                   distH*np.sin(alphaH)*0.5*sb[i] +
                   distH*np.sin(alphaH)*s6*sa[i] -
                   distH*np.cos(alphaH)*sij[i])
        
        xH3.append(xAI[i]-
                   distH*np.sin(alphaH)*0.5*sb[i] -
                   distH*np.sin(alphaH)*s6*sa[i] -
                   distH*np.cos(alphaH)*sij[i])
        
    return xH1,xH2,xH3

# Compare two lists of atoms    
def check_atoms(target_atoms,atoms):
    s = list(set(target_atoms)-set(atoms))
    s1 = list(set(atoms)-set(target_atoms))
    
    return s,s1


# Return the residue name for atom ai in list l                                
def get_resn(l,ai):
    resn = ""
    
    for i in range(len(l)):
        try:
            if l[i] and l[i][0].strip()==ai:
                resn = l[i][1]
        except:
            print "Error in get_resn(): ai=%s",ai
            sys.exit()
            
    return resn
        
def get_resi(l,ai):
    resi = -1
    
    for i in range(len(l)):
        try:
            if l[i] and l[i][0].strip()==ai:
                resi = l[i][2]
        except:
            print "Error in get_resi(): ai=%s",ai
            sys.exit()

    return resi

def get_chain(l,ai):
    chain = ""
    
    for i in range(len(l)):
        try:
            if l[i] and l[i][0].strip()==ai:
                chain = l[i][3]
        except:
            print "Error in get_chain(): ai=%s"%ai
            sys.exit()
            
    return chain


# Return the position in list for atom ai in list l                            
def get_pos_in_list(l,ai):
    
    pos = -1
    
    for i in range(len(l)):
        try:
            if l[i] and l[i][0].strip()==ai:
                pos = i
        except TypeError:
            print "Error in get_pos_in_list(): ai=%s"%ai
            sys.exit()

    return pos

# Return the xyz coordinates of the atom in ai in list l                       
def get_xyz_coords(l,ai):
    
    xyz = np.zeros((3,))
    
    for i in range(len(l)):
        try:
            if l[i] and l[i][0].strip()==ai:
                xyz[0]=l[i][3][0]
                xyz[1]=l[i][3][1]
                xyz[2]=l[i][3][2]
        except TypeError:
            print "Error in get_xyz_coords(): ai=%s"%ai
            sys.exit()
            
    return xyz


# Returns the number of the i'th residue
def get_resnum(prot,i):
    count = 0
    
    for resnum in prot.get_residues():
        if count == i:
            return resnum
        count = count + 1

    return -1
    
# Get coords of P-atoms
def get_p_coords(struct):
    
    p_coords = []
    for resnum in struct.get_residues():
        residue = struct.get_residue_data(resnum)
        
        for i in range(len(residue)):
            #print residue[i][0]
            if residue[i][0].strip() in accepted_p_atoms:
                #print "APA"
                #print residue[i][3]
                #print p_xyz
                p_coords.append(list(residue[i][3]))
        #print residue
        
    #print p_coords
    return p_coords


# Calculate and return a distance matrix of all the coordinates in coords
def contact_matrix(coords,cutoff=2.0):
    coords = np.array(coords)
    n,m = coords.shape
    dist_mat = np.zeros((n,n),'d')
    for d in xrange(m):
        data = coords[:,d]
        dist_mat += (data - data[:,np.newaxis])**2
    return np.sqrt(dist_mat)<cutoff
        
def make_contact_graph(contact_mat):
    #print contact_mat
    return NX.Graph(contact_mat)

def get_graph_components(graph):
    return [np.sort(component) for component in NX.connected_components(graph)]

def get_leaflet_idx_for_resnum(struct,resnum,components):
    for i in range(len(components)):
        for j in range(len(components[i])):
            comp_ij = components[i][j]
            
            resn = get_resnum(struct,comp_ij)
            
            if resn == resnum:
                return i

    return -1
