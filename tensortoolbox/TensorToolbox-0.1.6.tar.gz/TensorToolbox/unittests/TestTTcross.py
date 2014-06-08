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

import operator
import time

import numpy as np
import numpy.linalg as npla
import numpy.random as npr
import itertools

from scipy import stats

import TensorToolbox as DT
import TensorToolbox.multilinalg as mla

from SpectralToolbox import Spectral1D as S1D
from SpectralToolbox import SpectralND as SND
from UQToolbox import RandomSampling as RS

import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D

from aux import bcolors

npr.seed(1)
PLOTTING = False

def print_ok(string):
    print bcolors.OKGREEN + "[SUCCESS] " + string + bcolors.ENDC

def print_fail(string,msg=''):
    print bcolors.FAIL + "[FAILED] " + string + bcolors.ENDC
    if msg != '':
        print bcolors.FAIL + msg + bcolors.ENDC


####
# Test Tensor Wrapper
####
def f(x,params=None): 
    if x.ndim == 1:
        return np.sum(x)
    if x.ndim == 2:
        return np.sum(x,axis=1)

dims = [11,21,31]
X = [np.linspace(1.,10.,dims[0]), np.linspace(1,20.,dims[1]), np.linspace(1,30.,dims[2])]
XX = np.array(list(itertools.product(*X)))
F = f( XX ).reshape(dims)

tw = DT.TensorWrapper(f,X,None)

if F[5,10,15] == tw[5,10,15] and \
        np.all(F[1,2,:] == tw[1,2,:]) and \
        np.all(F[3:5,2:3,20:24] == tw[3:5,2:3,20:24]):
    print_ok("Tensor Wrapper")
else:
    print_fail("TensorWrapper")

####
# Test Maxvol
####
maxvoleps = 1e-2
pass_maxvol = True
N = 100

i = 0
while pass_maxvol == True and i < N:
    i += 1
    A = npr.random(600).reshape((100,6))
    (I,AsqInv,it) = DT.maxvol(A,delta=maxvoleps)
    if np.max(np.abs(np.dot(A,AsqInv))) > 1. + maxvoleps:
        pass_maxvol = False

if pass_maxvol == True:
    print_ok('Maxvol')
else:
    print_fail('Maxvol at it=%d' % i)


####
# Test Low Rank Approximation
####
maxvoleps = 1e-5
delta = 1e-5
pass_lowrankapprox = True
N = 10

i = 0
print "(rows,cols,rank) FroA, FroErr, FroErr/FroA, maxAAinv, maxAinvA"
while pass_lowrankapprox == True and i < N:
    i += 1
    size = npr.random_integers(10,100,2)
    r = npr.random_integers(max(1,np.min(size)-10),np.min(size))
    A = npr.random(np.prod(size)).reshape(size)
    (I,J,AsqInv,it) = DT.lowrankapprox(A,r,delta=delta,maxvoleps=maxvoleps)

    AAinv = np.max(np.abs( np.dot(A[:,J],AsqInv) ) )
    AinvA = np.max(np.abs( np.dot(AsqInv, A[I,:])  ) )
    FroErr = npla.norm( np.dot(A[:,J],np.dot(AsqInv, A[I,:])) - A , 'fro')
    FroA = npla.norm(A,'fro')
    print "(%d,%d,%d) %f, %f, %f %f %f" % (size[0],size[1],r,FroA, FroErr, FroErr/FroA, AAinv, AinvA)
    if AAinv > 1. + maxvoleps:
        pass_maxvol = False

if pass_maxvol == True:
    print_ok('Random Low Rank Approx')
else:
    print_fail('Random Low Rank Approx at it=%d' % i)


####
# Sin*Cos Low Rank Approximation
####
maxvoleps = 1e-5
delta = 1e-5

size = (100,100)
r = 1

# Build up the 2d tensor wrapper
def f(X,params): return np.sin(X[0])*np.cos(X[1])
X = [np.linspace(0,2*np.pi,size[0]), np.linspace(0,2*np.pi,size[1])]
TW = DT.TensorWrapper(f,X,None)

# Compute low rank approx
(I,J,AsqInv,it) = DT.lowrankapprox(TW,r,delta=delta,maxvoleps=maxvoleps)
fill = TW.get_fill_level()

