#!/usr/bin/env python

from omics_pipe.parameters.default_parameters import default_parameters
from omics_pipe.utils import *
p = Bunch(default_parameters)


def snpir_variants(sample, snpir_variants_flag):    
    '''Calls variants using SNPIR pipeline.
    
    input: 
        Aligned.out.sort.bam or accepted_hits.bam
    output: 
        final_variants.vcf file
    citation: 
        Piskol, R., et al. (2013). "Reliable Identification of Genomic Variants from RNA-Seq Data." The American Journal of Human Genetics 93(4): 641-651. 
    link:
        http://lilab.stanford.edu/SNPiR/
    parameters from parameters file:
        SNPIR_RESULTS:
        
        TEMP_DIR:
        
        SAMTOOLS_VERSION:
        
        BWA_VERSION:
        
        PICARD_VERSION:
        
        GATK_VERSION:
        
        BEDTOOLS_VERSION:
        
        UCSC_TOOLS_VERSION:
        
        GENOME:
        
        REPEAT_MASKER:
        
        SNPIR_ANNOTATION:
        
        RNA_EDIT:
        
        DBSNP:
        
        MILLS:
        
        G1000:
        
        WORKING_DIR:
        
        BWA_RESULTS:
        
        SNPIR_VERSION:
        
        SNPIR_CONFIG:
        
        SNPIR_DIR:
        
        ENCODING:
        
        '''
    spawn_job(jobname = 'snpir_variants', SAMPLE = sample, LOG_PATH = p.LOG_PATH, RESULTS_EMAIL = p.RESULTS_EMAIL, SCHEDULER = p.SCHEDULER, walltime = "240:00:00", queue = p.QUEUE, nodes = 1, ppn = 8, memory = "29gb", script = "/snpir_drmaa.sh", args_list = [p.SNPIR_RESULTS, p.TEMP_DIR, p.SAMTOOLS_VERSION, p.BWA_VERSION, p.PICARD_VERSION, p.GATK_VERSION, p.BEDTOOLS_VERSION, p.UCSC_TOOLS_VERSION, p.GENOME, p.REPEAT_MASKER, p.SNPIR_ANNOTATION, p.RNA_EDIT, p.DBSNP, p.MILLS, p.G1000, p.WORKING_DIR, sample, p.BWA_RESULTS, p.SNPIR_VERSION, p.SNPIR_CONFIG, p.SNPIR_DIR, p.ENCODING])
    job_status(jobname = 'snpir_variants', resultspath = p.SNPIR_RESULTS, SAMPLE = sample, outputfilename = sample + "/final_variants.vcf", FLAG_PATH = p.FLAG_PATH)
    return

if __name__ == '__main__':
    snpir_variants(sample, snpir_variants_flag)
    sys.exit(0)