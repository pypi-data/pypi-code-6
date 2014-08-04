#Author Joseph Hardin
import sys
sys.path.append('/home/jhardin/Dropbox/Projects/PythonRadarTools')
sys.path.append('/Users/jhardin/Dropbox/Projects/PythonRadarTools')##Please add the location to your own copy of this

import numpy as np
import pandas as pd
import scipy as sp
import matplotlib.pyplot as plt
import itertools
import scipy.optimize
import pytmatrix
import DSDProcessor
from pytmatrix.psd import GammaPSD
import csv
from pytmatrix.tmatrix import Scatterer
from pytmatrix.psd import PSDIntegrator, GammaPSD
from pytmatrix import orientation, radar, tmatrix_aux, refractive
import datetime
import expfit

class NASA_APU_reader:

    time    = [] #Time in minutes from start of recording
    Nd      = []
    Nt      = []
    T       = []
    W       = []
    D0      = []
    Nw      = []
    mu      = []
    rho_w = 1


    def __init__(self, filename):
        self.f = open(filename,'r')
        reader = csv.reader(self.f)
        self.diameter = [float(x) for x in reader.next()[0].split()[1:]]
        self.velocity = [float(x) for x in reader.next()[0].split()[1:]]

        for row in reader:
            self.time.append(float(row[0].split()[0]))
            self.Nd.append([float(x) for x in row[0].split()[1:]])

        self.time = np.array(self.time)
        self.Nd = np.array(self.Nd)


    def calculate_scattering(self, wavelength='X', shape='bc'):
        '''
        Calculates the radar moments based upon the DSDs. This uses the binned
        DSD and not the parameterized DSD.
        returns: Dictionary of radar moments
        '''
        time = self.time
        self._build_scattering_table()
        Zh  = np.zeros(len(time))
        Zdr = np.zeros(len(time))
        Kdp = np.zeros(len(time))
        Ah  = np.zeros(len(time))
        Adr = np.zeros(len(time))
        ldr = np.zeros(len(time))
        delta_hv = np.zeros(len(time))
        rho_hv = np.zeros(len(time))


        bins=np.hstack((0,self.diameter+np.array(self.spread)/2))

        for t in range(0,len(time)):
            BinnedDSD = pytmatrix.psd.BinnedPSD(bins, self.Nd[t,:])
            self.scatterer.psd = BinnedDSD
            self.scatterer.set_geometry(tmatrix_aux.geom_horiz_back)
            Zh[t] = 10*np.log10(radar.refl(self.scatterer))
            Zdr[t] = 10*np.log10(radar.Zdr(self.scatterer))
            ldr[t] = radar.ldr(self.scatterer)
            delta_hv[t] = radar.delta_hv(self.scatterer)
            rho_hv[t] = radar.rho_hv(self.scatterer)

            self.scatterer.set_geometry(tmatrix_aux.geom_horiz_forw)
            Kdp[t] = radar.Kdp(self.scatterer)
            Ah[t] = radar.Ai(self.scatterer)
            Adr[t] = Ah[t]-radar.Ai(self.scatterer, h_pol=False)

            res = {'Zh': Zh, 'Zdr': Zdr, 'Ldr': ldr, 'delta_hv': delta_hv, 'rho_hv': rho_hv,
                'Kdp': Kdp, 'Ah': Ah, 'Adr': Adr}

        self.moments = res
        return res


    def _build_scattering_table(self, wavelength=tmatrix_aux.wl_X):
        self.scatterer = Scatterer(wavelength=wavelength, m=refractive.m_w_10C[wavelength])
        self.scatterer.psd_integrator = PSDIntegrator()
        self.scatterer.psd_integrator.axis_ratio_func = lambda D: 1.0/self._bc(D)
        self.scatterer.psd_integrator.D_max = 10.0
        self.scatterer.psd_integrator.geometries = (tmatrix_aux.geom_horiz_back, tmatrix_aux.geom_horiz_forw)
        self.scatterer.or_pdf = orientation.gaussian_pdf(20.0)
        self.scatterer.orient = orientation.orient_averaged_fixed
        self.scatterer.psd_integrator.init_scatter_table(self.scatterer)


    def _bc(self, D_eq):
        return 1.0048 + 5.7*10**(-4) - 2.628 * 10**(-2) * D_eq**2 +\
            3.682*10**(-3)*D_eq**3 - 1.677*10**-4 * D_eq**4

   
    def plot_day(self, log_scale = True, focus=True):
        plt.figure()

        XX, YY = np.meshgrid( np.array(self.time)/60.0,self.diameter,)
        
        if log_scale:
            pc=pcolor(XX,YY,np.log10(self.Nd).T, vmin=0)
            cbar_label = '# of raindrops(log10)'
        else:
            pc=pcolor(XX,YY,array(self.Nd).T, vmin=0.1)
            cbar_label = '# of raindrops(linear)'

        plt.ylabel('Drop Diameter(mm)')
        plt.xlabel('Time(h)')
        pc.cmap.set_under(color='w')
        cbar = plt.colorbar()
        cbar.ax.set_ylabel(cbar_label)
        plt.xlim(0,self.time[-1]/60.0)
        plt.ylim(0,self.diameter[-1])

        if focus: #Probably a more pythonic way of doing this, but it works for now
           right_limit=array(self.Nd).shape[1]-list(sum(self.Nd,axis=0)>1)[::-1].index(True) 
           plt.ylim(0,self.diameter[right_limit])
        
        plt.show()
       
    def process_data(self,calculate_mu=False):
        self.D0=[]
        self.Nw=[]
        self.mu=[]
        self.W=[]
        self.Nt=[]
        self.Dm=[]
        self.Zh=[]
        self.Dmax=[]
        self.R=[]

        rho_w=1
        ##Goal is to have this return the different parameters as well as DSD parameters
        for t in range(0,len(self.time)):
            self.Nt.append(np.dot(self.spread,self.Nd[t]))
            self.W.append( 10**-3 * pi/6 * rho_w *np.dot([self.Nd[t][k]*self.spread[k] for k in range(0,32)], 
                array(self.diameter)**3))
            self.D0.append(self.calculate_D0(self.Nd[t]))

            D3 = sum([self.spread[k]*self.Nd[t][k]*self.diameter[k]**3 for k in range(0,len(self.diameter))])
            D4 = sum([self.spread[k]*self.Nd[t][k]*self.diameter[k]**4 for k in range(0,len(self.diameter))])
            self.Dm.append(D4/D3)

            self.Nw.append(   (3.67**4)/pi * (10**3 * self.W[t])/(self.D0[t]**4)  )
            self.Zh.append(sum([self.spread[k]*self.Nd[t][k]*self.diameter[k]**6 for k in \
                    range(0,len(self.diameter))]))
            self.Dmax.append(self.diameter[self.__get_last_nonzero(self.Nd[t])] )

            self.R.append(pi/6.0* sum([self.velocity[k]*self.spread[k]*self.Nd[t][k]*self.diameter[k]**3 for k in range(0,len(self.diameter))]))

                    
            if(calculate_mu):
                try:
                    res = scipy.optimize.minimize(self.mu_cost, 3, args=(self.Nd[t],self.Dm[t],self.Nw[t]), method='BFGS')
                    self.mu.append(res['x'][0])
                except:
                    self.mu.append(np.nan)

    def calculate_D0(self, N):
        rho_w=1

        cum_W = 10**-3 * pi/6 * rho_w * \
                np.cumsum([N[k]*self.spread[k]*(self.diameter[k]**3) for k in range(0,len(N))])
        cross_pt = list(cum_W<(cum_W[-1]*0.5)).index(False)-1
        slope = (cum_W[cross_pt+1]-cum_W[cross_pt])/(self.diameter[cross_pt+1]-self.diameter[cross_pt])
        run = (0.5*cum_W[-1]-cum_W[cross_pt])/slope
        return self.diameter[cross_pt]+run

    def mu_cost(self, mu, N, D0, Nw, debug=False):
        #Cost function between mu and the actual DSD
        dst=[]
        error = 0
        for k in range(0,len(self.diameter)):
            error += np.abs(self.gamma_dsd_n(self.diameter[k],Dm,mu) - N[k]/Nw)
            dst.append(self.gamma_dsd_n(self.diameter[k],Dm,mu))

        if(debug):
            plot(self.diameter,N,'r')
            plot(self.diameter,array(dst)*Nw,'b')
            legend(['Nd Disdrometer','Nd gamma_distribution'])

        return error
        
    def gamma_dsd_n(self,D,Dm,mu):
        return self.f_func(mu) * (D/Dm)**mu * np.exp(-(4+mu)*(D/Dm))

    def f_func(self,mu):
        return (6.0*(mu+4)**(mu+4))/(4.0**4 * np.math.gamma(mu+4))
        #return (6.0/3.67**4)* ((3.67+mu)**(mu+4))/np.math.gamma(mu+4)

    def __get_last_nonzero(self, N):
        k=0
        for i in range(0, len(N)):
            if(N[i]>0):
                k=i
        return k

    spread = [0.129, 0.129, 0.129, 0.129,0.129,0.129,0.129,0.129,0.129,0.129,0.257,
            0.257,0.257,0.257,0.257,0.515,0.515,0.515,0.515,0.515,1.030,1.030,
            1.030,1.030,1.030,2.060,2.060,2.060,2.060,2.060,3.090, 3.090]
    

if __name__=='__main__':
    filename ='/net/makalu/radar/tmp/jhardin/IFloodS_APU02_2013_0502_dsd.txt'

    apureader = APU_reader(filename)
    res = apureader.calculate_scattering()

    plt.scatter(res['Kdp'], res['Ah'])
    plt.xlabel('Kdp(deg/km)')
    plt.ylabel('Attenuation(db/km)')
    plt.title('Kdp vs Attenuation at X-Band')

    plt.show()