Fapprox = np.dot(TW[:,J].reshape((TW.shape[0],len(J))),np.dot(AsqInv, TW[I,:].reshape((len(I),TW.shape[1])) ) )
FroErr = npla.norm(Fapprox-TW[:,:], 'fro')
if FroErr < 1e-12:
    print_ok('sin(x)*cos(y) Low Rank Approx (FroErr=%e, Fill=%.2f%%)' % (FroErr,100.*np.float(fill)/np.float(TW.get_size())))
else:
    print_fail('sin(x)*cos(y) Low Rank Approx (FroErr=%e, Fill=%.2f%%)' % (FroErr,100.*np.float(fill)/np.float(TW.get_size())))

if PLOTTING:
    plt.figure(figsize=(12,7))
    plt.subplot(1,2,1)
    plt.imshow(TW[:,:])
    plt.subplot(1,2,2)
    plt.imshow(Fapprox)

####
# Sin(x+y) Low Rank Approximation
####
maxvoleps = 1e-5
delta = 1e-5

size = (100,100)
r = 2

# Build up the 2d tensor wrapper
def f(X,params): return np.sin(X[0])*np.cos(X[1])
def f(X,params): return np.sin(X[0]+X[1])
X = [np.linspace(0,2*np.pi,size[0]), np.linspace(0,2*np.pi,size[1])]
TW = DT.TensorWrapper(f,X,None)

# Compute low rank approx
(I,J,AsqInv,it) = DT.lowrankapprox(TW,r,delta=delta,maxvoleps=maxvoleps)
fill = TW.get_fill_level()

Fapprox = np.dot(TW[:,J],np.dot(AsqInv, TW[I,:]))
FroErr = npla.norm(Fapprox-TW[:,:], 'fro')
if FroErr < 1e-12:
    print_ok('sin(x+y) Low Rank Approx (FroErr=%e, Fill=%.2f%%)' % (FroErr,100.*np.float(fill)/np.float(TW.get_size())))
else:
    print_fail('sin(x+y) Low Rank Approx (FroErr=%e, Fill=%.2f%%)' % (FroErr,100.*np.float(fill)/np.float(TW.get_size())))

if PLOTTING:
    plt.figure(figsize=(12,7))
    plt.subplot(1,2,1)
    plt.imshow(TW[:,:])
    plt.subplot(1,2,2)
    plt.imshow(Fapprox)

# ####
# # High Rank Func - Low Rank Approximation
# ####
# maxvoleps = 1e-5
# delta = 1e-5

# size = (100,100)
# r = 10

# # Build up the 2d tensor wrapper
# def f(X,params): return np.float( X[0] > X[1] )
# X = [np.linspace(0,2*np.pi,size[0]), np.linspace(0,2*np.pi,size[1])]
# TW = DT.TensorWrapper(f,X)

# # Compute low rank approx
# (I,J,AsqInv,it) = DT.lowrankapprox(TW,r,delta=delta,maxvoleps=maxvoleps)
# fill = TW.get_fill_level()

# Fapprox = np.dot(TW[:,J],np.dot(AsqInv, TW[I,:]))
# FroErr = npla.norm(Fapprox-TW[:,:], 'fro')
# print '1[x>y] Low Rank Approx (FroErr=%e, Fill=%.2f%%)' % (FroErr,100.*np.float(fill)/np.float(TW.get_size()))

# if PLOTTING:
#     plt.figure(figsize=(12,7))
#     plt.subplot(1,2,1)
#     plt.imshow(TW[:,:])
#     plt.subplot(1,2,2)
#     plt.imshow(Fapprox)

#     plt.show(block=False)


####
# Sin(x)*cos(y)*Sin(z) TTcross Approximation
####
maxvoleps = 1e-5
delta = 1e-5
eps = 1e-10

size = (10,10,10)

# Build up the 2d tensor wrapper
def f(X,params): return np.sin(X[0])*np.cos(X[1])*np.sin(X[2])
X = [np.linspace(0,2*np.pi,size[0]), np.linspace(0,2*np.pi,size[1]), np.linspace(0,2*np.pi,size[2])]
TW = DT.TensorWrapper(f,X)

