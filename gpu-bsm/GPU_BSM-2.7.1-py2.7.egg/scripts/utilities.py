
# This file is part of GPU-BSM.

# GPU-BSM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# GPU-BSM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GPU-BSM.  If not, see <http://www.gnu.org/licenses/>.


# GPU-BSM is a GPU based program to map bisulfite treated reads
# rel. 2.7.1 2014-10-20
#
# contact andrea.manconi@itb.cnr.it


import os
import logging
import multiprocessing
from optparse import OptionParser
from subprocess import Popen
from pycuda import driver

class DirectoryError(Exception): pass
class BSProtocolError(Exception): pass
class SOAP3MismatchesError(Exception): pass
class QueryFormatException(Exception): pass
class QueryException(Exception): pass
class MultiQueryFormatException(Exception): pass
class InsertSizeException(Exception): pass
class GPUOptionTypeException(Exception): pass
class InvalidGPUidException(Exception): pass
class HitsOptionTypeException(Exception): pass
class InvalidHitsOptionException(Exception): pass
class MismatchesOptionTypeException(Exception): pass
class MismatchesOptionException(Exception): pass
class EDLimitOptionTypeException(Exception): pass
class EDLimitOptionException(Exception): pass
class MappingStrategyException(Exception): pass
class REDSizeOptionTypeException(Exception): pass
class ADPErrorRateTypeException(Exception): pass
class ADPOverlapTypeException(Exception): pass
class AdaptersOptionException(Exception): pass
class ThreadsOptionException(Exception): pass
class ThreadsOptionTypeException(Exception): pass
class NReadsOptionTypeException(Exception): pass
class MaxHitsOptionTypeException(Exception): pass
class SOAP3MisOptionTypeException(Exception): pass
class MatchScoreOptionTypeException(Exception): pass
class MismatchScoreOptionTypeException(Exception): pass
class GapOpenScoreOptionTypeException(Exception): pass
class GapExtendScoreOptionTypeException(Exception): pass
class ClippingOptionTypeException(Exception): pass

# service files
FRAGMENTS_FNAME_F = 'fragments.fwd' # (for serialization) FWD file name to store RRBS fragments
FRAGMENTS_FNAME_R = 'fragments.rev' # (for serialization) REV file name to store RRBS fragments
FRAGMENTS_FNAME = 'fragments.info' # to store valid fragments info
REF_NAMES_CONVERSION_FNAME = 'ref_name.map'
REFERENCE_FNAME = 'ref.ser' # used for serialization
ALIGNMENTS_FNAME = 'alignments.sam'
TRIMMED_FILE_PREFIX = 'trimmed_' # prefix used to store trimmed files
UTILS_PATH='utils/' 

def check_file(filename):
    with open(filename) as f: pass
    
def check_dir(f):
    f = os.path.expanduser(f)
    d = os.path.dirname(f)
    if (os.path.exists(d)==False):
        raise DirectoryError('%s directory does not exist'%(f))

def ensure_dir(f):
    if not os.path.exists(f):
        os.makedirs(f)

def create_path(path):
    path = os.path.abspath(path)
    if (os.path.exists(path)==True): raise DirectoryError('%s directory exists'%(path)) 
    else:
      head, tail = os.path.split(path) 
      tree=''
      for p in head.split('/'): 
	if p!='':
	  tree+='/'+p
	  ensure_dir(tree)
      tree+='/'+tail
      ensure_dir(tree)
     
def check_BS_protocol(protocol):
    if protocol not in [1 , 2]:
        raise BSProtocolError()

def check_soap3_mismatches(mismatches):
    try:
        mismatches = int(mismatches)
    except ValueError: raise SOAP3MisOptionTypeException()
    if (mismatches > 4 or mismatches<0):
        raise SOAP3MismatchesError()
    return mismatches   


def detect_query_format(reads_fname):
    '''
    Detect the format of the reads. Only FASTA and FASTQ format are supported.
    '''
    query_file=open(reads_fname,'r')
    header=query_file.readline()
    query_file.close()

    if header[0] not in ['@', '>']: raise QueryFormatException
    return header[0]=='@' and 'Illumina GAII FastQ' or 'fasta'

