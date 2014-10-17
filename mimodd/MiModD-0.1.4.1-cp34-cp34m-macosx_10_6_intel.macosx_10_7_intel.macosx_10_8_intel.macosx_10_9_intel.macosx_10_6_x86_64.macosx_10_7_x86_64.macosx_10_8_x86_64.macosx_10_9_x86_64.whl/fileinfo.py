import sys

from . import samheader, pyvcf, pysamtools, covtools

def get_samplenames(ifile, verbose = False):
    fformat = None
    try:
        try:
            samples = {rg['ID']:rg.get('SM', 'unknown') for rg in samheader.Header.frombam(ifile)['RG']}
            fformat = 'bam'
        except AssertionError:
            try:
                samples = {rg['ID']:rg.get('SM', 'unknown') for rg in samheader.Header.fromsam(ifile)['RG']}
                fformat = 'sam'
            except AssertionError:
                try:
                    samples = pyvcf.open(ifile).info.sample_names
                    fformat = 'vcf'
                except AssertionError:
                    samples = covtools.open(ifile).samplenames
                    fformat = 'cov'
    except (AssertionError, UnicodeDecodeError):
        raise AssertionError('Do not know how to parse the input file.')

    if verbose:
        print ('Detected file format: {0}'.format(fformat))
        
    return samples

def print_sampleinfo (ifile, ofile = None, verbose = False):
    ofo = open(ofile, 'w') if ofile else sys.stdout
    samples = get_samplenames(ifile, verbose = True)
    print ('Found the following samples:', file = ofo)
    if isinstance(samples, (list, tuple)):
        for sample in samples:
            print (sample, file = ofo)
    elif isinstance(samples, dict):
        for rg, sm in samples.items():
            print ('{0} (RG_ID: {1})'.format(sm, rg), file = ofo)