# Compute low rank approx
TTapprox = DT.TTvec(TW, method='ttcross',eps=eps,mv_eps=maxvoleps,lr_delta=delta)
fill = TW.get_fill_level()
crossRanks = TTapprox.ranks()
PassedRanks = all( map( operator.gt, crossRanks[1:-1], TTapprox.rounding(eps=delta).ranks()[1:-1] ) )

FroErr = mla.norm( TTapprox.to_tensor() - TW.copy()[tuple( [slice(None,None,None) for i in range(len(size))] ) ], 'fro')
if FroErr < eps:
    print_ok('sin(x)*cos(y)*sin(z) Low Rank Approx (FroErr=%e, Fill=%.2f%%)' % (FroErr,100.*np.float(fill)/np.float(TW.get_size())))
else:
    print_fail('sin(x)*cos(y)*sin(z) Low Rank Approx (FroErr=%e, Fill=%.2f%%)' % (FroErr,100.*np.float(fill)/np.float(TW.get_size())))

if PLOTTING:
    # Get filled idxs
    fill_idxs = np.array(TW.get_fill_idxs())
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(fill_idxs[:,0],fill_idxs[:,1],fill_idxs[:,2])
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    # Get last used idxs
    Is = TTapprox.ttcross_Is
    Js = TTapprox.ttcross_Js
    ndim = len(X)
    dims = [len(Xi) for Xi in X]
    idxs = []
    for k in range(len(Is)-1,-1,-1):
        for i in range(len(Is[k])):
            for j in range(len(Js[k])):
                for kk in range(dims[k]):
                    idxs.append( Is[k][i] + (kk,) + Js[k][j] )

    last_idxs = np.array(idxs)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(last_idxs[:,0],last_idxs[:,1],last_idxs[:,2],c='r')

    plt.show(block=False)


# ####
# # Hilbert TTcross Approximation
# ####
# maxvoleps = 1e-5
# delta = 1e-5
# eps = 1e-10

# size = 32
# d = 60

# # Build up the 2d tensor wrapper
# def f(X,params): return 1./np.sum(X)
# X = [np.arange(1.,size+1.) for i in range(d)]
# TW = DT.TensorWrapper(f,X)

# # Compute reference high-rank solution
# lr_r = [10]*
# TWcopy = TW.copy()
# RefTTapprox = DT.TTvec(TWcopy, method='ttcross',lr_r=lr_r)
# RefFill = TWcopy.get_fill_level()
# normConst = mla.norm(RefTTapprox,'fro')

# start = time.clock()
# TTapprox = DT.TTvec(TWcopy,method='ttcross',)
# stop = time.clock()
# fills = TWcopy.get_fill_level()
# times = stop - start
# FroErr = mla.norm( RefTTapprox - TTapprox, 'fro' )/normConst
# print "%d      %.2f      %e     %d" % (r,times[i],FroErr[i],fills[i])


# #########################################
# # Genz functions
# #########################################
# maxvoleps = 1e-5
# delta = 1e-5
# eps = 1e-6

# size1D = 80
# d = 2
# size = [size1D for i in range(d)]

# # ws = (npr.random(d)*2.)-1.
# ws = np.array([0.,0.])
# cs = npr.random(d)

# # Oscillatory
# def f(X,params): return 10. * np.cos( 2.*np.pi * np.sum(X) )
# # def f(X,params): return np.cos(2.*np.pi*params['ws'][0] + np.sum( params['cs'] * X ))

# # # Product peak
# # def f(X,params): return np.prod( ( params['cs']**-2. + (X - params['ws'])**2. )**-1. )

# # # Corner peak
# # def f(X,params): return (1.+ np.sum(params['cs'] * (X+1.)/2.))**(-d-1.)

# # # Gaussian
# # def f(X,params): return np.exp( - np.sum( params['cs']**2. * (X - params['ws'])**2. ) )

# # # Continuous
# # def f(X,params): return np.exp( - np.sum( params['cs']**2. * np.abs(X - params['ws']) ) )

# # # Discontinuous (not C^0)
# # def f(X,params):
# #     if np.sum(X + params['ws']) > 0.: return 0.
# #     else: return 1.

# # # C^0 function (not C^1)
# # def f(X,params): return np.abs(np.sum(X+params['ws'][0]))

# # # C^1 function (not C^2)
# # def f(X,params):
# #     if np.sum(X + params['ws']) > 0:
# #         return np.sum(X+params['ws'])**2.
# #     else:
# #         return -np.sum(X+params['ws'])**2.