def get_logger(log_file):
    '''
    A log manager
    '''
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger = logging.getLogger('GPU-BSM')
    logger.addHandler(console)
    hdlr = logging.FileHandler(log_file)

    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)

    return logger

def count_devices():
    '''
    Return the number of installed GPU cards
    '''
    driver.init()
    return driver.Device.count()

def check_gpu_id(dev_id, n_dev):
    '''
    Check if the selected gpu is valid
    '''
    try:
        dev_id = int(dev_id)
    except ValueError: raise GPUOptionTypeException()
    if (dev_id not in range(n_dev)):
        raise InvalidGPUidException()
    return dev_id
    
def check_n_reads(n_reads):
    try:
	n_reads = int(n_reads)
    except ValueError: raise NReadsOptionTypeException()
    return n_reads

def check_type_of_hits(type_of_hits):
    '''
    Check if the set H option is valid
    '''
    try:
        type_of_hits = int(type_of_hits)
    except ValueError: raise HitsOptionTypeException()
    if type_of_hits not in range(4)[1:]:
        raise InvalidHitsOptionException()
    return type_of_hits

def check_mismatches(mismatches):
    '''
    Check if the set m option is valid
    '''
    try:
        mismatches = int(mismatches)
    except ValueError: raise MismatchesOptionTypeException()
    if mismatches < 0:
        raise MismatchesOptionException()
    return mismatches


def check_ed_limit(ed_distance):
    '''
    Check if the set I option is valid
    '''
    try:
        ed_distance = int(ed_distance)
    except ValueError: raise EDLimitOptionTypeException()
    if ed_distance < 0:
        raise EDLimitOptionException()
    return ed_distance

def get_devices(n_dev, library):
    '''
    Return devices (ids) that will be exploited by GPU-BSM according to the user specified options, installed GPUs, and bs library
    '''
    if n_dev==1: return 0 # a single gpu card installed
    else: # multiple GPUs installed (at least 2)
        if library==1: return range(2) # Lister library
        else: # Cockus library
            if n_dev>=4: return range(4)
            else: return range(2)

def is_single_end(s, p1, p2):
    '''
    Detect errors in the type (single/pair - end) of the required alignment
    '''
    if s!=None:
        if (p1!=None or p2!=None): raise QueryException()
        return True
    elif (p1!=None):
        if (s!=None): raise QueryException()
        if (p2==None): raise QueryException()
        return False
    elif (p2!=None):
        if (s!=None): raise QueryException()
        if (p1==None): raise QueryException()
        return False
    elif (s==None and p1==None and p2==None): raise QueryException()


def check_red_site_length(length):
    '''
    Check if the lengths for the DNA fragments (RRBS) are valid 
    '''
    try:
        length = int(length)
    except ValueError: raise REDSizeOptionTypeException()
    return length
    

def check_max_hits(max_hits):
    '''
    Check if the lengths for the DNA fragments (RRBS) are valid 
    '''
    try:
        max_hits = int(max_hits)
    except ValueError: raise MaxHitsOptionTypeException()
    return max_hits

def check_alignment_scores(m_s, ms_s, go_s, ge_s):
    '''
    Check if the alignment scores options are valid values
    '''
    try:
        m_s = int(m_s)
    except ValueError: raise MatchScoreOptionTypeException()
    try:
        ms_s = int(ms_s)
    except ValueError: raise MismatchScoreOptionTypeException()
    try:
        go_s = int(go_s)
    except ValueError: raise GapOpenScoreOptionTypeException()
    try:
        ge_s = int(ge_s)
    except ValueError: raise GapExtendScoreOptionTypeException()
    return m_s, ms_s, go_s, ge_s
  

def check_clipping(max_fl_clip, max_el_clip):
   try:
     max_fl_clip = int(max_fl_clip)
     max_el_clip = int(max_el_clip)
   except ValueError: raise ClippingOptionTypeException()
   return max_fl_clip, max_el_clip 
   

