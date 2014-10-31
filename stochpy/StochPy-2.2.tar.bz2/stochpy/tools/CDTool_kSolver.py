"""
Class for calculating k, the population growth rate from equation 20 of Painter and Marr.

Inputs: 
    Phi - Mother volume distribution
    K - Division distribution
    Growthrate - Exponential volume growthrate
    Growthtype - exponential or linear

TODO?:
     - Plot g against k for linear growth.
     - Plot k estimated (from what eq?) against k solved.
     - Check convergence (see copied code at bottom of page).     
     - Check which distribution work and which don't. (e.g. Lognormal pdf has undifined value at 0.)
 
Changes:
    - All scipy.stats distributions now inputable (not certain if it also works).
    - Still works the same with beta distributions.
     
Written by T.R. Maarleveld and M. Moinat, Amsterdam, The Netherlands
E-mail: tmd200@users.sourceforge.net
Last Change: October 27, 2014
"""
from __future__ import division, print_function, absolute_import

from scipy import stats, integrate, optimize
import numpy as np
try:
    import matplotlib.pyplot as plt
except:
    print("Warning: The Matplotlib module is not available, so it is impossible to create plots")
    print("Info: See http://matplotlib.sourceforge.net/ for more information about Matplotlib")
import time,sys

def integrate_trapezoidal(f, a, b, n):
    """Approximates the definite integral of f from a to b by
    the composite trapezoidal rule, using n subintervals."""
    a = float(a)
    b = float(b)
    h = (b - a) / n-1
    s = f(a) + f(b)
    for i in range(1, n-1):
        s += 2 * f(a + i * h)
    return s * h / 2
    
def get_distribution(distr_name, *args):
    """ Tries to get from scipy.stats the pdf of the named distribution.
        Returns the pdf function and the interval on which the pdf is nonzero.
        
        The way in which the paramters of the distribution are handled by scipy differs per function.
        e.g. 'beta': args = alpha, beta, loc (alpha and beta have no default).
             'norm': args = loc, shape (both have default values).
    """
    parameters = args    
    
    try:
        distribution = stats.__dict__[distr_name]
        pdf = lambda x: distribution.pdf(x, *parameters)
    except (AttributeError, KeyError):
        raise Warning("The PDF of the distribution '%s' has not been found in the scipy stats module." % distr_name )
    
    x_interval = distribution.interval(1,*parameters)
    return pdf, x_interval
    
