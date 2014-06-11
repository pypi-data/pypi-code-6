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

__all__ = ['add','mul','dot','kron','contraction','norm','sd','cg','bicgstab','gmres']

import sys
import numpy as np
import numpy.linalg as npla
from scipy import linalg as scla
from scipy import sparse as scsp
from scipy.sparse import linalg as spla

###########################################
# External Multi Linear Algebra operations
###########################################

def add(A,B):
    return A + B
    

def mul(A,B):
    """
    * If A,B are TTvec/TTmat -> Hadamard product of two TT tensors
    * If A TTvec/TTmat and B scalar -> multiplication by scalar
    """
    return A * B

def dot(A,B):
    from TensorToolbox.core import TTvec
    from TensorToolbox.core import TTmat

    if isinstance(A,TTvec) and isinstance(B,TTvec) and not isinstance(A,TTmat) and not isinstance(B,TTmat):
        if not A.init or not B.init: raise NameError("TensorToolbox.multilinalg.dot: TT not initialized correctly")
        
        # TT vector-vector dot product
        # Check consistency
        if A.shape() != B.shape(): raise NameError("TensorToolbox.multilinalg.dot: A.shape != B.shape")
        
        Y = []
        for i,(Ai,Bi) in enumerate(zip(A.TT,B.TT)):
            Ai_rsh = np.reshape(Ai,(Ai.shape[0],1,Ai.shape[1],Ai.shape[2]))
            Ai_rsh = np.transpose(Ai_rsh,axes=(0,3,1,2))
            Ai_rsh = np.reshape(Ai_rsh,(Ai.shape[0]*Ai.shape[2],Ai.shape[1]))
            
            Bi_rsh = np.transpose(Bi,axes=(1,0,2))
            Bi_rsh = np.reshape(Bi_rsh,(Bi.shape[1],Bi.shape[0]*Bi.shape[2]))

            Yi_rsh = np.dot(Ai_rsh,Bi_rsh)
            Yi_rsh = np.reshape(Yi_rsh,(Ai.shape[0],Ai.shape[2],1,Bi.shape[0],Bi.shape[2]))
            Yi_rsh = np.transpose(Yi_rsh,axes=(0,3,2,1,4))
            Yi = np.reshape(Yi_rsh,(Ai.shape[0]*Bi.shape[0],1,Ai.shape[2]*Bi.shape[2]))
            
            if i == 0:
                out = Yi[:,0,:]
            else:
                out = np.dot(out, Yi[:,0,:])
        
        return out[0,0]
    
    elif isinstance(A,np.ndarray) and isinstance(B,np.ndarray):
        # tensor-tensor dot product (np.tensordot)
        return np.tensordot(A,B,(range(A.ndim),range(B.ndim)))
    
    elif isinstance(A,TTmat) and isinstance(B,TTvec) and not isinstance(B,TTmat):
        
        if not A.init or not B.init: raise NameError("TensorToolbox.multilinalg.dot: TT not initialized correctly")

        # TT matrix-vector dot product
        # Check consistency
        if (A.sparse_only and len(A.sparse_TT) != len(B.TT)) or (not A.sparse_only and len(A.TT) != len(B.TT)):
            raise NameError("TensorToolbox.multilinalg.dot: A and B must have the same number of cores")
        
        for bsize,Acols in zip(B.shape(),A.ncols):
            if bsize != Acols:
                raise NameError("TensorToolbox.multilinalg.dot: Matrix and Vector mode dimensions are not consistent")
        
        Y = []
        for i,(Ai,Bi,is_sparse,sp_A) in enumerate(zip(A.TT,B.TT,A.is_sparse,A.sparse_TT)):
            Bi_rsh = np.transpose(Bi,axes=(1,0,2))
            Bi_rsh = np.reshape(Bi_rsh,(Bi.shape[1],Bi.shape[0]*Bi.shape[2]))
            
            if is_sparse:
                Yi_rsh = sp_A.dot(Bi_rsh)
            else:
                Ai_rsh = np.reshape(Ai,(Ai.shape[0],A.nrows[i],A.ncols[i],Ai.shape[2]))
                Ai_rsh = np.transpose(Ai_rsh,axes=(0,3,1,2))
                Ai_rsh = np.reshape(Ai_rsh,(Ai.shape[0]*Ai.shape[2]*A.nrows[i],A.ncols[i]))
                Yi_rsh = np.dot(Ai_rsh,Bi_rsh)
            
            Ai0 = A.ranks()[i]
            Ai2 = A.ranks()[i+1]
            Yi_rsh = np.reshape(Yi_rsh,(Ai0,Ai2,A.nrows[i],Bi.shape[0],Bi.shape[2]))
            Yi_rsh = np.transpose(Yi_rsh,axes=(0,3,2,1,4))
            Yi = np.reshape(Yi_rsh,(Ai0*Bi.shape[0],A.nrows[i],Ai2*Bi.shape[2]))
            
            Y.append(Yi)
                
        return TTvec(Y)
    
    elif isinstance(A,TTmat) and isinstance(B,TTmat):
        
        if not A.init or not B.init: raise NameError("TensorToolbox.multilinalg.dot: TT not initialized correctly")

        # TT matrix-matrix dot product
        # Check consistency
        if len(A.TT) != len(B.TT):
            raise NameError("TensorToolbox.multilinalg.dot: A and B must have the same number of cores")
        
        for Brows,Acols in zip(B.nrows,A.ncols):
            if Brows != Acols:
                raise NameError("TensorToolbox.multilinalg.dot: Matrices mode dimensions are not consistent")
        
        Y = []
        for i,(Ai,Bi) in enumerate(zip(A.TT,B.TT)):
            Ai_rsh = np.reshape(Ai,(Ai.shape[0],A.nrows[i],A.ncols[i],Ai.shape[2]))
            Ai_rsh = np.transpose(Ai_rsh,axes=(0,3,1,2))
            Ai_rsh = np.reshape(Ai_rsh,(Ai.shape[0]*Ai.shape[2]*A.nrows[i],A.ncols[i]))

            Bi_rsh = np.reshape(Bi,(Bi.shape[0],B.nrows[i],B.ncols[i],Bi.shape[2]))
            Bi_rsh = np.transpose(Bi_rsh,axes=(1,0,3,2))
            Bi_rsh = np.reshape(Bi_rsh,(B.nrows[i],Bi.shape[0]*Bi.shape[2]*B.ncols[i]))
            
            Yi_rsh = np.dot(Ai_rsh,Bi_rsh)
            
            Yi_rsh = np.reshape(Yi_rsh,(Ai.shape[0],Ai.shape[2],A.nrows[i],Bi.shape[0],Bi.shape[2],B.ncols[i]))
            Yi_rsh = np.transpose(Yi_rsh,axes=(0,3,2,5,1,4))
            Yi = np.reshape(Yi_rsh,(Ai.shape[0]*Bi.shape[0],A.nrows[i]*B.ncols[i],Ai.shape[2]*Bi.shape[2]))
            
            Y.append(Yi)
        
        return TTmat(Y,A.nrows,B.ncols)
    
    elif isinstance(A,TTmat) and isinstance(B,np.ndarray):
        
        if not A.init: raise NameError("TensorToolbox.multilinalg.dot: TT not initialized correctly")
        
        # matrix-vector dot product with TTmat and full vector
        # Check consistency
        if len(A.shape()) != B.ndim:
            raise NameError("TensorToolbox.multilinalg.dot: A and B must have the same number of dimensions")
        for bsize,Acols in zip(B.shape,A.ncols):
            if bsize != Acols:
                raise NameError("TensorToolbox.multilinalg.dot: Matrix and Vector mode dimensions are not consistent")
        
        Bshape = B.shape
        Y = np.reshape(B,( (1,) + Bshape ))
        Yshape = Y.shape
        
        for k, Ak in enumerate(A.TT):
            # Note: Ak(alpha_{k-1},(i_k,j_k),alpha_{k})
            # Reshape it to Ak((alpha_{k},i_k),(alpha_{k-1},j_k))
            alpha0 = Ak.shape[0]
            alpha1 = Ak.shape[2]
            Ak_rsh = np.reshape(Ak, (alpha0,A.nrows[k],A.ncols[k],alpha1))
            Ak_rsh = np.transpose(Ak_rsh, axes=(3,1,0,2)) # Ak(alpha_{k},i_k,alpha_{k},j_k)
            Ak_rsh = np.reshape(Ak_rsh, (alpha1 * A.nrows[k], alpha0 * A.ncols[k]))
            
            # Reshape Y to Y((alpha_{k-1},j_k),(i_1,..,i_k-1,j_k+1,..,j_d))
            Y = np.transpose(Y,axes=(0,k+1)+tuple(range(1,k+1))+tuple(range(k+2,len(Bshape)+1)))
            Y = np.reshape( Y,(alpha0 * Yshape[k+1], np.prod(Yshape[1:k+1]) * np.prod(Yshape[k+2:])) )
            
            # Dot product
            Y = np.dot(Ak_rsh,Y)
            
            # Reshape Y
            Y = np.reshape(Y, (alpha1, A.nrows[k]) + Yshape[1:k+1] + Yshape[k+2:])
            Y = np.transpose(Y, axes=(0,) + tuple(range(2,k+2)) + (1,) + tuple(range(k+2,len(Bshape)+1)) )
            Yshape = Y.shape
        
        if Y.shape[0] != 1: raise NameError("TensorToolbox.multilinalg.dot: Last core dimenstion error")
        
        Y = np.reshape(Y,Y.shape[1:])
        
        return Y
    
    else:
        raise NameError("TensorToolbox.multilinalg.dot: Inner product not implemented for the input types")

