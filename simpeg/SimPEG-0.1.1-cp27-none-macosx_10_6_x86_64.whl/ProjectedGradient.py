from pylab import norm
from SimPEG import *
import scipy.sparse.linalg.dsolve as dsl
import numpy as np
from GaussNewton import IncompleteCG

class GradientProjectionCG(object):


    maxIter     = 20
    maxIterLS   = 10
    LSreduction = 1e-4   #: Expected decrease in the line-search
    LSshorten   = 0.5    #: Line-search step is shortened by this amount each time.
    tolX        = 1e-3

    printers = []

    Solver      = IncompleteCG
    solverOpts  = {'maxIter':10, 'tol':1e-4, 'verbose':False}


    lower = -np.inf
    upper = np.inf

    def __init__(self, **kwargs):
        Utils.setKwargs(self, **kwargs)

    def projection(self, x):
        """projection(x)

            Make sure we are feasible.

        """
        return np.median(np.c_[self.lower,x,self.upper], axis=1)

    def activeSet(self, x):
        """activeSet(x)

            If we are on a bound

        """
        return np.logical_or(x == self.lower, x == self.upper)

    def inactiveSet(self, x):
        """inactiveSet(x)

            The free variables.

        """
        return np.logical_not(self.activeSet(x))

    def bindingSet(self, x):
        """bindingSet(x)

            If we are on a bound and the negative gradient points away from the feasible set.

            Optimality condition. (Satisfies Kuhn-Tucker) MoreToraldo91

        """
        bind_up  = np.logical_and(x == self.lower, self.g >= 0)
        bind_low = np.logical_and(x == self.upper, self.g <= 0)
        return np.logical_or(bind_up, bind_low)

    def reducedHessian(self, xc, H):

        iSet  = self.inactiveSet(xc)  # The inactive set (free variables)
        bSet = self.bindingSet(xc)
        shape = (xc.size, np.sum(iSet))
        v = np.ones(shape[1])
        i = np.where(iSet)[0]
        j = np.arange(shape[1])

        Z = sp.csr_matrix((v, (i, j)), shape=shape)

        def multiplyZtHZ(v):
            # Z is tall and skinny
            return Z.T*(H*(Z*v))

        rH = sp.linalg.LinearOperator( (shape[1], shape[1]), multiplyZtHZ, dtype=xc.dtype )

        return rH, Z

    def minimize(self, objFunc, x0):

        # Make sure that the bounds are full arrays
        if Utils.isScalar(self.lower):
            self.lower = np.ones_like(x0)*self.lower
        if Utils.isScalar(self.upper):
            self.upper = np.ones_like(x0)*self.upper
        assert self.lower.size == x0.size and self.upper.size == x0.size, 'Upper and Lower bounds incorrect shape.'

        # initial output
        print "%s Projected Gradient %s" % ('='*30,'='*30)
        print "iter\tJc\t\t\t\tnorm(dJ)\tLS"
        print "%s" % '-'*73

        # initialize
        self.iter   = 0
        self.iterLS = 0

        xc     = self.projection(x0)  # ensure that we start of feasible.
        x_last = xc

        allBinding = lambda x: x.size <= np.sum(self.bindingSet(x))

        while True:
            # evaluate objective function
            self.f, self.g, self.H = objFunc(xc)

            itType = '.CG.' if self.iter % 2 else 'PG'

            print "%3d\t%1.2e\t\t%1.2e\t%d\t%s" % (self.iter, self.f, norm(self.g), self.iterLS, itType)

            # Find the Search Direction
            if itType == '.CG.':
                rH, Z = self.reducedHessian(xc, self.H)
                rHsolver = self.Solver(rH, **self.solverOpts)
                rdx = rHsolver * (-Z.T*self.g)
                dx = Z*rdx
            elif itType == 'PG':
                dx = -self.g
            else:
                raise Exception('itType %s is not defined.' % itType)

            ################## Armijo linesearch ##################

            LS = False
            muLS = 1.0
            self.iterLS = 1

            while  self.iterLS < self.maxIterLS:
                xt = self.projection(xc + muLS * dx)
                descent = np.vdot(self.g, xt - xc)
                ft = objFunc(xt, return_g=False, return_H=False)
                LS = ft <= self.f + self.LSreduction * descent
                LS = LS or allBinding(xt)
                if LS:
                    break
                self.iterLS += 1
                muLS *= self.LSshorten

            if not(LS):
                print "line search break"
                return xc

            ################ End Armijo linesearch #################


            # Stopping criteria
            STOP = np.empty(3, dtype=bool)
            STOP[0] = norm(xt-x_last) < self.tolX
            STOP[1] = self.maxIter < self.iter
            STOP[2] = allBinding(xc)

            if any(STOP): break

            # xt has satisfied the line-search so we can continue!
            f_last = self.f
            x_last, xc = xc, xt
            self.iter += 1

        print "%s STOP! %s" % ('-'*33,'-'*33)
        print "%d : |xc-x_last| =  %1.4e\t<=\ttolX      =  %1.4e"  % (STOP[0],norm(xc-x_last),self.tolX)
        print "%d : iter        = %3d\t\t\t<=\tmaxIter   = %3d" % (STOP[1],self.iter,self.maxIter)
        print "%s DONE! %s\n" % ('='*33,'='*33)

        return xc



if __name__ == '__main__':
    diag = np.r_[100,100,1,10.,1.]
    A = sp.csr_matrix((diag, (range(5), range(5))), shape=(5,5))
    b = -np.r_[1.,2.,5.,4.,5.]
    ans = -b/diag
    FUN = Tests.getQuadratic(A, b)
    x0 = np.zeros(5)
    # FUN = Tests.Rosenbrock
    # x0 = np.zeros(2)
    # ans = np.ones(2)

    lower = 0.2
    PG = GradientProjectionCG(maxIter=300,maxIterLS=50, lower=lower)
    xopt = PG.minimize(FUN, x0)
    print xopt, PG.projection(ans), norm(xopt - PG.projection(ans))
