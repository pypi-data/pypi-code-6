#! /usr/bin/env python
"""
StochPyTools
============

Written by T.R. Maarleveld, Amsterdam, The Netherlands
E-mail: tmd200@users.sourceforge.net
Last Change: October 06, 2014
"""

import re,sys,copy
from stochpy import model_dir as stochpy_model_dir
from ..modules.PyscesMiniModel import PySCeS_Connector

try: 
    import numpy as np
    np.seterr(divide = 'ignore') # catch the divide by zero error if species start at zero
except ImportError:
    print("Make sure that the NumPy module is installed")
    print("This program does not work without NumPy")
    print("See http://numpy.scipy.org/ for more information about NumPy")
    sys.exit()


class Species():
    def __init__(self):
        """ Object that is created to store the species amounts """
        pass
    
__species__ = Species()

class StochPySSA_Shared(): 
    def Parse(self,File,dir,IsTauLeaping=False,IsNRM=False,IsDelayed = False,IsSMM = False):
        """
        Parses the PySCeS MDL input file, where the model is desribed
   
        Input:
        - *File* filename.psc
        - *dir*  /home/user/Stochpy/pscmodels/filename.psc
        """
        try:
            model_file = File
            model_dir = dir            
            self.parse = PySCeS_Connector(model_file,model_dir,IsTauLeaping = IsTauLeaping, IsNRM = IsNRM,IsDelayed = IsDelayed,IsSMM = IsSMM)	# Parse model          
            if self.parse.IsConverted:
                model_file += '.psc'
                model_dir = stochpy_model_dir
                
            self.N_matrix_transpose = copy.deepcopy(self.parse.N_matrix.transpose()) # June 5th 2012
            self.X_matrixinit = copy.deepcopy(self.parse.X_matrix.transpose()[0])        

            self.rate_names = copy.deepcopy(self.parse.Mod.__reactions__)  
            self.rate_pos = {r_id:j for j,r_id in enumerate(self.rate_names)} # Determine once for each rate it's position
            self.n_reactions = len(self.parse.Mod.__reactions__)
            self.n_species = len(self.parse.species)
            self.fixed_species = copy.deepcopy(self.parse.Mod.__fixed_species__)     
                   
            self.__aDict__ = copy.deepcopy(self.parse.Mod.__aDict__) # support of assignments
            self.__eDict__ = copy.deepcopy(self.parse.Mod.__eDict__) # support of events (with triggers)
            self.species_names = copy.deepcopy(self.parse.species)
            self.species_names += [species for species in list(self.__aDict__)]
            self.species_names += [species for species in self.fixed_species]
            self.species_pos = {s_id:i for i,s_id in enumerate(self.species_names)} # Determine once for each species (variable, assigned, fixed) it's position
            
            if IsDelayed or IsSMM:
                self.N_matrix_transpose_reactants = copy.copy(self.parse.N_matrix_reactants.transpose()) #24-10-2013
                self.N_matrix_transpose_products  = copy.copy(self.parse.N_matrix_products.transpose())  #24-10-2013 
                             
            if IsSMM:
                # If depends_on and reactants don't correspond, like in a net catalyzed reaction, then force consumption and production of the catalyst.
                # Result: update of the catalyst in the tau_arrays without showing in the N_matrix
                self.products = copy.deepcopy(self.parse.product_indices)        # 28-10-2013 #Indices  
                for j in range(self.n_reactions):
                    self.products[j].extend( list(set(self.parse.depends_on[j]) - set(self.parse.reactant_indices[j])) )          
        except Exception as er:          
            print(er)
            print("Error: StochPy failed parsing input file '{0:s}' from directory '{1:s}'".format(model_file, model_dir) )
            sys.exit()
            
    def SpeciesSelection(self,settings):
        """ Prepare output indices (if specific species are selected) """
        self.IsSpeciesSelection = False    
        if settings.species_selection:
            self.species_output_indices = [0]
            for s_id in settings.species_selection:
                self.species_output_indices.append(self.species_pos[s_id] + 1) # (time on first index)
            self.species_output_indices.append(-1)
            self.IsSpeciesSelection = True       
            
    def RateSelection(self,settings):
        """ Prepare output indices (if specific rates are selected) """
        self.IsRateSelection = False    
        if settings.rate_selection:
            self.rate_output_indices = [0]
            for r_id in settings.rate_selection:
                self.rate_output_indices.append(self.rate_pos[r_id] + 1) # (time on first index)            
            self.IsRateSelection = True

    def SetEvents(self):
        """ Initialize events """
        self.__events__ = copy.deepcopy(self.parse.Mod.__events__)  # deepcopy, very important! Augustus 21, 2014
        self._IsPerformEvent = False    
        for ev in self.__events__:            
            for s_id in sorted(self.species_names, reverse=True): # makes sure that the longest identifiers are replaced first                
                if s_id not in self.fixed_species:               
                    ev.code_string = ev.code_string.replace('self.mod.{0:s}'.format(s_id),'X_matrix[{0:d}]'.format(self.species_pos[s_id]) )
            ev.xcode = compile("self.state = {0:s}".format(ev.code_string),'event{0}'.format(ev),'exec')

    def Propensities(self,IsTauleaping=False):
        """
        Determines the propensities to fire for each reaction at the current time point. At t=0, all the rate equations are compiled.
        
        Input:
         - *IsTauleaping* (boolean) [default = False]
        """
        if self._IsInitial:                                                   # Compile rate-eqs
            code_str = self.volume_code + '\n'                                # 27-01-2014                      
            self.sim_a_mu = np.zeros([self.n_reactions])                      # Initialize a(mu)
            for i in range(self.n_reactions):
                code_str += "r_vec[{0:d}]={1}\n".format(i,self.parse.propensities[i])           
            self.req_eval_code = compile(code_str,"RateEqEvaluationCode","exec")             
            [setattr(__species__,self.parse.species[s],self.X_matrix[s]) for s in range(self.n_species)] # Set species quantities
            [setattr(__species__,self.fixed_species[s],self.fixed_species_amount[s]) for s in range(len(self.fixed_species))]
            self._IsInitial = False
        else:  
            if not IsTauleaping:        
                [setattr(__species__,self.parse.species[s],self.X_matrix[s]) for s in self.species_to_update]
            else:
                [setattr(__species__,self.parse.species[s],self.X_matrix[s]) for s in range(self.n_species)] # Set species quantities         
        
        self.rateFunc(self.req_eval_code,self.sim_a_mu)                       # Calc. Propensities             
        assert self.sim_a_mu.min() >= 0, "Error: Negative propensities are found. Make sure that your rate equations are defined correctly!"
        self.sim_a_mu = abs(self.sim_a_mu)
        self.sim_a_0 = self.sim_a_mu.sum()
    
    def HandleEvents(self,IsTauleapingStep=False):    
        """
        Event handling 
        
        We distuingish two types of events:
        1. time events where we reset the simulation time to the trigger time
        2. trigger events which can involve species copy numbers, ..., ..., and also time.         
        """
        for ev in self.__events__:            
            IsTrigger = ev(self.sim_t,self.X_matrix)            
            IsModify = False            
            if IsTrigger:
                if '_TIME_' in ev.symbols and len(ev.symbols) == 1: # pure time event
                    n = re.search("\d*\.\d+|\d+",ev.formula)                      
                    ev.reset()                    
                    self._IsTimeEvent = True          # 10-04-2014
                    if not ev(10**-99,self.X_matrix): #  _TIME_ > 3.0
                        self.sim_t = float(n.group(0))                             
                        self.__events__.remove(ev)
                        IsModify = True                                                                                 
                        
                        if np.isnan(self.reaction_index): # reaction_index = nan, ignore nothing happend (probably the end time is reached)
                           pass                     
                        elif not IsTauleapingStep:                             
                            self.X_matrix -= self.N_matrix_transpose[self.reaction_index]       # reset reaction
                        elif IsTauleapingStep:                        
                            self.X_matrix -= np.dot(self.parse.N_matrix,self.K_vector).ravel()  # reset reactions    
                    else:                             #  _TIME  < 3.0, these can fire as long as it's valid
                        IsModify = True
                        ev.reset()                    
                else:                                 # Trigger event
                     IsModify = True
                             
                if IsModify:    
                    for s_id in list(self.__eDict__[ev.name]['assignments']):                    
                        if s_id not in self.fixed_species:
                            s_index = self.species_pos[s_id]
                            self.X_matrix[s_index] = float(int(self.__eDict__[ev.name]['assignments'][s_id]))                         
                        else:               
                           s_index = self.fixed_species.index(s_id)
                           self.fixed_species_amount[s_index] = float(int(self.__eDict__[ev.name]['assignments'][s_id]))
                           setattr(__species__,s_id, self.fixed_species_amount[s_index])

                    self._IsPerformEvent = True 
                    self.reaction_index = np.nan
                            
    def AssignmentRules(self):
        """ 
        Builds the assignment rules # updated version 06/08/14
        
        http://sbml.org/Software/libSBML/docs/java-api/org/sbml/libsbml/AssignmentRule.html        
        """ 
        code_string = """"""
        if self.sim_t == 0:
            self.assignment_labels = list(self.__aDict__)
            self.assignment_species = np.zeros(len(self.__aDict__))
            self._assignment_rules = [] # indices of species matrix species used for assignments
            for s_id in self.parse.species:
                for assign_species in list(self.__aDict__):
                    if s_id in self.__aDict__[assign_species]['formula']: # if 'normal' species in assignment relationship
                        index = self.species_pos[s_id]
                        if index not in self._assignment_rules:
                            self._assignment_rules.append(index)

        for index in self._assignment_rules:
            species_value = self.X_matrix[index]
            code_string += "{0:s}={1}\n".format(self.parse.species[index],species_value)                    
         
        for i,species in enumerate(self.__aDict__):
            code_string += "self.assignment_species[{0:d}]={1}\n".format(i,self.__aDict__[species]['formula'])
        #print(code_string)
        self.rateFunc(code_string,self.assignment_species)

    def rateFunc(self,rate_eval_code,r_vec):
        """
        Calculate propensities from the compiled rate equations
       
        Input:
         - *rate_eval_code* compiled rate equations
         - *r_vec* output for the calculated propensities
        """
        try:        
            exec(rate_eval_code)     
        except Exception as er:
            print(er)
            print("Error: Propensities cannot be determined. Please check if all variable species amounts are initialized")
            sys.exit()            
            
    def Initial_Conditions(self,IsTauleaping = False):              
        """ This function initiates the output format with the initial concentrations """
        self.sim_output = []
        if self.IsTrackPropensities:
            self.propensities_output = []            
            output_init = self.sim_a_mu.tolist()
            output_init.insert(0,self.sim_t)
            if self.IsRateSelection:
                output_init = [output_init[j] for j in self.rate_output_indices]
            self.propensities_output.append(output_init)         

        output_init = [self.sim_t]
        for init in self.X_matrix: # Output at t = 0 
            assert init >= 0, "Error: StochPy detected (initial) negative species amounts."    
            output_init.append(int(init))
            
        if self.__aDict__ != {}:
            self.AssignmentRules()  
            output_init += [value for value in self.assignment_species]
        
        for amount in self.fixed_species_amount:
            output_init.append(amount)            
        
        if not IsTauleaping:  
            output_init.append(np.NAN)
        
        if self.IsSpeciesSelection:
            output_init = [output_init[i] for i in self.species_output_indices]
        self.sim_output.append(output_init)
        
    def GenerateOutput(self,IsTauleaping = False,completion_delayed = False):
        """
        Add data of current state (species copy numbers, volume and propensities) to the output.
        
        Input:
         - *IsTauleaping* (boolean) [default = False]
         - *completion_delayed* (boolean) [default = False]
         
        Different output is generated for the tauleaping method and if there are completion delays        
        """        
        if completion_delayed:
            r_index = - (self.reaction_index + 1)                              # Completion reaction = - reaction index
        if not completion_delayed and not IsTauleaping:
            r_index = self.reaction_index + 1                                  # Initiation reaction = reaction index        
        
        timestep_output = self.X_matrix.tolist()         
        timestep_output += [amount for amount in self.fixed_species_amount]                
        if self.__aDict__ != {}:
            self.AssignmentRules()
            timestep_output += [value for value in self.assignment_species]                   
        timestep_output.insert(0,self.sim_t)
        if not IsTauleaping:
            if not self._IsPerformEvent:
                timestep_output.append(r_index)
            else: 
                timestep_output.append(np.nan)            
        self._IsPerformEvent = False
        if self.IsSpeciesSelection:    
            return [timestep_output[i] for i in self.species_output_indices]
        else:
            return timestep_output
