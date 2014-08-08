##Author: Cody Watson
##BCRL Dr. Jose Russo, Dr. Julia Pereira

import os
from tkFileDialog import askopenfilename
from Tkinter import Tk

##Program to calculate methylated regions and their sequences
def getMethylation():
    global DataFile
    global geneName
    global MethylationCount
    global Result_Directory
    global mappingQuality

    
    print("Chose the data file which holds results from bam file. \
This should be a text file.")
    Tk().withdraw()
    DataFile = askopenfilename()

    if os.path.isdir(os.path.expanduser('~') + "/Desktop/" + \
    "Methylated Results") == True:
        Result_Directory = os.path.expanduser('~') + "/Desktop/" + \
    "Methylated Results"
    else:
        os.makedirs(os.path.expanduser('~') + "/Desktop/" + \
        "Methylated Results")
        Result_Directory = os.path.expanduser('~') + "/Desktop/" + \
        "Methylated Results"

    
    geneName = raw_input("Type the gene name you are looking at. \
Example: 'ACACA' : ")


    mappingQuality_String = raw_input("What is the mapping quality needed for \
a read to be significant. Enter 0 for every read: ")
    mappingQuality = int(mappingQuality_String)

    
    MethylationCount_String = raw_input("Type the amount of coverage you would \
like have a sequence considered methylated. \
Example: 5 (which means regions have 5 overlapping sequences are saved) : ") 
    MethylationCount = int(MethylationCount_String)
    
    mainMethylated()

##Main function
def mainMethylated():
    if os.path.getsize(DataFile) > 0:
        ##Find methylated regions in all genes
        positions, readSequences, lineCount = fileInfo()
        if lineCount >= MethylationCount:
            regions, methylatedSequences = methylated(positions, readSequences)
            result_file = fileCreator(regions, methylatedSequences, geneName)
            if os.path.getsize(result_file) > 0:
                print("Done")
                print("Your results are in your desktop folder named \
Methylated Results")
            else:
                os.remove(result_file)
                print("No methylated detected, file removed")
        else:
            print("Not enough reads to warrant significant methylation \
no file was created.")
    else:
        print("File contained no sequences")





##Function that extracts information into lists
def fileInfo():
    lineCount = 0
    ##List of compilated positions
    positions = []
    ##List of sequences
    readSequences = []
    file_handle = open(DataFile, 'r')
    for line in file_handle:
        ##List of positions of sequence emptied every loop around
        ##because we are appending this list into a larger list
        temppositions = []
        ##This is a tab delineated file
        InfoString = line.split('\t')
        if mappingQuality <= int(InfoString[2]):
            lineCount += 1
            start = int(InfoString[0])
            end = int(InfoString[1])
            sequence = InfoString[3]
            ##Put start and end positions in a list then add that
            ##sublist to the positions list
            temppositions.append(start)
            temppositions.append(end)
            ##Where we append the smaller list into
            positions.append(temppositions)
            readSequences.append(sequence)
    file_handle.close()
    return positions, readSequences, lineCount


##Function finds areas that are heavily methylated by checking overlap of
##sequences. To manipulate how many sequences you get, change the MethylationCount
##variable
def methylated(positions, readSequences):
    ##Empty variables to be filled
    regions = []
    methylatedSequences = []
    sequenceLeft = True
    seqCount = 1
    refseq = ""
    i = 0
    begin = 0
    ##While loop to calculate regions of meet or exceed MethylationCount
    while sequenceLeft:
    
        beg = positions[begin][0]
        firstEnd = positions[i][1]

        
        try:
            secondStart = positions[i+1][0]        
            if firstEnd >= secondStart:
                if i == begin:
                    refseq += str(readSequences[i]).strip()
                    overlap = int(firstEnd) - int(secondStart)
                    refseq += str(readSequences[i+1][overlap:]).strip()
                else:
                    overlap = int(firstEnd) - int(secondStart)
                    refseq += str(readSequences[i+1][overlap:]).strip()
                seqCount += 1
                i += 1
            else:
                if seqCount >= MethylationCount:
                    tempregions = []
                    tempregions.append(positions[begin][0])
                    tempregions.append(positions[i][1])
                    regions.append(tempregions)
                    methylatedSequences.append(refseq)
                i += 1
                seqCount = 1
                refseq = ""
                begin = i


                
        except:
            sequenceLeft = False
            if seqCount >= MethylationCount:
                tempregions = []
                tempregions.append(positions[begin][0])
                tempregions.append(positions[i][1])
                regions.append(tempregions)
                methylatedSequences.append(refseq)

            
    return regions, methylatedSequences

    
            
##Function to create a file and write the results to it 
def fileCreator(regions, methylatedSequences, name):
    result_file = Result_Directory + "/" + name + ".txt"
    file_handle = open(result_file , 'w')
    for i in range(len(regions)):
        file_handle.write(str(regions[i]) + "\t" + str(methylatedSequences[i]))
        if i != len(regions) - 1:
            file_handle.write('\n')
    file_handle.close() 
    return result_file



