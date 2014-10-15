"""Provides an interface for handling the MiModD-specific .cov file format."""

import io

class CovEntry (object):
    def __init__(self, covline, samplenames):
        fields = covline.split()
        self.samplenames = [name for name in samplenames if name is not None]
        self.chrom = fields[0]
        self.pos = int(fields[1])
        self.ss_cov = {sample:int(cov) for sample, cov in zip(samplenames, fields[2:]) if sample is not None}

class CovReader (object):
    def __init__(self, ifo):
        self.ifo = ifo
        ifo.seek(0)
        self.parse_header()
        self.body_start = ifo.tell()
        self.ifo = ifo
    def __iter__(self):
        return self
    def __next__(self):
        return CovEntry(next(self.ifo), self.samplenames)
    def raw_iter (self):
        for line in self.ifo:
            yield line
    def __enter__(self):
        return self
    def __exit__(self, *error_desc):
        self.close()
    def seek(self, offset):
        return self.ifo.seek(self.body_start + offset)
    def close (self):
        self.ifo.close()
    def parse_header (self):
        """Checks whether ifo conforms to the cov format."""

        header = self.ifo.readline().split()
        assert header[0] == '#CHROM' and header[1] == 'POS', 'Invalid cov file: unrecognized header fields'
        self.samplenames = header[2:]
        assert self.samplenames, 'Invalid cov file: no sample names found on header line'
        samples = set(self.samplenames)
        assert len(samples) == len(self.samplenames), 'Invalid cov file: duplicate sample names ({0}) found.'\
               .format(', '.join([sm for sm in samples if self.samplenames.count(sm) > 1]))

def open (file, mode = 'r'):
    if mode == 'r':
        return CovReader(io.open(file, mode))
    else:
        raise RuntimeError('Only mode="r" currently implemented.')
