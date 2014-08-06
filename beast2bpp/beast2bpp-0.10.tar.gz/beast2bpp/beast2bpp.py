noloci = 0
nospecies = 0
noseqs = []
speciesNames = []
maxIndivs = []
maxNoSeqs = 0
indivIndexMap = {}
speciesTree = ''


def scan(name1):
    from xml.sax.handler import ContentHandler
    from xml.sax import parse
    global speciesTree
    
    beast_xml_file = name1
    f = open("bpp.txt",'w')
    m = open("bpp.Imap.txt",'w')
    c = open("bpp.ctl",'w')


    class noseqHandler(ContentHandler):
        locusIndex = -1
        currIndex = 0
    
        def __init__(self):
            ContentHandler.__init__(self)
            self.data = []
            self.firstcall = 0
            self.title=""
    
        def startElement(self,name,attrs):
            global noseqs
            self.data = name
            if name == "data":
                noseqs.append(0)
                self.firstcall=0
                self.locusIndex = self.locusIndex + 1
            elif name == "sequence":
                noseqs[self.locusIndex] = noseqs[self.locusIndex] + 1

    class dataHandler(ContentHandler):
        in_sequence = False
        nameIndex = 1
        currIndex = 0
        locusIndex = -1


        def __init__(self,sequence):
            ContentHandler.__init__(self)
            self.sequence = sequence
            self.data = []
            self.firstcall = 0
            self.title=""
       
        def startElement(self,name,attrs):
            global noloci
            global noseqs
            global maxNoSeqs
            global indivIndexMap
            self.data = name
            if name == "data":
                self.locusIndex = self.locusIndex + 1
                noloci+=1
                f.write('\n')
                f.write("  ")
                f.write(str(noseqs[self.locusIndex]))
                if int(noseqs[self.locusIndex]) > maxNoSeqs:
                    maxNoSeqs=int(noseqs[self.locusIndex])
                self.firstcall=0
            elif name == "sequence":
                self.title = attrs["taxon"]
                if self.title in indivIndexMap:
                    self.currIndex = indivIndexMap[self.title]
                else:
                    indivIndexMap[self.title] = self.nameIndex
                    self.currIndex = indivIndexMap[self.title]
                    self.nameIndex = self.nameIndex + 1
                self.in_sequence = True



        def endElement(self, name):
            if name == "sequence":
                astring=self.data
                a2=astring.strip()
                if self.firstcall==0:
                    a3=len(a2)
                    f.write("  ")
                    f.write(str(a3))
                    f.write('\n\n')
                    self.firstcall=1
                f.write(self.title)
                f.write("^")
                f.write(str(self.currIndex))
                f.write('\n')
                f.write(a2)
                f.write('\n')
                self.data = []

        def characters(self,string):
            if self.in_sequence:
                self.data=string
            
    class BeastHandler(ContentHandler):
        in_taxonsuperset = False
        currSpecies=''
        
        def startElement(self,name,attrs):
            global nospecies
            global speciesNames
            if name == 'taxonset':
                if attrs["id"] == 'taxonsuperset':
                    self.in_taxonsuperset = True
            if name == 'taxon':
                if self.in_taxonsuperset:
                    if attrs["spec"] == 'TaxonSet':
                        self.currSpecies=attrs["id"]
                        nospecies = nospecies + 1
                        maxIndivs.append(0)
                        speciesNames.append(self.currSpecies)
                    elif attrs["spec"] == 'Taxon':
                        m.write(str(indivIndexMap[attrs["id"]]))
                        m.write("\t")
                        m.write(self.currSpecies)
                        m.write("\n")
                        maxIndivs[nospecies-1] = maxIndivs[nospecies-1] + 1
    
        def endElement(self, name):
            if name == 'taxonset':
                self.in_taxonsuperset = False
    
    class treeHandler(ContentHandler):
    
        def startElement(self,name,attrs):
            if name =='tree':
                try:
                    if attrs["id"] == 'newickSpeciesTree':
                        speciesTree = attrs["newick"]
                except:
                    pass
    
    sequence = []
    species = []
    
    
    parse(beast_xml_file,noseqHandler())
    parse(beast_xml_file,dataHandler(sequence))
    parse(beast_xml_file,BeastHandler())
    c.write("    seed = -1\n")
    c.write("    seqfile = bpp.txt\n")
    c.write("    Imapfile = bpp.map.txt\n")
    c.write("    outfile = out.txt\n")
    c.write("    mcmcfile = mcmc.txt\n")
    c.write("    speciesdelimitation = 0 * fixed species tree\n")
    c.write("    speciestree = 1 * species-tree by NNI\n")
    c.write("    speciesmodelprior = 1         * 0: uniform labeled histories; 1:uniform rooted trees; 2:user probs\n")
    c.write("    species&tree = ")
    c.write(str(nospecies))
    c.write(" ")
    for word in speciesNames:
        c.write(" ")
        c.write(word)
    c.write(" \n")
    c.write("    ")
    for number in maxIndivs:
        c.write(" ")
        c.write(str(number))
    c.write(" \n")
    c.write("    ")
    parse(beast_xml_file,treeHandler())
    
    trList=[]
    myList=[]
    inNumber=False
    myList=list(speciesTree)
    for i in range(len(speciesTree)):
        if myList[i] == ':':
            inNumber = True
        elif inNumber == False:
            trList.append(myList[i])
        else:
            if myList[i] == ',':
                inNumber = False
                trList.append(myList[i])
            if myList[i] == ')':
                inNumber = False
                trList.append(myList[i])
    speciesTree = "".join(trList)
    c.write(speciesTree)
    c.write("\n")
    c.write("    usedata = 1    * 0: no data (prior); 1:seq like\n")
    c.write("    nloci = ")
    c.write(str(noloci))
    c.write("    * number of data sets in seqfile\n")
    c.write("    cleandata = 0    * remove sites with ambiguity data (1:yes, 0:no)?\n")
    c.write("\n")
    c.write("    thetaprior = 2 2000    # gamma(a, b) for theta\n")
    c.write("    tauprior = 2 2000 1  # gamma(a, b) for root tau & Dirichlet(a) for other tau's\n")
    c.write("    finetune = 1: .01 .01 .01 .01 .01 .01 .01 .01  # auto (0 or 1): finetune for GBtj, GBspr, theta, tau, mix, locusrate, seqerr\n")
    c.write("\n")
    c.write("    print = 1 0 0 0   * MCMC samples, locusrate, heredityscalars Genetrees\n")
    c.write("    burnin = 4000\n")
    c.write("    sampfreq = 2\n")
    c.write("    nsample = 10000\n")
    print("Beast2BPP file conversion script. Bruce Rannala, UC Davis <brannala@ucdavis.edu>")
    print("File",beast_xml_file, "with", noloci, "loci and a maximum of",maxNoSeqs,"sequences per locus was successfully converted to BPP format.")
    print("BPP files are named bpp.ctl, bpp.txt and bpp.Imap.txt")
    f.close()
    m.close()
    c.close()
    
