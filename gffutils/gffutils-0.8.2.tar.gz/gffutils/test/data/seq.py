"""
Demonstration of getting the coding sequence for each alterative isoform of
each gene in a GFF file.

Uses pybedtools.BedTool.seq to extract sequences from a FASTA file.
"""
import gffutils
import pybedtools
from gffutils.helpers import asinterval

fasta = '/DATA/genomes/dm3/dm3.masked.fa'
gff = gffutils.example_filename('FBgn0031208.gff')
db = gffutils.create_db(gff, ':memory:')

# Iterate over all genes,
for gene in db.features_of_type('gene'):

    # ...and all transcript for each gene
    for transcript in db.children(gene, level=1):

        coding_sequence = []

        # ...and all CDSs for each transcript.  To get mRNA sequence instead of
        # coding sequence, you can use "exon" instead of "CDS" for
        # well-formatted GFF files.
        for cds in db.children(transcript, level=1, featuretype='CDS'):

            coding_sequence.append(
                pybedtools.BedTool.seq((cds.chrom, cds.start, cds.stop), fasta)
            )

        # We want to ignore genes with transcript but no CDS (e.g., rRNA)
        if coding_sequence:
            coding_sequence = ''.join(coding_sequence)

            # This gives one long line for each seq.  Might want to run through
            # BioPython if you want nice 80-column wrapped format.
            print ">{0.id}.{1.id}\n{2}".format(
                gene, transcript, coding_sequence)
