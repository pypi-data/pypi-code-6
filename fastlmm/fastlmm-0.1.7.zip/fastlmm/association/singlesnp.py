from fastlmm.util.runner import *
import logging
import fastlmm.pyplink.plink as plink
import pysnptools.pysnptools.util.util as srutil
import fastlmm.util.util as flutil
import numpy as np
from fastlmm.inference import LMM
import scipy.stats as stats
from pysnptools.pysnptools.snpreader.bed import Bed
from fastlmm.util.pickle_io import load, save
import time
import pysnptools.pysnptools.util.util as srutil


def single_snp(test_snps,phen,cov=None,sid_list=None,
                 G0=None, G1=None, mixing=0.0, log_delta=None, min_log_delta=-5, max_log_delta=10, output_file=None,
                 cache_file = None,
                 runner=None):
    """
    Function performing single SNP GWAS with ML (never REML).

    :param test_snps: SNPs to test. If you give a string, it should be the base name of a set of PLINK Bed-formatted files.
    :type test_snps: a :class:`.SnpReader` or a string

    :param phen: A single phenotype: A 'pheno dictionary' contains an ndarray on the 'vals' key and a iid list on the 'iid' key.
      If you give a string, it should be the file name of a PLINK phenotype-formatted file.
    :type phen: a 'pheno dictionary' or a string

    :param cov: covariate information, optional: A 'pheno dictionary' contains an ndarray on the 'vals' key and a iid list on the 'iid' key.
      If you give a string, it should be the file name of a PLINK phenotype-formatted file.
    :type cov: a 'pheno dictionary' or a string

    :param sid_list: list of sids, optional:
            sids will be evaluated.
            If you give no sid_list, all sids in test_snps will be used.
    :type sid_list: list of strings

    :param G0: SNPs from which to construct a similarity kernel, optional. If you give no G0, the SNPs in test_snps will be used.
          If you give a string, it should be the base name of a set of PLINK Bed-formatted files.
    :type G0: a :class:`.SnpReader` or a string

    :param G1: values from which to construct another kernel, optional. If you give no G1, only G0 will be used. (Also, see 'mixing').
            A 'pheno dictionary' contains an ndarray on the 'vals' key and a iid list on the 'iid' key.
            If you give a string, it should be the file name of a PLINK phenotype-formatted file.
    :type G1: a 'pheno dictionary' or a string

    :param mixing: Weight between 0.0 (inclusive, default) and 1.1 (inclusive) given to G1 relative to G0.
            If you give no mixing number, G0 will get all the weight and G1 will be ignored.
    :type mixing: number

    :param log_delta: A parameter to LMM learning, optional
            If not given will search for best value.
    :type log_delta: number

    :param min_log_delta: (default:-5)
            When searching for log_delta, the lower bounds of the search.
    :type min_log_delta: number

    :param max_log_delta: (default:-5)
            When searching for log_delta, the upper bounds of the search.
    :type max_log_delta: number

    :param output_file: Name of file to write results to, optional. If not given, no output file will be created.
    :type output_file: file name

    :param cache_file: Name of  file to read or write cached precomutation values to, optional.
                If not given, no cache file will be used.
                If given and file does not exists, will write precomputation values to file.
                If given and file does exists, will read precomputation values from file.
                The file contains the U and S matrix from the decomposition of the training matrix. It is in Python's np.savez (*.npz) format.
                Calls using the same cache file should have the same 'G0'
    :type cache_file: file name

    :param runner: a runner, optional: Tells how to run locally, multi-processor, or on a cluster.
        If not given, the function is run locally.
    :type runner: a runner.

    :rtype: Two ndarrays of the same length. The first gives the sids. The second gives the pValue of that sid. Sorted by pValue.

    :Example:

    >>> import logging
    >>> from pysnptools.pysnptools.snpreader.bed import Bed
    >>> logging.basicConfig(level=logging.INFO)
    >>> test_snps = Bed('../../tests/datasets/all_chr.maf0.001.N300')
    >>> phen = r'../../tests/datasets/phenSynthFrom22.23.N300.randcidorder.txt'
    >>> cov = r'../../tests/datasets/all_chr.maf0.001.covariates.N300.txt'
    >>> sid_list,pvalue_list = single_snp(test_snps, phen, cov=cov, 
    ...                                 sid_list=test_snps.sid[:10]) #first 10 snps
    >>> print sid_list,round(pvalue_list[0],5),len(pvalue_list)
    1_12 0.07779 85

    """

    if runner is None:
        runner = Local()

    fastlmm = _SingleSnp(test_snps,phen,cov,sid_list, G0, G1, mixing, log_delta, min_log_delta, max_log_delta, output_file, cache_file)
    logging.info("# of sids is {0}".format(fastlmm.sid_count))
    fastlmm.fill_in_cache_file()
    result = runner.run(fastlmm)
    return result