def change_soap3_ini_file(soap_path, max_mismatches, dp, max_hits, end_to_end, m_s, ms_s, go_s, ge_s, max_fl_clip, max_el_clip):
    
    fin = open(soap_path+"soap3-dp.ini")
    fout = open(soap_path+"soap3-dp.ini~", "wt")

    for line in fin:
        if line.startswith('Soap3MisMatchAllow'):
	    newline = 'Soap3MisMatchAllow='+str(max_mismatches)+'\n'
            fout.write(line.replace(line, newline))  # replace and write
        elif line.startswith('SkipSOAP3Alignment'):
	    if dp==False: newline = 'SkipSOAP3Alignment=0\n'
	    elif dp==True: newline = 'SkipSOAP3Alignment=1\n'
	    if end_to_end: newline = 'SkipSOAP3Alignment=1\n'
            fout.write(line.replace(line, newline))  # replace and write
        elif line.startswith('MaxOutputPerRead'):
	    newline = 'MaxOutputPerRead='+str(max_hits)+'\n'
            fout.write(line.replace(line, newline))  # replace and write
        elif line.startswith('MaxOutputPerPair'):
	    newline = 'MaxOutputPerPair='+str(max_hits)+'\n'
            fout.write(line.replace(line, newline))  # replace and write    
        elif line.startswith('MaxFrontLenClipped'):
	    if end_to_end: newline = 'MaxFrontLenClipped='+str(0)+'\n'
            else: newline = 'MaxFrontLenClipped='+str(max_fl_clip)+'\n' # original value
            fout.write(line.replace(line, newline))  # replace and write  
        elif line.startswith('MaxEndLenClipped'):        
	    if end_to_end: newline = 'MaxEndLenClipped='+str(0)+'\n'
            else: newline = 'MaxEndLenClipped='+str(max_el_clip)+'\n' # original value
            fout.write(line.replace(line, newline))  # replace and write  
        elif line.startswith('MatchScore'):
	    newline = 'MatchScore='+str(m_s)+'\n'
            fout.write(line.replace(line, newline))  # replace and write
        elif line.startswith('MismatchScore'):
	    newline = 'MismatchScore='+str(ms_s)+'\n'
            fout.write(line.replace(line, newline))  # replace and write
        elif line.startswith('GapOpenScore'):
	    newline = 'GapOpenScore='+str(go_s)+'\n'
            fout.write(line.replace(line, newline))  # replace and write   
        elif line.startswith('GapExtendScore'):
	    newline = 'GapExtendScore='+str(ge_s)+'\n'
            fout.write(line.replace(line, newline))  # replace and write      
        else: fout.write(line)

    fin.close()
    fout.close()
    os.rename(soap_path+'soap3-dp.ini~',soap_path+'soap3-dp.ini')
    
    
def IUPAC(n):
  return {
    'A':('A'), 
    'C':('C'), 
    'G':('G'), 
    'T':('T'),
    'R':('A','G'), 
    'Y':('C','T'), 
    'S':('G','C'),
    'W':('A','T'), 
    'K':('G','T'), 
    'M':('A','C'), 
    'B':('C','G','T'), 
    'D':('A','G','T'), 
    'H':('A','C','T'),
    'V':('A','C','G'), 
    'N':('A','C','G','T')
  }[n]
  
  
def remove_adapters(adapters, in_fname, out_fname, info_file, overlap=3, error_rate=0.1):
  '''
  Use cutadapt to remove adapters
  '''
  remove=Popen('nohup cutadapt --info-file=%s -e %s -O %s -o %s -a %s %s'%(info_file, str(error_rate), str(overlap), out_fname, adapters, in_fname),shell=True)
  remove.wait()
  
  
def check_threads_option(n_threads):
  '''
  Check if the n_threads option is valid
  '''
  try:
    n_threads=int(n_threads)
  except ValueError: raise ThreadsOptionTypeException()  
  #if n_threads > multiprocessing.cpu_count(): raise ThreadsOptionException()  
  return n_threads
  
