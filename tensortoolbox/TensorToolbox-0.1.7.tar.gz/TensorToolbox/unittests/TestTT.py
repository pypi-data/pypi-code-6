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

import sys
import numpy as np
import numpy.linalg as npla
import itertools
from matplotlib import pyplot as plt
import time

import TensorToolbox as DT
import TensorToolbox.multilinalg as mla

from aux import bcolors

plt.close('all')
RUNTESTS = [0,1,2,3,4,5,7]
PLOTTING = False

def print_ok(string):
    print bcolors.OKGREEN + "[SUCCESS] " + string + bcolors.ENDC

def print_fail(string,msg=''):
    print bcolors.FAIL + "[FAILED] " + string + bcolors.ENDC
    if msg != '':
        print bcolors.FAIL + msg + bcolors.ENDC

opt = None
while (not len(RUNTESTS)>0 and (opt == None  or (opt != 'c' and opt != 's' and opt != 'q'))):
    print("Construction and basic algebra tests:")
    print("\t [c]: continue")
    print("\t [s]: skip")
    print("\t [q]: exit")
    opt = sys.stdin.read(1)
    if (opt ==  'q'):
        exit()

if (0 in RUNTESTS) or opt == 'c':
    N = 16
    d = 3
    nrows = [N for i in range(d)]
    ncols = [N for i in range(d)]
    D = np.diag(-np.ones((N-1)),-1) + np.diag(-np.ones((N-1)),1) + np.diag(2*np.ones((N)),0)
    I = np.eye(N)
    Dd = np.zeros((N**d,N**d))

    for i in range(d):
        tmp = np.array([1])
        for j in range(d):
            if i != j:
                tmp = np.kron(tmp,I)
            else:
                tmp = np.kron(tmp,D)
        Dd += tmp

    if PLOTTING:
        plt.figure()
        plt.spy(Dd)
        plt.show(block=False)

    idxs = [range(N) for i in range(d)]
    MI = list(itertools.product(*idxs)) # Multi indices

    # Canonical form of n-dimentional Laplace operator
    D_flat = D.flatten()
    I_flat = I.flatten()

    # CP = np.empty((d,d,N**2),dtype=np.float64) 
    CPtmp = [] # U[i][alpha,k] = U_i(alpha,k)
    for i in range(d):
        CPi = np.empty((d,N**2))
        for alpha in range(d):
            if i != alpha:
                CPi[alpha,:] = I_flat
            else:
                CPi[alpha,:] = D_flat
        CPtmp.append(CPi)

    CP = DT.Candecomp(CPtmp)

    # Let's compare Dd[i,j] with its Canonical counterpart
    T_idx = (10,9) # Index in the tensor product repr.
    idxs = np.vstack( (np.asarray(MI[T_idx[0]]), np.asarray(MI[T_idx[1]])) ) # row 1 contains row multi-idx, row 2 contains col multi-idx for Tensor
    # Now if we take the columns of idxs we get the multi-indices for the CP.
    # Since in CP we flattened the array, compute the corresponding indices for CP.
    CP_idxs = idxs[0,:]*N + idxs[1,:]

    TT = DT.TTmat(CP,nrows=N,ncols=N)

    if np.abs(Dd[T_idx[0],T_idx[1]] - CP[CP_idxs]) < 100.*np.spacing(1) and np.abs(CP[CP_idxs] - TT[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])]) < 100.*np.spacing(1):
        print_ok("0.1 Tensor Test: Entry comparison (pre-rounding) FULL, CP, TT")
    else:
        print_fail("0.1 Tensor Test: Entry comparison FULL, CP, TT")
        # print "  T      CP     TT"
        # print "%.5f  %.5f  %.5f" % (Dd[T_idx[0],T_idx[1]],CP[CP_idxs],TT[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])])

    # print "Space Tensor: %d" % np.prod(Dd.shape)
    # print "Space CP: %d" % CP.size()
    # print "Space TT: %d" % TT.size()

    ########################################
    # Multi-Linear Algebra
    ########################################
    
    # Sum by scalar
    CPa = DT.Candecomp([5.*np.ones((1,5)),np.ones((1,6)),np.ones((1,7))])
    TTa = DT.TTvec(CPa,1e-13)
    TTb = TTa + 3.
    if np.abs(TTb[3,3,3] - 8.) < 1e-12:
        print_ok("0.2 Tensor Test: TT sum by scalar")
    else:
        print_fail("0.2 Tensor Test: TT sum by scalar", "TT[idx] + b = %e, Expected = %e" % (TTb[3,3,3],8.))

    # Diff by scalar
    CPa = DT.Candecomp([5.*np.ones((1,5)),np.ones((1,6)),np.ones((1,7))])
    TTa = DT.TTvec(CPa,1e-13)
    TTb = TTa - 3.
    if np.abs(TTb[3,3,3] - 2.) < 1e-12:
        print_ok("0.2 Tensor Test: TT diff by scalar")
    else:
        print_fail("0.2 Tensor Test: TT diff by scalar", "TT[idx] + b = %e, Expected = %e" % (TTb[3,3,3],2.))

    # Mul by scalar
    CPa = DT.Candecomp([5.*np.ones((1,5)),np.ones((1,6)),np.ones((1,7))])
    TTa = DT.TTvec(CPa,1e-13)
    TTb = TTa * 3.
    if np.abs(TTb[3,3,3] - 15.) < 1e-12:
        print_ok("0.2 Tensor Test: TT mul by scalar")
    else:
        print_fail("0.2 Tensor Test: TT mul by scalar", "TT[idx] + b = %e, Expected = %e" % (TTb[3,3,3],15.))

    # Div by scalar
    CPa = DT.Candecomp([15.*np.ones((1,5)),np.ones((1,6)),np.ones((1,7))])
    TTa = DT.TTvec(CPa,1e-13)
    TTb = TTa / 3.
    if np.abs(TTb[3,3,3] - 5.) < 1e-12:
        print_ok("0.2 Tensor Test: TT div by scalar")
    else:
        print_fail("0.2 Tensor Test: TT div by scalar", "TT[idx] + b = %e, Expected = %e" % (TTb[3,3,3],5.))

    # Sum
    C = TT + TT
    if  C[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])] - 2. * Dd[T_idx[0],T_idx[1]] <= np.spacing(1):
        print_ok("0.2 Tensor Test: TT sum")
    else:
        print_fail("0.2 Tensor Test: TT sum", "TT[idx] + TT[idx] = %.5f" % C[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])])

    C = TT * TT
    if  C[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])] - Dd[T_idx[0],T_idx[1]]**2. <= np.spacing(1):
        print_ok("0.3 Tensor Test: TT mul")
    else:
        print_fail("0.3 Tensor Test: TT mul", "TT[idx] * TT[idx] = %.5f" % C[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])])

    # C *= (C+TT)
    # if  C[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])] == Dd[T_idx[0],T_idx[1]]**2. * (Dd[T_idx[0],T_idx[1]]**2.+Dd[T_idx[0],T_idx[1]]):
    #     print_ok("0.4 Tensor Test: TT operations")
    # else:
    #     print_fail("0.4 Tensor Test: TT operations", "(TT*TT)*(TT*TT+TT) = %.5f" % C[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])])

    if np.abs(npla.norm(Dd,ord='fro')-mla.norm(TT,ord='fro')) < TT.size() * 100.*np.spacing(1):
        print_ok("0.5 Tensor Test: Frobenius norm (pre-rounding) FULL, TT")
    else:
        print_fail("0.5 Tensor Test: Frobenius norm (pre-rounding) FULL, TT",
                   "                  T          TT\n"\
                       "Frobenius norm  %.5f         %.5f" % (npla.norm(Dd,ord='fro'), DT.norm(TT,ord='fro')))

    #######################################
    # Check TT-SVD
    #######################################

    # Contruct tensor form of Dd
    Dd_flat = np.zeros((N**(2*d)))
    for i in range(d):
        tmp = np.array([1])
        for j in range(d):
            if i != j:
                tmp = np.kron(tmp,I_flat)
            else:
                tmp = np.kron(tmp,D_flat)
        Dd_flat += tmp

    Dd_tensor= Dd_flat.reshape([N**2 for j in range(d)])

    TT_tensor = TT.to_tensor()

    # From Dd_tensor obtain a TT representation with accuracy eps
    eps = 0.001
    TT_svd = DT.TTmat(Dd_tensor,nrows=N,ncols=N,eps=eps)

    if np.abs(Dd[T_idx[0],T_idx[1]] - TT_svd[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])]) < d * 100.*np.spacing(1):
        print_ok("0.6 Tensor Test: Entry comparison FULL, TT-svd")
    else:
        print_fail("0.6 Tensor Test: Entry comparison FULL, TT-svd","  T - TT-svd = %e" % np.abs(Dd[T_idx[0],T_idx[1]] - TT_svd[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])]))

    Dd_norm = npla.norm(Dd,ord='fro')
    TT_svd_norm = mla.norm(TT_svd,ord='fro')
    if np.abs(Dd_norm - TT_svd_norm) < eps * Dd_norm:
        print_ok("0.6 Tensor Test: Frobenius norm FULL, TT-svd")
    else:
        print_fail("0.6 Tensor Test: Frobenius norm FULL, TT-svd",
                   "                  T          TT_svd\n"\
                       "Frobenius norm  %.5f         %.5f" % (npla.norm(Dd,ord='fro'), mla.norm(TT_svd,ord='fro')))

    #######################################
    # Check TT-SVD with kron prod
    #######################################

    # Contruct tensor form of Dd
    Dd = np.zeros((N**d,N**d))
    for i in range(d):
        tmp = np.array([1])
        for j in range(d):
            if i != j:
                tmp = np.kron(tmp,I)
            else:
                tmp = np.kron(tmp,D)
        Dd += tmp

    Dd_tensor = DT.matkron_to_mattensor(Dd,[N for i in range(d)],[N for i in range(d)])

    TT_tensor = TT.to_tensor()

    # From Dd_tensor obtain a TT representation with accuracy eps
    eps = 0.001
    TT_svd = DT.TTmat(Dd_tensor,nrows=N,ncols=N,eps=eps)

    if np.abs(Dd[T_idx[0],T_idx[1]] - TT_svd[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])]) < d * 100.*np.spacing(1):
        print_ok("0.7 Tensor Test: Entry comparison FULL, TT-svd-kron")
    else:
        print_fail("0.7 Tensor Test: Entry comparison FULL, TT-svd-kron",
                   "  T - TT-svd = %e" % np.abs(Dd[T_idx[0],T_idx[1]]-TT_svd[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])]))

    Dd_norm = npla.norm(Dd,ord='fro')
    TT_svd_norm = mla.norm(TT_svd,ord='fro')
    if np.abs(Dd_norm - TT_svd_norm) < eps * Dd_norm:
        print_ok("0.7 Tensor Test: Frobenius norm FULL, TT-svd-kron")
    else:
        print_fail("0.7 Tensor Test: Frobenius norm FULL, TT-svd-kron",
                   "                  T          TT_svd\n"\
                       "Frobenius norm  %.5f         %.5f" % (npla.norm(Dd,ord='fro'), mla.norm(TT_svd,ord='fro')))

    #######################################
    # Check TT-rounding
    #######################################
    TT_round = TT.copy()
    eps = 0.001
    TT_round.rounding(eps)

    if np.abs(TT_round[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])] - TT_svd[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])]) < d * 100.*np.spacing(1):
        print_ok("0.8 Tensor Test: Entry comparison (post-rounding) TT-svd, TT-round")
    else:
        print_fail("0.8 Tensor Test: Entry comparison  (post-rounding) TT-svd, TT-round",
               "  T-svd - TT-round = %e" % np.abs(TT_svd[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])] - TT_round[DT.idxfold(nrows,T_idx[0]),DT.idxfold(ncols,T_idx[1])]))

    Dd_norm = npla.norm(Dd,ord='fro')
    TT_svd_norm = mla.norm(TT_svd,ord='fro')
    TT_round_norm = mla.norm(TT_round,ord='fro')
    if np.abs(Dd_norm - TT_svd_norm) < eps * Dd_norm and np.abs(TT_svd_norm - TT_round_norm) < eps * Dd_norm:
        print_ok("0.8 Tensor Test: Frobenius norm (post-rounding) FULL, TT-svd, TT-round")
    else:
        print_fail("0.8 Tensor Test: Frobenius norm (post-rounding) FULL, TT-svd, TT-round",
                   "                  T          TT_svd         TT_rounding\n"\
                       "Frobenius norm  %.5f         %.5f           %.5f" % (Dd_norm, TT_svd_norm, TT_round_norm))