def kron(A,B):
    """
    Kron product between two tensors in TT format.
    Complexity: O(1)
    """
    from TensorToolbox.core import TTvec

    if not A.init or not B.init: raise NameError("TensorToolbox.multilinalg.kron: TT not initialized correctly")
    if not type(A) is type(B): raise NameError("TensorToolbox.multilinalg.kron: conflicting input types")
    
    C = A.copy()
    C.kron(B)
    return C

def contraction(A,U):
    """
    Multidimensional contraction of tensor A with vectors in list U.
    Complexity: O(dnr^2)

    Syntax:
        ``W = contraction(A,U)``

    :param A: Tensor in some form
    :param U: list of vectors of dimensions n_k for performing the contraction
    :type list U: list of vectors with dimension n_k (where n_k is the size of each tensor dimension)
    """
    from TensorToolbox.core import TTvec

    if isinstance(A,TTvec):
        if not A.init: raise NameError("TensorToolbox.multilinalg.contraction: TT not initialized correctly")

        # Check consistency
        if len(A.TT) != len(U): raise NameError("TensorToolbox.multilinalg.contraction: len(U) is not consistent with the number of cores of A")
        for i in range(len(A.TT)):
            if A.TT[i].shape[1] != len(U[i]): raise NameError("TensorToolbox.multilinalg.TT.contraction: len(U[%d]) is not consistent with the size of dimension %d of A" % (i,i))

        W = np.ones((1,1))
        for i in range(len(A.TT)):
            Gamma_i = np.zeros(A.TT[i][:,0,:].shape)
            for j in range(A.TT[i].shape[1]):
                Gamma_i += U[i][j] * A.TT[i][:,j,:]
            W = np.dot(W,Gamma_i)

        return W
    
    else:
        raise NameError("TensorToolbox.multilinalg.contraction: contraction not implemented for the input types")