class k_solver:
    """
    Names:
      - x                =   Volume
      - k                =   Population growth_rate
      - phi_PDF(x)       =   Distribution mothercell volume (given: *distr_phi*)
      - K                =   Distribution of volume partitioning ratio (given: *distr_K*)
      - psi_PDF(x)       =   Distribution daughtercell volume
      - lambda_PDF(x,k)  =   Distribution extantcell volume
      - V(x)             =   Differential of volume growth. (given: *growth_rate* and *growth_type*)
      - R(x,k)           =   Function, depends on type of volume growth.
      
    #Note: with DoQuad = True, calculating a lambda takes much longer (~60x, depending on the settings).
    """
    def __init__(self):
        """ Initializes a k_solver object with a default model.
            Use set_model to give arbitraty model paramters. """
        
        self.model_input = [['beta',5,5], ['beta',2,2], 1.5, 1, 'exponential'] #Default phi, K, growth_rate, growth_type
        self.assign_model()
        
    def set_model(self, distr_phi=None, distr_K=None, shift=None, growth_rate=None, growth_type = None):
        """ Set parameters for the celldivision model.
        Input:
            - distr_phi, [tuple of distr name and parameters]
            - distr_K, [tuple of distr name and parameters]
            - shift [float or None]. If given, it shifts the distr_phi this much to the right.
            - growth_rate [float] the exponential growth_rate.
            - growth_type [string] 'exponential' or 'linear' (TODO: 'double linear'?)
        Example:
        set_model(['lognorm',1,0,3],['beta',4,4], growth_rate = 2, growth_type = 'linear')
          #=lognormal phi, with sigma=1, mu=3 and no shift. beta K, alpha=beta=4. V = V0 + 2*t
          http://docs.scipy.org/doc/scipy/reference/stats.html
        """
            
        new_input = [distr_phi, distr_K, shift, growth_rate, growth_type]
        self.model_input = new_input #Backup to reset the given model, if needed
        self.assign_model()
        
    def assign_model(self):
        """(Re)Sets the module with parameters of the given model."""
        
        distr_phi, distr_K, self.shift, growth_rate, growth_type = self.model_input
        
        #Unpack distribution parameters
        self.phi_distributionName = distr_phi[0].lower()
        self.phi_parameters = distr_phi[1:] 
        if self.shift: self.phi_parameters = list(self.phi_parameters) + [self.shift] #Assume parameter after 
        self.phi_PDF, min_max = get_distribution(self.phi_distributionName, *self.phi_parameters)
        self.phi_min = min_max[0]
        self.phi_max = min_max[1]    #TODO: if min<0 or max=inf, print warning.    
        #print self.phi_distributionName, self.phi_parameters, min_max        
        
        self.K_distributionName = distr_K[0].lower() 
        self.K_parameters = distr_K[1:]
        if self.K_distributionName == self.phi_distributionName == 'beta': #Both beta, produce non overlapping phi and psi.
            self.set_K_betaPDF()
            self.K_min = self.K_shift
            self.K_max = 1 - self.K_shift #K always centered around 0.5
        else: #Any other, copy directly the given settings.            
            self.K_PDF, min_max = get_distribution(self.K_distributionName, *self.K_parameters)
            self.K_min = min_max[0]
            self.K_max = min_max[1]
        #print self.K_distributionName, self.K_parameters, (self.K_min, self.K_max )
        #TODO: Check whether the min and max of phi and K are reasonable.
        
        #Growth parameters
        self.growth_type = growth_type
        self.growth_rate = float(growth_rate)        

        if self.K_distributionName == self.phi_distributionName == 'beta':
            self.psi_min = self.phi_min*self.K_min
            self.psi_max = self.phi_max*self.K_max
            self.lambda_min = self.psi_min #Smallest daughter.
            self.lambda_max = self.phi_max #Largest mother.
        else: #Take bounds broad
            self.psi_min = self.lambda_min = 0              #Smallest possible cell.
            self.psi_max = self.lambda_max = self.phi_max   #Largest mother = largest possible cell.
      
        #Default integration parameters
        self.n = 20 #x
        
        self.DoQuad = False #default it does trapezoidal
        self.quadlimit = 8 #(Cycle?) limit of both quad integrations (psi_PDF and lambda_PDF)
        
    def set_integration_param(self, trapezoidal_n=20, doquad = False, lim_quad =8 ):
        self.n = trapezoidal_n #theta
        
        self.DoQuad =  doquad
        self.quadlimit = lim_quad        
        
    def set_K_betaPDF(self):
        """Sets K in such a way that phi and psi don't overlap."""        
        self.K_parameters = self.K_parameters[:2] #Make sure just alpha and beta are in there, discared all others.
        self.K_shift = 1.0/(self.shift + 1.0)
        K_multiply = (self.shift-1.0)/(self.shift+1.0) 
        
        self.K_PDF = lambda ratio: stats.beta.pdf((ratio-self.K_shift)/K_multiply, *self.K_parameters)/K_multiply #/self.K_multiply to normalize
        
    def psi_PDF(self, x):
        func = lambda theta: (self.phi_PDF(theta)/theta) * self.K_PDF(x/theta)
        if self.DoQuad:
            result = integrate.quad(func, x, self.phi_max, limit=self.quadlimit) #limit=8 gives 3 fold speed improvement
            result = result[0]
        else:
            result = integrate_trapezoidal(func, x, self.phi_max, self.n) #self.n subintervals
        return result

    def V(self, x):
        """ Rate of volume growth. =Derivative of volume function itself."""
        if self.growth_type == 'exponential':
            return  self.growth_rate*x
        elif self.growth_type == 'linear':
            return self.growth_rate
        else:
            raise Warning("Growthtype '%s' not recognised" % self.growth_type)
    
    def R(self, x, k, C_r = 0): #Anne: what value has this C?
        """ Equation below 20, R(x) = Integral[(V'(x)+k)/V(x)dx]. Calculated by hand for:
            - Exponential: V(x) = g*x
            - Linear: V(x) = g
        """
        if self.growth_type == 'exponential':
            return (self.growth_rate + k)/self.growth_rate * np.log(x) + C_r
        
        elif self.growth_type == 'linear':
            return k/self.growth_rate*x + C_r
            
        else:
            raise Warning("Growthtype '%s' not recognised" % self.growth_type)
    
    def lambda_PDF(self, x, k, C = 0):
        """ Equation 20. """
        integral_func = lambda x_: k * np.exp( self.R(x_,k) ) * (2 * self.psi_PDF(x_) - self.phi_PDF(x_))/self.V(x_) #x_ is local, and different from x.
        
        #This integral is defined for all volumes that can exist (from smallest daughter to largest mother.)
        if self.DoQuad:
            integral_result =  integrate.quad(integral_func, self.psi_min, x, limit=self.quadlimit) #limit=8 gives 3 fold speed improvement
            integral_result =  integral_result[0]
        else:
            integral_result =  integrate_trapezoidal(integral_func, self.psi_min, x, self.n) #Integrate upto x, because Indefinite integral to x_ and then asking for value of x is the same thing. F[x] = opp from 0 to x
        #Todo: Can 0.01 be replaced by self.lambda_min? This saves time, as 0.01 to min is not calculated.
            
        result = np.exp( - self.R(x,k) ) * integral_result + C*np.exp( - self.R(x,k) )
        return result

    def Plot_phi(self, n_points = 100, o = 0.2, plotnum = None):
        #o = offset around graph
        #plotnum can be used to plot all in one figure
        points_phi = np.linspace(self.phi_min - o, self.phi_max + o, n_points)
        
        plt.figure(plotnum) #plotnum = None opens new figure.
        plot = plt.plot(points_phi, [self.phi_PDF(x) for x in points_phi])
        plt.title('Phi PDF, Volume at division distribution for a sample of mothercells')
        plt.xlabel('Volume')
        plt.ylabel('Probability density')
        plt.show()
        
        return plot

    def Plot_K(self, n_points = 100, o = 0.2, plotnum = None):
        #o = offset around graph
        points_K = np.linspace(self.K_min - o, self.K_max + o, n_points)
        
        plt.figure(plotnum)
        plot = plt.plot(points_K, [self.K_PDF(frac) for frac in points_K])
        plt.title('K PDF, Partitioning ratio distribution')
        plt.xlabel('Partitioning ratio')
        plt.ylabel('Probability density')
        plt.show()
        
        return plot
        
    def Plot_psi(self, n_points = 50, o = 0.2, plotnum = None):
        #o = offset around graph
        points_psi = np.linspace(self.psi_min - o, self.psi_max + o, n_points)
        
        plt.figure(plotnum)
        plot = plt.plot(points_psi, [self.psi_PDF(x) for x in points_psi])
        plt.title('Psi PDF, Volume at birth distribution for a sample of mothercells')
        plt.xlabel('Volume')
        plt.ylabel('Probability density')
        plt.show()
        
        return plot
    
    def Plot_lambda(self, k = 1, n_points = 20, o = 0.2, plotnum = None):
        #o = offset around graph
        points_lambda = np.linspace(self.lambda_min - o, self.lambda_max + o, n_points)
        
        plt.figure(plotnum)
        plot = plt.plot(points_lambda, [self.lambda_PDF(x, k) for x in points_lambda])
        plt.title('Lambda PDF, Volume of extant cells distribution for a sample of mothercells')
        plt.xlabel('Volume')
        plt.ylabel('Probability density')
        plt.show()
        
        return plot

    def Plot_all_distr(self, plotnum = 5, k = 1):
        t1 = time.time()
        self.Plot_phi(plotnum = plotnum)
        self.Plot_K(plotnum = plotnum)
        self.Plot_psi(n_points = 50, plotnum = plotnum)        
        self.Plot_lambda(k = k, n_points = 20, plotnum = plotnum)
        t2 = time.time()
        print("Time to plot the four distributions:", t2-t1)
        
    def integral_lambda(self, k):
        func = lambda x: self.lambda_PDF(x,k)
        result = integrate_trapezoidal(func, self.lambda_min, self.lambda_max, self.n)
        return result
    def plot_integral_lambda(self, n_points = 50, max_k = 10, plotnum = None):
        points = np.linspace(0, max_k, n_points)
        plt.figure(plotnum) 
        plt.plot(points, [self.integral_lambda(k) for k in points])
        plt.title('Area under the Lambda PDF.')
        plt.xlabel('k')
        plt.ylabel('Area')
        plt.show()
        
    def Solve_k(self, init_guess = 1, tol=1.48e-8, maxiter_newton=50, check_result = True, print_params = True):
        """ Use secant method (function optimize.newton()) to solve system for k"""
        
        if print_params:
            print("Solving for k started with model parameters:")
            print ("\n".join(['%-16s - %s']*5)  % ("Phi distribution", (self.phi_distributionName, self.phi_parameters),"Shift", self.shift, "K distribution", (self.K_distributionName, self.K_parameters),  "Growth-type", self.growth_type,"Growthrate", self.growth_rate) )           
            print("\nIntegration parameters:")
            print("\n".join(['%-16s - %s']*1)  % ('Subintervals Trapezoidal', self.n) ) #initial guess, integration, boundaries.
            sys.stdout.flush() #Force a print
        
        t1 = time.time()
        k = self.Get_k(init_guess, tol, maxiter_newton)
        print("k = %f" % k)
        print('Time to solve:', time.time() - t1)
        sys.stdout.flush()
        
        self.warning = False
        if check_result:
            print("Checking the value of k:")
            t2 = time.time()
            # Give higher trapezoidal precision and broader bounds. 
                # Checking is faster than Newton Rhapson, because the calculation of integral(lambda) is just done once.
            self.n *= 3 #TODO, check with integrate.quad. =Too costly
            self.phi_max *= 2
            self.psi_min = 0.01 #Can't be zero, otherwise dividing by zero
            self.lambda_min = self.psi_min
            self.lambda_max *= 2
            print("Parameters for the check:")
            print("\n".join(['%-16s - %s']*1) % ('Subintervals Trapezoidal', self.n)) #initial guess, integration method, boundaries
            
            area = self.integral_lambda(k)           
            print("With k=%f, the integral of lambda goes to %.20f." %(k, area))
            
            if 1 - area > 0.1:
                self.warning = True
                print("Warning, the integral does not evaluate to 1!")
                
            print( "Time to check result:", time.time() - t2)

            self.assign_model() #Resets to given parameters (and default (!!) limits and bounds)

        return k
        
    def Get_k(self, init_guess = 1, tol=1.48e-8, maxiter_newton=50):
        """ Use secant method (function optimize.newton()) to solve system for k"""        
        try:
            k = optimize.newton(lambda k: self.integral_lambda(k) - 1, init_guess, tol=tol, maxiter=maxiter_newton) #Integral(lambda(x,k)) == 1
        except RuntimeError as e:
            # Failed to converge after the first <maxiter_newton> iterations.
            print(e)
            new_init = self.growth_rate            
            print("Solving again with initial guess of", new_init)
            k = optimize.newton(lambda k: self.integral_lambda(k) - 1, new_init, tol=tol, maxiter=maxiter_newton) #Integral(lambda(x,k)) == 1    

        return k
        
