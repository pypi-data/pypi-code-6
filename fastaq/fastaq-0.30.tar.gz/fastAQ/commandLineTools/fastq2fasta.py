import sys

input_file = sys.argv[1]

## FASTQ2FASTA
from fastAQ.fastq2fasta import Fastq2Fasta
out = Fastq2Fasta(input_file)
out.fasta()