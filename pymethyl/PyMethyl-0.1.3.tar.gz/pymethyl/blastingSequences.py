##Author: Cody Watson
##BCRL Fox Chase: Dr. Jose Russo, Dr. Julia Periera

##Program to create fasta files of methylated regions to blast
##Then blasting those sequences and deleting those files so they
##don't take up massive amounts of memory. Then saving the output
##files in a folder in the desktop. We will then search those files
##to see if we got a hit or not. We will record the hit in an excell file.



##Packages needed for program
import os
import commands
import re
from tkFileDialog import askopenfilename
from Tkinter import Tk
import shutil

##These directories you should change to match your own personal computers
##directories. Do not change the code, just these directories. They are global
##variables. Bad coding but makes it easier to use when changing directories.
##The DB varaible may completely change depending on what you name your database

def blast():
    global methylated_directory
    global results_directory
    global temp_directory
    global blast_directory
    global db
    global typeBlast
    
    methylated_directory = os.path.expanduser('~') + "/Desktop/" + \
    "Methylated Results"
    
    if os.path.isdir(os.path.expanduser('~') + \
                     "/Desktop/Result_From_Blast"):
        results_directory = os.path.expanduser('~') + \
                        "/Desktop/Result_From_Blast"
    else:
        os.makedirs(os.path.expanduser('~') + \
                   "/Desktop/Result_From_Blast")
        results_directory = os.path.expanduser('~') + \
                            "/Desktop/Result_From_Blast"

    if os.path.isdir(os.path.expanduser('~') + "/Desktop/Temp_Fasta"):
        temp_directory = os.path.expanduser('~') + \
                         "/Desktop/Temp_Fasta"
    else:
        os.makedirs(os.path.expanduser('~') + "/Desktop/Temp_Fasta")
        temp_directory = os.path.expanduser('~') + \
                         "/Desktop/Temp_Fasta"

    
    blast_directory = os.path.expanduser('~') + \
                      "/Desktop/ncbi-blast-2.2.29+/bin"

    typeBlast = raw_input("Enter the type of BLAST that you want \
to perform. Types of BLAST can be found on the NCBI website. \
Example: blastn : ")

    
    db = os.path.expanduser('~') + "/Desktop/ncbi-blast-2.2.29+/db/" + \
         raw_input("Name of the database you are searching. \
Would be the database you made with the MakeDatabase() function. \
Example: Sequences : ")

    
    mainblast()
    shutil.rmtree(temp_directory)


##Main Program that runs all helper functions
def mainblast():
    os.chdir(methylated_directory)
    directory = os.getcwd()
    ##List out files in your current working directory where all your methylated
    ##sequences should be.
    files = os.listdir(directory)
    problems = []
    count = 0
    ##Loops through every single gene that has methylation
    for nxtfile in files:
        os.chdir(methylated_directory) 
        nxtfile = str(nxtfile)
        name = fastaFile(nxtfile)
        ##Tries to blast all the methylation regions
        ##try:
            ##Helper functions to blast and to check information
            ##Counts how many events took place.
        try:
            blastFiles(name)
        ##If blasting the methylation fails it collects the errors here
        ##except:
        except:
            print("Error")
            problems.append(name)
    count = checkInfo()
    print("Went through " + str(len(files)) + " data files")
    print("Counted " + str(count) + " events")


##Program that actually changes all methylated regions to their own fasta files
##that way they can be blasted against the db
def fastaFile(nxtfile):
    file_handle = open(nxtfile, 'r')
    i = 0
    os.chdir(temp_directory)
    for line in file_handle:
        info = line.split()
        filename = ""
        num = str(i)
        filename = nxtfile[:-4] + "_" + num + ".fasta"
        fasta_handle = open(filename, 'w')
        seq = info[2]
        fasta_handle.write(">"+ str(nxtfile[:-4]) + " Sequence\n")
        fasta_handle.write(seq)
        i += 1
        fasta_handle.close()
    file_handle.close()
    return nxtfile[:-4]



##Program takes those fasta files and then blasts them against the db
##It uses the cmd to run the command.
def blastFiles(name):
    ##Gets a list of all the files you want to blast
    os.chdir(temp_directory)
    files = os.listdir(os.getcwd())
    os.chdir(blast_directory)
    ##Goes through every fasta file individually
    for f in files:
        fname = str(f)
        filename = ''
        filename = temp_directory + "/" + fname
        resultfile = results_directory + "/" + fname[:-6] + ".txt"
        ##Runs the CMD command to blast the file.
        ##You can change this command to change the type of blast done
        cmd = str(typeBlast) + " -query " + str(filename) + " -db " + db +\
        " -out " + str(resultfile)
        output = commands.getstatusoutput(cmd)
        os.remove(filename)

##Checks all of the blast results to see if there was a clear match.
##The files will have a match, the e-value, and the alignment.
def checkInfo():
    os.chdir(results_directory)
    files = os.listdir(os.getcwd())
    newcount = 0
    ##Goes through all of the files to check if there were any hits
    for f in files:
        name = str(f)
        file_handle = open(name, 'r')
        contents = file_handle.read()
        ##Searches file for a flag to determine if there was a hit
        check = re.search("No hits found", contents)
        ##If there were no hits then just remove file
        try:
            check.group()
            file_handle.close()
            removeFile = results_directory + "/" + str(f)
            print(removeFile + " did not match database and is being removed")
            os.remove(removeFile)
        ##If there was a hit then copy the file to a result file and
        ##delete everything else
        except:
            newcount += 1
    return newcount
            
            
            
    
        
    


        
        
    
    
    
    