# # # C^2 function (not C^3)
# # def f(X,params):
# #     if np.sum(X + params['ws']) > 0:
# #         return np.sum(X+params['ws'])**3.
# #     else:
# #         return -np.sum(X+params['ws'])**3.

# # # C^3 function (not C^4)
# # def f(X,params):
# #     if np.sum(X + params['ws']) > 0:
# #         return np.sum(X+params['ws'])**4.
# #     else:
# #         return -np.sum(X+params['ws'])**4.

# # # C^inf poly function
# # def f(X,params): return np.sum(X+params['ws'])**6.

# # C^1 cos func
# def f(X,params):
#     if np.sum(X) < 0:
#         return np.cos(np.sum(X))-1
#     else:
#         return -np.cos(np.sum(X))+1

# # Build up the 2d tensor wrapper
# P = S1D.Poly1D(S1D.JACOBI,(0.,0.))
# X = []
# W = []
# for i in range(d):
#     [x,w] = P.GaussLobattoQuadrature(size[i],normed=True)
#     X.append(x)
#     W.append(w)
# params = {'ws':ws,'cs':cs}
# TW_tmp = DT.TensorWrapper(f,X,params)

# if d <= 3:
#     fr_norm = npla.norm(TW_tmp[tuple([ slice(None,None,None) for i in range(d)])].flatten(),2)
#     def f1(X,params): return f(X,params)/fr_norm
#     TW = DT.TensorWrapper(f1,X,params)
# else:
#     TW = TW_tmp

# TTapprox = DT.TTvec(TW, method='ttcross',lr_delta=delta,mv_eps=maxvoleps,eps=eps)
# fill = TW.get_fill_level()
# crossRanks = TTapprox.ranks()

# TWcopy = TW.copy()

# # Compute Fourier coefficients TT
# TThat = []
# Vs = []
# for i in range(d):
#     V1D = P.GradVandermonde1D(X[i],size[i],0,norm=False)
#     Vs.append(V1D)
#     TTi = TTapprox.TT[i]
#     tth = np.zeros(TTi.shape)
#     for itt in range(TTi.shape[0]):
#         for jtt in range(TTi.shape[2]):
#             # tth[itt,:,jtt] = npla.solve(V1D,TTi[itt,:,jtt])
#             tth[itt,:,jtt] = np.dot(V1D.T,W[i]*TTi[itt,:,jtt])

#     TThat.append(tth)

# TT_four = DT.TTvec(TThat)

# if d == 2:
#     fig = plt.figure(figsize=(12,7))
#     ax = fig.add_subplot(121, projection='3d')
#     [XX,YY] = np.meshgrid(X[0],X[1])
#     ax.plot_surface(XX,YY,TWcopy[tuple( [slice(None,None,None) for i in range(len(size))] ) ],rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
#     plt.title("Original")

#     ax = fig.add_subplot(122, projection='3d')
#     ax.plot_surface(XX,YY,TTapprox.to_tensor(),rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
#     plt.title("TTapprox")

#     # Plot left and right singular vectors
#     plt.figure(figsize=(12,7))
#     plt.subplot(1,2,1)
#     for i in range(TTapprox.TT[0].shape[2]):
#         plt.plot(X[0],TTapprox.TT[0][0,:,i],label='%d-th'%i)
#     plt.legend()
#     plt.subplot(1,2,2)
#     for i in range(TTapprox.TT[1].shape[0]):
#         plt.plot(X[0],TTapprox.TT[1][i,:,0],label='%d-th'%i)
#     plt.legend()
    
#     # Plot 2D Fourier Coeff from tensor product
#     V2D = np.kron(Vs[0],Vs[1])
#     WW = np.kron(W[0],W[1])
#     fhat = np.dot(V2D.T,WW*TWcopy[:,:].flatten()).reshape([s+1 for s in size])