def norm(A,ord='fro',round_eps=1e-10,eps=1e-4,maxit=1000,pow_guess=None,info=False):
    """
    Compute the norm of tensor A

    Syntax:
        ``w = norm(A,[ord])``

    :param A: Tensor in some form
    :param ord: Specifies the type of norm that needs to be computed. Available norms are
                * Frobenius norm: 'fro'
    """
    from TensorToolbox.core import TTvec
    from TensorToolbox.core import TTmat
    
    if ord == 'fro':
        if isinstance(A,TTvec):            
            # For the Frobenius norm in general we need to make the right to left rounding part
            # and store the Frobenius norms of the R matrices (????)
            d = len(A.TT)
            ns = A.shape()
            # Right to left orthogonalization
            nrm = np.empty(d,dtype=np.float64)
            C = A.TT[d-1]
            for k in range(d-1,0,-1):
                # Computation of rq
                alphakm1 = C.shape[0]
                betak = C.shape[2]
                Gk = np.reshape(C,(alphakm1,C.shape[1]*betak))
                (R,Q) = scla.rq(Gk,mode='economic') # Only R is needed
                betakm1 = R.shape[1]
                nrm[k] = npla.norm(R,'fro')
                R = R / max(nrm[k],1e-300)
                # 3-mode product G[k-1] x_3 R
                C = np.reshape(A.TT[k-1],(A.TT[k-1].shape[0]*A.TT[k-1].shape[1],A.TT[k-1].shape[2]))
                C = np.reshape(np.dot(C,R),(A.TT[k-1].shape[0],A.TT[k-1].shape[1],betakm1))
            nrm[0] = npla.norm(C.flatten(),2)
            return np.prod(nrm)
            
        elif isinstance(A,np.ndarray):
            return np.sqrt(np.sum(A**2.))
        else:
            raise NameError("TensorToolbox.multilinalg.norm: Frobenius norm not implemented for the input types")
    if ord == 2:
        from TensorToolbox.core import randvec
        if isinstance(A,TTvec) and not isinstance(A,TTmat):
            # For vectors 2-norm == Frob norm
            return norm(A,'fro')
        elif isinstance(A,TTmat):
            # 2-norm of matrix
            # Use power method to determine the maximum eigenvalue of the operator 
            # within a certain accuracy. (This works only if lmb_1 has multiplicity 1)
            if pow_guess == None:
                # Use randomly generated starting vector guess with dimensions A.ncols
                pow_guess = randvec(len(A.shape()),A.ncols)
            elif isinstance (pow_guess,TTvec) and not isinstance(pow_guess,Tmat):
                # Check consistency
                if list(pow_guess.shape()) != list(A.ncols):
                    raise NameError("TensorToolbox.multilinalg.norm: Initial guess vector provided is in TTvec format, but the shape does not agree with A.ncols")
            else:
                raise NameError("TensorToolbox.multilinalg.norm: Initial guess vector provided is not in TTvec format")
            
            # Power iteration method
            q = pow_guess
            lmb = 1.
            k = 0
            while norm( dot(A,q) - lmb * q ,2) > eps and k < maxit:
                k += 1
                q = dot(A,q).rounding(round_eps)
                q *= 1./norm(q,2)
                lmb = dot(q,dot(A,q))
            
            return lmb
        else:
            raise NameError("TensorToolbox.multilinalg.norm: 2-norm not implemented for the input types")
    else:
        raise NameError("TensorToolbox.multilinalg.norm: norm not implemented for the input types")


