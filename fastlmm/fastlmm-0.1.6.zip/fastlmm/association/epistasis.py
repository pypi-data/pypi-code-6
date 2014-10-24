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

def epistasis(test_snps,phen,cov=None,sid_list_0=None,sid_list_1=None,
                 G0=None, G1=None, mixing=0.0, log_delta=None, min_log_delta=-5, max_log_delta=10, output_file=None,
                 cache_file = None,
                 runner=None):
    """
    Function performing epistasis GWAS with ML (never REML).  See http://www.nature.com/srep/2013/130122/srep01099/full/srep01099.html.

    :param test_snps: SNPs from which to test pairs. If you give a string, it should be the base name of a set of PLINK Bed-formatted files.
    :type test_snps: a :class:`.SnpReader` or a string

    :param phen: A single phenotype: A 'pheno dictionary' contains an ndarray on the 'vals' key and a iid list on the 'iid' key.
      If you give a string, it should be the file name of a PLINK phenotype-formatted file.
    :type phen: a 'pheno dictionary' or a string

    :param cov: covariate information, optional: A 'pheno dictionary' contains an ndarray on the 'vals' key and a iid list on the 'iid' key.
      If you give a string, it should be the file name of a PLINK phenotype-formatted file.
    :type cov: a 'pheno dictionary' or a string

    :param sid_list_0: list of sids, optional:
            All unique pairs from sid_list_0 x sid_list_1 will be evaluated.
            If you give no sid_list_0, all sids in test_snps will be used.
    :type sid_list_0: list of strings

    :param sid_list_1: list of sids, optional:
            All unique pairs from sid_list_0 x sid_list_1 will be evaluated.
            If you give no sid_list_1, all sids in test_snps will be used.
    :type sid_list_1: list of strings

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

    :rtype: Three ndarrays of the same length. The first two give the sids of a pair. The third gives the pValue of that pair. Sorted by pValue.

    :Example:

    >>> import logging
    >>> from pysnptools.pysnptools.snpreader.bed import Bed
    >>> logging.basicConfig(level=logging.INFO)
    >>> test_snps = Bed('../../tests/datasets/all_chr.maf0.001.N300')
    >>> phen = r'../../tests/datasets/phenSynthFrom22.23.N300.randcidorder.txt'
    >>> cov = r'../../tests/datasets/all_chr.maf0.001.covariates.N300.txt'
    >>> sid0_list,sid1_list,pvalue_list = epistasis(test_snps, phen, cov=cov, 
    ...                                 sid_list_0=test_snps.sid[:10], #first 10 snps
    ...                                 sid_list_1=test_snps.sid[5:15]) #Skip 5 snps, use next 10
    >>> print sid0_list[0],sid1_list[0],round(pvalue_list[0],5),len(pvalue_list)
    1_12 1_9 0.07779 85

    """

    if runner is None:
        runner = Local()

    epistasis = _Epistasis(test_snps,phen,cov,sid_list_0,sid_list_1, G0, G1, mixing, log_delta, min_log_delta, max_log_delta, output_file, cache_file)
    logging.info("# of pairs is {0}".format(epistasis.pair_count))
    epistasis.fill_in_cache_file()
    result = runner.run(epistasis)
    return result

def write(sid0_list, sid1_list, pvalue_list, output_file):
    """
    Given three arrays of the same length [as per the output of epistasis(...)], writes a header and the values to the given output file.
    """
    with open(output_file,"w") as out_fp:
        out_fp.write("{0}\t{1}\t{2}\n".format("sid0","sid1","pvalue"))
        for i in xrange(len(pvalue_list)):
            out_fp.write("{0}\t{1}\t{2}\n".format(sid0_list[i],sid1_list[i],pvalue_list[i]))


