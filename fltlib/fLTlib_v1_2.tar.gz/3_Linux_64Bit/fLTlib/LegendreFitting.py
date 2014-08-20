# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#
#    This file demonstrates how to fit a single EXP curve using Finite Legendre Transform (fLT)
#
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
from numpy import *
from pylab import *
from scipy.optimize import leastsq
import matplotlib.pyplot as plt
from LegendrePolynomials import *

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#    One can either use a data file (please type 1) or simulated data (please type 0)
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
simData = 1			# take simulated data (1) or read real data from file (0)
if int(raw_input("using simulated data (1) or read real data from file (0)?"))==0:
	simData = 0

if  simData:
	# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
	#    simulated data: exponential with Poisson noise
	# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
	A1, tau1, ofs   = 12.0, 0.6, 0.5
	nt	= 1000
	t	= linspace(-1+1./nt,1-1./nt,nt)
	y0	= A1*np.exp(-t/tau1) + ofs
	yn	= np.random.poisson(y0, nt) 	# noisy exp
#					
else:
	# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
	#    If a data file is used, it should have two columns with time and amplitude
	# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
	z	= np.loadtxt('noisyExp.dat')		# read data from test file 
	t	= z[:,0]						# time points
	yn	= z[:,1] 						# amplitudes
	nt	= len(t)						# length of vectors in time domain
	Tr	= t[nt-1]						# last time point, needed for final rescaling
	t	= linspace(-1+1./nt,1-1./nt,nt)		# rescale time axis to (-1,1)

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#   Now we start to fit
#   First: finite Legendre transform of input data
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
nl			= 15							# we use 15 Legendre components (any value between 10 to 20 would be OK).
ind 		= np.arange(nl)
P			= makeLP_expl(nl,nt)	# get Legendre polynomials ...
psinvP_T	= pinv(P.T)				# ... and its transposed pseudoinverse
LT_y		= LT(yn,nl)				# take the L-transform of the data

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#   After the transform we can display the spectrum and let the user choose the number of components for fitting
#   A typical value for single EXP fitting lies between 3 and 8. Higher components are only noise.
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
plt.title('Legendre spectrum of data')
plt.plot( ind, LT_y,ind, LT_y,'r*' )
plt.ion();plt.show()

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
#   Here we let the user choose the number
#   And later recalculate the L-spectrum (LT_y) for fitting
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
nl = int(raw_input("number of Legendre components to be used: ")) + 1    # the index of the last highest good-looking component should be entered
ind		= np.arange(nl)
P		= makeLP_expl(nl,nt)		# get Legendre polynomials ...
psinvP_T= pinv(P.T)					# ... and its transposed pseudoinverse
LT_y	= LT(yn,nl)					# take the L-transform of the data

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
#      Nonlinear least squares fit of the experimental Legendre spectrum to the parameter-dependent Legendre spectrum 
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
def Lspect(ind,pL):	     # get parameter-dependent Legendre spectrum that is to be fitted to the data spectrum
	nl = len(ind)
	[A1, tau1,ofs] = pL
	LT_fit = LT_analtcl(A1,tau1,nl)
	LT_fit[0]  += ofs
	return LT_fit		

def residuals(pL, ind, LT_y):	# take the deviation vector between experimentally obtained spectrum and model spectrum
	[A1, tau1, ofs] = pL
	err = LT_y  -  Lspect(ind,pL)
	return err

A1     = 13.									# initial values
tau1  = 0.7	
ofs    = A1/100
pL = [A1, tau1,ofs]

plsq = leastsq(residuals, pL, args=(ind, LT_y))	# scipy NNLSQ fitting routine. Find parameters such that the chi2-sum of residuals is minimized
A,tau,ofs = plsq[0]
print  "A,tau,ofs: ",  A,tau,ofs 

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
# 		Output:
#		 re-scaling tau and A
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 

if not simData:
	t_real     = (t+1)*Tr/2.
	tau_real = tau*Tr/2.
	A_real   = A*exp(1./tau)
	print "tau_real: ", tau_real
	print "A_real: ", A_real

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
# 		Plot
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = 
plt.close()
plt.plot( t, yn, t, A*exp(-t/tau)+ofs )
plt.title('Least-squares fit to noisy data')
plt.legend(['Fit', 'Noisy', 'True'])
plt.ioff();plt.show()

