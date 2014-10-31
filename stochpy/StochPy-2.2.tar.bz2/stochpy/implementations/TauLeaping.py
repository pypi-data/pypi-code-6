#! /usr/bin/env python
"""
Optimized Tau-Leaping
=====================
This program performs Optimized Explicit Tau-leaping algorithm, which is an approximate version of the exact Stochastic Simulation Algorithm (SSA). Here, an efficient step size selection procedure for the tau-leaping method [1] is used.

[1] Cao. Y, Gillespie D., Petzold L. (2006), "Efficient step size selection for the tau-leaping method", J.Chem. Phys. 28:124-135

Written by T.R. Maarleveld, Amsterdam, The Netherlands
E-mail: tmd200@users.sourceforge.net
Last Change: October 31, 2014
"""

from __future__ import division, print_function, absolute_import

############################## IMPORTS ###################################

import sys,copy,time,os,random,re
from .StochPyTools import __species__,StochPySSA_Shared,np

########################### END IMPORTS ##################################

class OTL(StochPySSA_Shared):
    """  
    Input:  
     - *File* filename.psc
     - *dir* /home/user/Stochpy/pscmodels/filename.psc    
    """
    def __init__(self,File,dir):
        self.Parse(File,dir,IsTauLeaping = True)  

    def Execute(self,settings,IsStatusBar=False,epsilon = 0.03,critical_reactions=[]):
        """
        Generates T trajectories of the Markov jump process. 
         - *settings* (python class)
         - *epsilon* [default = 0.03] (float)       
         - *critical_reactions* [default = [] ] (list)
        """
        if settings.UseSeed:
            np.random.seed(5)
            random.seed(5)
        
        self._IsInitial = True
        self._HAS_Gi_OPTIONS = False
        self.fixed_species_amount = copy.deepcopy(self.parse.fixed_species_amount)
        self.X_matrix = copy.deepcopy(settings.X_matrix)
        self.IsTrackPropensities = copy.copy(settings.IsTrackPropensities)
        self.sim_t = copy.copy(settings.starttime)        
        try:
            self.volume_code = settings.volume_code
        except AttributeError: # No volume_code present in settings
            self.volume_code = "self._current_volume = 1"  
        
        self.sim_epsilon = epsilon
        self.sim_Nc = 10
        self.g_vector = np.zeros(self.n_species)                  # Initialize g vector   
        self.sim_mu  = np.zeros(self.n_species)                   # Init mu  (32.a)
        self.sim_var = np.zeros(self.n_species)                   # Init var (32.b)       
        
        self._user_defined_critical_reactions = []
        for r in critical_reactions:
            assert r in self.rate_names, "Error: user-defined critical reaction '{0}' does not exist".format(r)
            self._user_defined_critical_reactions.append(self.rate_names.index(r))                    
             
        #self.state_change_vector = copy.copy(self.N_matrix_transpose)
        self._InitialOTLstep = True   
        if self.sim_t == 0:            
            randoms = np.random.random(1000)
            self.randoms_log = np.log(randoms)*-1
            self.randoms = np.random.random(1000)
            self.count = 0      
        IsExhausted = False
        self._IsNegative = False
        sim_OTL_steps = 0  
              
        self.__events__ = copy.deepcopy(self.parse.Mod.__events__)  # deepcopy, very important! Augustus 21, 2014
        self._IsPerformEvent = False
        for ev in self.__events__:
            for s_id in sorted(self.species_names, reverse=True): # makes sure that the longest identifiers are replaced first
                if s_id not in self.fixed_species:
                    ev.code_string = ev.code_string.replace('self.mod.{0:s}'.format(s_id),'X_matrix[{0:d}]'.format(self.species_pos[s_id]) )
            ev.xcode = compile("self.state = {0:s}".format(ev.code_string),'event{0}'.format(ev),'exec') 
        
        self.Propensities(IsTauleaping=True)
        self.SpeciesSelection(settings)
        self.RateSelection(settings)
        
        if not self.sim_t:      
            self.timestep = 1
            self.Initial_Conditions(IsTauleaping = True)      
            self.V_output = [self._current_volume]      # 27-01-2014   
                   
        nstep_counter = 1 
        t1 = time.time()
        while self.sim_t < settings.endtime and self.timestep < settings.timesteps:
            if not self._IsNegative:				                    # If there are no negative conc. after a Tau-leap step
                self.GetCriticalReactions()
                self.GetG()                
                if self.sim_a_0 <= 0:                           # All reactants got exhausted  
                     break               
                self.GetMuVar()
                self.GetTauPrime()
            ##################### start Possible Feedback loop ##################       
            self.DetermineMethod()
            ##### Optimized Tau-Leaping step #####
            if self._IsOTL:
                self.GetTauPrimePrime()
                self.GetK()
                self.Execute_K_Reactions()
                if not self._IsNegative:  
                    self.sim_t += self.sim_tau
                    self.HandleEvents(IsTauleapingStep=True)                                                      
                    self.Propensities(IsTauleaping = True)                    
                    if not settings.IsOnlyLastTimepoint:
                        self.sim_output.append(self.GenerateOutput(IsTauleaping=True))                        
                        self.V_output.append(self._current_volume)       
                        if self.IsTrackPropensities:
                            output_step = self.sim_a_mu.tolist()
                            output_step.insert(0,self.sim_t)
                            if self.IsRateSelection:
                                output_step = [output_step[j] for j in self.rate_output_indices]
                            self.propensities_output.append(output_step)
                    
                    sim_OTL_steps += 1
                    self.timestep += 1                
                elif self._IsNegative:                              # Start feedback loop                     
                    self.sim_tau_prime /= 2.0   
            elif self._IsExact:                                     # Direct SSA step
                i=1
                ExactTimesteps = 100       
                while (i < ExactTimesteps) and (self.sim_t < settings.endtime) and (self.timestep < settings.timesteps):                    
                    if self.sim_a_0 <= 0:                           # All reactants got exhausted
                        IsExhausted = True           
                        break
                        
                    self.RunExactTimestep(settings)
                    self.HandleEvents()
                    self.Propensities(IsTauleaping=True)                    
                    
                    if not settings.IsOnlyLastTimepoint:
                        self.sim_output.append(self.GenerateOutput(IsTauleaping=True))
                        self.V_output.append(self._current_volume)                           
                        if self.IsTrackPropensities:
                            output_step = self.sim_a_mu.tolist()
                            output_step.insert(0,self.sim_t)
                            if self.IsRateSelection:
                                output_step = [output_step[j] for j in self.rate_output_indices]
                            self.propensities_output.append(output_step)
                    i+=1            
                    
                    t2 = time.time()
                    if IsStatusBar and t2-t1> 1:
                        t1 = time.time()                        
                        sys.stdout.write('\rsimulating {0:s}'.format('.'*nstep_counter) ) 
                        sys.stdout.flush()
                        nstep_counter+=1
                        if nstep_counter > 10:
                            nstep_counter = 1
                            sys.stdout.write('\rsimulating {0:s}         '.format('.'*nstep_counter) )
                            sys.stdout.flush()
            #################### End possible feedback loop #################
            t2 = time.time()               
            if IsStatusBar and t2-t1> 1:
                t1 = time.time()                
                sys.stdout.write('\rsimulating {0:s}'.format('.'*nstep_counter) ) 
                sys.stdout.flush() 
                nstep_counter+=1
                if nstep_counter > 10:
                    nstep_counter = 1
                    sys.stdout.write('\rsimulating {0:s}         '.format('.'*nstep_counter) )
                    sys.stdout.flush()
                    
            if IsExhausted:                
                break
                
        if settings.IsOnlyLastTimepoint:              
            self.sim_output = [self.GenerateOutput()]
            self.V_output = [self._current_volume]
            if self.IsTrackPropensities:
                output_step = self.sim_a_mu.tolist()
                output_step.insert(0,self.sim_t)
                if self.IsRateSelection:
                    output_step = [output_step[j] for j in self.rate_output_indices]
                self.propensities_output.append(output_step)

        if IsStatusBar and t1:
            sys.stdout.write('\rsimulation done!               \n')

    def RunExactTimestep(self,settings):
        """ Perform a direct method SSA time step"""
        if self.count == 1000:
            randoms = np.random.random(1000)
            self.randoms_log = np.log(randoms)*-1
            self.randoms = np.random.random(1000)
            self.count = 0      
   
        self.sim_r2  = self.randoms[self.count]                   # Draw random number 2 [0-1]    
        self.sim_tau = self.randoms_log[self.count]/self.sim_a_0  # reaction time generation       
        if (self.sim_t + self.sim_tau) < settings.endtime:
            self.sim_t += self.sim_tau                            # Time update
            self.count+=1

            self.reaction_index = 0
            sum_of_as = self.sim_a_mu[self.reaction_index]
            criteria =  self.sim_r2*self.sim_a_0
            while sum_of_as < criteria:                           # Use r2 to determine which reaction will occur
                self.reaction_index += 1    	                    # Index
                sum_of_as += self.sim_a_mu[self.reaction_index]
            
            try:
                self.X_matrix += self.N_matrix_transpose[self.reaction_index]
                self.timestep += 1
            except MemoryError as ex:
                print(ex)
                sys.exit()
        else: 
            self.sim_t = settings.endtime
            self.reaction_index = np.nan            

    def GetCriticalReactions(self):
        """ Determines the critical reactions (as a boolean vector) """
        if self._InitialOTLstep:            
            self._Nt_nan = copy.copy(self.N_matrix_transpose)     
            self._Nt_nan[self._Nt_nan>=0]= np.nan # look only at the metabolites it's going to exhaust
            self._InitialOTLstep = False
      
        self.critical_reactions = []        
        output = self.X_matrix.ravel()/abs(self._Nt_nan)
        minima = np.nanmin(output,axis=1)
        for reaction in minima:
            if reaction < self.sim_Nc:
                self.critical_reactions.append(1)
            else:
                self.critical_reactions.append(0)
        for j in self._user_defined_critical_reactions:
            self.critical_reactions[j] = 1
                
    
    def GetG(self):
        """ Determine the G-vector based on options provided in [1], page 6 """ 
        if not self._HAS_Gi_OPTIONS: # Determine once the Gi options metnioned in [1] page 6
            self.options = np.zeros(self.n_species) 
            for i,hor_i in enumerate(self.parse.species_HORs):
                if hor_i == 2:
                    if self.parse.species_max_influence[i] == 1:
                        self.options[i] = 2
                    elif self.parse.species_max_influence[i] == 2:
                        self.options[i] = 3                    
                elif hor_i == 3:
                    if self.parse.species_max_influence[i] == 1:
                        self.options[i] = 4
                    elif self.parse.species_max_influence[i] == 2:
                        self.options[i] = 5
                    elif self.parse.species_max_influence[i] == 3:
                        self.options[i] = 6                   
            self._HAS_Gi_OPTIONS = True  

        self.g_vector = np.ones(self.n_species)        
        for i,option in enumerate(self.options):
            if option == 1: self.g_vector[i] = 1
            elif option == 2: self.g_vector[i] = 2
            elif option == 3: self.g_vector[i] = 2 + 1.0/(self.X_matrix[i]-1)            
            elif option == 4: self.g_vector[i] = 3
            elif option == 5:
                try:
                    self.g_vector[i] = 3 + 1.5/(self.X_matrix[i]-1)
                except:
                    self.g_vector[i] = 3
            elif option == 6:
                try: 
                    self.g_vector[i] = 3 + 1.0/(self.X_matrix[i]-1) + 2.0/(self.X_matrix[i]-2)
                except:
                    self.g_vector[i] = 3            

    def GetMuVar(self):
        """ Calculate the estimates of mu and var for each species (i) """        
        for i,v_i in enumerate(self.parse.N_matrix):
            self.sim_mu[i] = np.dot(v_i,self.sim_a_mu)
            self.sim_var[i]= np.dot(v_i*v_i,self.sim_a_mu)            

    def GetTauPrime(self):
        """ Calculate tau' """
        part = np.divide(self.X_matrix.ravel(),self.g_vector)*self.sim_epsilon # eps*x[i]/g[i] for all i
        num = np.array([part,np.ones(len(part))])                  # eps*x[i]/g[i] for all i , 1 for all i
        numerator = num.max(axis=0)                                # max(eps*x[i]/g[i],1) for all i
        abs_mu = np.abs(self.sim_mu)                               # abs(mu) for all i
        bound1 = np.divide(numerator,abs_mu)                       # max(eps*x[i]/g[i],1) / abs(mu[i]) for all i
        numerator_square = np.square(numerator)    	
        bound2 = np.divide(numerator_square,self.sim_var)          # max(eps*x[i]/g[i],1)^2 / abs(mu[i]) for all i
        tau_primes = np.array([bound1,bound2])			
        try:
            self.sim_tau_prime = np.min(tau_primes[~np.isnan(tau_primes)]) # min (bound1,bound2)
        except:
            self.sim_tau_prime = 10**6
        
    def DetermineMethod(self):
        """ Determines for each time step what to perform: exact of approximate SSA """         
        criteria = 10.0/self.sim_a_0                               # Based on literature [2] (Cao et et. 2006)
        if self.sim_tau_prime > criteria and self.sim_tau_prime != 10**6:
            self._IsExact = False
            self._IsOTL = True
        else:
            self._IsExact = True
            self._IsOTL = False

    def GetA0c(self):
        """ Calculate the total propensities for all critical reactions """
        self.sim_a_0_c = np.dot(self.critical_reactions,self.sim_a_mu)
    
    def GetTauPrimePrime(self):
        """ Calculate Tau'' """
        if self.count == 1000:                                     # Re-generate random numbers
            randoms = np.random.random(1000)  
            self.randoms_log = np.log(randoms)*-1         
            self.count = 0      
        self.GetA0c()  
        if self.sim_a_0_c == 0:					                           # a_0_c = 0
            self.sim_tau_prime_prime = 10**6
        elif self.sim_a_0_c != 0:
            self.sim_tau_prime_prime = self.randoms_log[self.count]/self.sim_a_0_c
            self.count+=1      

    def GetK(self):        
        """ Determines the K-vector, which describes the number of firing reactions for each reaction. """
        self.K_vector = np.zeros((self.n_reactions,1),dtype = int)
        if self.sim_tau_prime < self.sim_tau_prime_prime:          # tau' < tau''
            self.sim_tau = self.sim_tau_prime            
            for j,IsCritical in enumerate(self.critical_reactions):
                if not IsCritical:
                    a_j = self.sim_a_mu[j]
                    Lambda = self.sim_tau * a_j       
                    k_j = np.random.poisson(Lambda)           
                    self.K_vector[j] = [k_j] 
              
        else:
            self.sim_tau = self.sim_tau_prime_prime                # tau' > tau''            
            probs = []
            IsCrit = False
            for j,IsCritical in enumerate(self.critical_reactions):         
                a_j = self.sim_a_mu[j]
                if IsCritical:
                    IsCrit = True
                    p = float(a_j)/self.sim_a_0          
                    probs.insert(j,p)
                    if p == 1:                                     # Only one critical reaction
                        self.K_vector[j] = [1]
                elif not IsCritical:
                    probs.insert(j,0.0)
                    Lambda = self.sim_tau * a_j
                    k_j = np.random.poisson(Lambda)
                    self.K_vector[j] = [k_j]                
            if IsCrit:                                             # Bug fixed jan 15 2011
                (prob,index) = GetSample(probs)                    # Select one crit.reaction that fires once
                self.K_vector[index] = [1]

    def Execute_K_Reactions(self):
        """ Perform the determined K reactions """
        self._IsNegative = False  
        x_temp  = copy.copy(self.X_matrix)    
        x_temp += np.dot(self.parse.N_matrix,self.K_vector).ravel()     
        minimal_amount = x_temp.min()
        if minimal_amount < 0:                                     # Check for negatives after the K reactions 
            self.sim_tau = self.sim_tau/2.0
            self._IsNegative = True
        else:            
            self.X_matrix = x_temp                                 # Confirm the done K reactions

################### Useful functions #########################

def MinPositiveValue(List):
    """
    This function determines the minimum positive value

    Input:
     - *List*
    Output: 
     - *minimum positive value*
    """
    positives = []
    for value in List:
        if value > 0:
            positives.append(value)
    return min(positives)

def GetSample(probs):  
    """
    This function extracts a sample from a list of probabilities.
    The 'extraction chance' is identical to the probability of the sample.

    Input:
     - *probs*: (list)
    Output: 
     - *sample*
     - *sample index*
    """
    output = []
    MinimumProb = float(MinPositiveValue(probs))
    for prob in probs:
        for i in range(0,int(100*prob/MinimumProb)):
            output.append(probs.index(prob))
    random.sample(output,1)
    index = random.sample(output,1)[0]
    return (probs[index],index)
