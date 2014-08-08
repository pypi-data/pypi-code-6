##Author Cody Watson
##
##BCRL Fox Chase Dr. Jose Russo, Dr. Julia Periera

##Program that will take sequences from text file that has the name of the gene,
##the locations of the begining and end or the gene. It converts these sequences
##to fasta files that can be transformed into a database.


##Packages needed to run program
import os
from cruzdb.sequence import sequence
from tkFileDialog import askopenfilename
from Tkinter import Tk


##Global varaible directory names. Change them to your specific directories
##and file names. Some are file names that depend on what you are making a
##database for. 


##Main program that runs helper functions
def DatabaseCreation():
    global database_info
    global db_directory
    global database_fasta
    global dbname
    global dbtype
    global database

    
    print("Choose the text file to make into a database")
    Tk().withdraw()
    database_info = askopenfilename()

    
    db_directory = os.path.expanduser('~') + "/Desktop/ncbi-blast-2.2.29+/db"

    
    database_fasta = db_directory + "/database.fasta"

    
    dbname = db_directory + "/" + raw_input("Name of your Database: ")

    
    dbtype = raw_input("NCBI Database type, leave empty if unsure: ")
    if dbtype == "":
        dbtype = "nucl"

        
    database = raw_input("Which database will you get the sequences from \
Example: hg18 : ")

    print("Your database is processing, not to worry, this can take some time.")

    
    fastaFileCreation()
    databaseCreation()


##Creates fasta files from 
def fastaFileCreation():
    file_handle = open(database_info, 'r')
    file_output = open(database_fasta, 'w')
    ##Loops through and makes a database of fasta files from the sequences of
    ##either the transcribable region or the transcribable region.
    for line in file_handle:
        info = line.split()
        if info[1] == "X":
            chromosome = "X"
        elif info[1] == "Y":
            chromosome = "Y"
        else:
            chromosome = int(info[1])
        start_number = int(info[2])
        end_number = int(info[3])
        ##get sequence of specific region for database
        try:
            seq = sequence(db = database, chrom = chromosome, start = start_number,
                           end = end_number)
            file_output.write(">" + line.strip() + '\n')
            file_output.write(seq + "\n")
        except:
            print("ERROR FOUND")
    file_output.close()
    file_handle.close() 




def databaseCreation():
    ##Fasta files were held in this directory as they should be
    try:
        ##Runs this command with windows cmd
        os.system("makeblastdb -in " + database_fasta +
                  " -out " + dbname + " -dbtype "
                  + dbtype)
    ##Databases that gave me any issues
    except:
        print("FAILURE")
    print("Done")

