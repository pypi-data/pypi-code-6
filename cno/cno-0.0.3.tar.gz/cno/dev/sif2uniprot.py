# -*- python -*-
#
#  This file is part of cellnopt software
#
#  Copyright (c) 2011-2012 - EBI-EMBL
#
#  File author(s): Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: http://www.cellnopt.org
#
##############################################################################
#import cellnopt.core.sif
#from cellnopt.core.sif import readSIF
from bioservices import UniProt
from easydev import console, logging_tools
from cellnopt.data import cnodata
from cellnopt.core import *
# TODO if il1r returns il1rA but it could be il1r1 and il1r2 need to check both
# letter/numbers at the same time actually


# The SIF file in cellnopt format
#sif_example1 = cnodata("PKN-ExtLiverPCB.sif")
#sif_example2 = cnodata("PKN-ToyMMB.sif")

#test on BMC2012 data set
# some species are hardcoded such as lipids (pip3, lps) or not found in uniprot
# (p38). except pi3k and ck2 all others are more or less correct. 
# _D means found in the description
# ? means not found. kept as it is
# small caps means not in uniprot or lipids
# _n means original name had a n at the end of its name
# >akt< means compressed version of AKT1/AKT2/AKT3


# ERK does not work so far because there is an entry ith gen name == ERK so all
# ERK1, ERK2, ERK3 are not found.


