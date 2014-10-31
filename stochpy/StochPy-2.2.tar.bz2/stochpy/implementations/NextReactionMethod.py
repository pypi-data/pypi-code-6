#! /usr/bin/env python
"""
Next Reaction Method
====================
This module performs the Next Reaction Method from Gibson and Bruck [1]. Therefore, it is also called the Gibson and Bruck algorithm.

[1] M.A. Gibson and J. "Bruck Efficient Exact Stochastic Simulation of Chemical Systems with Many Species and Many
Channels", J. Phys. Chem., 2000, 104, 1876-1889

Written by T.R. Maarleveld, Amsterdam, The Netherlands
E-mail: tmd200@users.sourceforge.net

Speed improvements by M. Moinat.
Last Change: October 28, 2014
"""

############################# IMPORTS #################################### 

from __future__ import division, print_function, absolute_import

import time,os,sys,copy

from ..tools.Priority_queue import PQDict
from .StochPyTools import  __species__,StochPySSA_Shared,np

########################### END IMPORTS ##################################

class NextReactionMethod(StochPySSA_Shared):
    """ 
    Next Reaction Method from Gibson and Bruck 2000 [1]. 

    [1] M.A. Gibson and J. "Bruck Efficient Exact Stochastic Simulation of Chemical Systems with Many Species and Many Channels", J. Phys. Chem., 2000,104,1876-1889 

    Input:  
     - *File* filename.psc
     - *dir* /home/user/Stochpy/pscmodels/filename.psc    
    """
    def __init__(self,File,dir):
        self.Parse(File,dir,IsNRM=True,IsDelayed = False, IsSMM = False)   

    def Execute(self,settings,IsStatusBar=False):
        """
        Generates T trajectories of the Markov jump process.

        Input:
         - *settings* (class object)   
        """
        if settings.UseSeed:
            np.random.seed(5)             

        self._IsInitial = True
        self.fixed_species_amount = copy.deepcopy(self.parse.fixed_species_amount)
        self.X_matrix = copy.deepcopy(settings.X_matrix)
        self.IsTrackPropensities = copy.copy(settings.IsTrackPropensities)
        self.sim_t = copy.copy(settings.starttime)
        self.endtime = settings.endtime    # 26-11-2013
        self.endsteps = settings.timesteps # 26-11-2013
        
        #Volume addition (also modification in self.propensities) 15-10-2013 21-11-2013
        try:
            self.volume_eval_code = settings.volume_code  ##15-10-2013
            self.HasVolumeCode = True      # 21-11-2013
        except AttributeError:             # No volume_code present in settings
            self.HasVolumeCode = False     # 21-11-2013
            
        self.SetEvents()        
        self.Propensities()        
        self.InitialMonteCarloStep() #Initialize TauHeap         
        self.SpeciesSelection(settings)    
        self.RateSelection(settings)
        
        if not self.sim_t:      
            self.timestep = 1
            self.Initial_Conditions()
            if self.HasVolumeCode:
                self.V_output = [self._current_volume]
                
        nstep_counter = 1
        t1 = time.time()
        while self.sim_t < self.endtime and self.timestep < self.endsteps:            
            if self.sim_a_0 <= 0:           # All reactants got exhausted
                 break                 
                  
            self.RunExactTimestep()         # Run time step   
            self.HandleEvents()               
            
            if (self.sim_t < self.endtime): # Needed for self.reaction_index = nan
                self.Propensities()         # Update Propensities  
                self.UpdateHeap()                  
            if not settings.IsOnlyLastTimepoint:                
                self.sim_output.append(self.GenerateOutput())    
                if self.HasVolumeCode:      #21-11-2013
                    self.V_output.append(self._current_volume)    
                     
                if self.IsTrackPropensities:
                    output_step = self.sim_a_mu.tolist()
                    output_step.insert(0,self.sim_t)
                    if self.IsRateSelection:
                        output_step = [output_step[j] for j in self.rate_output_indices]
                    self.propensities_output.append(output_step)
            
            t2 = time.time()
            if IsStatusBar and t2-t1> 1:
                t1 = time.time()             
                sys.stdout.write('\rsimulating {0:s}'.format('.'*nstep_counter) ) 
                sys.stdout.flush() 
                nstep_counter+=1
                if nstep_counter > 10:
                    nstep_counter = 1                
                    sys.stdout.write('\rsimulating {0:s}         '.format('.'*nstep_counter))
                    sys.stdout.flush()
                    
        if settings.IsOnlyLastTimepoint:              
            self.sim_output = [self.GenerateOutput()]
            if self.HasVolumeCode: #21-11-2013
                self.V_output = [self._current_volume]                        
            if self.IsTrackPropensities:
                output_step = self.sim_a_mu.tolist()
                output_step.insert(0,self.sim_t)
                if self.IsRateSelection:
                    output_step = [output_step[j] for j in self.rate_output_indices]
                self.propensities_output.append(output_step)
                    
        if IsStatusBar and t1:
            sys.stdout.write('\rsimulation done!               \n')   
   
    def InitialMonteCarloStep(self): 
        """ Monte Carlo step to determine all taus and to create a pqdict indexed priority queue """  
        randoms = np.random.random(self.n_reactions)               # Pre-generate for each reaction random numbers
        self.randoms_log_init = -1 * np.log(randoms)      
        self.sim_taus = self.randoms_log_init/self.sim_a_mu + self.sim_t # Make all taus absolute with sim_t (= given starttime)
        
        pairs = [(j, self.sim_taus[j]) for j in range(self.n_reactions)] #(key, priority) pairs   
        self.heap = PQDict(pairs)        
        
        ##Build initial randoms for taus to come, always at start of execution nrm
        self.randoms_log = -1 * np.log(  np.random.random(1000)  ) # Pre-generate random numbers
        self.count = 0
        
    def UpdateHeap(self): #3-11-2013
        """Renews the changed propensities in the priority queue heap."""
        if not self._IsPerformEvent:
            self.prop_to_update = self.parse.dep_graph[self.reaction_index] # Propensities to update  
        else:
            self.prop_to_update = [r for r in range(self.n_reactions)]        
              
        if self.count >= (1000-len(self.prop_to_update)):
            randoms = np.random.random(1000)              # Pre-generate random numbers
            self.randoms_log = -1 * np.log(randoms)
            self.count = 0
            
        for j in self.prop_to_update: #Updated propensities should also be updated in the heap
            if j == self.reaction_index: #5c
                tau_new = self.randoms_log[self.count]/self.sim_a_mu[j] + self.sim_t
                self.count += 1
            else: #5b, changed propensity
                if self.sim_a_mu_prev[j] == 0: 
                    ##Note: due to zero propensity (and an inf tau), it is difficult to reuse random. Assume getting new random is faster.
                    tau_new = self.randoms_log[self.count]/self.sim_a_mu[j] + self.sim_t
                    self.count += 1
                else: #Normal update
                    tau_alpha = self.sim_taus[j]        #Faster than getting from heap directly (self.heap[j])
                    tau_new = self.sim_a_mu_prev[j]/self.sim_a_mu[j]*(tau_alpha- self.sim_t) + self.sim_t              
            #Note, no exception for self.sim_a_mu == 0. Then tau_new automatically becomes infintie (faster than if statement to except this)          
            self.sim_taus[j] = tau_new #Keep track of the reaction taus, parallel to the heap.
            self.heap.updateitem(j, tau_new) #Updates the tau with index j and resorts the heap.

    def Propensities(self):
        """ Determines the propensities to fire for each reaction at the current time point. At t=0, all the rate equations are compiled. """   
        if self._IsInitial:
            self.sim_a_mu = np.zeros(self.n_reactions)            # Initialize a(mu)
            if self.HasVolumeCode: #26-11-2013 Pre-compile volume code
                self.volume_eval_code = compile(self.volume_eval_code, 'VolumeCode', 'exec')
            [setattr(__species__,self.parse.species[s],self.X_matrix[s]) for s in range(self.n_species)] # Set species quantities
            [setattr(__species__,self.fixed_species[s],self.fixed_species_amount[s]) for s in range(len(self.fixed_species))]
            self.reaction_fired = -1     #Update all propensities
            self._IsInitial = False     
        else:          
            self.sim_a_mu_prev = copy.copy(self.sim_a_mu) #Backup old propensity 
            if self._IsPerformEvent:
                [setattr(__species__,self.parse.species[s],self.X_matrix[s]) for s in range(self.n_species)] #Update all species, to be sure.
                self.reaction_fired = -1 #Update all propensities                
            else:
                self.species_to_update = self.parse.reaction_affects[self.reaction_index] # Determine vars to update
                [setattr(__species__,self.parse.species[s],self.X_matrix[s]) for s in self.species_to_update]
                self.reaction_fired = self.reaction_index
        
        if self.HasVolumeCode: #21-11-2013. Calculate the new Volume
            exec(self.volume_eval_code)
        
        propensity_eval_code = self.parse.propensity_codes[ self.reaction_fired ] #21-11-2013, select code of subset to be updated. [-1] updates all
        self.rateFunc(propensity_eval_code, self.sim_a_mu)        # Calc. Propensities and put result in sim_a_mu
        
        assert self.sim_a_mu.min() >= 0, "Error: Negative propensities are found" 
        self.sim_a_mu = abs(self.sim_a_mu)                        # -0 to 0
        self.sim_a_0 = self.sim_a_mu.sum()

    def RunExactTimestep(self):
        """ Perform a direct SSA time step and pre-generate M random numbers """ 
        #np.random.seed(5) 
        minimum = self.heap.peek()                                # peek() returns item at top of heap (has lowest tau)
        self.reaction_index = minimum[0]                          # Pick reaction to executeO(1)
        self.sim_tau = minimum[1]                                 # Pick tau O(1)         
        if self.sim_tau < self.endtime:
            self.sim_t = self.sim_tau                             # New time
            try:
                self.X_matrix += self.N_matrix_transpose[self.reaction_index]
                self.timestep += 1
            except MemoryError as ex:
                print(ex)
                sys.exit()      
        else: 
            self.sim_t = self.endtime
            self.reaction_index = np.nan
