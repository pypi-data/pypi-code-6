import os
import glob
import re
import sys
from structure import Protein
from forcefields import ff_conversions
import aux

regexp = re.compile('^ *\[ *(.*) *\]')

class convert():
    def __init__(self):
        self.conversions = {}
        
    def read_conversions(self):
        for ff in ff_conversions:
            fn = ""

            try:
                path = os.path.dirname(__file__)
                path = os.path.join(path,ff,'conversions.top')
                fn = open(path,'r')
            except:
                print "Could not open convert file for %s"%ff
                
            add_atoms = []
            remove = []
            rename = []
            
            lin = ""
            lout = ""

            for line in fn:
                l = line.strip()

                if l.startswith("["):
                    d = re.findall(regexp,l)[0].strip().lower()
                    
                    # If we get to end of an entry, store it
                    if d=='end':
                        
                        # Create a new dict for this entry
                        m = {}
                        m['add']=add_atoms
                        m['remove']=remove
                        m['rename']=rename
                        
                        # Add this combination of ff,lin and lout
                        # as a tuple key
                        self.conversions[ff,lin,lout]=m

                        # Reset these three
                        rename = []
                        add_atoms = []
                        remove = []

                    continue

                if not l:
                    continue

                elif d == 'rename':
                    rename.append(l.split())
                    
                elif d == 'add':
                    add_atoms.append(l.split())
                    
                elif d == 'remove':
                    remove.append(l.split())

                elif d == 'molecule':
                    lin = l.split()[0]
                    
                elif d =='target':
                    lout = l.split()[0]

    def do(self,prot,ff,lin,lout,n,asymmetry):
        
        new = Protein()

        # Get the total number of residues
        total_resnum = len(prot.get_residues())
        
        # Treat the asymmetric case separetly
        if asymmetry:
            
            print "Asymmetric conversion requested"
            print "Building distance matrix of P-atoms"
            
            # Algoritm to implement (following N. Michaud-Agrawal et al,
            # J. Comput. Chem. 32 (2011), 2319

            # 1. Get the coords of the P-atoms
            p_coords = aux.get_p_coords(prot)
            
            # 2. Calculate distance matrix for coords
            distance_mat = aux.contact_matrix(p_coords)
            
            # 3. Identify the lipids in each leaflet
            print "Attempting to identify individual leaflets"
            graph = aux.make_contact_graph(distance_mat)
            components = aux.get_graph_components(graph)
            
            # 4. Convert each leaflet separately
            print "Converting leaflets separately"
            
            convert_count = [0,0]
            
            lin_leaflets = lin.split(':')
            lout_leaflets = lout.split(':')
            n_leaflets = n.split(':')
            
            for resnum in prot.get_residues():
                residue = prot.get_residue_data(resnum)
                resname = residue[0][1]
                
                # Get the leaflet index for this residue
                leaflet_idx = aux.get_leaflet_idx_for_resnum(prot,resnum,components)
                
                # Do error checking for leaflet_idx
                lin_i = lin_leaflets[leaflet_idx]
                lout_i = lout_leaflets[leaflet_idx]
                n_i = int(n_leaflets[leaflet_idx])
                
                if resname == lin_i:
                    convert_count[leaflet_idx] = convert_count[leaflet_idx] + 1
                    
                if convert_count[leaflet_idx]%n_i==0 and resname == lin_i:
                    try:
                        lipid = residue[0][1]
                        add_atoms = self.conversions[ff,lin_i,lout_i]['add']
                        rename_atoms = self.conversions[ff,lin_i,lout_i]['rename']
                        remove_atoms = self.conversions[ff,lin_i,lout_i]['remove']
                    except:
                        print "No conversion between %s and %s in %s found"%(lin_i,lout_i,ff)
                        sys.exit()
                        
                            # Do the conversions
                    transformed = self.remove_atoms(residue,remove_atoms)
                    transformed = self.rename_atoms(transformed,rename_atoms)
                    transformed = self.build_atoms(transformed,add_atoms)
                    transformed = self.update_resname(transformed,lout_i)
                    print "Converted residue %s %d to %s (total numres: %d)"%(lin_i,resnum,lout_i,total_resnum)
                else:
                    transformed = residue

                    # Add the result to a new protein
                new.add_residue_data(transformed)
                    
            return new
        
        else:
            convert_count = 0

            for resnum in prot.get_residues():
                residue = prot.get_residue_data(resnum)
                resname = residue[0][1]
                
                if resname == lin:
                    convert_count = convert_count + 1

                # Is this a residue we want to change?
                if convert_count%n==0 and resname == lin:
                    try:
                        lipid = residue[0][1]
                        add_atoms = self.conversions[ff,lin,lout]['add']
                        rename_atoms = self.conversions[ff,lin,lout]['rename']
                        remove_atoms = self.conversions[ff,lin,lout]['remove']
                    except:
                        print "No conversion between %s and %s in %s found"%(lin,lout,ff)
                        sys.exit()
                    
                    # Do the conversions
                    transformed = self.remove_atoms(residue,remove_atoms)
                    transformed = self.rename_atoms(transformed,rename_atoms)
                    transformed = self.build_atoms(transformed,add_atoms)
                    transformed = self.update_resname(transformed,lout)
                    print "Converted residue %s %d to %s (total numres: %d)"%(lin,resnum,lout,total_resnum)
                else:
                    transformed = residue
                
                # Add the result to a new protein   
                new.add_residue_data(transformed)

            return new
            
    def remove_atoms(self,residue,remove_atoms):
        
        # Make a local copy of the atom names her
        # so we can make operations on the residue 
        # list in the loop
        atoms = [i[0].strip() for i in residue]

        for i in range(len(remove_atoms)):
            ai = remove_atoms[i][0]
            
            for j in range(len(atoms)):
                aj = atoms[j]
                if ai == aj:
                    
                    # This is important since atoms and residue
                    # will be out of sync 
                    pos = aux.get_pos_in_list(residue,aj)
                    residue.pop(pos)
                    
        return residue


    def rename_atoms(self,residue,rename_atoms):

        atoms = [i[0].strip() for i in residue]
               
        for i in range(len(rename_atoms)):
            ai = rename_atoms[i][0]
            aout = rename_atoms[i][1]

            for j in range(len(atoms)):
                aj = atoms[j]

                if ai == aj:
                    #print ai,aout
                    residue[j]=(aout,
                                residue[j][1],
                                residue[j][2],
                                residue[j][3])
        return residue
                    
    def build_atoms(self,residue,add_atoms):
        
        for i in range(len(add_atoms)):
            
            # Get the data for building atoms
            name,suffix,ai,aj,ak = add_atoms[i]
            
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
                
        return residue
        

    def update_resname(self,residue,lout):
        residue = [list(i) for i in residue]
        
        for i in range(len(residue)):
            residue[i][1]=lout
    
        return residue
