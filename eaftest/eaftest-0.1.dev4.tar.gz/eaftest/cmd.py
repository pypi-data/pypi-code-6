# FIXME: Python 2 only!
# -*- coding: utf-8 -*-
# 

from __future__ import division, absolute_import, \
                       unicode_literals
from .utils.py3k import *

import sys, os
import time
import numpy as np
from . import datasets
from . import libaft
from . import bintools
from . import eaf_test_kscoarse as clkernel
from . import libeafbb as cpukernel

def main(args=None):
    if args == None:
        args = list(sys.argv)

    print "\nSecond-order EAF KS-like two-sample two-sided test"
    print "==================================================\n"
    
    if len(args) < 3:
        execname = os.path.basename(args[0])
        print "Usage: %s <fileA> <fileB>" % execname
        print "       %s -i <indicators_file>" % execname
        print 
        print "<fileA> and <fileB>: non-dominated sets of two-dimensional"
        print "                     objective vectors"
        print "<indicators_file>: point indicator file from the joint-eaf"
        print "                   computation"
        print
        return
    
    if args[1] == '-i':
        ind = main_load_ind(args[2])
    else:
        ind = main_load_nps(args[1], args[2])
    
    main_eaftest(ind)


def main_load_nps(fileA, fileB):
    """Load files and compute EAF (with text output)"""
    
    print "- Loading the following non-dominated sets of two-dimensional"
    print "  objective vectors and computing the joint-EAF:"
    print "  * A:", fileA
    print "  * B:", fileB
    print
    
    npsetA = datasets.load_nps(fileA)
    npsetB = datasets.load_nps(fileB)
    assert len(npsetA) == len(npsetB), ("The npsets must have the same length "
        "(i.e. same number of executions)")

    point_ind = eafindicators(npsetA, npsetB)
    return point_ind


def main_load_ind(indfile):
    """Load point indicator file"""
    print "- Loading the following file with attainment indicator values:"
    print "  *", indfile
    print
    
    point_ind = datasets.load_ind(indfile, flat=True)
    return point_ind

def main_eaftest(point_ind, permutations=10240, alpha=0.05):
    """
    Statistical hypothesis testing (with text output)
    - permutations: number of random permutations
    - alpha: significance level
    """
    
    # ------ Attainment indicator values information ------
    
    npoints = len(point_ind)
    nvars = len(point_ind[0])       # Número de execuções total
    nruns = nvars // 2              # Número de execuções de 1 algo
    
    print "- Attainment indicator values information:"
    print "  * Number of points:", npoints
    print "  * Joint executions:", nvars, "(%d + %d)" % (nruns, nruns)
    print
    
    assert nvars % 2 == 0, "Number of total joint executions must be even."
    assert nvars <= 64, "Not implemented with more than 64 joint executions."
    
    # ------ Test Statistic ------

    print "- Computing the test statistic..."    
    stat2 = libaft.ksstat(point_ind, order=2)
    print "  * Test statistic = %d/%d" % (stat2, nruns)
    print "                   = %f" % (stat2 / float(nruns)), '\n'
    
    # ------ Estimate null distribution ------

    print "- Using %d random permutations to estimate null distribution." % permutations
    print "  Please be patient..."
    maxdist = np.zeros(permutations, dtype=np.int32)    # Max distance array
    rtime = time.time()
    
    masks = bintools.make_masks(permutations, nvars, seed=64)
    for i, maxd in enumerate(cpukernel.runkernel(point_ind, masks)):
        maxdist[i] = maxd
        if (i+1) % (permutations//16) == 0:
            print "    %6d permutations, %7.3f sec" % (i+1, time.time()-rtime)
    print "  * Time elapsed: %7.3f" % (time.time()-rtime)
    
    # Compute null distribution from max distance array
    tail = np.bincount(maxdist, minlength=nruns+1)
    print "  * Non-normalized null distribution:"
    print tail
    print
    
    # ------ Accept/reject null hypothesis ------
    
    # NB: -1 resulta das diferentes convenções para a definição de valor crítico
    crit = criticalvalue(tail, alpha * permutations) - 1
    pval = pvalue(tail, stat2) / float(permutations)
    
    print "- Null hypothesis decision:"  
    print "  * Critical value = %d/%d" % (crit, nruns)
    print "                   = %f" % (crit / float(nruns))
    print "  * p-value = %f" % pval
    if pval <= alpha:
        print "            <= alpha (%s)\n" % alpha
        print "  * Decision: REJECT the null hypothesis"
    else:
        print "            > alpha (%s)\n" % alpha
        print "  * Decision: do NOT REJECT the null hypothesis"
    print


def criticalvalue(tail, alpha):
    """Derive a critical value (tail index) from a null distribution"""
    cumtail = np.cumsum(tail[::-1])
    # Valor crítico. Atenção! Não é a mesma convenção do aft-test...
    # este valor crítico ainda pertence à região crítica!
    critvalue = next(i for i, p in enumerate(cumtail[::-1]) if p < alpha)
    return critvalue


def pvalue(tail, stat):
    """Derive p-value from a test statistic and null distribution"""
    pvalue = 0
    for i in range(len(tail)-1, stat-1, -1):
        pvalue += tail[i]
    return pvalue


def eafindicators(npsA, npsB):
    """From the output of two optimizers (NP sets), get eaf indicators"""
    # calcular os indicadores com o eaf conjunto
    lt, ind = libaft.eaf2d(npsA + npsB, ind=True)
    # espalmar lista, ou seja,
    # (m listas) * (n pontos) * (b bits) -> lista de (m * n pontos) * (b bits)
    flat_ind = [point for level in ind for point in level]
    return flat_ind


if __name__ == '__main__':
    main(sys.argv)