#     # Plot 2D Fourier Coeff
#     TT_fourier_abs = np.maximum(np.abs(TT_four.to_tensor()),1e-20*np.ones(TT_four.shape()))
#     fhat_abs = np.maximum(np.abs(fhat),1e-20*np.ones(fhat.shape))
#     VMAX = max( np.max(np.log10(TT_fourier_abs)), np.max(np.log10(fhat_abs)))
#     VMIN = min( np.min(np.log10(TT_fourier_abs)), np.min(np.log10(fhat_abs)))
#     fig = plt.figure(figsize=(20,7))
#     plt.subplot(1,3,1)
#     plt.title("TT Fourier")
#     plt.imshow(np.log10(TT_fourier_abs), interpolation='none', vmin = VMIN, vmax = VMAX)
#     plt.colorbar(shrink=0.8)
#     plt.subplot(1,3,2)
#     plt.title("Exact Fourier")
#     plt.imshow(np.log10(fhat_abs), interpolation='none', vmin = VMIN, vmax = VMAX)
#     plt.colorbar(shrink=0.8)
#     plt.subplot(1,3,3)
#     plt.title("Fourier error")
#     plt.imshow( np.log10(np.abs(TT_fourier_abs - fhat_abs)), interpolation = 'none')
#     plt.colorbar(shrink=0.8)
    
#     FroErr = mla.norm( TTapprox.to_tensor() - TWcopy[tuple( [slice(None,None,None) for i in range(len(size))] ) ], 'fro')

# # Compute integral by contraction
# TT_int = mla.contraction(TTapprox,W)

# # Compute integral by MC
# N = 10**4
# dists = [ stats.uniform(loc=-1.,scale=2.) for i in range(d) ]
# samples = RS.lhc(N,d,dists)
# lhc_res = np.zeros(N)
# for i in range(N): lhc_res[i] = f(samples[i,:],params)
# LHC_int = 1./float(N) * np.sum(lhc_res)

# print 'Low Rank Approx ( IntErr=%e, Fill=%.2f%%)' % ( np.abs(TT_int-LHC_int), 100.*np.float(fill)/np.float(TW.get_size()))

# if d == 2:

#     # Get filled idxs
#     fill_idxs = np.array(TW.get_fill_idxs())
#     fig = plt.figure()
#     plt.plot(fill_idxs[:,0],fill_idxs[:,1],'o')

#     # Get last used idxs
#     Is = TTapprox.ttcross_Is
#     Js = TTapprox.ttcross_Js
#     ndim = len(X)
#     dims = [len(Xi) for Xi in X]
#     idxs = []
#     for k in range(len(Is)-1,-1,-1):
#         for i in range(len(Is[k])):
#             for j in range(len(Js[k])):
#                 for kk in range(dims[k]):
#                     idxs.append( Is[k][i] + (kk,) + Js[k][j] )

#     last_idxs = np.array(idxs)
#     plt.plot(last_idxs[:,0],last_idxs[:,1],'or')

# if d == 3:
#     # Get filled idxs
#     fill_idxs = np.array(TW.get_fill_idxs())
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     # Get last used idxs
#     Is = TTapprox.ttcross_Is
#     Js = TTapprox.ttcross_Js
#     ndim = len(X)
#     dims = [len(Xi) for Xi in X]
#     idxs = []
#     for k in range(len(Is)-1,-1,-1):
#         for i in range(len(Is[k])):
#             for j in range(len(Js[k])):
#                 for kk in range(dims[k]):
#                     idxs.append( Is[k][i] + (kk,) + Js[k][j] )

#     last_idxs = np.array(idxs)

#     overlap = [np.any([np.all(i == x) for x in list(last_idxs)]) for i in list(fill_idxs)]
#     notover = fill_idxs[np.logical_not(overlap),:]

#     ax.scatter(notover[:,0],notover[:,1],notover[:,2],c='b',marker='o')
#     ax.scatter(last_idxs[:,0],last_idxs[:,1],last_idxs[:,2],c='r',marker='o')
#     plt.show(block=False)

# # Construct Lagrange interpolant
# sizeI = 100
# xi = np.linspace(-1.,1.,sizeI)

# Ms = []
# for i in range(d):
#     bw = S1D.BarycentricWeights(X[i])
#     Ms.append( S1D.LagrangeInterpolationMatrix(X[i],bw,xi) )

# # TT_MND = DT.TTmat(Ms[0].flatten(),nrows=sizeI,ncols=size[0]+1)
# # for i in range(1,d):
# #     TT_MND.kron( DT.TTmat(Ms[i].flatten(),nrows=sizeI,ncols=size[i]+1) )

# # TTapproxI = mla.dot(TT_MND,TTapprox).rounding(1e-8)

