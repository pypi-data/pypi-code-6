"""
Extrapolates species copy numbers of single lineage data to extant cell population.

Three steps:
 - Sampling the data at fixed intervals
 - Bin the data
 - Calculating the mass density function form the binned data.
 
Written by T.R. Maarleveld and M. Moinat, Amsterdam, The Netherlands
E-mail: tmd200@users.sourceforge.net
Last Change: October 30, 2014
"""

from __future__ import division, print_function, absolute_import
import numpy as np,time,sys

class ExtrapolateExtant:    
    def __init__(self, data_stochsim, data_stochsim_celldivision):        
        """
        This class allows for the calculation of population statistics from the simulation of a single lineage        
        """
        self.time_array = data_stochsim.time[:,0]
        self.species_array = data_stochsim.species
        self.species_labels = data_stochsim.species_labels
        self.IDT_array = data_stochsim_celldivision.interdivision_times[:,0]
        self.age_array = data_stochsim_celldivision.ages[:,0]
        self.generation_timesteps = data_stochsim_celldivision.generation_timesteps
        
    def make_full_IDT(self):
        """ Creates a list with for each time point the interdivision time value of the corresponding generation. """
        self.full_IDT_array = np.zeros(sum(self.generation_timesteps))
        n=0
        for IDT, n_steps in zip(self.IDT_array, self.generation_timesteps):
            self.full_IDT_array[n:n+n_steps] = IDT
            n+=n_steps     
    
    def sample_per_generation(self,n_samples):
        """
        Sample the ages, interdivision times and species at fixed time intervals in each generation
        reason: no shifts in cell ages.
        
        Example:
        t(tau=0)=0, t(tau=1)=1, t(tau=2)=2, ..., t(tau=0)=35.54, t(tau=1),36.54), ....
        
        Input:
          - *n_samples* number of fixed width samples to make.        
        """
        tend = self.time_array[-1]
        self.sample_timepoints = np.array([])
        t1 = 0
        n_generations = len(self.IDT_array)
        current_steps = 0
        current_intervals = 0
        self.sample_indices = []
        for n,t2 in enumerate(self.IDT_array.cumsum()): 
            n_intervals = round(((self.IDT_array[n]/tend))*n_samples)            
            self.sample_timepoints = np.append(self.sample_timepoints, np.linspace(t1, t2,n_intervals ))
            t1 += self.IDT_array[n]            

            self.sample_indices += list(self.time_array[current_steps:current_steps+self.generation_timesteps[n]].searchsorted(self.sample_timepoints[current_intervals:current_intervals+n_intervals], side = 'right') - 1 + int(current_steps)) # Get point before 
            current_steps += self.generation_timesteps[n]
            current_intervals += n_intervals
        
        IDT_runtotal = self.time_array - self.age_array # Absolute time of start of generation
        self.sampled_ages = self.sample_timepoints - IDT_runtotal[self.sample_indices] # 07-02-2014
        self.sampled_species = self.species_array[self.sample_indices]
        self.sampled_IDTs = self.full_IDT_array[self.sample_indices] 
        
    
    def sample_fixedinterval(self, n_samples):
        """ 
        Samples the ages, interdivision times and species at fixed time intervals over the entire lineage
        
        Example:        
        t(tau=0)=0, t(tau=1)=1, t(tau=2)=2, ..., t(tau=0.48)=35, t(tau=1.48)=36, ...
        
        Input:
          - *n_samples* number of fixed width samples to make.
        """        
        IDT_runtotal = self.time_array - self.age_array # Absolute time of start of generation
        
        self.sample_timepoints = np.linspace(0, self.time_array.max(), n_samples)        
        sample_indices = self.time_array.searchsorted(self.sample_timepoints, side = 'right') - 1 # Get point before
                
        self.sampled_ages = self.sample_timepoints - IDT_runtotal[sample_indices] # 07-02-2014
        self.sampled_species = self.species_array[sample_indices]
        self.sampled_IDTs = self.full_IDT_array[sample_indices] 
    
    def bin_data(self, n_bins_IDT,n_bins_age):
        """
        Bins the copy number, interdivision time, and age data in one histogram structure. Also determines the value of each bin.
        
        We allow a different number of bins for IDTs and age.
        
        Binning for each species:
        - One bin for each interdivision time bin -> for each age bin -> for each copy number.
        - Count how often a species copy number occurs in an age, in an interdivision time.
        
        Input:
            - *n_bins_IDT* number of bins to make for IDT
            - *n_bins_age* number of bins to make for age
        """                        
        self.fm_hist, fm_edges = np.histogram(self.IDT_array, n_bins_IDT, normed=True)             
        self.fm_values = [(x+y)/2. for x,y in list(zip(fm_edges,fm_edges[1:]))]  # What's this?                  
        
        # For each species make a 3D histogram structure and make a list of the index of every bin to be raised.
        # Result: total_hist[species][species_amount, IDT, age]
        self.total_hist = []
        for i in range(len(self.species_labels)):
            species_amounts = self.sampled_species[:,i]        
            min_amount = species_amounts.min()
            max_amount = species_amounts.max()
            n_bins_species = max_amount - min_amount + 1
            species_values = range(min_amount,max_amount  + 1)      
          
            hist3d, hist_edges = np.histogramdd((species_amounts, self.sampled_IDTs, self.sampled_ages), (n_bins_species, n_bins_IDT, n_bins_age))
            self.total_hist.append( (hist3d,species_values) )
        
        # Age and IDT value of each bin (=mean of left and right bin edge). This is for every species the same.
        self.IDT_values = [(x+y)/2. for x,y in list(zip(hist_edges[1],hist_edges[1][1:]))]  
        self.age_values = [(x+y)/2. for x,y in list(zip(hist_edges[2],hist_edges[2][1:]))]
    
    def Calculate_ExtantCellCN(self, k,integration_method= 'trapezoidal' ):
        """
        Calculates the probability mass function of the species copy number in extant cells, using the binned data.
        
        Input:            
            *k* - specific population growth rate. 
            *integration_method* (string) [default = 'trapezoidal']
        """
        self.k = k
        dIDT = self.IDT_values[1] - self.IDT_values[0]
        dage = self.age_values[1] - self.age_values[0]
        
        self.extant_species_pn = [] # Stores for each species the p(n) extant
        self.extant_species_pn_sum = []
        if integration_method.lower() == 'riemann':
             print("Using the Riemann sum approximation for numerical integration ...")
        else:
            print("Using the 2D trapezoil rule for numerical integration ...")
        
        for species_index in range(len(self.species_labels)):
            #print('Species:', cmod.data_stochsim.species_labels[species_index])
            species_hist = self.total_hist[species_index][0]        
            species_amount_values = self.total_hist[species_index][1]
            
            # Sum over the species, gives 2D array of sum per age and IDT.
            self.species_sums = species_hist.sum(axis = 0)
            
            # Initialize p
            p = {n:0 for n in species_amount_values}               
            sum_p_n = 0
            if integration_method.lower() == 'riemann': ### 2D Riemann Sum (less accurate) ####                   
                # For every species amount
                for s_amount_hist, n in list(zip(species_hist, species_amount_values)):
                    index_IDT = 0
                    # For every IDT
                    for age_hist, IDT_value in list(zip(s_amount_hist, self.IDT_values)):
                        index_age = 0
                        # For every age
                        for bin_count, age_value in list(zip(age_hist, self.age_values)):
                            normalization = self.species_sums[index_IDT][index_age]                         
                            if normalization > 0: # Then bin_count also > 0. Prevents dividing 0 by 0
                                p[n] += self.fm_hist[index_IDT] * self.h(age_value,IDT_value) * bin_count/normalization * dage * dIDT                                 
                            index_age += 1        
                        index_IDT += 1                
                    sum_p_n += p[n]            
             
            else: ### 2D trapezoidal rule:  http://mathfaculty.fullerton.edu/mathews/n2003/SimpsonsRule2DMod.html                      
                dx = dIDT
                dy = dage
                
                a = self.IDT_values[0]
                b = self.IDT_values[-1]            
                c = self.age_values[0]
                d = self.age_values[-1]         
                for s_amount_hist,n in zip(species_hist,species_amount_values):
                    f_a_c = 0
                    f_b_c = 0
                    f_a_d = 0
                    f_b_d = 0                    
                    normalization = self.species_sums[0][0] 
                    bin_count = s_amount_hist[0][0]
                    if normalization > 0:                      
                        f_a_c = self.fm_hist[0] * self.h(c,a) * bin_count/normalization
                
                    normalization = self.species_sums[-1][0]     
                    bin_count = s_amount_hist[-1][0]
                    if normalization > 0:   
                        f_b_c = self.fm_hist[-1] * self.h(c,b) * bin_count/normalization
                
                    normalization = self.species_sums[0][-1]                
                    bin_count = s_amount_hist[0][-1]   
                    if normalization > 0:     
                        f_a_d = self.fm_hist[0] * self.h(d,a) * bin_count/normalization
                    
                    normalization = self.species_sums[-1][-1]        
                    bin_count = s_amount_hist[-1][-1]
                    if normalization > 0:      
                        f_b_d = self.fm_hist[-1] * self.h(d,b) * bin_count/normalization

                    sum_f_x_c = 0
                    sum_f_x_d = 0
                    sum_f_a_y = 0
                    sum_f_b_y = 0
                    sum_f_x_y = 0                
                    x_i = 1                
                    for x in self.IDT_values[1:-1]:
                        normalization = self.species_sums[x_i][0]  # x[i],c
                        bin_count = s_amount_hist[x_i][0]         
                        if normalization > 0:      
                            sum_f_x_c += self.fm_hist[x_i] * self.h(c,x) * bin_count/normalization       
                                         
                        normalization = self.species_sums[x_i][-1] # x[i],d
                        bin_count = s_amount_hist[x_i][-1] 
                        if normalization > 0:      
                            sum_f_x_d += self.fm_hist[x_i] * self.h(d,x) * bin_count/normalization                        
                        x_i += 1
                    
                    y_i = 1                
                    for y in self.age_values[1:-1]:
                        normalization = self.species_sums[0][y_i] # a,y[i]
                        bin_count = s_amount_hist[0][y_i]
                        if normalization > 0:      
                            sum_f_a_y += self.fm_hist[0] * self.h(y,a) * bin_count/normalization                    
                            
                        normalization = self.species_sums[-1][y_i] # b,y[i]
                        bin_count = s_amount_hist[-1][y_i]
                        if normalization > 0:      
                            sum_f_b_y += self.fm_hist[-1] * self.h(y,b) * bin_count/normalization                        
                        y_i += 1                    
                    
                    x_i = 1                
                    for x in self.IDT_values[1:-1]:     
                        y_i = 1              
                        for y in self.age_values[1:-1]:  
                            normalization = self.species_sums[x_i][y_i]
                            bin_count = s_amount_hist[x_i][y_i]  # x[i],y[i]
                            if normalization > 0:      
                                sum_f_x_y += self.fm_hist[x_i] * self.h(y,x) * bin_count/normalization                    
                            y_i += 1
                        x_i += 1
                    #print(f_a_c,f_b_c,f_a_d,f_b_d)
                    #print(sum_f_x_c,sum_f_x_d,sum_f_a_y,sum_f_b_y,sum_f_x_y)                
                    p[n] = 0.25*dx*dy*(f_a_c + f_b_c + f_a_d + f_b_d + 2*(sum_f_x_c + sum_f_x_d + sum_f_a_y + sum_f_b_y) + 4*sum_f_x_y)                    
                    sum_p_n += p[n]
                #print(sum_p_n)
                
            self.extant_species_pn.append(p) 
            self.extant_species_pn_sum.append(sum_p_n)
            
    def h(self,a,tau):
        """
        conditional probability of cell age a given that the interdivision time equals tau for a sample of extant cells
        
        - *a* = age (float)
        - *tau* = IDT (float)
        """
        return self.k * np.exp(self.k*(tau-a))  
