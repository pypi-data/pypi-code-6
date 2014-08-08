##Author Cody Watson
##
##BCRL Fox Chase: Dr. Jose Russo, Dr. Julia Pereira

##Program that grabs the promoter regions from UCSC Database
##Must have a file "InfoFile" that holds the gene names, chromosome,
##start position, and end position.

##Packages needed to import
from cruzdb import *
import re

##Main function that runs
def getPromoter(geneName, database):
    ##Database you search. Could change to 19 if needed.
    g = Genome(database)
    ##Grab the promoter regions which is 2000bp. If you want 1000
    ##You will have to change it.
    try:
        gene = g.refGene.filter_by(name2=geneName).first()
        genePromoter = gene.promoter()
        gene = str(gene)
        glist = gene.split()
        ##Try to search from chromosome number if error then it is on the X
        ##chromosome
        try:
            chromosome = re.search('(?<=chr)\d{1,}', glist[0])
            chromosome_number = chromosome.group()
        except:
            chromosome = re.search('(?<=chr)\D{1}', glist[0])
            chromosome_number = chromosome.group()
        promoter = str(genePromoter)
        start = re.search('(?<=[(])\d*', promoter)
        end = re.search('(?<=, )\d*', promoter)
        start = start.group()
        end = str(int(end.group())-1000)
        return geneName + "\t" + chromosome_number + "\t" + start + "\t" + end
    ##If error add gene to problem list
    except:
        print("Promoter not found for " + geneName)
                    
        
            
        
        
