##File that opens up the interface for the user

##Author: Cody Watson
##Must import all other files.

import blastingSequences
import GeneInfoUCSC
import getPromoterUCSC
import MakeDatabaseUCSC
import Methylation
import ResultInfoGather
import extractbamfile


def regionInfo():
    geneName = raw_input("What is the name of the gene you are interested in?: ")
    database = raw_input("What is the reference genome you are searching? \
Example: hg18 : ")
    region = raw_input("Do you want to search the Promoter Region? (Y/N): ")
    if region == "Y" or region == "y":
        print("Here is the promoter region data")
        info = getPromoterUCSC.getPromoter(geneName, database)
    else:
        print("Here is the transcribable region data")
        info = GeneInfoUCSC.infoGather(geneName, database)
    return info

def makeDatabase():
    MakeDatabaseUCSC.DatabaseCreation()

def extractReads():
    extractbamfile.extractBamFile()
    

def findMethylation():
    Methylation.getMethylation()


def blastIt():
    blastingSequences.blast()
    

def findResults():
    info = ResultInfoGather.getResults()
    return info
