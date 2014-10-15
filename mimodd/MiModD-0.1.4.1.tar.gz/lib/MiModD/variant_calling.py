"""Provides a functional approach to variant calling.

The current version supports variant calling using samtools mpileup and
bcftools through the single function varcall.
"""

import sys
import os
import io
import tempfile
import time
import signal
import random
import subprocess
from . import samheader, pysamtools, tmpfiles, pyvcf, config, mimodd_base, pysam
from .fasta import FastaReader

def varcall(ref_genome, inputfiles, output_vcf = None, output_cov = None,
            cov_stats = None, depth = None, sites = None, output_sites = None,
            group_by_id = False, verbose = False, quiet = True):
    """Variant calling using samtools mpileup and bcftools.

    The function speeds up variant calling through multiprocessing (one call
    to mpileup/bcftools per chromosome). It uses the output of the combined
    tools to generate up to three results files in a single pass:
    a vcf file with all variant sites, an optional second vcf file with a
    fixed list of user-defined sites (variant or not), and a genome-wide
    coverage file.
    It enhances the original output further by adding information about
    sample-specific allele frequencies (similar to GATK).
    
    Arguments:
    ref_genome: reference genome file (mpileup -f parameter,
                but varcall will take care of indexing the genome)
    inputfiles: an iterable of inputfiles (varcall will take care
                of indexing
    output_vcf:   optional, name of the variant sites vcf file
                  (default = stdout)
    output_cov:   optional, name of the coverage file
                  (default = no coverage output)
    cov_stats:  optional, name of the coverage stats file
                (default = no statistical report)
    output_sites: optional, name of the fixed sites vcf file
                  (default = stdout)
                  ignored if sites is None
    depth: optional, max per-BAM depth (to avoid excessive memory usage
           (mpileup option -d)
    sites: optional name of a vcf file specifying genomic positions at which
           information should always be retained, even if these aren't
           variant sites. Resulting data will be written to output_sites.
    group_by_id: if True, reads with different read group IDs are never pooled;
                 if False, reads with matching sample names are grouped
                 independent of their read group IDs (samtools' default)."""
    
    tempfile_dir = config.tmpfiles_path
    signal.signal(signal.SIGTERM, mimodd_base.catch_sigterm)