opt = None
while (not len(RUNTESTS)>0 and (opt == None  or (opt != 'c' and opt != 's' and opt != 'q'))):
    print("Rounding convergence tests")
    print("\t [c]: continue")
    print("\t [s]: skip")
    print("\t [q]: exit")
    opt = sys.stdin.read(1)
    if (opt ==  'q'):
        exit()

if (1 in RUNTESTS) or opt == 'c':
    ###################################################################
    # Test timings and comp. rate for compression of Laplace-like op.
    ###################################################################
    eps = 0.001
    Ns = 2**np.arange(4,7,1,dtype=int)
    ds = 2**np.arange(4,6,dtype=int)
    timing = np.zeros((len(Ns),len(ds)))
    comp_rate = np.zeros((len(Ns),len(ds)))
    for i_N, N in enumerate(Ns):
        D = np.diag(-np.ones((N-1)),-1) + np.diag(-np.ones((N-1)),1) + np.diag(2*np.ones((N)),0)
        I = np.eye(N)
        D_flat = D.flatten()
        I_flat = I.flatten()
        for i_d, d in enumerate(ds):
            sys.stdout.write('N=%d   , d=%d      [STARTED]\r' % (N,d))
            sys.stdout.flush()
            # Canonical form of n-dimentional Laplace operator
            CPtmp = [] # U[i][alpha,k] = U_i(alpha,k)
            for i in range(d):
                CPi = np.empty((d,N**2))
                for alpha in range(d):
                    if i != alpha:
                        CPi[alpha,:] = I_flat
                    else:
                        CPi[alpha,:] = D_flat
                CPtmp.append(CPi)
            CP = DT.Candecomp(CPtmp)

            # Canonical to TT
            sys.stdout.write("\033[K")
            sys.stdout.write('N=%4d   , d=%3d      [CP->TT]\r' % (N,d))
            sys.stdout.flush()
            TT = DT.TTmat(CP,nrows=N,ncols=N)
            TT_pre = TT.copy()
            pre_norm = mla.norm(TT_pre,'fro')

            # Rounding TT
            sys.stdout.write("\033[K")
            sys.stdout.write('N=%4d   , d=%3d      [TT-round]\r' % (N,d))
            sys.stdout.flush()
            st = time.clock()
            TT.rounding(eps)
            end = time.clock()

            if np.max(TT.ranks()) != 2:
                print_fail("\033[K" + "1.1 Compression Timing N=%4d   , d=%3d      [RANK ERROR]   Time: %f" % (N,d,end-st))
            elif mla.norm(TT_pre - TT,'fro') > eps * pre_norm:
                print_fail("\033[K" + "1.1 Compression Timing N=%4d   , d=%3d      [NORM ERROR]   Time: %f" % (N,d,end-st))
            else:
                print_ok("\033[K" + "1.1 Compression Timing N=%4d   , d=%3d      [ENDED]   Time: %f" % (N,d,end-st))

            comp_rate[i_N,i_d] = float(TT.size())/N**(2.*d)
            timing[i_N,i_d] = end-st

    # Compute scalings with respect to N and d
    if PLOTTING:
        d_sc = np.polyfit(np.log2(ds),np.log2(timing[-1,:]),1)[0]
        N_sc = np.polyfit(np.log2(Ns),np.log2(timing[:,-1]),1)[0]
        sys.stdout.write("Scaling: N^%f, d^%f\n" % (N_sc,d_sc))
        sys.stdout.flush()

        plt.figure(figsize=(14,7))
        plt.subplot(1,2,1)
        plt.loglog(Ns,comp_rate[:,-1],'o-',basex=2, basey=2)
        plt.grid()
        plt.xlabel('N')
        plt.ylabel('Comp. Rate TT/FULL')
        plt.subplot(1,2,2)
        plt.loglog(Ns,timing[:,-1],'o-',basex=2, basey=2)
        plt.grid()
        plt.xlabel('N')
        plt.ylabel('Round Time (s)')
        plt.show(block=False)

        plt.figure(figsize=(14,7))
        plt.subplot(1,2,1)
        plt.loglog(ds,comp_rate[-1,:],'o-',basex=2, basey=2)
        plt.grid()
        plt.xlabel('d')
        plt.ylabel('Comp. Rate TT/FULL')
        plt.subplot(1,2,2)
        plt.loglog(ds,timing[-1,:],'o-',basex=2, basey=2)
        plt.grid()
        plt.xlabel('d')
        plt.ylabel('Round Time (s)')
        plt.show(block=False)

        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        (NN,dd) = np.meshgrid(np.log2(Ns),np.log2(ds))
        T = timing.copy().T
        T[T==0.] = np.min(T[np.nonzero(T)])
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(NN,dd,np.log2(T),rstride=1, cstride=1, cmap=cm.coolwarm,
                linewidth=0, antialiased=False)
        plt.show(block=False)

