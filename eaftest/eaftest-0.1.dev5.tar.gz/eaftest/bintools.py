# FIXME: Python 2 only!
# -*- coding: utf-8 -*-
# Binary tools using numpy for the eaf statistic tests

import numpy as np

def popcount(v):
    return bin(v).count('1')

def mask(n, p):
    s = np.zeros(n, dtype=np.uint8)
    s[:p] = 1
    return s

def randmask(m, n, p, seed=64):
    np.random.seed(seed)
    s = np.zeros(n, dtype=np.uint8)
    s[:p] = 1
    # FIXME: ineficiente - cria 2 listas
    return np.array([np.random.permutation(s) for i in xrange(m)])

def binary_to_uint32(b, invertbits=False):
    """Converts a flat binary array (1 and 0) to uint32 np array"""
    size = len(b)
    nbits = ((size-1)//32 + 1) * 32
    
    new = np.zeros((nbits, ), dtype=np.uint8)
    new[:size] = b
    # inverte a ordem dos bits (desnecessario - ficar igual a versao C)
    if invertbits:
        new = new.reshape((nbits//8, 8))[:,::-1]
    data32 = np.packbits(new).view(dtype=np.uint32)
    return data32

def binarrays_to_uint32(ba, invertbits=False):
    """Converts a list of binary arrays (or binary matrix) into uint32 np array"""
    width, height = len(ba[0]), len(ba)
    nbits = ((width-1)//32 + 1) * 32
    
    new = np.zeros((height, nbits), dtype=np.uint8)
    new[:,:width] = ba
    if invertbits:
        new = new.reshape((height, nbits//8, 8))[:,:,::-1]
        new = new.reshape((height, nbits))
    data32 = np.packbits(new, -1).view(dtype=np.uint32)
    return data32

def make_bindata32(point_ind, permutations=10240):
    # permutations = number of permutations to do, should be >= 10000
    # nvars = (number of runs optimizerA + optimizerB)
    # npoints = total number of points (indicators)
    nvars, npoints = len(point_ind[0]), len(point_ind)
    intpp = (nvars-1)//32 + 1  # numero de uint32 por ponto
    # constroi random permutation masks e empacota bits, convertendo para uint32
    rmasks = randmask(permutations, nvars, nvars//2)
    bmask32 = binarrays_to_uint32(rmasks)
    bdata32 = binarrays_to_uint32(point_ind)
    return bdata32, bmask32, nvars

def pack_arrays_uint32(point_ind, masks):
    nvars, npoints = len(point_ind[0]), len(point_ind)
    bdata32 = binarrays_to_uint32(point_ind)
    bmask32 = binarrays_to_uint32(rmasks)
    return bdata32, bmask32, nvars

def make_masks(n_permutations, nvars, seed=64):
    rmasks = randmask(n_permutations, nvars, nvars//2, seed)
    return rmasks