# TTapproxI = TTapprox.interpolate(Ms,eps=1e-8)

# if d == 2:
#     fig = plt.figure()
#     plt.title("Lagrange interpolation")
#     ax = fig.add_subplot(111, projection='3d')
#     [XX,YY] = np.meshgrid(xi,xi)
#     ax.plot_surface(XX,YY,TTapproxI.to_tensor(),rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

# sizeI = 100
# xi = np.linspace(-1.,1.,sizeI)

# Ms = [ S1D.LinearInterpolationMatrix(X[i],xi) for i in range(d) ]
# is_sparse = [True]*d

# TTapproxI = TTapprox.interpolate(Ms,eps=1e-8,is_sparse=is_sparse)

# if d == 2:
#     fig = plt.figure()
#     plt.title("Linear Interpolation")
#     ax = fig.add_subplot(111, projection='3d')
#     [XX,YY] = np.meshgrid(xi,xi)
#     ax.plot_surface(XX,YY,TTapproxI.to_tensor(),rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

# # Construct TT-polynomial expansion
# Vs = []
# for i in range(d):
#     V1D = P.GradVandermonde1D(X[i],size[i],0)
#     Vs.append(V1D)

# # TT_V1D = DT.TTmat(Vs[0].flatten(),nrows=size[0]+1,ncols=size[0]+1)
# # TT_VND = TT_V1D.copy()
# # for i in range(1,d):
# #     TT_VND.kron( DT.TTmat(Vs[i].flatten(),nrows=size[i]+1,ncols=size[i]+1) )

# # # npla.norm( mla.kron(TT_V1D,TT_V1D).to_tensor() - DT.matkron_to_mattensor(np.kron(V1D,V1D),nrows=[size[0]+1,size[0]+1],ncols=[size[0]+1,size[0]+1]), 'fro') # Check

# # # Compute expansion coefficients
# # (TT_xhat, conv, info) = mla.gmres(TT_VND,TTapprox,eps=delta, restart=10, eps_round=delta, ext_info=True)

# # # Compute interpolation
# # sizeI = 100
# # XI = np.linspace(-1.,1.,sizeI)

# # VIs = []
# # for i in range(d):
# #     V1DI = P.GradVandermonde1D(XI,size[i],0)
# #     VIs.append(V1DI)

# # TT_V1DI = DT.TTmat(VIs[0].flatten(),nrows=sizeI,ncols=size[0]+1)
# # TT_VNDI = TT_V1DI.copy()
# # for i in range(1,d):
# #     TT_VNDI.kron( DT.TTmat(VIs[i].flatten(),nrows=sizeI,ncols=size[i]+1) )

# # TTapproxI = mla.dot(TT_VNDI,TT_xhat).rounding(1e-8)

# # if d == 2:
# #     fig = plt.figure()
# #     ax = fig.add_subplot(111, projection='3d')
# #     [XX,YY] = np.meshgrid(XI,XI)
# #     ax.plot_surface(XX,YY,TTapproxI.to_tensor(),rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)

# # # Convergence test
# # N = 10
# # r_start = 1

# # for ord_pow in range(1,N+1):
# #     size1D = 2**ord_pow
# #     size = [size1D for i in range(d)]

# #     # Build up the 2d tensor wrapper
# #     P = S1D.Poly1D(S1D.JACOBI,(0.,0.))
# #     X = []
# #     W = []
# #     for i in range(d):
# #         [x,w] = P.GaussLobattoQuadrature(size[i],normed=True)
# #         X.append(x)
# #         W.append(w)
# #     params = {'ws':ws,'cs':cs}
# #     TW = DT.TensorWrapper(f,X,params)

# #     PassedRanks = False
# #     while PassedRanks == False:
# #         r_start += 1
# #         # Compute low rank approx
# #         lr_r = [1]
# #         for i in range(d-1): lr_r.append(r)
# #         lr_r.append(1)
# #         TTapprox = DT.TTvec(TW, method='ttcross',lr_r=lr_r)
# #         fill = TW.get_fill_level()
# #         crossRanks = TTapprox.ranks()
# #         PassedRanks = all( map( operator.gt, crossRanks[1:-1], TTapprox.rounding(eps=delta).ranks()[1:-1] ) )
    
# #     # Compute


# plt.show(block=False)