class SIF2UniProt(object):
    """

        # takes a while to load
        u = SIF2UniProt("validSIFfile", reviewed_only=True)
        #u.buffer_all_entries()
        u.species = ["akt"]
        u.mapping()
        u.write("newUP.sif")

        for later, you can save s.all_entries into a file and load it back::

        all_entries = u.all_entries.copy()

        u = SIF2UniProt("validSIF", all_entries=all_entries.copy())


    """
    def __init__(self, filename=None, all_entries=None, reviewed_only=False):
        # for human taxonomy only !!
        self.u = UniProt(verbose=False)
        self.limit = 6  # number of rows to keep from uniprot . 6 at least is require for instance to get correct EGFR !!
        self.filename = filename
        if filename:
            self.load_sif_model(filename)
        self.taxonomy = "9606"
        self._columns = "entry name, taxonomy, id, genes, protein names"

        self.logging = logging_tools.Logging("INFO")
        # need to retrieve all uniprot entries, or 
        if all_entries == None:
            self.buffer_all_entries(reviewed_only=reviewed_only)
        else:
            self.all_entries = all_entries

    def load_sif_model(self, filename):
        # use cellnopt.wrapper but we cold use someting less heavy such as
        # cellnopt.core ?
        self.model = SIF(cnodata(filename))
        self.species = sorted(self.model.namesSpecies)

    def buffer_all_entries(self, reviewed_only=False):
        """Reads all entries once for all

        :param bool reviewed_only: retrieve reviewed entries only.

        """
        self.logging.info("Reading all uniprot entries once for all. Takes a minute or two depending on your connection")
        all_entries = {}
        query = "taxonomy:9606" 

        if reviewed_only:
            query+="+and+reviewed:yes"
        res = self.u.search(query, format="tab", columns=self._columns)
        res = res.split("\n")[1:-1]  # skip header and last empty entry
        for x in res:
            entry_name, entry, gene, des = x.split("\t")
            all_entries[entry_name] = {
                'Gene names': gene,
                'Description': des,
                'Entry':entry}
        self.all_entries = all_entries.copy()

    def search_in_description(self, specy):
        """Search for a specy name into all description"""
        candidates = []
        for k in self.all_entries.keys():
            if specy.lower() in self.all_entries[k]['Description'].lower():
                candidates.append(k)
        return candidates

    def levenshtein_entry_name(self, specy, distance=0, startswith=True, verbose=True):
        """Search for entry name using a levenshtein algorithm

        """
        import Levenshtein
        if self.taxonomy != "9606":
            raise NotImplementedError

        specytax = specy.lower() +"_"+ "human"

        candidates = []
        for this in range(0, distance+1):
            res = [(x,Levenshtein.distance(x.lower(),specytax)) for x in self.all_entries.keys() \
                if Levenshtein.distance(x.lower(),specytax)==this]
            if verbose:print("Entry name: found %s candidates with distance %s" % (len(res),this))
            if len(res) == 1 and this == 0:
                return [res[0][0]]

            for x in res:
                if startswith==False:
                    candidates.append(x[0])
                    if verbose:print("Found ", x[0], specy.upper())
                elif x[0].startswith(specy.upper()):
                    if verbose:print("Found ", x[0], specy.upper())
                    candidates.append(x[0])
        return candidates

    def levenshtein_gene_names(self, specy, distance=0, startswith=True, verbose=True):
        """Search for entry name using a levenshtein algorithm"""
        import Levenshtein
        if self.taxonomy != "9606":
            raise NotImplementedError

        candidates = []
        for this in range(0, distance+1):
            for k, v in self.all_entries.iteritems():
                genenames = v['Gene names']
                for name in genenames.split(" "):
                    if self.levenshtein(specy, name) == this :
                        if len(candidates)==0: print("")
                        print("    Gene names: found %s name with distance %s (Entry name=%s)" % (name,this,k))
                        candidates.append(k)
        res  = list(set(candidates))
        candidates = []
        for x in res:
            candidates.append(x)
        return candidates

    def levenshtein(self, a, b, mode=0):
        import Levenshtein
        distance = Levenshtein.distance(a.lower(), b.lower())
        return distance


    def mapping(self, merge=False):
        """search for all species in the entries"""
        mapping = {}
        for specy in self.species:
            res = self.mapping_individual(specy, merge=merge)
            mapping[specy] = res[specy]
        self.mapping_data = mapping.copy()
        return mapping


    def mapping_individual(self, species, merge=False):
        """search for one specy in the entries"""
        mapping = {}

        # special case to not look at
        if species.startswith("and"):
            mapping[species] = species
            return mapping

        # some tricky cases. e.g., IRS1S returns IRS1
        # p38 not found, a20 returns far too many candidates
        if species.lower() == "histh3":
            mapping[species] = "H31T/H33"
            return mapping
        if species.lower() == "p38":
            mapping[species] = "p38"
            return mapping
        if species.lower() == "p38n":
            mapping[species] = "p38_n"
            return mapping
        if species.lower() == "a20":
            mapping[species] = "TNAP3"
            return mapping
        if species.lower() == "irs1s":
            mapping[species] = "IRS1_s"
            return mapping
        if species.lower() == "irs1t":
            mapping[species] = "IRS1_y"
            return mapping
        if species.lower() in ["pip2", "pip3", "lps"]:
            # lipid cases
            mapping[species] = species.lower()
            return mapping


        # The for loop can be removed ?
        for specy in [species]:
            # a perfect match .ma
            print "\n--------- >>>>>>>>>>> Parsing specy ", specy
            res = self.levenshtein_entry_name(specy, 0, verbose=False)
            print(console.bold(" Searching for perfect match with entry name")),
            if len(res):
                assert len(res)==1
                print(console.blue("Found it"))
                mapping[specy] = res[0].split("_")[0]
                print "--------- <<<<<<<<<<< proposal", mapping[specy]
                continue
            print("not found.")
            #print(console.red("...not found"))

            #erk12n
            if specy[-1] == "n" and specy[-3].isdigit() and specy[-2].isdigit():
                print(console.bold(" Searching for perfect match with entry name (splitting last two digits and removing trailing n character)")),
                name = specy[:-3]
                res1 = self.levenshtein_entry_name(name + specy[-3], 0, verbose=False, startswith=False)
                res2 = self.levenshtein_entry_name(name + specy[-2], 0, verbose=False, startswith=False)
                if len(res1):
                    res = res1[:]
                    res.extend(res2)
                elif len(res2):
                    res = res2[:]
                else:
                    print("not found")
                    res = []
                if len(res):
                    mapping[specy] = "/".join([x.split("_")[0] + "_n" for x in sorted(res)])
                    print "--------- <<<<<<<<<<< proposal", mapping[specy]
                    continue

            # STAT3n
            if specy[-1] == "n" and specy[-2].isdigit():
                print(console.bold(" Searching for perfect match with entry name (splitting last digit and removing trailing n character)")),
                name = specy[:-2]
                res = self.levenshtein_entry_name(name + specy[-2], 0, verbose=False, startswith=False)
                if len(res):
                    mapping[specy] = "/".join([x.split("_")[0] + "_n" for x in sorted(res)])
                    print "\n--------- <<<<<<<<<<< proposal", mapping[specy]
                    continue
                else:
                    print("not found")


            # 
            if specy[-1].isdigit() and specy[-2].isdigit():
                if int(specy[-1]) <=3 and int(specy[-2])<=3:
                    
                    print(console.bold(" Searching for perfect match with entry name (splitting last two digits, LvD=0)")),
                    name = specy[:-2]
                    res1 = self.levenshtein_entry_name(name + specy[-2], 0, verbose=False, startswith=False)
                    res2 = self.levenshtein_entry_name(name + specy[-1], 0, verbose=False, startswith=False)
                    if len(res1):
                        res = res1[:]
                        res.extend(res2)
                    elif len(res2):
                        res = res2[:]
                    else:
                        print("not found")
                        res = []
                    if len(res):
                        mapping[specy] = "/".join([x.split("_")[0] for x in sorted(res)])
                        print "\n--------- <<<<<<<<<<< proposal", mapping[specy]
                        continue

            #mek12nm jnk12
            if specy[-1] == "n" and specy[-3].isdigit() and specy[-2].isdigit():
                print(console.bold(" Searching for perfect match with gene names (splitting last two digits and removing trailing n character)")),
                name = specy[:-3]
                res1 = self.levenshtein_gene_names(name + specy[-3], 0, verbose=False, startswith=False)
                res2 = self.levenshtein_gene_names(name + specy[-2], 0, verbose=False, startswith=False)
                if len(res1):
                    res = res1[:]
                    res.extend(res2)
                elif len(res2):
                    res = res2[:]
                else:
                    print("not found")
                    res = []
                if len(res):
                    mapping[specy] = "/".join([x.split("_")[0] + "_n" for x in sorted(res)])
                    print "--------- <<<<<<<<<<< proposal", mapping[specy]
                    continue



            #jnk12, mek12
            if specy[-1].isdigit() and specy[-2].isdigit():
                if int(specy[-1]) <=3 and int(specy[-1])<=3:
                    print(console.bold(" Searching for perfect match with gene name (splitting last two digits, LvD=0")),
                    name = specy[:-2]
                    res1 = self.levenshtein_gene_names(name + specy[-2], 0, verbose=False, startswith=False)
                    res2 = self.levenshtein_gene_names(name + specy[-1], 0, verbose=False, startswith=False)
                    if len(res1):
                        res = res1[:]
                        res.extend(res2)
                    elif len(res2):
                        res = res2[:]
                    else:
                        print("not found")
                        res = []
                    if len(res):
                        mapping[specy] = "/".join([x.split("_")[0] for x in sorted(res)])
                        print "\n--------- <<<<<<<<<<< proposal", mapping[specy]
                        continue
                    else:
                        print("not found")


            # akt
            print(console.bold(" Searching for close match with entry name (adding letter, Lvd=0)")),
            # this if is alwasy true ?
            if specy not in mapping.keys():
                res = [self.levenshtein_entry_name(specy+value, 0, verbose=False) for value in [chr(x) for x in range(65,91)]]
                res = [x for x in res if len(x)] # remove empty lists
                res = [item for sublist in res for item in sublist] # flatten the list
                res = [x.split("_")[0] for x in res] #remove taxid suffix
                if len(res):
                    print(console.blue("Found several candidates with very similar entry name (letter case)"))
                    if len(res)>1:
                        if merge == False:
                            mapping[specy] = "/".join([x for x in sorted(res)])
                        else:
                            mapping[specy] = ">" + res[0][:-1].lower() + "<"
                    else:
                        assert len(res)==1
                        mapping[specy] = res[0]
                    print "--------- <<<<<<<<<<< proposal", mapping[specy]
                    #continue # do no return yet because there may be also candidates with numbers
                else:
                    print("not found")
                #    print(console.red("...not found"))

            print(console.bold(" Searching for close match with entry name (adding number, Lvd=0)")),
            #if specy not in mapping.keys():
            if 1==1: # if above seems always true
                res = [self.levenshtein_entry_name(specy+value, 0, verbose=False) for value in [str(x) for x in range(1,10)]]
                res = [x for x in res if len(x)] # remove empty lists
                res = [item for sublist in res for item in sublist] # flatten the list
                res = [x.split("_")[0] for x in res] #remove taxid suffix
                if len(res):
                    print(console.blue("Found several candidates with very similar entry name (number case)"))
                    if len(res)>1:
                        if merge == False:
                            if specy in mapping.keys():
                                mapping[specy] += "/" + "/".join([x for x in sorted(res)])
                            else:
                                mapping[specy] = "/".join([x for x in sorted(res)])
                        else:
                            # if there are alraeay sometinh in mapping[specy] we
                            # can just overwrite it since we merge names
                            mapping[specy] = ">" + res[0][:-1].lower() + "<"
                    else:
                        assert len(res)==1
                        if specy in mapping.keys():
                            mapping[specy] += "/" + res[0]
                        else:
                            mapping[specy] = res[0]
                    print("/".join([x.split("_")[0] for x in sorted(res)]))
                    print "--------- <<<<<<<<<<< proposal", mapping[specy]
                    continue
                else:
                    print("not found")
             
            if specy in mapping.keys():
                print "--------- <<<<<<<<<<< proposal", mapping[specy]
                continue
                #    print(console.red("...not found"))

            # if not yet found, look into entry name again with distance 1 and




            # if not yet found, look into gene names with distance 0
            print(console.bold(" Searching for perfect match with gene names")),
            res = self.levenshtein_gene_names(specy, 0, verbose=False)
            if len(res):
                res = [x.split("_")[0] for x in res] # remove trailing taxid
                print(console.yellow("Found %s candidates with same Gene name" % len(res)))
                if len(res)>1:
                    print(console.yellow(" Select only names close to the specy (LvD<=4)")),
                    print res
                    res2 = [x for x in res if self.levenshtein(x.lower(), specy.lower())<=4]
                    if len(res2) != 0:
                        res = res2

                if specy not in mapping.keys():
                    mapping[specy] = "/".join([x for x in res])
                    print "--------- <<<<<<<<<<< proposal", mapping[specy]
                    continue
                else:
                    for r in res:
                        mapping[specy] += "/" +  r
                        print "--------- <<<<<<<<<<< proposal", mapping[specy]
                        continue
            else:
                print("not found")

            print(console.bold(" Searching for close match with gene names (adding number, Lvd=0)")),
            if specy not in mapping.keys():
                res = [self.levenshtein_gene_names(specy+value, 0, verbose=False) for value in [str(x) for x in range(1,10)]]
                res = [x for x in res if len(x)] # remove empty lists
                res = [item for sublist in res for item in sublist] # flatten the list
                res = [x.split("_")[0] for x in res] #remove taxid suffix
                res2 = [x for x in res if self.levenshtein(x.lower(), specy.lower())<=3]
                if len(res2) != 0:
                    res = res2
                if len(res):
                    print(console.blue("Found %s candidates with very similar gene name (number case)" % len(res)))
                    if len(res)>1:
                        if merge == False:
                            mapping[specy] = "/".join([x for x in sorted(res)])
                        else:
                            mapping[specy] = ">" + res[0][:-1].lower() + "<"
                    else:
                        assert len(res)==1
                        mapping[specy] = res[0]
                    print("/".join([x for x in sorted(res)]))
                    print "--------- <<<<<<<<<<< proposal", mapping[specy]
                    continue
                else:
                    print("not found")

            print(console.bold(" Searching for close match with entry name (LvD=1)")),
            if specy not in mapping.keys():
                res = self.levenshtein_entry_name(specy, 1, verbose=False, startswith=True)
                if len(res):
                    print(console.blue("Found several candidates with very similar entry name"))
                    if len(res)>1:
                        mapping[specy] = "/".join([x.split("_")[0] for x in sorted(res)])
                    else:
                        assert len(res)==1
                        mapping[specy] = res[0].split("_")[0]
                        print "--------- <<<<<<<<<<< proposal", mapping[specy]
                        continue
                else:
                    print("not found")

            # Use description
            if specy not in mapping.keys():
                print(console.bold(" Searching in the description")),
                res = self.search_in_description(specy)
                if len(res) == 1:
                    print(console.blue("Found 1 candidate"))
                    mapping[specy] = res[0].split("_")[0] + '_D'
                    print "--------- <<<<<<<<<<< proposal", mapping[specy]
                    continue
                elif len(res)>1:
                    similar = True
                    res1 = res[0].split("_")[0]
                    print res
                    for res2 in res:
                        print res1, res2, res2.split("_")[0]
                        if self.levenshtein(res1, res2.split("_")[0]) >2:
                            similar = False
                    if similar == True:
                        mapping[specy] = "/".join([x.split("_")[0] for x in sorted(res)])
                        print(console.blue("Found %s similar candidates" %len(res)))
                        print "--------- <<<<<<<<<<< proposal", mapping[specy]
                        continue
                    # if they all starts with same tag, it is probably correct

                    else:
                        print("not found")
                else:
                        print("not found")

            # if not yet found, look into entry name again with distance 1 and
            # force the candidates to start with the specy name
            print(console.bold(" Searching for close match with entry name (LvD=1, starting like specy name)")),
            if specy not in mapping.keys():
                res = self.levenshtein_entry_name(specy, 1, verbose=False, startswith=False)
                if len(res):
                    print(console.blue("Found %s candidates with very similar entry name" % len(res)))
                    if len(res)>10:
                        print("too many candidates. suspicious. skipped")
                    elif len(res)>1:
                        print res
                        mapping[specy] = "/".join([x.split("_")[0] for x in sorted(res)]) + "*"
                        print "--------- <<<<<<<<<<< proposal", mapping[specy]
                        continue
                    else:
                        assert len(res)==1
                        mapping[specy] = res[0].split("_")[0]
                        print "--------- <<<<<<<<<<< proposal", mapping[specy]
                        continue
                else:
                    print("not found")
            print("")


            if len(res)!=0:
                print("not found")
                # now let us be more flexible and search for candidates that do not
                # start with specy name and look into entry name and gene names
                res1 = set(self.levenshtein_entry_name(specy,2, startswith=False))
                res2 = set(self.levenshtein_gene_names(specy,1, startswith=False))
                res = res1.intersection(res2)
                if len(res2) == 1:
                    mapping[specy] = res2[0] + "**"
                elif len(res)>1:
                    print res

            if specy not in mapping.keys():
                print(console.red("not Found"))
                mapping[specy] = "?" + specy
            print "--------- <<<<<<<<<<< proposal", mapping[specy]
        return mapping


    def search(self, specy, format="tab"):
        """Search for a specy in uniprot

        :param str specy: specy to search for

        You can change the following attriburs: limit, _columns

        """
        query = "%s+and+taxonomy:9606" % specy
        res = self.u.search(query, format=format, limit=self.limit,
            columns=self._columns)
        return res

    def getCandidates(self, res):
        """Transforms the uniprot tab output into dictionaries

        :param res: output of a uniprot search in tab format
        :return: list of dictionaries. Each dictionary contains keys found in
            the header of the input res

        >>> res = u.search("akt")
        >>> u.getCandidates(res)[0]
        {'Entry': 'Q96B36',
         'Entry name': 'AKTS1_HUMAN',
         'Gene names': 'AKT1S1 PRAS40',
         'Protein names': 'Proline-rich AKT1 substrate 1 (40 kDa proline-rich AKT substrate)'}

        .. warning:: obsolet
        """
        res = res.strip()
        candidates = []

        headers = res.split("\n")[0].split("\t")
        assert "Entry" in headers
        indexEntries = headers.index("Entry")
        entries = [x.split("\t")[indexEntries] for x in res.split("\n")][1:]

        for j, entry in enumerate(entries):
            candidate = {}
            for i, header in enumerate(headers):
                candidate[header] = [x.split("\t")[i] for x in res.split("\n")][1:][j]
            candidates.append(candidate)
        return candidates

    def select(self, name, data, mode=None, org="HUMAN"):
        """

        :param data: output of getCandidate
        :param name: name of the psecy
        :param mode: internal usage. Set to None
        :return: a single candidate dictionary or a list of candidate
            dictionaries

        .. warning:: obsolet
        """
        candidates = []
        if mode:
            name = name[:-len(mode)]

        print(name)

        # simple case: the name is correct and match the "Entry name". That's it we found the perfect
        # candidate
        print(" Checking the Entry name..."),
        for candidate in data:
            if name.lower() == candidate['Entry name'].replace("_"+org, "").lower():
                print(console.blue(" PERFECT Match. "))
                return candidate
        print(console.red("...not found"))



        # Now let try to find someting close in the Entry name by adding numbers
        # 1,2,3,...20 (20 should be good enough ?)
        # We need to search again and extract the candidates using the new 
        # appended name
        print(" Looking again at Entry name by adding integer"),
        for value in range(1,10):
            newguess = name.lower()+str(value)
            print("."),
            newdata = self.search(newguess)
            if newdata:
                newdata = self.getCandidates(newdata)
                for candidate in newdata:
                    if newguess.lower() == candidate['Entry name'].replace("_"+org,"").lower():
                        candidates.append(candidate)
        if len(candidates)>0:
            print(console.blue("Found candidates " % candidates))
            return candidates
        print(console.red("...not found"))

        print(" Looking again at Entry name by adding integer2 (old version)"),
        for candidate in data:
            values = range(1,10)
            for i in values:
                if name.lower()+str(i) == candidate['Entry name'].replace("_"+org, "").lower():
                    print(console.turquoise("found something wierd"))
                    candidates.append(candidate)

        # If we found someting, since accession Ids are unique, no need to check
        # for redundancie and we can return the results
        if len(candidates)>0:
            print(console.blue("Found candidates " % candidates))
            return candidates
        print(console.red("...not found"))



        # Same but with letter appended to the name
        print(" Looking again at Entry name by adding letter"),
        for value in [chr(x) for x in range(65,91)]:
            newguess = name.lower()+str(value)
            print("."),
            newdata = self.search(newguess)
            if newdata:
                newdata = self.getCandidates(newdata)
                for candidate in newdata:
                    if newguess.lower() == candidate['Entry name'].replace("_"+org, "").lower():
                        candidates.append(candidate)

        if len(candidates)>0:
            print(console.blue("Found %s candidates " % len(candidates)))
            return candidates
        print(console.red("...not found"))

        # If it fits perfectly a Gene names, we consider that it is correct as
        # well but several candidates may have the same gene name. Look for all
        # of them ?
        print(" Checking the Gene names"),
        for candidate in data:
            gene_names = [x.lower() for x in candidate['Gene names'].split()]
            if name.lower() in gene_names:
                candidates.append(candidate)
        if len(candidates)==1:
            print(console.blue("Found a perfect candidate" % candidates))
            return candidates
        elif len(candidates):
            print(console.blue("Found several ambiguous candidates (%s). Reset and try something else" % [(x['Entry name'], x['Gene names']) for x in candidates]))
            #candidates = []
        else:
            print(console.red("...not found"))
        print(" Looking again at Gene names by adding integer"),

        # let us look at the gene names
        #for candidate in data:
        #    names = [x.strip().lower() for x in candidate['Gene names'].split()]
        #    if name.lower() in names:
        #        print "case5 gene names "
        #        candidates.append(candidate)

        # let us look at the gene names adding numbers
        for candidate in data:
            names = [x.strip().lower() for x in candidate['Gene names'].split()]
            #if mode in ["12", "12n"]:
            #    values = [1,2]
            #elif mode == "13":
            #    values = [1,3]
            #else:
            #    values = range(1,20)
            for i in values:
                if name.lower()+str(i) in names:
                    candidates.append(candidate)
         
        candidates = self._removeRedudantCandidates(candidates)
        print(console.red("Found %s candidates so far" % len(candidates)))

        print(" Let us now look at the description (protein names)")
        # If we still have not found any candidate, let us dig up in the protein
        # names
        if len(candidates)==0:
            print(console.turquoise("Trying the description !!!"))
            for candidate in data:
                print  name.lower(), " in " , candidate['Protein names'].lower(), "?",
                if name.lower() in candidate['Protein names'].lower():
                    print(console.blue("yes"))
                    candidates.append(candidate)

        if len(candidates)>1:
            print(console.blue("    Several candidates were found (%s):" % len(candidates)))

            for x in  candidates:
                print "    ---", x['Entry name'], x['Gene names']
            return candidates
        return candidates

    def _removeRedudantCandidates(self, candidates):
        # cleanup redundancies of candidates
        new_candidates = []
        for c in candidates:
            if c not in new_candidates:
                new_candidates.append(c)
        candidates = new_candidates
        return candidates

    def run(self, *args, **kargs):
        """alias to mapping method"""
        res = self.mapping(args, kargs)
        return res

    def sif2uniprot(self):
        """does not handle AND"""
        sif = []
        for reaction in self.model.reacID:
            x,y = reaction.split("=")
            if "!" in x:
                link = -1
                x = x.replace("!", "")
            else:
                 link = 1
            data = [self.mapping_data[x], str(link), self.mapping_data[y]]
            print "\t".join([x for x in data])
            sif.append(data)

        return sif

    def write(self, filename):
        sif = self.sif2uniprot()
        f = open(filename, "w")
        for x in sif:
            f.write("\t".join(x) +"\n")
        f.close()



if __name__ == "__main__":
    u = SIF2UniProt(sif_example1)
    u.mapping()
    u.write("PKN-UP.sif")
