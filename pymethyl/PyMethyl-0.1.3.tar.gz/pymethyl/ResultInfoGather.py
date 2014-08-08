##Author Cody Watson
##
##BCRL Fox Chase Dr. Jose Russo, Dr. Julia Pereira

##Program to put results into file that can be easily seen.

##Packages needed for this program
import re
import os


def getResults():
        global result_folder
        global searching_for

        ##Global variable directory names. These are embedded into the code and were
        ##made for beginers to be able to place their own directories in place and
        ##program should run.
        result_folder = os.path.expanduser('~') + "/Desktop/Result_From_Blast"
        searching_for = raw_input("Type the methylated gene you are looking at: ")
        result = Results()
        return result
        
##Main program that gathers the info of the hits that were seen.
def Results():
        ##opens giles and writes a header to the result file
        files = os.listdir(result_folder)
        stringfiles = str(files)
        ##Loop that finds how many hits there were and records the amount of
        ##methylated regions and if the regions was methylated at all or not.
        gene = re.findall(searching_for, stringfiles)
        if gene == None:
                gene = str(0)
        else:
                gene = str(len(gene))
        return("There are " + gene + " events of methylation within this region.")


    
        