###########################################
# Iterative solvers of linear equations
###########################################

def sd(A,b,x0=None,eps=1e-8,maxit=1000,eps_round=1e-10,ext_info=False):
    """ Solves the system :math:`Ax=b` using the Steepest Descent method in Tensor Train format.
    
    :param TTmat A: Tensor train matrix
    :param TTvec/ndarray b: Right hand side
    
    :param TTvec/ndarray x0: [default == :py:func:`TensorToolbox.core.zerosvec`] initial guess of solution ``x``
    :param float eps: [default == 1e-8] stop criteria
    :param int maxit: [default == 1000] maximum number of iterations
    :param float eps_round: [default == 1e-10] accuracy for Tensor Train rounding operations
    :param bool ext_info: [default == False] whehter of not to have additional info returned

    :return: tuple :py:data:`(x,conv,info)`
       
       * :py:data:`x` (TTvec): solution of the linear system if converged or last iterate if not converged
       * :py:data:`conv` (bool): True -> converged, False -> Not converged / Zero Inner Product exeception
       * :py:data:`info` (dict): ``iter`` -> total number of iterations; ``r`` -> last residual in TT format; ``res`` -> residual history
    
    """

    from TensorToolbox.core import TTvec
    from TensorToolbox.core import zerosvec
    from TensorToolbox.core import TTmat

    if isinstance(A,TTmat):
        if not A.init : raise NameError("TensorToolbox.multilinalg.cg: TT not initialized correctly")
        
        if isinstance(b,TTvec) and not isinstance(b,TTmat): is_tt = True
        elif isinstance(b,np.ndarray): is_tt = False
        else: raise NameError("TensorToolbox.multilinalg.cg: invalid type of b")

        if is_tt: 
            if not b.init:
                raise NameError("TensorToolbox.multilinalg.cg: TT not initialized correctly")
        
        if x0 == None:
            if is_tt:
                x0 = zerosvec(len(b.shape()),b.shape())
            else:
                x0 = np.zeros(b.shape)
        else:
            if is_tt:
                if not isinstance(x0,TTvec) or b.shape() != x0.shape():
                    raise NameError("TensorToolbox.multilinalg.cg: Initial guess must be in TT format and have the same shape of b")
            else:
                if not isinstance(x0,np.ndarray) or b.shape != x0.shape:
                    raise NameError("TensorToolbox.multilinalg.cg: Initial guess must be in ndarray format and have the same shape of b")

        # Steepest descent init
        x = x0.copy()
        i = 0
        r = (b - dot(A,x)).rounding(eps_round)
        p = dot(A,r).rounding(eps_round)
        res = [dot(r,r)]
        delta_0 = res[-1]
        while i < maxit and res[-1] > eps**2. * delta_0:
            alpha = dot(r,r)/dot(p,r)
            x += alpha * r
            x.rounding(eps_round)
            r -= alpha * p
            r.rounding(eps_round)
            res.append(norm(r,2))
            p = dot(A,r).rounding(eps_round)
            p.rounding(eps_round)
            
            if isinstance(x,TTvec):
                sys.stdout.write("SD: err=%e ranks=%s\r" % (res[-1],x.ranks()))
            elif isinstance(x,np.ndarray):
                sys.stdout.write("SD: err=%e \r" % (res[-1]))
            sys.stdout.flush()

            i += 1

        conv = (i < maxit)
        if ext_info:
            info = {'iter': i,
                    'r'   : r,
                    'res' : res}
            return (x,conv,info)
        else:
            return (x,conv)

        