# ARGUMENTS PREPROCESSING
# additional information via stdout: parameter settings

    if not isinstance(depth, (int, type(None))):
        raise TypeError("Need integer or None value for 'depth' parameter.")
    if not output_vcf and sites and not output_sites:
        raise RuntimeError('Only one output (variant OR fixed sites) can go to stdout. Provide an output file name for at least one of them.')

    # retrieve chromosome and read group names from input file headers
    # get all headers and assert that they use the same sequence dictionary
    inputheaders = [samheader.Header.frombam(file) for file in inputfiles]
    if not all((h['SQ'] == inputheaders[0]['SQ'] for h in inputheaders[1:])):
        raise RuntimeError ('The input files use different reference sequence dictionaries in their headers. Cannot start combined SNP calling.')
    seqdict = inputheaders[0]['SQ'] # get the chromosome names from the header of the first file
    all_read_groups = [rg for h in inputheaders for rg in h['RG']] # get the read groups of all input files as a flat list
    
    if verbose:
        print ('INPUT FILE SUMMARY:')
        print ()
        print ('Read groups found:')
        for rg in all_read_groups:
            print('ID: {0}\tSample Name: {1}'.format(rg['ID'], rg['SM']))
        print ('Sequences found:')
        for seq in seqdict:
            print (seq['SN'])
        print ()

    require_reheader = False
    # currently, there are two situations when we need to reheader the input
    # bam files
    # no. 1: the reference genome has sequence names that do not match the bam
    # sequence dictionary; if that's the case, but corresponding sequences can
    # be identified through their MD5 checksums, then we use the reference
    # names.
    # no. 2: if strict grouping (by RG ID) is active but there are duplicate
    # sample names defined in the bam headers, we need to make them unique
    # (by appending the RG ID to them) to prevent samtools from treating these
    # together.
    
    # check md5sums of reference and bam header seqs to verify identity of
    # reference during alignment and variant calling
    for seq in seqdict:
        if not seq.get('M5'):
            break
    else:
        # we do this only if every sequence in the first header has an M5 entry
        with open(ref_genome, 'r') as ifo:
            md5sums = {md5: title for title, md5 in FastaReader(ifo).md5sums()}
        try:
            for seq in seqdict:
                if md5sums[seq['M5']] != seq['SN']:
                    # go through all SQs of all headers and replace matching sequence names
                    # with the name found in the reference genome
                    for hdr in inputheaders:
                        for s in hdr['SQ']:
                            if s['SN'] == seq['SN']:
                                s['SN'] = md5sums[seq['M5']]
                    require_reheader = True
        except KeyError:
            raise RuntimeError("""Non-matching md5sums between reference genome and bam header sequences!
                                  Please use the same reference genome that was used for the alignment to call variants.""")

    if group_by_id and len(all_read_groups) != len({rg['SM'] for rg in all_read_groups}):
        # grouping of samples should occur strictly by read group ID,
        # but there are duplicate sample names in our input files
        # reheader input files to obtain sample names in the format
        require_reheader = True
        if verbose:
            print('Going to reheader the input files to group samples by read group id ...')
        for hdr in inputheaders:
            hdr.uniquify_sm() # change header SM entries to <old_sm>_<rg_id>

    original_files, inputfiles = inputfiles, []
    try:
        # temporary file IO starting here
        if verbose:
            print ('Preparing input files ..')               
        if require_reheader:
            for hdr, ifile in zip(inputheaders, original_files):
                tmp_reheadered = []
                tmp_output = tmpfiles.unique_tmpfile_name('tmpbam_', '.bam')
                tmp_reheadered.append(tmp_output)
                if verbose:
                    print ('original file: {0} ---> reheadered copy: {1}'.format(ifile, tmp_output))
                pysamtools.reheader(hdr, ifile, tmp_output)
            # use the reheadered files as the input files
            inputfiles = tmp_reheadered
            # recalculate the all_read_groups list
            all_read_groups = [rg for h in inputheaders for rg in h['RG']] # a flat list of the read groups from all input files
        else:
            inputfiles = [tmpfiles.tmp_hardlink(ifile, 'tmp_indexed_bam_', '.bam') for ifile in original_files]
            if verbose:
                for n, b in zip(inputfiles, original_files):
                    print ('Generated hard link {0} from {1}.'.format(n,b))

        # generate a mapping of rg ids to sample names
        rgid_sm_mapping = {rg['ID']:rg['SM'] for rg in all_read_groups} # a dict mapping of all read group IDs to their sample names
        
        # index the reference genome
        tmp_ref_genome = tmpfiles.tmp_hardlink(ref_genome, 'tmp_genome', '.fa')
        if verbose:
            print ('Generated hard link {0} for reference genome file {1}.'.format(tmp_ref_genome, ref_genome))
            print ()
            print ('indexing the reference genome ..')
            print ()
        pysamtools.faidx(tmp_ref_genome)
    
        # index the inputfiles
        if verbose:
            print ('indexing the aligned reads input files ..')
        for file in inputfiles:
            call, results, errors = pysamtools.index(file)
            if verbose:
                print (call)
            if errors:
                raise RuntimeError('ERROR raised by samtools index with input file: {0}\n{1}'.format(file, errors))
        if verbose:
            print ()

        # start variant calling
        calls = [('{0} mpileup {1} -r {2}: -t DP,DPR -gu -f {3} {4}'.
                 format(pysamtools.samtools_exe, '-d '+str(depth) if depth else '', seq['SN'], tmp_ref_genome, ' '.join(inputfiles)),
                 '{0} call -m -f GQ -O v -'.format(pysamtools.bcftools_exe)
                  ) for seq in seqdict] # create a tuple of calls to samtools mpileup and bcftools for each chromosome

        if verbose:
            print ('Starting variant calling ..')

        # create and open temporary output files with unique names
        # to redirect subprocess output to
        tmp_io = [tempfile.NamedTemporaryFile(mode='wb', prefix=seq['SN']+'_', suffix='.vcf', dir=config.tmpfiles_path, delete=False) for seq in seqdict]

        # launch subprocesses and monitor their status
        subprocesses = []
        error_table = {call:['',''] for call in calls}

        while subprocesses or calls:
            while calls and len(subprocesses) < config.multithreading_level:
                # launch a new paired call to samtools mpileup and bcftools 
                call = calls.pop()
                ofo = tmp_io[len(calls)] # calls and temporary output file objects have the same order

                p1 = subprocess.Popen(call[0].split(), stdout = subprocess.PIPE, stderr = subprocess.PIPE)
                p2 = subprocess.Popen(call[1].split(), stdin = p1.stdout, stdout = ofo, stderr = subprocess.PIPE)
                p1.stdout.close()
                subprocesses.append((call, p1, p2))
                # needto check the type of the redirected stderr streams now
                # because subprocess.PIPE returns a buffered IO object in Python 3.3
                # but an unbuffered one with earlier versions
                if isinstance(p1.stderr, io.RawIOBase):
                    p1.stderr.read1 = p1.stderr.read
                if isinstance(p2.stderr, io.RawIOBase):
                    p2.stderr.read1 = p2.stderr.read
                
                if verbose:
                    print ('executing:', ' | '.join(call))
                    
            for call, p1, p2 in subprocesses:
                # monitor processes 
                p1_stat = p1.poll()
                p2_stat = p2.poll()

                error_table[call][0] += p1.stderr.read1(256).decode()
                error_table[call][1] += p2.stderr.read1(256).decode()

                if p1_stat is not None or p2_stat is not None:
                    # there is an outcome for this process, lets see what it is
                    if p1_stat or p2_stat:
                        print (error_table[call][0], error_table[call][1], file = sys.stderr)
                        raise RuntimeError('Execution error in: {0} | {1}'.format(call[0], call[1]))
                    if p2_stat == 0:
                        # things went fine
                        if verbose:
                            print ('finished:', ' | '.join(call))
                        subprocesses.remove((call, p1, p2))
                        break
            # wait a bit in between monitoring cycles
            time.sleep(2)
        for tmp_file in tmp_io:
            tmp_file.close()
        if verbose:
            print()

        # mpileup and bcftools write a lot to stderr
        # currently, we don't screen this output for real errors,
        # but simply rewrite them to stderr.
        if not quiet:
            print('stderr output from samtools mpileup/bcftools:'.upper(), file = sys.stderr)
            for call, errors in error_table.items():
                print (' | '.join(call), ':', file = sys.stderr)
                print ('-' * 20, file = sys.stderr)
                print ('samtools mpileup output:', file = sys.stderr)
                print (errors[0], file = sys.stderr)
                print ('bcftools view output:', file = sys.stderr)
                print (errors[1], file = sys.stderr)
    
        # OUTPUT POST-PROCESSING
        # the samtools mpileup and bcftools calls above write one file per
        # chromosome each of which holds information about every nucleotide
        # position. Post-processing converts these files into a single vcf
        # with only variant sites. In parallel, it generates a .cov file
        # reporting the read coverage for every nucleotide position in the
        # genome and, if sites is given, an additional vcf with the sites
        # found in the sites file independent of whether they are variant
        # sites or not. In addition, sample-specific allele frequency
        # information is added to both vcf output files.
        
        # open all necessary input and output files
        # read the vcf specified by sites
        if verbose:
            print ('Postprocessing and merging results ..')
        inbams = [pysam.Samfile(bamfile, 'rb') for bamfile in inputfiles]
        if output_vcf:
            out_vcf = open(output_vcf, 'w')
        else:
            out_vcf = sys.stdout
        if sites:
            with pyvcf.open(sites, 'r') as site_vcf:
                sites_set = {(site.chrom, site.pos) for site in site_vcf} # fast lookup!   
            if output_sites:
                out_sites = open(output_sites, 'w')
            else:
                out_sites = sys.stdout
        else:
            sites_set = set()
        if output_cov:
            out_cov = open(output_cov, 'w')
        if cov_stats:
            cstats = open(cov_stats, 'w')
            

        # initialize some loop variables
        analyze_coverage = output_cov or cov_stats # flag for indicating whether coverage data needs to be looked at
        last_chr_covered = ''
        last_pos_covered = 0
        # start generating output
        for file_no, output in enumerate(tmp_file.name for tmp_file in tmp_io): # iterate over all subprocess-outputfiles (one for each chromosome)
            if verbose:
                print ('Processing partial results file {0} of {1} ..'.format(file_no + 1, len(tmp_io)))
            # pyvcf.open returns a VCFReader object for convenient access to a vcf file
            with pyvcf.open(output, 'r') as raw_vcf:
                # copy comment and header lines over to post-processed vcf file
                # write the header line of the coverage file
                # determine the number of samples and their names from the vcf input  
                if file_no == 0:    # do all this only for the first vcf input file
                    # before writing, change the 'reference' metadata back to
                    # the original reference fasta instead of the temporary
                    # file used in the call to mpileup
                    raw_vcf.info.comments['reference'] = [ref_genome]            
                    out_vcf.write(str(raw_vcf.info)+'\n')
                    sample_names = raw_vcf.info.sample_names   # retrieve the sample names from the VCFReader object
                    sample_count = len(sample_names)
                    # write the header line to the coverage file
                    if output_cov:
                        out_cov.write('#CHROM\tPOS\t{0}\n'.format('\t'.join([sample for sample in sample_names])))
                    if cov_stats:
                        cstats.write('#CHROM\t{0}\n'.format('\t'.join([sample for sample in sample_names])))
                        contig_lengths = raw_vcf.info.contigs
                    # write comment and header lines to the fixed sites vcf
                    if sites:
                        out_sites.write(str(raw_vcf.info)+'\n')
                
                # start writing the real content
                for line in raw_vcf.raw_iter():    # the raw_iter() method of the VCFReader object provides fast, line-based access to the body of a vcf file
                    fields = line.split()
                    chrom = fields[0]
                    pos = int(fields[1])

                    # writing only variant sites to vcf file adding sample-specific allele frequencies
                    try:
                        # the fifth field in a vcf line holds alternate allele information, but a '.' content tells us that this is not a variant site
                        if fields[4] != '.' or (chrom, pos) in sites_set:
                            # this is a variant line; convert it to a VCFEntry object for more convenient manipulation
                            var = pyvcf.VCFEntry(line, sample_names)
                            var.sampleinfo['AD']={}
                            reads = []
                            for inbam in inbams:
                                for pileup in inbam.pileup(var.chrom, var.pos-1, var.pos):
                                    if pileup.pos == var.pos-1:
                                        reads.extend(pileup.pileups)
                                        break

                            alt_c = dict.fromkeys(var.samplenames, 0)
                            ref_c = dict.fromkeys(var.samplenames, 0)
    
                            for read in reads:
                                rgid = read.alignment.tags[[tag[0] for tag in read.alignment.tags].index('RG')][1]
                                rg = rgid_sm_mapping[rgid]
                                if chr(read.alignment.seq[read.qpos]) == var.alt:
                                    alt_c[rg] += 1
                                elif chr(read.alignment.seq[read.qpos]) == var.ref:
                                    ref_c[rg] += 1

                            for rg in var.samplenames:
                                var.sampleinfo['AD'][rg] = '{0},{1}'.format(str(ref_c[rg]), str(alt_c[rg]))

                            out_line = str(var)+'\n'
                            if fields[4] != '.':
                                out_vcf.write(out_line)
                            if (chrom, pos) in sites_set:
                                out_sites.write(out_line)
                    except:
                        raise RuntimeError(line)

                    if analyze_coverage:
                        # need to process coverage information
                        if last_chr_covered != chrom:
                            if cov_stats and last_chr_covered != '':
                                cov_mean = [str(cov // contig_lengths[last_chr_covered]) for cov in cov_sum]
                                cstats.write('{0}\t{1}\n'.format(last_chr_covered, '\t'.join(cov_mean)))
                            last_pos_covered = 0
                            last_chr_covered = chrom
                            cov_sum = [0] * sample_count
                        if pos - last_pos_covered != 1:
                            if output_cov:
                                for n in range(last_pos_covered+1, pos):
                                    zero_cov = '\t'.join(('0',)*sample_count)  # a string of sample_count * tab-separated 0s
                                    out_cov.write('{0}\t{1}\t{2}\n'.format(chrom, n, zero_cov))
                        last_pos_covered = pos
                        tags = (fields[8]).split(':')             # splits the 'Format' field
                        DP_index = tags.index('DP')               # DP_index tells us where to find the coverage value in the subsequent fields
                        cov_line_elements = [fields[0], fields[1]] # starting to build the output line with chromosome and position
                        for c in range(sample_count):
                            dp_str = fields[9+c].split(':')[DP_index]
                            # beginning with field #9 the next number(samples) fields hold the coverage information at position DP_index
                            cov_line_elements.append(dp_str) # continue building the output line
                            if cov_stats:
                                cov_sum[c] += int(dp_str)
                        if output_cov:
                            out_cov.write('\t'.join(cov_line_elements)+'\n')    # writing output as a string
        if verbose:
            print ()
    # clean up
    finally:
        try:
            out_vcf.close()
        except:
            pass
        try:
            out_sites.close()
        except:
            pass
        try:
            out_cov.close()
        except:
            pass
        try:
            cstats.close()
        except:
            pass
        if locals().get('inbams'):
            for inbam in inbams:
                try:
                    inbam.close()
                except:
                    pass
        for tmp_bam in inputfiles:
            # when we get here, the original input files are tucked away
            # in original_files, so if inputfiles has any elements, these
            # are guaranteed to be temporary file names
            try:
                os.remove(tmp_bam)
            except:
                pass
            try:
                os.remove(tmp_bam + '.bai')
            except:
                pass
        if locals().get('tmp_io'):
            for file in tmp_io:       # temporary output files
                try:
                    os.remove(file.name)
                except:
                    raise
                    # pass

        try:
            os.remove(tmp_ref_genome)   # hard link to reference genome
        except:
            pass
        try:
            os.remove(tmp_ref_genome + '.fai')  # indexed reference genome
        except:
            pass
