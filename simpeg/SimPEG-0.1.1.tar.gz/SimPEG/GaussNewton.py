from pylab import norm
from SimPEG import Utils
import scipy.sparse.linalg.dsolve as dsl
import numpy as np
from SimPEG.Solvers import IncompleteCG


class GaussNewton(object):


    maxIter     = 20
    maxIterLS   = 10
    LSreduction = 1e-4   #: Expected decrease in the line-search
    LSshorten   = 0.5    #: Line-search step is shortened by this amount each time.
    tolX        = 1e-3

    Solver      = IncompleteCG
    solverOpts  = {'maxIter':10, 'tol':1e-4, 'verbose':False}

    def __init__(self, **kwargs):
        Utils.setKwargs(self, **kwargs)

    def minimize(self, objFunc, x0):
        """
            GaussNewton Optimization

            Input:
            ------
                funciton - objective Function
                x0   - starting guess

            Output:
            -------
                xOpt - numerical optimizer
        """

        # initial output
        print "%s GaussNewton %s" % ('='*30,'='*30)
        print "iter\tJc\t\t\t\tnorm(dJ)\tLS"
        print "%s" % '-'*73

        # initialize
        self._iter   = 0
        self._iterLS = 0
        xc           = x0
        x_last       = xc

        while True:
            # evaluate objective function
            self.f, self.g, self.H = objFunc(xc)

            print "%3d\t%1.2e\t\t%1.2e\t%d" % (self._iter, self.f, norm(self.g), self._iterLS)

            # Find the Search Direction
            Hinv = self.Solver(self.H, **self.solverOpts)
            dx = Hinv * (-self.g)

            ################## Armijo linesearch ##################

            descent = np.vdot(self.g,dx)
            LS = False
            muLS = 1.0
            self._iterLS = 1

            while  self._iterLS < self.maxIterLS:
                xt = xc + muLS * dx
                ft = objFunc(xt, return_g=False, return_H=False)
                LS = ft <= self.f + muLS * self.LSreduction * descent
                if LS: break
                self._iterLS += 1
                muLS *= self.LSshorten

            if not(LS):
                print "line search break"
                return xc

            ################ End Armijo linesearch #################

            # xt has satisfied the line-search so we can continue!
            xc = xt
            self._iter += 1

            # Stopping criteria
            STOP = np.empty(2, dtype=bool)
            STOP[0] = norm(xc-x_last) < self.tolX
            STOP[1] = self.maxIter < self._iter

            if any(STOP): break

            # store old values
            f_last = self.f
            x_last = xc

        print "%s STOP! %s" % ('-'*33,'-'*33)
        print "%d : |xc-x_last| =  %1.4e\t<=\ttolX      =  %1.4e"  % (STOP[0],norm(xc-x_last),self.tolX)
        print "%d : iter        = %3d\t\t\t<=\tmaxIter   = %3d" % (STOP[1],self._iter,self.maxIter)
        print "%s DONE! %s\n" % ('='*33,'='*33)

        return xc



if __name__ == '__main__':
    from SimPEG import Tests
    xopt = GaussNewton(maxIter=30,maxIterLS=30).minimize(Tests.Rosenbrock, np.r_[5,5.])
    print xopt