def cg(A,b,x0=None,eps=1e-8,maxit=1000,eps_round=1e-10,ext_info=False):
    """ Solves the system :math:`Ax=b` using the Conjugate Gradient method in Tensor Train format.
    
    :param TTmat A: Tensor train matrix
    :param TTvec/ndarray b: Right hand side
    
    :param TTvec/ndarray x0: [default == :py:func:`TensorToolbox.core.zerosvec`] initial guess of solution ``x``
    :param float eps: [default == 1e-8] stop criteria for Bi-CGSTAB iterations
    :param int maxit: [default == 1000] maximum number of iterations for Bi-CGSTAB
    :param float eps_round: [default == 1e-10] accuracy for Tensor Train rounding operations
    :param bool ext_info: [default == False] whehter of not to have additional info returned

    :return: tuple :py:data:`(x,conv,info)`
       
       * :py:data:`x` (TTvec): solution of the linear system if converged or last iterate if not converged
       * :py:data:`conv` (bool): True -> converged, False -> Not converged / Zero Inner Product exeception
       * :py:data:`info` (dict): ``iter`` -> total number of iterations; ``r`` -> last residual in TT format; ``res`` -> residual history
    
    """

    from TensorToolbox.core import TTvec
    from TensorToolbox.core import zerosvec
    from TensorToolbox.core import TTmat

    if isinstance(A,TTmat):
        if not A.init : raise NameError("TensorToolbox.multilinalg.cg: TT not initialized correctly")
        
        if isinstance(b,TTvec) and not isinstance(b,TTmat): is_tt = True
        elif isinstance(b,np.ndarray): is_tt = False
        else: raise NameError("TensorToolbox.multilinalg.cg: invalid type of b")

        if is_tt: 
            if not b.init:
                raise NameError("TensorToolbox.multilinalg.cg: TT not initialized correctly")
        
        if x0 == None:
            if is_tt:
                x0 = zerosvec(len(b.shape()),b.shape())
            else:
                x0 = np.zeros(b.shape)
        else:
            if is_tt:
                if not isinstance(x0,TTvec) or b.shape() != x0.shape():
                    raise NameError("TensorToolbox.multilinalg.cg: Initial guess must be in TT format and have the same shape of b")
            else:
                if not isinstance(x0,np.ndarray) or b.shape != x0.shape:
                    raise NameError("TensorToolbox.multilinalg.cg: Initial guess must be in ndarray format and have the same shape of b")
        
        # CG init
        x = x0
        i = 0
        r = (b - dot(A,x))
        if is_tt: r.rounding(eps_round)
        d = r
        res = [dot(r,r)]
        delta_0 = res[-1]
        while i < maxit and res[-1] > eps: # * delta_0:
            q = dot(A,d)
            if is_tt: q.rounding(eps_round)
            alpha = res[-1]/dot(d,q)
            x += alpha * d
            if is_tt: x.rounding(eps_round)
            if i % 5 == 0:
                r = (b - dot(A,x))
                if is_tt: r.rounding(eps_round)
            else:
                r -= alpha * q
                if is_tt: r.rounding(eps_round)
            delta_old = res[-1]
            res.append( dot(r,r) )
            beta = res[-1]/delta_old

            d *= beta
            d += r
            if is_tt: d.rounding(eps_round)

            sys.stdout.write("\033[K")
            if isinstance(x,TTvec):
                sys.stdout.write("CG: err=%e ranks=%s\r" % (res[-1],x.ranks() ))
            elif isinstance(x,np.ndarray):
                sys.stdout.write("CG: err=%e \r" % (res[-1]))
            sys.stdout.flush()

            i += 1
        
        conv = (i < maxit)
        if ext_info:
            info = {'iter': i,
                    'r'   : r,
                    'res' : res}
            return (x,conv,info)
        else:
            return (x,conv)
        
    else:
        raise NameError("TensorToolbox.multilinalg.cg: Conjugate gradient not implemented for the input types")

