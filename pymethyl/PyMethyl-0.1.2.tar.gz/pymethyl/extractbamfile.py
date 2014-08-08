import pysam
import os
from tkFileDialog import askopenfilename
from Tkinter import Tk

def extractBamFile():

        print("Choose the data file which holds the information of the gene \
that you are looking for. Format gene name, chromosome, start position, end position.")
        Tk().withdraw()
        text_file_path = askopenfilename()

        print("Choose the BAM file that you are extracting reads from.")
        Tk().withdraw()
        bam_file_path = askopenfilename()

        sample_name = raw_input("What is the name of the sample the reads are coming from: ")

        sequence_size = raw_input("What is the length of each read's sequence: ")
        
        path = text_file_path.split('/')
        path.pop()
        path = '/'.join(path)
        path = '/' + path
        
        directory_path = path + '/' + sample_name
        if os.path.isdir(directory_path) == False:
                os.mkdir(directory_path)

        fin = open(text_file_path, 'r')
        
        for line in fin:
                try:       
                        gene_info = line.split("\t")
                        gene_name = gene_info[0]
                        chromosome = 'chr' + gene_info[1]
                        start_position = gene_info[2]
                        end_position = gene_info[3]
                        
                        samfile = pysam.Samfile(bam_file_path, "rb")
                        iter = samfile.fetch(chromosome, int(start_position), int(end_position))
                        
                        file_name = directory_path + '/' + gene_name + '.txt'
                        gene_file = open(file_name, 'w')
                        
                        for x in iter:
                                current_read = str(x)
                                read_info = current_read.split("\t")
                                read_start = read_info[3]
                                read_end = str(int(read_info[3]) + int(sequence_size))
                                read_mapping_quality = read_info[4]
                                read_sequence = read_info[9]
                                selected_read_info = [read_start, read_end, read_mapping_quality, read_sequence]
                                output_string = '\t'.join(selected_read_info) + '\n'
                                gene_file.write(output_string)
                        gene_file.close()
                except:
                        print("Error Found")
        print("Done")
        fin.close()
        return;
