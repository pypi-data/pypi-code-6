#!/usr/bin/env python

from omics_pipe.parameters.default_parameters import default_parameters
from omics_pipe.utils import *
p = Bunch(default_parameters)


def mutect(sample, mutect_flag):
    '''Runs MuTect on paired tumor/normal samples to detect somatic point mutations in cancer genomes.
    
    input: 
        .bam
    output: 
        call_stats.txt
    citation: 
        Cibulskis, K. et al. Sensitive detection of somatic point mutations in impure and heterogeneous cancer samples. Nat Biotechnology (2013).doi:10.1038/nbt.2514
    link: 
        http://www.broadinstitute.org/cancer/cga/mutect
    parameters from parameters file:
        BWA_RESULTS:
            
        TEMP_DIR:
            
        GATK_VERSION:
        
        GENOME:
        
        DBSNP:
        
        MILLS:
        
        G1000:
        
        CAPTURE_KIT_BED:
        ''' 
    
    spawn_job(jobname = 'mutect', SAMPLE = sample, LOG_PATH = p.LOG_PATH, RESULTS_EMAIL = p.RESULTS_EMAIL, SCHEDULER = p.SCHEDULER, walltime = "240:00:00", queue = p.QUEUE, nodes = 1, ppn = 8, memory = "31gb", script = "/mutect.sh", args_list = [p.BWA_RESULTS, sample, p.TEMP_DIR,p.GATK_VERSION, p.GENOME, p.DBSNP,p.MILLS,p.G1000,p.CAPTURE_KIT_BED])
    job_status(jobname = 'mutect', resultspath = p.BWA_RESULTS, SAMPLE = sample,  outputfilename = sample + ".ready.bam", FLAG_PATH = p.FLAG_PATH)
    return

if __name__ == '__main__':
    mutect(sample, mutect_flag)
    sys.exit(0)