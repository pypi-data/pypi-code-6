#
# This file is part of TensorToolbox.
#
# TensorToolbox is free software: you can redistribute it and/or modify
# it under the terms of the LGNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TensorToolbox is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# LGNU Lesser General Public License for more details.
#
# You should have received a copy of the LGNU Lesser General Public License
# along with TensorToolbox.  If not, see <http://www.gnu.org/licenses/>.
#
# DTU UQ Library
# Copyright (C) 2014 The Technical University of Denmark
# Scientific Computing Section
# Department of Applied Mathematics and Computer Science
#
# Author: Daniele Bigoni
#

import numpy as np
import TensorToolbox as TT

#
# DESCRIPTION
# 
# Construct a tensor wrapper around an numpy.ndarray and check that all the 
# slicing functions work.
# The test checks that the output of the tensor wrapper is equal to the output
# of the original array and that the function evaluations done are right.
#

from aux import bcolors

def print_ok(testn,string):
    print bcolors.OKGREEN + "[SUCCESS] " + str(testn) + " Tensor Wrapper: " + string + bcolors.ENDC

def print_fail(testn,string,msg=''):
    print bcolors.FAIL + "[FAILED] " + str(testn) + " Tensor Wrapper: " + string + bcolors.ENDC
    if msg != '':
        print bcolors.FAIL + msg + bcolors.ENDC

testn = 0

###################################################################
# 00: Construction of the multidimensional array and the corresponding tensor wrapper
#

shape = [2,3,4,5]
A = np.arange(np.prod(shape)).reshape(shape)

feval = 0
def f(X, params):
    global feval 
    feval += 1
    return A[tuple(X)]

X = [ np.arange(s,dtype=int) for s in shape ]
TW = TT.TensorWrapper(f, X, None,dtype=A.dtype)

testn += 1
print_ok(0,"Construction")

def test(testn, title, idx):
    global feval
    feval = 0
    TW.data = {}
    out = TW[idx]
    if np.any(A[idx] != out) or np.any(A[idx].shape != out.shape):
        print_fail(testn,title,msg='Different output - idx: ' + str(idx))
    elif feval != np.prod(A[idx].shape):
        print_fail(testn,title,msg='Wrong number of function evaluations - idx: ' + str(idx))
    else:
        print_ok(testn,title)


###################################################################
# 01: Single address access
#
idx = (1,2,3,4)
feval = 0
out = TW[idx]
testn += 1
if A[idx] != out:
    print_fail(testn,"Single address access",msg='Different output')
elif feval != 1:
    print_fail(testn,"Single address access",msg='Wrong number of function evaluations')
else:
    print_ok(testn,"Single address access")
    

###################################################################
# Single slice
#
testn += 1
idx = (1,slice(None,None,None),3,4)
test(testn,"Single slice",idx)

###################################################################
# Partial slice
#
testn += 1
idx = (1,2,slice(1,3,1),4)
test(testn,"Partial slice",idx)

###################################################################
# Partial stepping slice
#
testn += 1
idx = (1,2,slice(0,4,2),4)
test(testn,"Partial stepping slice",idx)

###################################################################
# Multiple slice
#
testn += 1
idx = (1,slice(None,None,None),3,slice(0,4,2))
test(testn,"Multiple slice",idx)

###################################################################
# Full slice
#
testn += 1
idx = tuple([slice(None,None,None)] * len(shape))
test(testn,"Full slice",idx)

###################################################################
# List 
#
testn += 1
idx = ([0,1],[1,2],[1,3],[0,4])
test(testn,"Lists",idx)

###################################################################
# Single list 
#
testn += 1
idx = (0,1,[1,3],3)
test(testn,"Single list",idx)

###################################################################
# Double list 
#
testn += 1
idx = (0,[0,2],[1,3],3)
test(testn,"Double list",idx)

###################################################################
# Single list slice
#
testn += 1
idx = (0,[0,2],slice(None,None,None),3)
test(testn,"Single list slice",idx)

testn += 1
idx = (0,slice(None,None,None),[0,2],3)
test(testn,"Single list slice",idx)

testn += 1
idx = (slice(None,None,None),0,[0,2,3],3)
test(testn,"Single list slice",idx)

###################################################################
# Double list slice
#
testn += 1
idx = ([0,1],slice(None,None,None),[0,2],3)
test(testn,"Double list slice",idx)

testn += 1
idx = (slice(None,None,None),0,slice(None,None,None),[0,2,3])
test(testn,"Double slice list",idx)

###################################################################
# Lists slice
#
testn += 1
idx = ([0,1],[0,2],slice(None,None,None),[1,3])
test(testn,"Lists slice",idx)
