


class VCF(object):
    """Variant Call Data




    ftp://ftp.1000genomes.ebi.ac.uk/vol1/ftp
    """
    raise NotImplementedError

    self.chromosome = None
    self.identifier = None
    self.reference = None
    self.alt = None
    """
    self.qual
    self.filter
    self.info
    self.format
    self.genotype"""

    def data_slicer(self):
        pass

    def to_ped(self):
        pass

    def variant_effect_predictor(self):
        pass

    def forge(self):
        pass

    def allele_frequency(self):
        pass
