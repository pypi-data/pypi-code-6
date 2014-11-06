# FIXME: Python 2 only!
# -*- coding: utf-8 -*-

import os, sys
import numpy as np
import pyopencl as cl
from time import time, clock
from .clkernels import loadkernel
from .bintools import make_bindata32
from .datasets import load_ind

# Compilation errors & warnings output
os.environ['PYOPENCL_COMPILER_OUTPUT'] = '1'
# Use the first opencl device
os.environ['PYOPENCL_CTX'] = '0'

def data_attributes(bdata, bmask):
    npoints, unitspp = bdata.shape
    permutations, _  = bmask.shape
    bytespu = bdata.dtype.itemsize
    return npoints, permutations, unitspp, bytespu

def runkernel(indicators, permutations):
    # Create context and command queue
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)
    
    # Make indicator & permutation masks binary data
    data, mask, nvars = make_bindata32(indicators, permutations)
    # Data attributes: number of points, permutations, units per point, bytes per unit
    npoints, perms, unitspp, bytespu = data_attributes(data, mask)
    
    # Create device buffers
    mf = cl.mem_flags
    databuf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=data)
    maskbuf = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=mask)
    
    # Maximal distance for 8 permutations
    dist = np.zeros(8, dtype=np.int32)
    distbuf = cl.Buffer(ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, hostbuf=dist)
    #datab, maskb, dist, distb = databuf, maskbuf, dist, distbuf
    
    # Kernel arguments
    kargs = {"npoints": npoints, "intpp": unitspp,
             "bytespu": bytespu, "nvars": nvars, "masklen": nvars//2}
    
    # Kernel custom arguments
    tblock, pblock = 128, 8
    tdivs = (npoints-1)//tblock + 1
    tdivs = ((tdivs-1)//8+1)*8
    kargs.update(tblock=tblock, pblock=pblock, tdivs=tdivs)
    
    # Load and build kernel
    kstr, kopt = loadkernel("reduce4-xor", **kargs)
    prg = cl.Program(ctx, kstr).build(options=kopt)

    # Run kernel
    globalsize, localsize = (tdivs*tdivs,), (64,)
    
    for z in xrange(0, permutations, 8):
        dist[:] = 0
        cl.enqueue_copy(queue, distbuf, dist)
        #prg.zerodist(queue, (8,), None, distbuf)
        prg.eaf_test2(queue, globalsize, localsize, databuf, maskbuf, distbuf,
            np.uint32(z)).wait()
        cl.enqueue_copy(queue, dist, distbuf)
        # Yield 8 maximum distances
        for d in dist:
            yield d


if __name__ == '__main__':
    # Load indicators
    indicators = load_ind("indicators/local2-25-b.AB.u", flat=True)
    permutations = 10240
    # Number of executions
    nvars = len(indicators[0])
    
    # Run kernel
    gen = runkernel(indicators, permutations)
    # Max distance array
    maxdist = np.zeros(permutations, dtype=np.int32)
    real = time()
    for i, maxd in enumerate(gen):
        maxdist[i] = maxd
        if (i+1) % (permutations//40) == 0:
            print "%6d perms, %7.3f sec" % (i+1, time() - real)
        if (i+1) % (permutations//10) == 0:
            print "tail:", np.bincount(maxdist[:i+1], minlength=nvars//2+1)
    
    print "total elapsed", time() - real