def write(sid_list, pvalue_list, output_file):
    """
    Given two arrays of the same length [as per the output of fastlmm(...)], writes a header and the values to the given output file.
    """
    with open(output_file,"w") as out_fp:
        out_fp.write("{0}\t{1}\n".format("sid","pvalue"))
        for i in xrange(len(pvalue_list)):
            out_fp.write("{0}\t{1}\n".format(sid_list[i],pvalue_list[i]))


# could this be written without the inside-out of IDistributable?
class _SingleSnp(object) : #implements IDistributable

    def __init__(self,test_snps,phen,cov=None,sid_list=None,
                 G0=None, G1=None, mixing=0.0, log_delta=None, min_log_delta=-5, max_log_delta=10, output_file=None, cache_file=None):
        self.test_snps = test_snps
        self.phen = phen
        self.output_file_or_none = output_file
        self.cache_file = cache_file
        self.cov = cov
        self.sid_list = sid_list
        self.G0=G0
        self.G1_or_none=G1
        self.mixing=mixing
        self.external_log_delta=log_delta
        self.min_log_delta = min_log_delta
        self.max_log_delta = max_log_delta
        self._ran_once = False
        self._str = "{0}({1},{2},cov={3},sid_list_0={4},G0={6},G1={7},mixing={8},log_delta={9},min_log_delta={10},max_log_delta={11},output_file={12},cache_file={13})".format(
            self.__class__.__name__, self.test_snps,self.phen,self.cov,self.sid_list,None,
                 self.G0, self.G1_or_none, self.mixing, self.external_log_delta, self.min_log_delta, self.max_log_delta, output_file, cache_file)
        self.block_size = 1000

    def _run_once(self):
        #!!!cmk this code (and must of the code in fastlmm.py) is almost the same as epistasis.py
        if self._ran_once:
            return
        self._ran_once = None

        if isinstance(self.test_snps, str):
            self.test_snps = Bed(self.test_snps)

        if self.G0 is None:
            self.G0 = self.test_snps
        elif isinstance(self.G0, str):
            self.G0 = Bed(self.G0)

        if isinstance(self.phen, str):
            self.phen = plink.loadOnePhen(self.phen,vectorize=True) #!!!cmk07292014 what about missing=-9?

        if self.cov is not None and isinstance(self.cov, str):
            self.cov = plink.loadPhen(self.cov)#!!!cmk07292014 what about missing=-9?

        if self.G1_or_none is not None and isinstance(self.G1_or_none, str):
            self.G1_or_none = plink.loadPhen(self.G1_or_none)

        if self.sid_list is None:
            self.sid_list = self.test_snps.sid

        self.test_snps, self.phen, self.cov, self.G0, self.G1_or_none = srutil.intersect_apply([self.test_snps, self.phen, self.cov, self.G0, self.G1_or_none]) #should put G0 and G1 first

        #cmk07292014 for now always add 1's, Should fix up to add only of no constant columns - will need to add a test case for this
        if self.cov is None:
            self.cov = np.ones((self.test_snps.iid_count, 1))
        else:
            self.cov = np.hstack((self.cov['vals'],np.ones((self.test_snps.iid_count, 1))))
        self.n_cov = self.cov.shape[1] 


        if self.output_file_or_none is None:
            self.__tempdirectory = ".working"
        else:
            self.__tempdirectory = self.output_file_or_none + ".working"

        self._ran_once = True
        

 #start of IDistributable interface--------------------------------------
    @property
    def work_count(self):
        self._run_once()
        block_count = self.div_ceil(self.sid_count, self.block_size)
        return block_count



    def work_sequence(self):
        self._run_once()

        return self.work_sequence_range(0,self.work_count)

    def work_sequence_range(self, start, end):
        self._run_once()

        lmm = self.lmm_from_cache_file()
        lmm.sety(self.phen['vals'])

        for sid_list in self.pair_block_sequence_range(start,end):
            yield lambda lmm=lmm,sid_list=sid_list : self.do_work(lmm,sid_list,)  # the 'lmm=lmm,...' is need to get around a strangeness in Python

    def reduce(self, result_sequence):
        #doesn't need "run_once()"

        #!!! would be better to use a table-like data structure
        result_list = []
        for result_sub in result_sequence:
            result_list.extend(result_sub)

            if len(result_list) % 1000 == 0:
                logging.info("reducing combination {0}".format(len(result_sub)))
        result_list.sort() # doing a full sort so that tied pvalue_list will be sorted by the sid's

        sid_list = []
        pvalue_list = []
        for pvalue,sid, in result_list:
            sid_list.append(sid)
            pvalue_list.append(pvalue)



        if self.output_file_or_none is not None:
            write(sid_list, pvalue_list, self.output_file_or_none)
        return sid_list, pvalue_list


    @property
    def tempdirectory(self):
        self._run_once()
        return self.__tempdirectory

    #optional override -- the str name of the instance is used by the cluster as the job name
    def __str__(self):
        #Doesn't need run_once
        return self._str


    def copyinputs(self, copier):
        self._run_once()
        if isinstance(self.test_snps, str):
            copier.input(self.test_snps + ".bed")
            copier.input(self.test_snps + ".bim")
            copier.input(self.test_snps + ".fam")
        else:
            copier.input(self.test_snps)

        copier.input(self.phen)
        copier.input(self.cov)

        if isinstance(self.G0, str):
            copier.input(self.G0 + ".bed")
            copier.input(self.G0 + ".bim")
            copier.input(self.G0 + ".fam")
        else:
            copier.input(self.G0)

        copier.input(self.G1_or_none)
        copier.input(self.cache_file)

    def copyoutputs(self,copier):
        #Doesn't need run_once
        copier.output(self.output_file_or_none)

 #end of IDistributable interface---------------------------------------

    @staticmethod
    def div_ceil(num, den): #cmk!!!move to utils!!! (code also in epistasis)
        return -(-num//den) #The -/- trick makes it do ceiling instead of floor. "//" will do integer division even in the future and on floats.
    
    def pair_block_sequence_range(self,block_start,block_end):
        self._run_once()
        assert 0 <= block_start and block_start <= block_end and block_end <= self.work_count, "real assert"

        for block_index in xrange(block_start,block_end):
            start = block_index * self.sid_count // self.work_count
            next_start = (block_index+1) * self.sid_count // self.work_count
            yield self.sid_list[start:next_start]


    @property
    def sid_count(self):
        self._run_once()
        return len(self.sid_list)

    #!!!cmk same code in epstasis
    def lmm_from_cache_file(self):
        logging.info("Loading precomputation from {0}".format(self.cache_file))
        lmm = LMM()
        with np.load(self.cache_file) as data:
            lmm.U = data['arr_0']
            lmm.S = data['arr_1']
        return lmm

    #!!!cmk almost same code in epstasis
    def fill_in_cache_file(self):
        self._run_once()

        logging.info("filling in the cache_file and log_delta, as needed")

        if self.G1_or_none is None:
            self.G1val_or_none = None
        else:
            self.G1val_or_none = self.G1_or_none['vals']

        # The S and U are always cached, in case they are needed for the cluster or for multi-threaded runs
        if self.cache_file is None:
            self.cache_file = os.path.join(self.__tempdirectory, "cache_file.npz")
            if os.path.exists(self.cache_file): # If there is already a cache file in the temp directory, it must be removed because it might be out-of-date
                os.remove(self.cache_file)

        lmm = None
        if not os.path.exists(self.cache_file):
            logging.info("Precomputing eigen")
            lmm = LMM()
            G0_standardized = self.G0.read().standardize()
            lmm.setG(G0_standardized.val, self.G1val_or_none, a2=self.mixing)
            logging.info("Saving precomputation to {0}".format(self.cache_file))
            util.create_directory_if_necessary(self.cache_file)
            np.savez(self.cache_file, lmm.U,lmm.S) #using np.savez instead of pickle because it seems to be faster to read and write

        if self.external_log_delta is None:
            if lmm is None:
                lmm = self.lmm_from_cache_file()

            logging.info("searching for internal delta")
            lmm.setX(self.cov)
            lmm.sety(self.phen['vals'])
            result = lmm.find_log_delta(REML=False, sid_count=self.G0.sid_count, min_log_delta=self.min_log_delta, max_log_delta=self.max_log_delta  ) #!!!what about findA2H2? minH2=0.00001
            self.external_log_delta = result['log_delta']

        self.internal_delta = np.exp(self.external_log_delta) * self.G0.sid_count
        logging.info("internal_delta={0}".format(self.internal_delta))
        logging.info("external_log_delta={0}".format(self.external_log_delta))


    do_count = 0
    do_time = time.time()

    def do_work(self, lmm, sid_list):
        result_list = []

        sid_index_list = self.test_snps.sid_to_index(sid_list)
        snps_read = self.test_snps[:,sid_index_list].read().standardize()

        X = np.hstack((self.cov, snps_read.val))
        UX = lmm.U.T.dot(X)
        k = lmm.S.shape[0]
        N = X.shape[0]
        if (k<N):
            UUX = X - lmm.U.dot(UX)
        else:
            UUX = None

        for sid_index, sid in enumerate(sid_list):

            index_list_alt = np.array([sid_index]) #index to product
            index_list_alt = index_list_alt + self.cov.shape[1] #Shift by the number of values in the cov
            index_list_alt = np.hstack((np.arange(self.cov.shape[1]),index_list_alt)) #indexes of the cov
            index_list_null = index_list_alt[:-1] #index to cov, not snp

            #Null -- just the cov
            lmm.X = X[:,index_list_null]
            lmm.UX = UX[:,index_list_null]
            if (k<N):
                lmm.UUX = UUX[:,index_list_null]
            else:
                lmm.UUX = None
            res_null = lmm.nLLeval(delta=self.internal_delta, REML=False)
            ll_null = -res_null["nLL"]

            #Alt -- now with the snp as a feature, too
            lmm.X = X[:,index_list_alt]
            lmm.UX = UX[:,index_list_alt]
            if (k<N):
                lmm.UUX = UUX[:,index_list_alt]
            else:
                lmm.UUX = None
            res_alt = lmm.nLLeval(delta=self.internal_delta, REML=False)
            ll_alt = -res_alt["nLL"]

            test_statistic = ll_alt - ll_null
            degrees_of_freedom = 1
            pvalue = stats.chi2.sf(2.0 * test_statistic, degrees_of_freedom)
            logging.debug("{0}, null={2}, alt={3}, pvalue={4}".format(sid,None,ll_null,ll_alt,pvalue))
            result_list.append((pvalue, sid))

            self.do_count += 1
            if self.do_count % 100 == 0:
                start = self.do_time
                self.do_time = time.time()
                logging.info("do_count={0}, time={1}".format(self.do_count,self.do_time-start))

        return result_list


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    import doctest
    doctest.testmod()

    print "done"

