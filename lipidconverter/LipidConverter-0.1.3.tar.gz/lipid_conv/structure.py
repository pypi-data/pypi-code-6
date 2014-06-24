import math
import re
import os
import sys
import numpy as np
from forcefields import ff_sortings,lipid11_residues,is_lipid

Vsites = ['MN1','MN2']
directive = re.compile('^ *\[ *(.*) *\]')

class Sort:
    def __init__(self):
        self.sorts = {}

    def sort(self,ff,resmap):
        # Get everything
        self.read_sortings()
        
        new = Protein()
        
        for resnum in self.get_residues():
            residue = self.get_residue_data(resnum)

            # amber/lipid11 
            if resmap is not None:
                # Need to subtract 1 from resnum since we start
                # with 0-indexing in python, but most likely not
                # in the pdb-file
                resname = resmap[resnum-1]
            else:
                resname = residue[0][1]

            out = self.sort_residue(residue,ff,resname)
            new.add_residue_data(out)

        return new
        
    def sort_residue(self,residue,ff,resname=None):

        # Get the name of the residue to be sorted
        if resname:
            resn = resname
        else:
            resn = residue[0][1]
            
        sort_data = self.sorts[ff,resn]['atoms']
        out = [0]*len(sort_data)
        
        if ff == 'lipid11':

            for i,(ai_atname,ai_resname) in enumerate(sort_data):
                
                found = 0
                for j in range(len(residue)):
                    aj_atname = residue[j][0]
                    aj_resname = residue[j][1]
                    
                    if ( (ai_atname == aj_atname) and
                         (ai_resname == aj_resname) ):
                                
                        found = 1
                        out[i]=(aj_atname,
                                aj_resname,
                                residue[j][2],
                                residue[j][3])
                        
                        #sorted[j]=1
                        # Some lipids in lipid11 have two identical tails
                        # (eg. DPPC) we cannot simply compare two lists
                        # with each other. We therefore delete it from the 
                        # list so that it cannot be "found" again, and also
                        # then need to break out of the loop
                        residue.pop(j)
                        break
                
                if found == 0:
                    print "Could not sort atom %s in residue %s"%(ai_atname,resn)
        else:
            for i,ai in enumerate(sort_data):
                ai = sort_data[i][0]
            
                for j in range(len(residue)):
                    aj = residue[j][0]
                
                    if ai == aj:
                    #print ai,aj
                        out[i]=(aj,
                                residue[j][1],
                                residue[j][2],
                                residue[j][3])
        #print out
        
        #sys.exit()
        return out
                
    def read_sortings(self):
        for ff in ff_sortings:
            fn = ""
            
            try:
                path = os.path.dirname(__file__)
                path = os.path.join(path,ff,'sortings.top')
                fn = open(path,'r')
            except:
                print "Could not open sortings file for %s"%ff

            atoms = []
            lipid = ""
            
            for line in fn:
                s = line.strip()
                
                if s.startswith("["):
                    d = re.findall(directive,s)[0].strip().lower()

                    # If we get to end of an entry, store it 
                    if d=='end':

                        # Create a new dict for this entry 
                        m = {}
                        m['atoms']=atoms
                        #print ff,lipid
                        self.sorts[ff,lipid]=m
                        # Reset atoms  
                        atoms = []
                        
                    continue
                if not s:
                    continue
                
                elif d == 'atoms':
                    atoms.append(s.split())

                elif d == 'molecule':
                    lipid = s.split()[0]