def bicgstab(A,b,x0=None,eps=1e-8,maxit=1000,eps_round=1e-10,ext_info=False):
    """ Solves the system :math:`Ax=b` using the Bi-Conjugate Gradient Stabilized method using Tensor Train format.
    
    :param TTmat A: Tensor train matrix
    :param TTvec b: Right hand side
    
    :param TTvec x0: [default == :py:func:`TensorToolbox.core.zerosvec`] initial guess of solution ``x``
    :param float eps: [default == 1e-8] stop criteria for Bi-CGSTAB iterations
    :param int maxit: [default == 1000] maximum number of iterations for Bi-CGSTAB
    :param float eps_round: [default == 1e-10] accuracy for Tensor Train rounding operations
    :param bool ext_info: [default == False] whehter of not to have additional info returned

    :return: tuple :py:data:`(x,conv,info)`
       
       * :py:data:`x` (TTvec): solution of the linear system if converged or last iterate if not converged
       * :py:data:`conv` (bool): True -> converged, False -> Not converged / Zero Inner Product exeception
       * :py:data:`info` (dict): ``iter`` -> total number of iterations; ``r`` -> last residual in TT format; ``rho`` -> last value of dot(r0,r) must be bigger than np.spacing(1); ``r0v`` -> last value of dot(r0,v) must be bigger than np.spacing(1)
    
    """

    from TensorToolbox.core import TTvec
    from TensorToolbox.core import zerosvec
    from TensorToolbox.core import TTmat
    
    if not A.init or not b.init: raise NameError("TensorToolbox.multilinalg.cg: TT not initialized correctly")
    if not (isinstance(A,TTmat) and isinstance(b,TTvec) and not isinstance(b,TTmat)):
        raise NameError("TensorToolbox.multilinalg.cg: Conjugate gradient not implemented for the input types")

    if x0 == None:
        x0 = zerosvec(len(b.shape()),b.shape())
    elif not isinstance(x0,TTvec) or b.shape() != x0.shape():
        raise NameError("TensorToolbox.multilinalg.cg: Initial guess must be in TT format and have the same shape of b")

    # Bi-CGSTAB init
    x = x0
    i = 0
    r = (b - dot(A,x)).rounding(eps_round)
    r0 = r.copy()
    delta_0 = norm(r0,2)
    delta_new = delta_0
    rho_old = 1.
    alpha = 1.
    omega = 1.
    v = zerosvec(len(b.shape()),b.shape())
    p = zerosvec(len(b.shape()),b.shape())
    while i < maxit and delta_new > eps**2. * delta_0:
        i += 1

        rho_new = dot(r0,r)

        if np.abs(rho_new) < np.spacing(1): # Break computations
            conv = False
            if ext_info:
                info = {'iter': i,
                        'r': r,
                        'rho': rho_new,
                        'r0v': r0v}
                return (x,conv,info)
            else:
                return (x,conv)

        beta = (rho_new/rho_old) * (alpha/omega)
        p = r + beta * (p - omega * v)
        p.rounding(eps_round)
        v = dot(A,p).rounding(eps_round)
        r0v = dot(r0,v)

        if np.abs(r0v) < np.spacing(1): # Break computations
            conv = False
            if ext_info:
                info = {'iter': i,
                        'r': r,
                        'rho': rho_new,
                        'r0v': r0v}
                return (x,conv,info)
            else:
                return (x,conv)

        alpha = rho_new / r0v   
        s = r - alpha * v
        s.rounding(eps_round)

        if norm(s,2) <= eps**2. * delta_0: # Convergence already reached, update and break loop
            x = x + alpha * p
            conv = True
            if ext_info:
                info = {'iter': i,
                        's': r,
                        'rho': rho_new,
                        'r0v': r0v}
                return (x,conv,info)
            else:
                return (x,conv)

        t = dot(A,s).rounding(eps_round)
        omega = dot(t,s)/norm(t,2)
        x = x + alpha * p + omega * s
        x.rounding(eps_round)
        # The exit was here, but we can postpone it ...
        r = s - omega * t
        r.rounding(eps_round)

        # Update new -> old
        delta_new = norm(r,2)
        rho_old = rho_new

        sys.stdout.write("Bi-CGSTAB: err=%e\r" % (delta_new))
        sys.stdout.flush()

    conv = (i < maxit)
    if ext_info:
        info = {'iter': i,
                'r': r,
                'rho': rho_new,
                'r0v': r0v}
        return (x,conv,info)
    else:
        return (x,conv)



