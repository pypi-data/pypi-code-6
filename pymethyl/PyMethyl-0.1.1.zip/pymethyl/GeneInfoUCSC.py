##Author: Cody Watson
##BCRL Dr. Jose Russo, Dr. Julia Pereira
##Program to find Chromosome and Location of all Genes
##so long as you have the Gene name.




##Packages needed to be imported
import re
from cruzdb import *


    
##Program that pulls information from genes
def infoGather(geneName, database):
    ##Database you are pulling information from
    g = Genome(database)
    ##Built in function to fetch information about gene
    try:
        gene = g.refGene.filter_by(name2= geneName).first()
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
        start = glist[1]
        end = glist[2]
        name = glist[3]
        return name + "\t" + chromosome_number + "\t" + start + "\t" + end
    except:
        print("Could Not Find " + geneName)
        
