## AUTHOR  : Zhenfei Yuan, Taizhong Hu
## EMAIL   : zf.yuan.y@gmail.com; thu@ustc.edu.cn
## URL     : taizhonglab.ustc.edu.cn/software/pycounts.html
## DATE    : Mar, 26, 2013
## LICENCE : GPL (>= 2)

from rdiscrete import rpois, rgpois, rzigp, rnb


class CountRV:
    def __init__(self, family, par1, par2 = 0, par3 = 0):
        """
        Initialization function for discrete distributions. Currently
        contains Poisson, Generalized Poisson, Zero Inflated
        Generalized Poisson and Negative Binomial.

        Parameter
        ---------
        family : str. 'p' for Poisson, 'gp' for Generalized Poisson,
                 'zigp' for Zero Inflated Generalized Poisson, 'nb'
                 for negative binomial.

        par : array of float.
        """
        if family not in ['p', 'gp', 'zigp', 'nb']:
            raise ValueError("'family' illegal.")

        self.family = family
        self.par1 = par1
        self.par2 = par2
        self.par3 = par3


    def sim(self, u):
        """
        Generate samples via inverse c.d.f method.

        Parameter
        ---------

        u : array. Samples of U(0, 1).

        Return
        ------

        x : array. F^{-1}(u).
        """
        if self.family == 'p':
            return rpois(self.par1, u)
        elif self.family == 'gp':
            return rgpois(self.par1, self.par2, u)
        elif self.family == 'zigp':
            return rzigp(self.par1, self.par2, self.par3, u)
        elif self.family == 'nb':
            return rnb(self.par1, self.par2, u)