class Protein(Sort):
    def __init__(self,file_in=None,longresnum=False,debug=0):
        self.title=''
        self.atcounter = 0
        
        self.header = []
        self.footer = []
        
        self.label = []
        self.atnum = []
        self.elem = []
        self.mass = []
        self.atname = []
        self.atalt = []
        self.resname = []
        self.chain = []
        self.resnum = []
        self.resext = []
        self.coord = []
        self.occ = []
        self.b = []
        self.sequence = {}
        self.box = []
        self.velocity = []
        
        self.debug = debug
        
        # Read in the file based on its extension
        if file_in:
            filetype = os.path.splitext(file_in)[1]
            
            gro = re.compile('.gro')
            pdb = re.compile('.pdb')
            
            if gro.match(filetype):
                self.read_gro(file_in)
            elif pdb.match(filetype):
                self.read_pdb(file_in,longresnum)
            else:
                print "Unknown file-type"
                sys.exit()
                
        # We also need to inititate the Sort base class here
        # This is a bit weird, but I'm a noob at oop anyway :-)
        Sort.__init__(self)

    def read_pdb(self,file_in,longresnum,debug=0):
        lines = file(file_in).readlines()
        self.read_pdb_lines(lines,longresnum,debug)
        
    def read_pdb_lines(self,lines,longresnum,debug):
        atom_hetatm = re.compile('(ATOM  |HETATM)')
      
        for line in lines:
            if atom_hetatm.match(line):
                
                line = line[:-1]
                # We throw away a bunch of stuff in the input
                # pdb file here... this could be changed of course
                if ( line[12:16].strip() not in Vsites  and
                     (line[17:21].strip() in is_lipid)):
                    self.atname.append(line[12:16].strip())
                    self.resname.append(line[17:21].strip())
                    if longresnum:
                        self.resnum.append(int(line[22:27]))
                    else:
                        self.resnum.append(int(line[22:26]))
                    self.coord.append((float(line[30:38])/10, float(line[38:46])/10, float(line[46:54])/10))
                    
                    self.atcounter += 1
                
        if debug:
            return len(self.atnum),self.atcounter
                            
    def read_gro(self,file_in,debug=0):
        lines = file(file_in).readlines()
        self.read_gro_lines(lines,debug)
        
    def read_gro_lines(self,lines,debug):
        self.title = lines[0][:-1]
        # We first set atcounter to whatever it is in the input file
        self.atcounter = int(lines[1][:-1])

        if self.debug:
            print self.title
            print self.atcounter
            print lines[2][:-1],len(lines[2])
 
        ctr = 0
        # and use that value to read in all atoms
        for line in lines[2:self.atcounter+3][:-1]:
            if (line[10:15].strip() not in Vsites and
                (line[5:10].strip() in is_lipid)):
                self.resnum.append(int(line[0:5]))
                self.resname.append(line[5:10].strip())
                self.atname.append(line[10:15].strip())
                self.atnum.append(int(line[15:20]))
                
                first_decimal = line.index('.')
                second_decimal = line[first_decimal+1:].index('.')
                #print first_decimal
                #print second_decimal
                incr = second_decimal + 1
                #print incr
                #print line[20:20+incr]
                #print line[28:20+2*incr]
                self.coord.append((float(line[20:20+incr]), float(line[28:20+2*incr]), float(line[36:20+3*incr])))
                
                ctr = ctr + 1

        self.atcounter = ctr

    def get_residues(self):
        res = np.unique(self.resnum)
        return res

    def get_resnames(self):
        resnames = []
        for resnum in self.get_residues():
            resnames.append(self.resname[resnum])
            
        return resnames

    # For lipid11, we need a routine that makes sense of the PA/PC/OL
    # nomenclature, and translates into a single residue name
    # translation table in lipid11_residues
    def get_canonical_residue_name(self,residue):
        resnames = []
        
        for i  in range(len(residue)):
            resn = residue[i][1]
            resnames.append(resn)

        # By converting to a set we can compare two lists
        # as long as we don't care about order (which we don't here)
        unique_resnames = set(resnames)
        #unique_resnames = list(unique_resnames)
        
        resn_out = ""

        for r in lipid11_residues:
            l11_res = set(lipid11_residues[r])
            
            if l11_res == unique_resnames:
                resn_out = r
         
        #print len(resn_out)
        #print resn_out
        #sys.exit()
        if len(resn_out)>0:
            return resn_out
        else:
            print "Could not find a canonical residue name for the"
            print "[%s] combination of residue names in lipid11"%', '.join(map(str, list(unique_resnames)))
            sys.exit()
    
    def get_residue_data(self,resi):
        out = []
        
        for i in range(self.atcounter):
            if self.resnum[i]==resi:
                
                out.append((#self.atnum[i],
                            self.atname[i],
                            #self.atalt[i],
                            self.resname[i],
                            #self.chain[i],
                            self.resnum[i],
                            #self.resext[i],
                            self.coord[i]))
                            #self.occ[i],
                            #self.b[i]))
                
        return out
                
    def add_residue_data(self,residue):
        
        for i in range(len(residue)):
            #print residue[i]
            #if residue[i] == 0
            atname = residue[i][0]
            resname = residue[i][1]
            resnum = residue[i][2]
            coords = residue[i][3]

            self.resnum.append(resnum)
            self.resname.append(resname)
            self.atname.append(atname)
            self.coord.append(coords)

            self.atcounter = self.atcounter + 1
            
    def write_pdb(self,file_out):
        f = open(file_out,'w')

        for i in range(self.atcounter):
            atnum = i % 99999
            self.write_pdb_line(f,i,atnum)

        f.close()

    def write_pdb_line(self,file_out,i,atnum):
        label = 'ATOM  '
        atalt = ' '
        chain = ' '
        resext = ' '
        occ = 1.0
        b = 0.0
        elem = ''
        blank = ''

        # This isn't the strict pdb format string, but it lets us
        # write pdb-files that have 4-letter long reside codes
        # and 5-numbered residue numbers
        file_out.write('%-6s%5d %4s%1s%-4s %4d    %8.3f%8.3f%8.3f%6.2f%6.2f          %2s%2s\n'%(label,atnum+1,self.atname[i],atalt,self.resname[i],self.resnum[i],self.coord[i][0]*10.,self.coord[i][1]*10.,self.coord[i][2]*10.,occ,b,blank,elem)) 
        
    def write_gro(self,file_out):
        f = open(file_out,'w')
        
        f.write('lipid-converter gro-file\n')
        f.write('%d\n'%self.atcounter)

        for i in range(self.atcounter):
            atnum = i % 99999
            self.write_gro_line(f,i,atnum)

        f.write('%10.5f%10.5f%10.5f'%(0,0,0))
        f.close()

    def write_gro_line(self,file_out,i,atnum):
        file_out.write("%5d%-5s%5s%5d%8.3f%8.3f%8.3f\n"%(self.resnum[i]%1e5,self.resname[i],self.atname[i],atnum+1,self.coord[i][0],self.coord[i][1],self.coord[i][2]))

    def write(self,filename):
        filetype = os.path.splitext(filename)[1]
        
        gro = re.compile('.gro')
        pdb = re.compile('.pdb')
        
        if gro.match(filetype):
            self.write_gro(filename)
        elif pdb.match(filetype):
            self.write_pdb(filename)
        else:
            print "Unknown filetype in write"
            sys.exit()