opt = None
while (not len(RUNTESTS)>0 and (opt == None  or (opt != 'c' and opt != 's' and opt != 'q'))):
    print("Matrix-vector product tests:")
    print("\t [c]: continue")
    print("\t [s]: skip")
    print("\t [q]: exit")
    opt = sys.stdin.read(1)
    if (opt ==  'q'):
        exit(0)

if (2 in RUNTESTS) or opt == 'c':
    #####################################################################################
    # Test matrix-vector product by computing the matrix-vector product
    #####################################################################################
    span = np.array([0.,1.])
    d = 2
    N = 16
    h = 1/float(N-1)
    eps = 1e-10

    # sys.stdout.write("Matrix-vector: Laplace  N=%4d   , d=%3d      [START] \n" % (N,d))
    # sys.stdout.flush()

    # Construct 2D Laplace (with 2nd order finite diff)
    D = -1./h**2. * ( np.diag(np.ones((N-1)),-1) + np.diag(np.ones((N-1)),1) + np.diag(-2.*np.ones((N)),0) )
    D[0,0:3] = np.array([1./(3.*h**2.),-2./(3.*h**2.),1./(3.*h**2.)])
    D[-1,-3:] = -np.array([1./(3.*h**2.),-2./(3.*h**2.),1./(3.*h**2.)])
    I = np.eye(N)
    FULL_LAP = np.zeros((N**d,N**d))
    for i in range(d):
        tmp = np.array([[1.]])
        for j in range(d):
            if i != j: tmp = np.kron(tmp,I)
            else: tmp = np.kron(tmp,D)
        FULL_LAP += tmp

    # Construction of TT Laplace operator
    CPtmp = []
    # D = -1./h**2. * ( np.diag(np.ones((N-1)),-1) + np.diag(np.ones((N-1)),1) + np.diag(-2.*np.ones((N)),0) )
    # I = np.eye(N)
    D_flat = D.flatten()
    I_flat = I.flatten()
    for i in range(d):
        CPi = np.empty((d,N**2))
        for alpha in range(d):
            if i != alpha:
                CPi[alpha,:] = I_flat
            else:
                CPi[alpha,:] = D_flat
        CPtmp.append(CPi)

    CP_lap = DT.Candecomp(CPtmp)
    TT_LAP = DT.TTmat(CP_lap,nrows=N,ncols=N)
    TT_LAP.rounding(eps)
    CPtmp = None
    CP_lap = None

    # Construct input vector
    X = np.linspace(span[0],span[1],N)
    SIN = np.sin(X)
    I = np.ones((N))
    FULL_SIN = np.zeros((N**d))
    for i in range(d):
        tmp = np.array([1.])
        for j in range(d):
            if i != j: tmp = np.kron(tmp,I)
            else: tmp = np.kron(tmp,SIN)
        FULL_SIN += tmp

    if PLOTTING:
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        (XX,YY) = np.meshgrid(X,X)
        fig = plt.figure()
        if d == 2:
            # Plot function
            ax = fig.add_subplot(221,projection='3d')
            ax.plot_surface(XX,YY,FULL_SIN.reshape((N,N)),rstride=1, cstride=1, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False)
            plt.show(block=False)

    # Construct TT input vector
    CPtmp = []
    for i in range(d):
        CPi = np.empty((d,N))
        for alpha in range(d):
            if i != alpha: CPi[alpha,:] = I
            else: CPi[alpha,:] = SIN
        CPtmp.append(CPi)
    
    CP_SIN = DT.Candecomp(CPtmp)
    TT_SIN = DT.TTvec(CP_SIN)
    TT_SIN.rounding(eps)
    
    if PLOTTING and d == 2:
        # Plot function
        ax = fig.add_subplot(222,projection='3d')
        ax.plot_surface(XX,YY,TT_SIN.to_tensor(),rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
        plt.show(block=False)

    # Apply full laplacian
    FULL_RES = np.dot(FULL_LAP,FULL_SIN)
    if PLOTTING and d == 2:
        # Plot function
        ax = fig.add_subplot(223,projection='3d')
        ax.plot_surface(XX,YY,FULL_RES.reshape((N,N)),rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
        plt.show(block=False)
    
    # Apply TT laplacian
    TT_RES = mla.dot(TT_LAP,TT_SIN)
    if PLOTTING and d == 2:
        # Plot function
        ax = fig.add_subplot(224,projection='3d')
        ax.plot_surface(XX,YY,TT_RES.to_tensor(),rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
        plt.show(block=False)

    # Check results
    if not np.allclose(FULL_RES,TT_RES.to_tensor().flatten()):
        print_fail("2.1 Matrix-vector: Laplace  N=%4d   , d=%3d" % (N,d))
    else:
        print_ok("2.1 Matrix-vector: Laplace  N=%4d   , d=%3d" % (N,d))

    #####################################################################################
    # Test matrix-vector product by computing the matrix-vector product of randomly generated input
    #####################################################################################
    span = np.array([0.,1.])
    d = 3
    nrows = [16,20,24]
    ncols = [16,12,14]
    if isinstance(nrows,int): nrows = [nrows for i in range(d)]
    if isinstance(ncols,int): ncols = [ncols for i in range(d)]
    eps = 1e-10

    # sys.stdout.write("Matrix-vector: Random\n  nrows=[%s],\n  ncols=[%s],  d=%3d      [START] \n" % (','.join(map(str,nrows)),','.join(map(str,ncols)),d))
    # sys.stdout.flush()

    # Construction of TT random matrix
    TT_RAND = DT.randmat(d,nrows,ncols)

    # Construct FULL random tensor
    FULL_RAND = TT_RAND.to_tensor()
    import itertools
    rowcol = list(itertools.chain(*[[ri,ci] for (ri,ci) in zip(nrows,ncols)]))
    FULL_RAND = np.reshape(FULL_RAND,rowcol)
    idxswap = range(0,2*d,2)
    idxswap.extend(range(1,2*d,2))
    FULL_RAND = np.transpose(FULL_RAND,axes=idxswap)
    FULL_RAND = np.reshape(FULL_RAND,(np.prod(nrows),np.prod(ncols)))
    
    # Construct TT random vector
    TT_VEC = DT.randvec(d,ncols)

    # Construct FULL random vector
    FULL_VEC = TT_VEC.to_tensor().flatten()
    
    # Apply TT
    TT_RES = mla.dot(TT_RAND,TT_VEC)
    
    # Apply FULL
    FULL_RES = np.dot(FULL_RAND,FULL_VEC)

    # Check results
    if not np.allclose(FULL_RES,TT_RES.to_tensor().flatten()):
        print_fail("2.2 Matrix-vector: Random  N=%4d   , d=%3d" % (N,d),'')
    else:
        print_ok("2.2 Matrix-vector: Random  N=%4d   , d=%3d" % (N,d))

opt = None
while (not len(RUNTESTS)>0 and (opt == None  or (opt != 'c' and opt != 's' and opt != 'q'))):
    print("Matrix 2-norm tests:")
    print("\t [c]: continue")
    print("\t [s]: skip")
    print("\t [q]: exit")
    opt = sys.stdin.read(1)
    if (opt ==  'q'):
        exit(0)

if (3 in RUNTESTS) or opt == 'c':
    #####################################################################################
    # Test matrix 2-norm on random matrices
    #####################################################################################
    span = np.array([0.,1.])
    d = 3
    nrows = 16
    ncols = 16
    if isinstance(nrows,int): nrows = [nrows for i in range(d)]
    if isinstance(ncols,int): ncols = [ncols for i in range(d)]
    eps = 1e-6
    round_eps = 1e-12

    # sys.stdout.write("Matrix 2-norm: Random\n  nrows=[%s],\n  ncols=[%s],  d=%3d      [START] \n" % (','.join(map(str,nrows)),','.join(map(str,ncols)),d))
    # sys.stdout.flush()

    # Construction of TT random matrix
    TT_RAND = DT.randmat(d,nrows,ncols)

    # Construct FULL random tensor
    FULL_RAND = TT_RAND.to_tensor()
    import itertools
    rowcol = list(itertools.chain(*[[ri,ci] for (ri,ci) in zip(nrows,ncols)]))
    FULL_RAND = np.reshape(FULL_RAND,rowcol)
    idxswap = range(0,2*d,2)
    idxswap.extend(range(1,2*d,2))
    FULL_RAND = np.transpose(FULL_RAND,axes=idxswap)
    FULL_RAND = np.reshape(FULL_RAND,(np.prod(nrows),np.prod(ncols)))
    
    # Check results
    tt_norm = mla.norm(TT_RAND,2,round_eps=round_eps,eps=eps)
    full_norm = npla.norm(FULL_RAND,2)
    if np.abs(tt_norm-full_norm)/npla.norm(FULL_RAND,'fro') <= 0.02:
        print_ok("3.1 Matrix 2-norm: Random  nrows=%s, ncols=%s , d=%3d  , TT-norm = %.5f , FULL-norm = %.5f" % (str(nrows),str(ncols),d,tt_norm,full_norm))
    else:
        print_fail("3.1 Matrix 2-norm: Random  nrows=%s, ncols=%s, d=%3d  , TT-norm = %.5f , FULL-norm = %.5f" % (str(nrows),str(ncols),d,tt_norm,full_norm),'')


# opt = 'a'
# while (opt != 'c' and opt != 's' and opt != 'q'):
#     print("Matrix-vector product test with Schrodinger operator:")
#     print("\t [c]: continue")
#     print("\t [s]: skip")
#     print("\t [q]: exit")
#     opt = sys.stdin.read(1)
#     if (opt ==  'q'):
#         exit(0)

# if opt == 'c':
#     #####################################################################################
#     # Test matrix-vector product by computing the smallest eigenvalue of the operator in
#     # "Tensor-Train decomposition" I.V.Oseledets
#     # "Algorithms in high dimensions" Beylkin and Mohlenkamp
#     #####################################################################################
#     span = np.array([0.,1.])
#     d = 2
#     N = 16
#     h = 1/float(N-1)
#     cv = 100.
#     cw = 5.
#     eps =1e-10

#     # Construction of TT Laplace operator
#     CPtmp = []
#     D = -1./h**2. * ( np.diag(np.ones((N-1)),-1) + np.diag(np.ones((N-1)),1) + np.diag(-2.*np.ones((N)),0) )
#     I = np.eye(N)
#     D_flat = D.flatten()
#     I_flat = I.flatten()
#     for i in range(d):
#         CPi = np.empty((d,N**2))
#         for alpha in range(d):
#             if i != alpha:
#                 CPi[alpha,:] = I_flat
#             else:
#                 CPi[alpha,:] = D_flat
#         CPtmp.append(CPi)
    
#     CP_lap = DT.Candecomp(CPtmp)
#     TT_lap = DT.TTmat(CP_lap,nrows=N,ncols=N)
#     TT_lap.rounding(eps)
#     CPtmp = None
#     CP_lap = None

#     # Construction of TT Potential operator
#     CPtmp = []
#     X = np.linspace(span[0],span[1],N)
#     # B = np.diag(np.cos(2.*np.pi*X),0)
#     B = np.diag(np.cos(X),0)
#     I = np.eye(N)
#     B_flat = B.flatten()
#     I_flat = I.flatten()
#     for i in range(d):
#         CPi = np.empty((d,N**2))
#         for alpha in range(d):
#             if i != alpha:
#                 CPi[alpha,:] = I_flat
#             else:
#                 CPi[alpha,:] = B_flat
#         CPtmp.append(CPi)
    
#     CP_pot = DT.Candecomp(CPtmp)
#     TT_pot = DT.TTmat(CP_pot,nrows=N,ncols=N)
#     TT_pot.rounding(eps)
#     CPtmp = None
#     CP_pot = None

#     # Construction of TT electron-electron interaction
#     CPtmp_cos = []
#     CPtmp_sin = []
#     X = np.linspace(span[0],span[1],N)
#     # Bcos = np.diag(np.cos(2.*np.pi*X),0)
#     # Bsin = np.diag(np.sin(2.*np.pi*X),0)
#     Bcos = np.diag(np.cos(X),0)
#     Bsin = np.diag(np.sin(X),0)
#     I = np.eye(N)
#     # D_flat = D.flatten()
#     Bcos_flat = Bcos.flatten()
#     Bsin_flat = Bsin.flatten()
#     I_flat = I.flatten()

#     for i in range(d):
#         CPi_cos = np.zeros((d*(d-1)/2,N**2))
#         CPi_sin = np.zeros((d*(d-1)/2,N**2))
#         k=0
#         for alpha in range(d):
#             for beta in range(alpha+1,d):
#                 if alpha == i or beta == i :
#                     CPi_cos[k,:] = Bcos_flat
#                     CPi_sin[k,:] = Bsin_flat
#                 else:
#                     CPi_cos[k,:] = I_flat
#                     CPi_sin[k,:] = I_flat
#                 k += 1
#         CPtmp_cos.append(CPi_cos)
#         CPtmp_sin.append(CPi_sin)

#     CP_int_cos = DT.Candecomp(CPtmp_cos)
#     CP_int_sin = DT.Candecomp(CPtmp_sin)
#     TT_int_cos = DT.TTmat(CP_int_cos,nrows=N,ncols=N)
#     TT_int_sin = DT.TTmat(CP_int_sin,nrows=N,ncols=N)
#     TT_int_cos.rounding(eps)
#     TT_int_sin.rounding(eps)
#     TT_int = (TT_int_cos + TT_int_sin).rounding(eps)
#     CPtmp_cos = None
#     CPtmp_sin = None
#     CP_int_cos = None
#     CP_int_sin = None

#     # # Construction of TT Scholes-tensor
#     # CPtmp = []
#     # X = np.linspace(span[0],span[1],N)
#     # D = 1./(2*h) * (np.diag(np.ones(N-1),1) - np.diag(np.ones(N-1),-1))
#     # D[0,0] = -1./h
#     # D[0,1] = 1./h
#     # D[-1,-1] = 1./h
#     # D[-1,-2] = -1./h
#     # I = np.eye(N)
#     # D_flat = D.flatten()
#     # I_flat = I.flatten()
#     # for i in range(d):
#     #     CPi = np.zeros((d*(d-1)/2,N**2))
#     #     k = 0
#     #     for alpha in range(d):
#     #         for beta in range(alpha+1,d):
#     #             if alpha == i:
#     #                 CPi[k,:] = D_flat
#     #             elif beta == i:
#     #                 CPi[k,:] = D_flat
#     #             else:
#     #                 CPi[k,:] = I_flat
#     #             k += 1
#     #     CPtmp.append(CPi)

#     # CP_sch = DT.Candecomp(CPtmp)
#     # TT_sch = DT.TTmat(CP_sch,nrows=N,ncols=N)
#     # TT_sch.rounding(eps)

#     H = (TT_lap + TT_pot + TT_int).rounding(eps)
#     Cd = mla.norm(H,2)

#     # Identity tensor
#     TT_id = DT.eye(d,N)

#     Hhat = (Cd * TT_id - H).rounding(eps)
    
####################################################################################
# Test Steepest Descent method on simple multidim laplace equation
####################################################################################

opt = None
while (not len(RUNTESTS)>0 and (opt == None  or (opt != 'c' and opt != 's' and opt != 'q'))):
    print("Steepest Descent on Laplace eq.:")
    print("\t [c]: continue")
    print("\t [s]: skip")
    print("\t [q]: exit")
    opt = sys.stdin.read(1)
    if (opt ==  'q'):
        exit(0)

if (4 in RUNTESTS) or opt == 'c':
    import scipy.sparse as sp
    import scipy.sparse.linalg as spla

    span = np.array([0.,1.])
    d = 2
    N = 64
    h = 1/float(N-1)
    eps_cg = 1e-3
    eps_round = 1e-6

    # sys.stdout.write("Steepest Descent: Laplace  N=%4d   , d=%3d      [START] \n" % (N,d))
    # sys.stdout.flush()

    dofull = True
    try:
        # Construct d-D Laplace (with 2nd order finite diff)
        D = -1./h**2. * ( np.diag(np.ones((N-1)),-1) + np.diag(np.ones((N-1)),1) + np.diag(-2.*np.ones((N)),0) )
        D[0,0:2] = np.array([1.,0.])
        D[-1,-2:] = np.array([0.,1.])
        D_sp = sp.coo_matrix(D)
        I_sp = sp.identity(N)
        I = np.eye(N)
        FULL_LAP = sp.coo_matrix((N**d,N**d))
        for i in range(d):
            tmp = sp.identity((1))
            for j in range(d):
                if i != j: tmp = sp.kron(tmp,I_sp)
                else: tmp = sp.kron(tmp,D_sp)
            FULL_LAP = FULL_LAP + tmp
    except MemoryError:
        print "FULL CG: Memory Error"
        dofull = False

    # Construction of TT Laplace operator
    CPtmp = []
    D_flat = D.flatten()
    I_flat = I.flatten()
    for i in range(d):
        CPi = np.empty((d,N**2))
        for alpha in range(d):
            if i != alpha:
                CPi[alpha,:] = I_flat
            else:
                CPi[alpha,:] = D_flat
        CPtmp.append(CPi)

    CP_lap = DT.Candecomp(CPtmp)
    TT_LAP = DT.TTmat(CP_lap,nrows=N,ncols=N,is_sparse=[True]*d)
    TT_LAP.rounding(eps_round)
    CPtmp = None
    CP_lap = None

    # Construct Right hand-side (b=1, Dirichlet BC = 0)
    X = np.linspace(span[0],span[1],N)
    b1D = np.ones(N)
    b1D[0] = 0.
    b1D[-1] = 0.

    if dofull:
        # Construct the d-D right handside
        tmp = np.array([1.])
        for j in range(d):
            tmp = np.kron(tmp,b1D)
        FULL_b = tmp

    # Construct the TT right handside
    CPtmp = []
    for i in range(d):
        CPi = np.empty((1,N))
        CPi[0,:] = b1D
        CPtmp.append(CPi)
    CP_b = DT.Candecomp(CPtmp)
    TT_b = DT.TTvec(CP_b)
    TT_b.rounding(eps_round)
    
    if dofull:
        # Solve full system using npla.solve
        (FULL_RES,FULL_CONV) = spla.cg(FULL_LAP,FULL_b,tol=eps_cg)

    if PLOTTING:
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        (XX,YY) = np.meshgrid(X,X)
        fig = plt.figure(figsize=(18,7))
        plt.suptitle("SD")
        if d == 2:
            # Plot function
            ax = fig.add_subplot(131,projection='3d')
            ax.plot_surface(XX,YY,FULL_RES.reshape((N,N)),rstride=1, cstride=1, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False)
            plt.show(block=False)

    # Solve TT cg
    x0 = DT.zerosvec(d,N)
    (TT_RES,TT_conv,TT_info) = mla.sd(TT_LAP,TT_b,x0=x0,maxit=10000,eps=eps_cg,ext_info=True,eps_round=eps_round)
    if PLOTTING and d == 2:
        # Plot function
        ax = fig.add_subplot(132,projection='3d')
        ax.plot_surface(XX,YY,TT_RES.to_tensor(),rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
        plt.show(block=False)

    # Error
    if PLOTTING and d == 2:
        # Plot function
        ax = fig.add_subplot(133,projection='3d')
        ax.plot_surface(XX,YY,np.abs(TT_RES.to_tensor()-FULL_RES.reshape((N,N))),rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
        plt.show(block=False)

    err2 = npla.norm(TT_RES.to_tensor().flatten()-FULL_RES,2)
    if err2 < 1e-2:
        print_ok("4.1 SD: Laplace  N=%4d   , d=%3d  , 2-err=%f" % (N,d,err2))
    else:
        print_fail("4.1 SD: Laplace  N=%4d   , d=%3d  , 2-err=%f" % (N,d,err2))
    
####################################################################################
# Test Conjugate Gradient method on simple multidim laplace equation
####################################################################################

opt = None
while (not len(RUNTESTS)>0 and (opt == None  or (opt != 'c' and opt != 's' and opt != 'q'))):
    print("Conjugate-Gradient on Laplace eq.:")
    print("\t [c]: continue")
    print("\t [s]: skip")
    print("\t [q]: exit")
    opt = sys.stdin.read(1)
    if (opt ==  'q'):
        exit(0)

if (5 in RUNTESTS) or opt == 'c':
    import scipy.sparse as sp
    import scipy.sparse.linalg as spla

    span = np.array([0.,1.])
    d = 2
    N = 64
    h = 1/float(N-1)
    eps_cg = 1e-3
    eps_round = 1e-6

    # sys.stdout.write("Conjugate-Gradient: Laplace  N=%4d   , d=%3d      [START] \n" % (N,d))
    # sys.stdout.flush()

    dofull = True
    try:
        # Construct d-D Laplace (with 2nd order finite diff)
        D = -1./h**2. * ( np.diag(np.ones((N-1)),-1) + np.diag(np.ones((N-1)),1) + np.diag(-2.*np.ones((N)),0) )
        D[0,0:2] = np.array([1.,0.])
        D[-1,-2:] = np.array([0.,1.])
        D_sp = sp.coo_matrix(D)
        I_sp = sp.identity(N)
        I = np.eye(N)
        FULL_LAP = sp.coo_matrix((N**d,N**d))
        for i in range(d):
            tmp = sp.identity((1))
            for j in range(d):
                if i != j: tmp = sp.kron(tmp,I_sp)
                else: tmp = sp.kron(tmp,D_sp)
            FULL_LAP = FULL_LAP + tmp
    except MemoryError:
        print "FULL CG: Memory Error"
        dofull = False

    # Construction of TT Laplace operator
    CPtmp = []
    D_flat = D.flatten()
    I_flat = I.flatten()
    for i in range(d):
        CPi = np.empty((d,N**2))
        for alpha in range(d):
            if i != alpha:
                CPi[alpha,:] = I_flat
            else:
                CPi[alpha,:] = D_flat
        CPtmp.append(CPi)

    CP_lap = DT.Candecomp(CPtmp)
    TT_LAP = DT.TTmat(CP_lap,nrows=N,ncols=N,is_sparse=[True]*d)
    TT_LAP.rounding(eps_round)
    CPtmp = None
    CP_lap = None

    # Construct Right hand-side (b=1, Dirichlet BC = 0)
    X = np.linspace(span[0],span[1],N)
    b1D = np.ones(N)
    b1D[0] = 0.
    b1D[-1] = 0.

    if dofull:
        # Construct the d-D right handside
        tmp = np.array([1.])
        for j in range(d):
            tmp = np.kron(tmp,b1D)
        FULL_b = tmp

    # Construct the TT right handside
    CPtmp = []
    for i in range(d):
        CPi = np.empty((1,N))
        CPi[0,:] = b1D
        CPtmp.append(CPi)
    CP_b = DT.Candecomp(CPtmp)
    TT_b = DT.TTvec(CP_b)
    TT_b.rounding(eps_round)
    
    if dofull:
        # Solve full system using npla.solve
        (FULL_RES,FULL_CONV) = spla.cg(FULL_LAP,FULL_b,tol=eps_cg)

    if PLOTTING:
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        (XX,YY) = np.meshgrid(X,X)
        fig = plt.figure(figsize=(18,7))
        plt.suptitle("CG")
        if d == 2:
            # Plot function
            ax = fig.add_subplot(131,projection='3d')
            ax.plot_surface(XX,YY,FULL_RES.reshape((N,N)),rstride=1, cstride=1, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False)
            plt.show(block=False)

    # Solve TT cg
    x0 = DT.zerosvec(d,N)
    (TT_RES,TT_conv,TT_info) = mla.cg(TT_LAP,TT_b,x0=x0,eps=eps_cg,ext_info=True,eps_round=eps_round)
    if PLOTTING and d == 2:
        # Plot function
        ax = fig.add_subplot(132,projection='3d')
        ax.plot_surface(XX,YY,TT_RES.to_tensor(),rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
        plt.show(block=False)

    # Error
    if PLOTTING and d == 2:
        # Plot function
        ax = fig.add_subplot(133,projection='3d')
        ax.plot_surface(XX,YY,np.abs(TT_RES.to_tensor()-FULL_RES.reshape((N,N))),rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
        plt.show(block=False)
    
    err2 = npla.norm(TT_RES.to_tensor().flatten()-FULL_RES,2)
    if err2 < 1e-2:
        print_ok("5.1 CG: Laplace  N=%4d   , d=%3d  , 2-err=%f" % (N,d,err2))
    else:
        print_fail("5.1 CG: Laplace  N=%4d   , d=%3d  , 2-err=%f" % (N,d,err2))

####################################################################################
# Test Stabilized Bi-Conjugate Gradient method on simple multidim laplace equation
####################################################################################

opt = None
while (not len(RUNTESTS)>0 and (opt == None  or (opt != 'c' and opt != 's' and opt != 'q'))):
    print("Bi-Conjugate Gradient Stabilized on Laplace eq.:")
    print("\t [c]: continue")
    print("\t [s]: skip")
    print("\t [q]: exit")
    opt = sys.stdin.read(1)
    if (opt ==  'q'):
        exit(0)

if (6 in RUNTESTS) or opt == 'c':
    span = np.array([0.,1.])
    d = 2
    N = 16
    h = 1/float(N-1)
    eps_cg = 1e-8
    eps_round = 1e-10

    # sys.stdout.write("Bi-Conjugate Gradient Stab.: Laplace  N=%4d   , d=%3d      [START] \n" % (N,d))
    # sys.stdout.flush()

    # Construct d-D Laplace (with 2nd order finite diff)
    D = -1./h**2. * ( np.diag(np.ones((N-1)),-1) + np.diag(np.ones((N-1)),1) + np.diag(-2.*np.ones((N)),0) )
    D[0,0:2] = np.array([1.,0.])
    D[-1,-2:] = np.array([0.,1.])
    I = np.eye(N)
    FULL_LAP = np.zeros((N**d,N**d))
    for i in range(d):
        tmp = np.array([[1.]])
        for j in range(d):
            if i != j: tmp = np.kron(tmp,I)
            else: tmp = np.kron(tmp,D)
        FULL_LAP += tmp

    # Construction of TT Laplace operator
    CPtmp = []
    D_flat = D.flatten()
    I_flat = I.flatten()
    for i in range(d):
        CPi = np.empty((d,N**2))
        for alpha in range(d):
            if i != alpha:
                CPi[alpha,:] = I_flat
            else:
                CPi[alpha,:] = D_flat
        CPtmp.append(CPi)

    CP_lap = DT.Candecomp(CPtmp)
    TT_LAP = DT.TTmat(CP_lap,nrows=N,ncols=N)
    TT_LAP.rounding(eps_round)
    CPtmp = None
    CP_lap = None

    # Construct Right hand-side (b=1, Dirichlet BC = 0)
    X = np.linspace(span[0],span[1],N)
    b1D = np.ones(N)
    b1D[0] = 0.
    b1D[-1] = 0.
    # Construct the d-D right handside
    tmp = np.array([1.])
    for j in range(d):
        tmp = np.kron(tmp,b1D)
    FULL_b = tmp
    # Construct the TT right handside
    CPtmp = []
    for i in range(d):
        CPi = np.empty((1,N))
        CPi[0,:] = b1D
        CPtmp.append(CPi)
    CP_b = DT.Candecomp(CPtmp)
    TT_b = DT.TTvec(CP_b)
    TT_b.rounding(eps_round)
    

    # Solve full system using npla.solve
    FULL_RES = npla.solve(FULL_LAP,FULL_b)

    if PLOTTING:
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        (XX,YY) = np.meshgrid(X,X)
        fig = plt.figure(figsize=(18,7))
        plt.suptitle("BiCG-stab")
        if d == 2:
            # Plot function
            ax = fig.add_subplot(131,projection='3d')
            ax.plot_surface(XX,YY,FULL_RES.reshape((N,N)),rstride=1, cstride=1, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False)
            plt.show(block=False)

    # Solve TT cg
    x0 = DT.zerosvec(d,N)
    (TT_RES,conv,info) = mla.bicgstab(TT_LAP,TT_b,x0=x0,ext_info=True)
    print info
    if PLOTTING and d == 2:
        # Plot function
        ax = fig.add_subplot(132,projection='3d')
        ax.plot_surface(XX,YY,TT_RES.to_tensor(),rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
        plt.show(block=False)

    # Error
    if PLOTTING and d == 2:
        # Plot function
        ax = fig.add_subplot(133,projection='3d')
        ax.plot_surface(XX,YY,np.abs(TT_RES.to_tensor()-FULL_RES.reshape((N,N))),rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
        plt.show(block=False)

    err2 = npla.norm(TT_RES.to_tensor().flatten()-FULL_RES,2)
    if err2 < 1e-2:
        print_ok("6.1 BI-CGSTAB: Laplace  N=%4d   , d=%3d  , 2-err=%f" % (N,d,err2))
    else:
        print_fail("6.1 BI-CGSTAB: Laplace  N=%4d   , d=%3d  , 2-err=%f" % (N,d,err2))


####################################################################################
# Test GMRES method on simple multidim laplace equation
####################################################################################

opt = None
while (not len(RUNTESTS)>0 and (opt == None  or (opt != 'c' and opt != 's' and opt != 'q'))):
    print("GMRES on Laplace eq.:")
    print("\t [c]: continue")
    print("\t [s]: skip")
    print("\t [q]: exit")
    opt = sys.stdin.read(1)
    if (opt ==  'q'):
        exit(0)

if (7 in RUNTESTS) or opt == 'c':
    import scipy.sparse as sp
    import scipy.sparse.linalg as spla
    
    span = np.array([0.,1.])
    d = 2
    N = 64
    h = 1/float(N-1)
    eps_gmres = 1e-3
    eps_round = 1e-6

    # sys.stdout.write("GMRES: Laplace  N=%4d   , d=%3d      [START] \r" % (N,d))
    # sys.stdout.flush()

    # Construct d-D Laplace (with 2nd order finite diff)
    D = -1./h**2. * ( np.diag(np.ones((N-1)),-1) + np.diag(np.ones((N-1)),1) + np.diag(-2.*np.ones((N)),0) )
    D[0,0:2] = np.array([1.,0.])
    D[-1,-2:] = np.array([0.,1.])
    D_sp = sp.coo_matrix(D)
    I_sp = sp.identity(N)
    I = np.eye(N)
    FULL_LAP = sp.coo_matrix((N**d,N**d))
    for i in range(d):
        tmp = sp.identity((1))
        for j in range(d):
            if i != j: tmp = sp.kron(tmp,I_sp)
            else: tmp = sp.kron(tmp,D_sp)
        FULL_LAP = FULL_LAP + tmp

    # Construction of TT Laplace operator
    CPtmp = []
    D_flat = D.flatten()
    I_flat = I.flatten()
    for i in range(d):
        CPi = np.empty((d,N**2))
        for alpha in range(d):
            if i != alpha:
                CPi[alpha,:] = I_flat
            else:
                CPi[alpha,:] = D_flat
        CPtmp.append(CPi)

    CP_lap = DT.Candecomp(CPtmp)
    TT_LAP = DT.TTmat(CP_lap,nrows=N,ncols=N,is_sparse=[True]*d)
    TT_LAP.rounding(eps_round)
    CPtmp = None
    CP_lap = None

    # Construct Right hand-side (b=1, Dirichlet BC = 0)
    X = np.linspace(span[0],span[1],N)
    b1D = np.ones(N)
    b1D[0] = 0.
    b1D[-1] = 0.
    # Construct the d-D right handside
    tmp = np.array([1.])
    for j in range(d):
        tmp = np.kron(tmp,b1D)
    FULL_b = tmp
    # Construct the TT right handside
    CPtmp = []
    for i in range(d):
        CPi = np.empty((1,N))
        CPi[0,:] = b1D
        CPtmp.append(CPi)
    CP_b = DT.Candecomp(CPtmp)
    TT_b = DT.TTvec(CP_b)
    TT_b.rounding(eps_round)
    

    # Solve full system using npla.solve
    (FULL_RES,FULL_info) = spla.gmres(FULL_LAP,FULL_b,tol=eps_gmres)

    if PLOTTING:
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib import cm
        (XX,YY) = np.meshgrid(X,X)
        fig = plt.figure(figsize=(18,7))
        plt.suptitle("GMRES")
        if d == 2:
            # Plot function
            ax = fig.add_subplot(131,projection='3d')
            ax.plot_surface(XX,YY,FULL_RES.reshape((N,N)),rstride=1, cstride=1, cmap=cm.coolwarm,
                            linewidth=0, antialiased=False)
            plt.show(block=False)

    # Solve TT cg
    x0 = DT.zerosvec(d,N)
    (TT_RES,conv,TT_info) = mla.gmres(TT_LAP,TT_b,x0=x0,restart=10,eps=eps_gmres,ext_info=True)
    if PLOTTING and d == 2:
        # Plot function
        ax = fig.add_subplot(132,projection='3d')
        ax.plot_surface(XX,YY,TT_RES.to_tensor(),rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
        plt.show(block=False)

    # Error
    if PLOTTING and d == 2:
        # Plot function
        ax = fig.add_subplot(133,projection='3d')
        ax.plot_surface(XX,YY,np.abs(TT_RES.to_tensor()-FULL_RES.reshape((N,N))),rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0, antialiased=False)
        plt.show(block=False)

    err2 = npla.norm(TT_RES.to_tensor().flatten()-FULL_RES,2)
    if err2 < 1e-2:
        print_ok("7.1 GMRES: Laplace  N=%4d   , d=%3d  , 2-err=%f" % (N,d,err2))
    else:
        print_fail("7.1 GMRES: Laplace  N=%4d   , d=%3d  , 2-err=%f" % (N,d,err2))
