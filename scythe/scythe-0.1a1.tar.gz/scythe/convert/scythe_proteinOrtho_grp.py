class ProteinOrthoParser(object):
    def readInfo(self, po):
        po = open(po, 'r')
        res = ""
        for l in po:
            if l.startswith("#"):
                res+=l
        po.close()
        return(res)

    def readGroups(self, po, speciesNames = None):
        """Iterate over proteinOrtho output and return numbered list with orthogroups."""
        po = open(po, 'r')
        cnt = 0
        #if columnNames aren't provided, use first line as names
        l = po.readline()
        if not speciesNames:
            sn = l.strip().split("\t")[3:]
            #print(sn)
        else:
            if len(speciesNames) == len(l.strip().split("\t")[3:]):
                sn = speciesNames
            else:
                raise ScytheError("Number of speciesNames must equal the number of species in the file.")
        for l in po:
            if l.startswith("#"):
                pass
            else:
                tmp_list=l.strip().split("\t")[3:]
                tmp_list = [l.split(",") for l in tmp_list]
                tmp_list = [val for tmp in tmp_list for val in tmp]
                yield cnt, tmp_list, sn
                cnt +=1
        po.close()

    def groupDct(self, po, speciesNames = None):
        res = {}
        for gr,ids,spec in self.readGroups(po, speciesNames):
            res[gr] = ids
        return(res)

    def findOrthologs(self, po, geneID):
        #return geneID's friends
        res = []
        for a in self.readGroups(po):
            if geneID in a[1]:
                res.append(a)
        return(res)