def main():
    a = k_solver()
    #a.set_model([5,5],[2,2],1.5,1)
    a.set_integration_param(10,10,5) #a.solve(maxiter_newton=10) gives answer in +-140 sec (k=1.9410642841195287)

    spam = k_solver()
    spam.set_model([23,23],[1,1],3,2)
    spam.set_integration_param(trapezoidal_m=20, trapezoidal_n=20, lim_quad =50) #20,20,50 takes too long


    #Non-normalised start
    beta_distr = lambda x,a,b: sympy.Piecewise( (0,sympy.re(x)<0),(0,sympy.re(x)>1), (x**(a-1)*(1-x)**(b-1), True)) 
    def psi_PDF(x, shift, a=5, b=5):    
        return beta_distr(x - shift ,a,b)
    #sympy.plot(psi_PDF(x,1.5),(x,0,3))
    def K_PDF(x, shift, a=2, b=2):
        K_shift = 1/(shift + 1)
        K_multiply = (shift-1)/(shift+1)  
        return beta_distr(  (x-K_shift)/K_multiply, a,b)
    #sympy.plot(K_PDF(x,1.5),(x,0,1))

solver = k_solver()

#Test for convergence:
# for i in [1,2,5,7,10,20,30,40,50,70,100]: #At n=10, it is correct up to the third decimal (4 significant figures)
    # print i, fm_PDF_trap(0.7, limx=[0.6,1.5], limtheta=[1.5,2.5], n_theta=i, n_x=i)

#Test different growthrates
# t1 = time.time()
# result = []
# sol_mod = k_solver()
# for g in [0.5,1,2,3,4]:
    # sol_mod.set_model([5,5], [2,2], 1.5, growthrate = g)
    # sol_mod.set_integration_param(5,5,5)
    
    # sol_mod.solve(maxiter_newton = 10, check_result = False)
    # result.append([g,sol_mod.k])
    
# print "Time for loop:", time.time() -t1
