from option import Option


class GenomicTagOption(Option):

    def __init__(self, *args, **kwargs):
        self.valid_keys = ["-10_signal", "-35_signal", "3'UTR", "5'UTR",
                           "CAAT_signal", "CDS", "C_region", "D-loop",
                           "D_segment", "GC_signal", "J_segment", "LTR",
                           "N_region", "RBS", "STS", "S_region", "TATA_signal",
                           "V_region", "V_segment", "assembly_gap",
                           "attenuator", "enhancer", "exon", "gap", "gene",
                           "iDNA", "intron", "mRNA", "mat_peptide", "misc_RNA",
                           "misc_binding", "misc_difference", "misc_feature",
                           "misc_recomb", "misc_signal", "misc_structure",
                           "mobile_element", "modified_base", "ncRNA",
                           "old_sequence", "operon", "oriT", "polyA_signal",
                           "polyA_site", "precursor_RNA", "prim_transcript",
                           "primer_bind", "promoter", "protein_bind", "rRNA",
                           "rep_origin", "repeat_region", "sig_peptide",
                           "source", "stem_loop", "tRNA", "terminator",
                           "tmRNA", "transit_peptide", "unsure", "variation",
                           # These are "custom"
                           "whole", "all"]
        self.validKeySet = {x: x for x in sorted(self.valid_keys)}
        kwargs['options'] = self.validKeySet
        Option.__init__(self, *args, **kwargs)