def gmres(A,b,x0=None,eps=1e-8,maxit=1000,restart=1000,eps_round=1e-10,ext_info=False):
    """ Solves the system :math:`Ax=b` using the Generalized Minimum Residual method with Modified Gram-Schmidt iterations using Tensor Train format.
    
    :param TTmat A: Tensor train matrix
    :param TTvec b: Right hand side
    
    :param TTvec x0: [default == :py:func:`TensorToolbox.core.zerosvec`] initial guess of solution ``x``
    :param float eps: [default == 1e-8] stop criteria for GMRES iterations
    :param int maxit: [default == 1000] maximum number of iterations for GMRES
    :param int restart: [default == 1000] restart constant for GMRES (nothing is implemented to retain information, i.e. Hessemberg and Krylov space are reset)
    :param float eps_round: [default == 1e-10] accuracy for Tensor Train rounding operations
    :param bool ext_info: [default == False] whehter of not to have additional info returned

    :return: tuple :py:data:`(x,conv,info)`
       
       * :py:data:`x` (TTvec): solution of the linear system if converged or last iterate if not converged
       * :py:data:`conv` (bool): True -> converged, False -> Not converged / Zero Inner Product exeception
       * :py:data:`info` (dict): ``iter`` -> total number of iterations; ``TT_r`` -> last residual in TT format; ``res`` -> norm of last residual; ``err`` -> residual history per iteration
    
    :note: not optimized for symmetric A
    """

    from TensorToolbox.core import TTvec
    from TensorToolbox.core import zerosvec
    from TensorToolbox.core import TTmat

    if not A.init or not b.init: raise NameError("TensorToolbox.multilinalg.cg: TT not initialized correctly")
    if not (isinstance(A,TTmat) and isinstance(b,TTvec) and not isinstance(b,TTmat)):
        raise NameError("TensorToolbox.multilinalg.cg: Conjugate gradient not implemented for the input types")

    if x0 == None:
        x0 = zerosvec(len(b.shape()),b.shape())
    elif not isinstance(x0,TTvec) or b.shape() != x0.shape():
        raise NameError("TensorToolbox.multilinalg.cg: Initial guess must be in TT format and have the same shape of b")
    
    sys.stdout.write("GMRES: Starting\r")
    sys.stdout.flush()

    # Iterate
    x = x0.copy()
    counter = 0
    j = restart
    err = []
    while counter < maxit:
        if j == restart:
            if counter > 0:
                # Compute y_m: Solve y_m = H^-1 g_m
                y = npla.solve(H[:-1,:],g[:-1])
                # Compute
                for i in range(restart):
                    x += y[i] * v[i]
                    x.rounding(eps_round)
            
            Q = np.eye(restart+1)
            H = np.zeros((restart+1,restart))
            g = np.zeros((restart+1))
            r = (b - dot(A,x)).rounding(eps_round)
            g[0] = norm(r,2) # beta
            v = [1./g[0] * r]
            j = 0
        
        w = dot(A,v[j]).rounding(eps_round)
        for i in range(j+1):
            H[i,j] = dot(w,v[i])
            w -= H[i,j] * v[i]
            w.rounding(eps_round)
        H[j+1,j] = norm(w,2)
        if np.abs(H[j+1,j]) < np.spacing(1):
            # lucky break
            break
        v.append(1./H[j+1,j] * w)
        
        # Apply old givens rotations to the new column
        H[:j+2,j] = np.dot(Q[:j+2,:j+2], H[:j+2,j])
        # New Givens rotation
        omega = np.eye((j+2))
        c = H[j,j] / np.sqrt(H[j,j]**2. + H[j+1,j]**2.)
        s = H[j+1,j] / np.sqrt(H[j,j]**2. + H[j+1,j]**2.)
        omega[j,j] = c
        omega[j+1,j+1] = c
        omega[j,j+1] = s
        omega[j+1,j] = -s
        # Apply to the Q, H and g
        Q[:j+2,:j+2] = np.dot(omega,Q[:j+2,:j+2])
        H[:j+2,:j+1] = np.dot(omega,H[:j+2,:j+1])
        g[j+1] = -s*g[j]
        g[j] *= c
        err.append(np.abs(g[j+1]))

        if isinstance(x,TTvec):
            sys.stdout.write("GMRES: err=%e ranks=%s\r" % (err[-1],x.ranks() ))
        elif isinstance(x,np.ndarray):
            sys.stdout.write("GMRES: err=%e \r" % (err[-1]))
        sys.stdout.flush()
        
        if err[-1] < eps:
            # convergent break
            break
        
        counter += 1
        j += 1
    
    conv = (counter < maxit)
    
    # Compute y_j: Solve H y_j = g_j
    y = npla.solve(H[:j+1,:j+1],g[:j+1])
    # Compute solution
    for i in range(j+1):
        x += y[i] * v[i]
        x.rounding(eps_round)
    
    r = (b-dot(A,x)).rounding(eps_round)

    sys.stdout.write("GMRES: Done \r")
    sys.stdout.flush()
    
    if ext_info:
        info = {'iter': counter,
                'TT_r': r,
                'res': norm(r,2),
                'err': err}
        return (x,conv,info)
    else:
        return (x,conv)
        