# could this be written without the inside-out of 
class _Epistasis(object) : #implements IDistributable

    def __init__(self,test_snps,phen,cov=None,sid_list_0=None,sid_list_1=None,
                 G0=None, G1=None, mixing=0.0, log_delta=None, min_log_delta=-5, max_log_delta=10, output_file=None, cache_file=None):
        self.test_snps = test_snps
        self.phen = phen
        self.output_file_or_none = output_file
        self.cache_file = cache_file
        self.cov = cov
        self.sid_list_0 = sid_list_0
        self.sid_list_1 = sid_list_1
        self.G0=G0
        self.G1_or_none=G1
        self.mixing=mixing
        self.external_log_delta=log_delta
        self.min_log_delta = min_log_delta
        self.max_log_delta = max_log_delta
        self._ran_once = False
        self._str = "{0}({1},{2},cov={3},sid_list_0={4},sid_list_1{5},G0={6},G1={7},mixing={8},log_delta={9},min_log_delta={10},max_log_delta={11},output_file={12},cache_file={13})".format(
            self.__class__.__name__, self.test_snps,self.phen,self.cov,self.sid_list_0,self.sid_list_1,
                 self.G0, self.G1_or_none, self.mixing, self.external_log_delta, self.min_log_delta, self.max_log_delta, output_file, cache_file)
        self.block_size = 1000

    def set_sid_sets(self):
        sid_set_0 = set(self.sid_list_0)
        self.intersect = sid_set_0.intersection(self.sid_list_1)
        self.just_sid_0 = sid_set_0.difference(self.intersect)
        self.just_sid_1 = self.intersect.symmetric_difference(self.sid_list_1)
        self._pair_count = len(self.just_sid_0)*len(self.intersect) + len(self.just_sid_0)*len(self.just_sid_1) + len(self.intersect)*len(self.just_sid_1) + len(self.intersect) * (len(self.intersect)-1)//2
        self.test_snps, self.phen, self.cov, self.G0, self.G1_or_none = srutil.intersect_apply([self.test_snps, self.phen, self.cov, self.G0, self.G1_or_none])

    def _run_once(self):
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

        if self.sid_list_0 is None:
            self.sid_list_0 = self.test_snps.sid

        if self.sid_list_1 is None:
            self.sid_list_1 = self.test_snps.sid

        self.set_sid_sets()

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
        block_count = self.div_ceil(self._pair_count, self.block_size)
        return block_count



    def work_sequence(self):
        self._run_once()

        return self.work_sequence_range(0,self.work_count)

    def work_sequence_range(self, start, end):
        self._run_once()

        lmm = self.lmm_from_cache_file()
        lmm.sety(self.phen['vals'])

        for sid0_list, sid1_list in self.pair_block_sequence_range(start,end):
            yield lambda lmm=lmm,sid0_list=sid0_list,sid1_list=sid1_list : self.do_work(lmm,sid0_list,sid1_list)  # the 'sid0=sid0,sid1=sid1,...' is need to get around a strangeness in Python

    def reduce(self, result_sequence):
        #doesn't need "run_once()"

        #!!! would be better to use a table-like data structure
        result_list = []
        for result_sub in result_sequence:
            result_list.extend(result_sub)

            if len(result_list) % 1000 == 0:
                logging.info("reducing combination {0}".format(len(result_sub)))
        result_list.sort() # doing a full sort so that tied pvalue_list will be sorted by the sid's

        sid0_list = []
        sid1_list = []
        pvalue_list = []
        for pvalue,sid0,sid1 in result_list:
            sid0_list.append(sid0)
            sid1_list.append(sid1)
            pvalue_list.append(pvalue)



        if self.output_file_or_none is not None:
            write(sid0_list, sid1_list, pvalue_list, self.output_file_or_none)
        return sid0_list, sid1_list, pvalue_list


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
    def div_ceil(num, den): #!!!move to utils?
        return -(-num//den) #The -/- trick makes it do ceiling instead of floor. "//" will do integer division even in the future and on floats.
    
    def pair_block_sequence_range(self,block_start,block_end):
        self._run_once()
        assert 0 <= block_start and block_start <= block_end and block_end <= self.work_count, "real assert"

        block_index = block_start
        start = block_index * self.pair_count // self.work_count
        next_start = (block_index+1) * self.pair_count // self.work_count
        size_goal = next_start - start
        end = block_end * self.pair_count // self.work_count

        sid0_list = []
        sid1_list = []
        for sid0, sid1 in self.pair_sequence_range(start,end):
            sid0_list.append(sid0)
            sid1_list.append(sid1)
            if len(sid0_list) == size_goal:
                yield sid0_list, sid1_list
                block_index += 1
                if block_index == block_end:
                    return
                sid0_list = []
                sid1_list = []
                start = next_start
                next_start = (block_index+1) * self.pair_count // self.work_count
                size_goal = next_start - start
        assert len(sid0_list) == 0, "real assert"

    #If start == end, then returns without yielding anything 
    def pair_sequence_range(self,start,end):
        self._run_once()
        assert 0 <= start and start <= end and end <= self._pair_count, "real assert"

        i = start
        for sid0, sid1 in self.pair_sequence_with_start(start):
            yield sid0, sid1
            i = i + 1
            if i == end:
                break
        assert i == end, "Not enough items found. Didn't get to the end"


    def pair_sequence_with_start(self,start):
        self._run_once()

        skip_ref = [start]

        just_sid_0_list = list(self.just_sid_0)
        just_sid_1_list = list(self.just_sid_1)
        intersect_list = list(self.intersect)

        for sid0, sid1 in self.combo_distinct(just_sid_0_list, intersect_list, skip_ref):
            yield sid0, sid1
        for sid0, sid1 in self.combo_distinct(just_sid_0_list, just_sid_1_list, skip_ref):
            yield sid0, sid1
        for sid0, sid1 in self.combo_distinct(intersect_list, just_sid_1_list, skip_ref):
            yield sid0, sid1
        for sid0, sid1 in self.combo_same(intersect_list, skip_ref):
            yield sid0, sid1
        assert skip_ref[0] == 0, "real assert"


    def combo_distinct(self, distinct__list0, distinct__list1, skip_ref):
        row_count = len(distinct__list0)
        col_count = len(distinct__list1)

        if skip_ref[0] >= row_count * col_count:
            skip_ref[0] = skip_ref[0] - row_count * col_count
            assert skip_ref[0] >=0, "real assert"
            return

        row_start = skip_ref[0] // col_count
        skip_ref[0] = skip_ref[0] - row_start * col_count
        assert skip_ref[0] >=0, "real assert"

        for row_index in xrange(row_start, row_count):
            sid0 = distinct__list0[row_index]
            if row_index == row_start:
                col_start = skip_ref[0]
                skip_ref[0] = 0
            else:
                col_start = 0
            for col_index in xrange(col_start, col_count):
                sid1 = distinct__list1[col_index]
                yield sid0, sid1

    def combo_same(self, list, skip_ref):
        count = len(list)
        full_size = count * (count + 1) // 2
        if skip_ref[0] >= full_size:
            skip_ref[0] = skip_ref[0] - full_size
            assert skip_ref[0] >=0, "real assert"
            return

        row_start = int((-1 + 2*count - np.sqrt(1 - 4*count + 4*count**2 - 8*skip_ref[0]))/2)
        skip_ref[0] = skip_ref[0] - (count*row_start - (row_start*(1 + row_start))//2)
        assert skip_ref[0] >=0, "real assert"

        for row_index in xrange(row_start, count):
            sid0 = list[row_index]
            if row_index == row_start:
                col_start = skip_ref[0]
                skip_ref[0] = 0
            else:
                col_start = 0
            for col_index in xrange(col_start + 1 + row_index, count):
                sid1 = list[col_index]
                assert sid0 is not sid1, "real assert"
                yield sid0, sid1



    @property
    def pair_count(self):
        self._run_once()
        return self._pair_count

    def lmm_from_cache_file(self):
        logging.info("Loading precomputation from {0}".format(self.cache_file))
        lmm = LMM()
        with np.load(self.cache_file) as data:
            lmm.U = data['arr_0']
            lmm.S = data['arr_1']
        return lmm

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
    do_pair_count = 0
    do_pair_time = time.time()

    def do_work(self, lmm, sid0_list, sid1_list):
        result_list = []

        #This is some of the code for a different way that reads and dot-products 50% more, but does less copying. Seems about the same speed
        #sid0_index_list = self.test_snps.sid_to_index(sid0_list)
        #sid1_index_list = self.test_snps.sid_to_index(sid1_list)
        #sid_index_union_dict = {}
        #sid0_index_index_list = self.create_index_index(sid_index_union_dict, sid0_index_list)
        #sid1_index_index_list = self.create_index_index(sid_index_union_dict, sid1_index_list)
        #snps0_read = self.test_snps[:,sid0_index_list].read().standardize()
        #snps1_read = self.test_snps[:,sid1_index_list].read().standardize()

        sid_union = set(sid0_list).union(sid1_list)
        sid_union_index_list = sorted(self.test_snps.sid_to_index(sid_union))
        snps_read = self.test_snps[:,sid_union_index_list].read().standardize()

        sid0_index_list = snps_read.sid_to_index(sid0_list)
        sid1_index_list = snps_read.sid_to_index(sid1_list)

        products = snps_read.val[:,sid0_index_list] * snps_read.val[:,sid1_index_list] # in the products matrix, each column i is the elementwise product of sid i in each list
        X = np.hstack((self.cov, snps_read.val, products))
        UX = lmm.U.T.dot(X)
        k = lmm.S.shape[0]
        N = X.shape[0]
        if (k<N):
            UUX = X - lmm.U.dot(UX)
        else:
            UUX = None

        for pair_index, sid0 in enumerate(sid0_list):
            sid1 = sid1_list[pair_index]

            index_list = np.array([pair_index]) #index to product
            index_list = index_list + len(sid_union_index_list) #Shift by the number of snps in the union
            index_list = np.hstack((np.array([sid0_index_list[pair_index],sid1_index_list[pair_index]]),index_list)) # index to sid0 and sid1
            index_list = index_list + self.cov.shape[1] #Shift by the number of values in the cov
            index_list = np.hstack((np.arange(self.cov.shape[1]),index_list)) #indexes of the cov

            index_list_less_product = index_list[:-1] #index to everything but the product

            #Null -- the two additive SNPs
            lmm.X = X[:,index_list_less_product]
            lmm.UX = UX[:,index_list_less_product]
            if (k<N):
                lmm.UUX = UUX[:,index_list_less_product]
            else:
                lmm.UUX = None
            res_null = lmm.nLLeval(delta=self.internal_delta, REML=False)
            ll_null = -res_null["nLL"]

            #Alt -- now with the product feature
            lmm.X = X[:,index_list]
            lmm.UX = UX[:,index_list]
            if (k<N):
                lmm.UUX = UUX[:,index_list]
            else:
                lmm.UUX = None
            res_alt = lmm.nLLeval(delta=self.internal_delta, REML=False)
            ll_alt = -res_alt["nLL"]

            test_statistic = ll_alt - ll_null
            degrees_of_freedom = 1
            pvalue = stats.chi2.sf(2.0 * test_statistic, degrees_of_freedom)
            logging.debug("<{0},{1}>, null={2}, alt={3}, pvalue={4}".format(sid0,sid1,ll_null,ll_alt,pvalue))
            result_list.append((pvalue, sid0, sid1))

            self.do_pair_count += 1
            if self.do_pair_count % 100 == 0:
                start = self.do_pair_time
                self.do_pair_time = time.time()
                logging.info("do_pair_count={0}, time={1}".format(self.do_pair_count,self.do_pair_time-start))

        return result_list


if __name__ == "__main__":
    #logging.basicConfig(level=logging.INFO)

    #import logging
    #from pysnptools.pysnptools.snpreader.bed import Bed
    #logging.basicConfig(level=logging.INFO)

    #os.chdir(r"C:\Source\carlk\july_7_14\fastlmm\feature_selection\examples")


    #test_snps = Bed('toydata')
    #phen = 'toydata.phe'
    #snp_list=["null_576","null_4684"]
    #sid_0,sid_1,pvalue_list = epistasis(test_snps, phen, sid_list_0=snp_list, sid_list_1=snp_list, log_delta=1.3853)
    #print sid_0[0],sid_1[0],round(pvalue_list[0],5),len(pvalue_list)


    logging.basicConfig(level=logging.INFO)

    from pysnptools.pysnptools.snpreader.bed import Bed
    from fastlmm.association.epistasis import epistasis, write
    from fastlmm.util.runner import Local, Hadoop, Hadoop2, HPC, LocalMultiProc, LocalInParts, LocalFromRanges


    os.chdir(r"d:\data\carlk\cachebio\genetics\wtccc\data")
    whole = Bed('filtered/wtcfb')

    runner = HPC(2, 'RR1-N13-09-H44',r'\\msr-arrays\Scratch\msr-pool\Scratch_Storage3\Redmond',
                    remote_python_parent=r"\\msr-arrays\Scratch\msr-pool\Scratch_Storage3\REDMOND\carlk\Source\carlk\july_7_14",
                    update_remote_python_parent=True,
                    priority="AboveNormal",unit="node")

    runner = LocalMultiProc(20)
    #runner = LocalFromRanges([2,9,10])
    #runner = LocalFromRanges([1,2,3,4,5,6,7,8,9,10])
    #runner = LocalFromRanges([1])
    #runner = Local()
    #runner = LocalInParts(100000000-22,100000000,mkl_num_threads=20)
    #runner = LocalInParts(10000000-22,10000000,mkl_num_threads=20)
    #runner = LocalInParts(0,10,mkl_num_threads=20)
    #runner = LocalInParts(2,10,mkl_num_threads=20)

    #snp_idx = whole.sid_to_index(["rs3798343","rs17146094"])
    #test_snps = whole[:,snp_idx]
    #sid_list_0=None
    #sid_list_1=None

    test_snps = whole
    num = 100
    sid_list_union = test_snps.sid[::int(test_snps.sid_count)/num]
    test_snps = whole
    sid_list_0=sid_list_union[:num*2//3]
    sid_list_1=sid_list_union[num//3:]

    #test_snps = whole
    ##sid_list_0 = test_snps.sid[-1:]
    ##sid_list_1 = test_snps.sid[:6]

    G0 = whole#[:,:200] #First snps
    phen = r'pheno\cad.txt'
    log_delta=1.11123 #None # 1.12266 #None #1.031585551
    cache_file = "whole.search.cache.npz"
    sid_0,sid_1,pvalue_list = epistasis(test_snps, phen, sid_list_0=sid_list_0,sid_list_1=sid_list_1, G0=G0, log_delta=log_delta,cache_file=cache_file,runner=runner)
    print sid_0[0],sid_1[0],round(pvalue_list[0],5),len(pvalue_list)


    #import doctest
    #doctest.testmod()

    print "done"

