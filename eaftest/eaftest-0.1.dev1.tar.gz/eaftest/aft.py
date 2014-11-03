#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# libaft python foreign function interface

import os
import ctypes
from ctypes import c_int, c_double, c_byte, POINTER
import ctypes.util

LIB_PATH = os.path.join(os.path.dirname(__file__),
                        "libaft", "libaft.so")
_lib = ctypes.cdll.LoadLibrary(LIB_PATH)

# Output data type
class LEVELDATA(ctypes.Structure):
    _fields_ = [("nlevels", c_int),
                ("llen", POINTER(c_int)),
                ("p", POINTER(POINTER(2*c_double))),
                ("ind", POINTER(POINTER(c_byte)))]
# accumulator
def _accum(l):
    acc = 0
    for x in l:
        acc += x
        yield acc

def eaf2d(npsets, ind=True):
    # TODO: verificar correcao do dados inputs (ex: dimensionalidade)
    # argumentos
    nruns = nlevels = len(npsets)
    cumsize = (c_int*nruns)(*_accum(map(len, npsets)))
    datalen = 2 * cumsize[-1]
    # espalmar dados em "row-major order"
    data = (c_double*datalen)(*(coord for npset in npsets
                                for point in npset for coord in point))
    # att levels a serem determinados, neste momento todos: [1..nruns]
    attlevel = (c_int*nruns)(*range(1,nruns+1))
    
    # chamar a funcao
    _lib.eaf2d.restype = POINTER(LEVELDATA)
    ldataptr = _lib.eaf2d(data, cumsize, nruns, attlevel, nlevels, ind)
    ldata = ldataptr.contents
    # converter para tipos de dados nativos de python
    pointsets = [map(tuple, points[:n]) for points, n in
                 zip(ldata.p[:nlevels], ldata.llen[:nlevels])]
    # indicadores
    indsets = []
    if ind:
        indsets = [[p[i*nruns:(i+1)*nruns] for i in range(n)] for p, n in
                    zip(ldata.ind[:nlevels], ldata.llen[:nlevels])]
    
    _lib.free_lvdata(ldataptr)
    return pointsets, indsets

# argumentos para testes kslike
def _ksargs(points):
    nvars, npoints = len(points[0]), len(points)
    arraytype = c_int * (nvars * npoints)
    bindata = arraytype(*(bit for point in points for bit in point))
    return bindata, nvars, npoints

# Estatística de teste
def ksstat(points, order=1):
    func = _lib.eaf_ks_stat if order == 1 else _lib.eaf2_ks_stat
    bindata, nvars, npoints = _ksargs(points)
    return func(bindata, nvars, npoints)

# Determinacao do valor critico
def kstest(points, order=1, alpha=0.05, permutations=10000):
    func = _lib.eaf_ks_tail if order == 1 else _lib.eaf2_ks_tail
    bindata, nvars, npoints = _ksargs(points)
    func.restype = POINTER(c_int * (1 + nvars / 2))
    ptr = func(bindata, nvars, npoints, c_double(alpha), permutations)
    tail = ptr.contents[:]       # copia os dados
    _lib.free_data(ptr)      # liberta o array devolvido
    return tail
