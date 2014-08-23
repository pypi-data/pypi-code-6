#!/usr/bin/env python

from omics_pipe.parameters.default_parameters import default_parameters
from omics_pipe.utils import *
p = Bunch(default_parameters)


def bwa1(sample, bwa1_flag):
    '''BWA aligner for read1 of paired_end reads.
    
    input: 
        .fastq
    output: 
        .sam
    citation: 
        Li H. and Durbin R. (2009) Fast and accurate short read alignment with Burrows-Wheeler transform. Bioinformatics, 25, 1754-1760. [PMID: 19451168]
    link: 
        http://bio-bwa.sourceforge.net/bwa.shtml
    parameters from parameters file:
        BWA_RESULTS:
            
        TEMP_DIR:
            
        SAMTOOLS_VERSION:
            
        BWA_VERSION:
            
        BWA_INDEX:
            
        RAW_DATA_DIR:
            
        GATK_READ_GROUP_INFO:
    ''' 
    SAMPLE1 = sample + "_1"
    spawn_job(jobname = 'bwa1', SAMPLE = SAMPLE1, LOG_PATH = p.LOG_PATH, RESULTS_EMAIL = p.RESULTS_EMAIL, SCHEDULER = p.SCHEDULER, walltime = "240:00:00", queue = p.QUEUE, nodes = 1, ppn = 8, memory = "29gb", script = "/bwa_drmaa_RNA.sh", args_list = [p.BWA_RESULTS, p.TEMP_DIR, p.SAMTOOLS_VERSION, p.BWA_VERSION, p.BWA_INDEX, SAMPLE1, p.RAW_DATA_DIR, p.GATK_READ_GROUP_INFO])
    job_status(jobname = 'bwa1', resultspath = p.BWA_RESULTS, SAMPLE = sample,  outputfilename = SAMPLE1 + "/" + SAMPLE1 + ".sam", FLAG_PATH = p.FLAG_PATH)
    return

def bwa2(sample, bwa2_flag):
    '''BWA aligner for read2 of paired_end reads.
    
    input: 
        .fastq
    output: 
        .sam
    citation: 
        Li H. and Durbin R. (2009) Fast and accurate short read alignment with Burrows-Wheeler transform. Bioinformatics, 25, 1754-1760. [PMID: 19451168]
    link: 
        http://bio-bwa.sourceforge.net/bwa.shtml
    parameters from parameters file:
        BWA_RESULTS:
            
        TEMP_DIR:
           
        SAMTOOLS_VERSION:
           
        BWA_VERSION:
            
        BWA_INDEX:
         
        RAW_DATA_DIR:
           
        GATK_READ_GROUP_INFO:
    ''' 
    SAMPLE2 = sample + "_2" 
    spawn_job(jobname = 'bwa2', SAMPLE = SAMPLE2, LOG_PATH = p.LOG_PATH, RESULTS_EMAIL = p.RESULTS_EMAIL, SCHEDULER = p.SCHEDULER, walltime = "240:00:00", queue = p.QUEUE, nodes = 1, ppn = 8, memory = "29gb", script = "/bwa_drmaa_RNA.sh", args_list = [p.BWA_RESULTS, p.TEMP_DIR, p.SAMTOOLS_VERSION, p.BWA_VERSION, p.BWA_INDEX, SAMPLE2, p.RAW_DATA_DIR, p.GATK_READ_GROUP_INFO])
    job_status(jobname = 'bwa2', resultspath = p.BWA_RESULTS, SAMPLE = sample, outputfilename = SAMPLE2 + "/" + SAMPLE2 + ".sam", FLAG_PATH = p.FLAG_PATH)
    return

def bwa_RNA(sample, bwa_flag):
    '''BWA aligner for single end reads.
    
    input: 
        .fastq
    output:    
        .sam
    citation: 
        Li H. and Durbin R. (2009) Fast and accurate short read alignment with Burrows-Wheeler transform. Bioinformatics, 25, 1754-1760. [PMID: 19451168]
    link: 
        http://bio-bwa.sourceforge.net/bwa.shtml
    parameters from parameters file:
        BWA_RESULTS:
        
        TEMP_DIR:
        
        SAMTOOLS_VERSION:
        
        BWA_VERSION:
        
        BWA_INDEX:
        
        RAW_DATA_DIR:
        
        GATK_READ_GROUP_INFO:
    ''' 
    spawn_job(jobname = 'bwa', SAMPLE = sample, LOG_PATH = p.LOG_PATH, RESULTS_EMAIL = p.RESULTS_EMAIL, SCHEDULER = p.SCHEDULER, walltime = "240:00:00", queue = p.QUEUE, nodes = 1, ppn = 8, memory = "29gb", script = "/bwa_drmaa_RNA.sh", args_list = [p.BWA_RESULTS, p.TEMP_DIR, p.SAMTOOLS_VERSION, p.BWA_VERSION, p.BWA_INDEX, sample, p.RAW_DATA_DIR, p.GATK_READ_GROUP_INFO])
    job_status(jobname = 'bwa', resultspath = p.BWA_RESULTS, SAMPLE = sample, outputfilename = sample + "/" + sample + ".sam", FLAG_PATH = p.FLAG_PATH)
    return


def bwa_mem(sample,bwa_mem_flag):
    '''BWA aligner with BWA-MEM algorithm.
    
    input: 
        .fastq
    output: 
        .sam
    citation: 
        Li H. and Durbin R. (2009) Fast and accurate short read alignment with Burrows-Wheeler transform. Bioinformatics, 25, 1754-1760. [PMID: 19451168]
    link: 
        http://bio-bwa.sourceforge.net/bwa.shtml
    parameters from parameters file:
        BWA_RESULTS:
        
        TEMP_DIR:
        
        SAMTOOLS_VERSION:
        
        BWA_VERSION:
        
        GENOME:
        
        RAW_DATA_DIR:
        
        BWA_OPTIONS:
    ''' 
    spawn_job(jobname = 'bwa_mem', SAMPLE = sample, LOG_PATH = p.LOG_PATH, RESULTS_EMAIL = p.RESULTS_EMAIL, SCHEDULER = p.SCHEDULER, walltime = "240:00:00", queue = p.QUEUE, nodes = 1, ppn = 16, memory = "15gb", script = "/bwa_drmaa_" + p.ENDS + "_DNA.sh", args_list = [p.BWA_RESULTS, p.TEMP_DIR, p.SAMTOOLS_VERSION, p.BWA_VERSION, p.BWA_INDEX, sample, p.RAW_DATA_DIR, p.BWA_OPTIONS])
    job_status(jobname = 'bwa_mem', resultspath = p.BWA_RESULTS, SAMPLE = sample, outputfilename = sample + "/" + sample + "_sorted.bam", FLAG_PATH = p.FLAG_PATH)
    return

#(resultspath + "/" + outputfilename)

if __name__ == '__main__':
    bwa1(sample, bwa1_flag)
    bwa2(sample, bwa2_flag)
    bwa_RNA(sample, bwa_flag)
    bwa_mem(sample,bwa_mem_flag)
    sys.exit(0)