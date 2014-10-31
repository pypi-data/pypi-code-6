 #! /usr/bin/env python
"""
StochPy Cell Division Module
============================

Example of a sequential simulator. This simulator tracks one cell for N generations. 

Most of the functionalities of the SSA module such as plotting and writing to a file are also available in this module.

Written by T.R. Maarleveld and M. Moinat, Amsterdam, The Netherlands
E-mail: tmd200@users.sourceforge.net
Last Change: October 31, 2014
"""
from __future__ import division, print_function, absolute_import

############################## IMPORTS ###################################
import os,sys,copy,time,random

try:
    import pickle
except ImportError:
    import Cpickle as pickle

try: import numpy as np
except:
    print("Make sure that the NumPy module is installed")
    print("This program does not work without NumPy")
    print("See http://numpy.scipy.org/ for more information about NumPy")
    sys.exit()

from . import Analysis
from . import StochSim
from .PyscesMiniModel import RegularGridDataObj
from .PyscesMiniModel import IntegrationStochasticDataObj

from ..tools.Progress_bar import Progress_bar
from ..tools.ParseDistributions import ParseDistributions,convertInput2IndicesAndValues,MakeDistributionFunction
from ..tools.CDTool_kSolver import k_solver
from ..tools.CDTool_ExtrapolateExtant import ExtrapolateExtant

class RegularGridDataObj(RegularGridDataObj):
    HAS_AVERAGE_SPECIES_EXTANT_DISTRIBUTIONS = False    
    
    def setSpeciesExtantDistributionAverage(self,mean,std):
        """
        Set means and stds of species data
        
        Input:
         - *mean* (list)
         - *std* (list)
        """
        self.species_extant_distributions_means = mean
        self.species_extant_distributions_standard_deviations = std
        self.HAS_AVERAGE_SPECIES_EXTANT_DISTRIBUTIONS = True   

class CellDivision():
    """
    Input options:     
     - *File*  [default = CellDivision.psc]
     - *dir*   [default = /home/user/stochpy/pscmodels/ImmigrationDeath.psc]     
     
    Usage (with High-level functions):
    >>> cmod = stochpy.CellDivision()
    >>> help(cmod)
    >>> cmod.DoCellDivisionStochSim()
    >>> cmod.DoCellDivisionStochSim(self,end = 5, mode= 'generations',IsTrackPropensities=False)
    >>> cmod.Model(File = 'filename.psc', dir = '/.../')
    >>> smod.Reload()
    >>> cmod.AnalyzeExtantCells()
    >>> cmod.PlotInterdivisionTimeDistribution()
    >>> cmod.PlotCellAgeDistribution()
    >>> cmod.PlotSpeciesTimeSeries()
    >>> cmod.PlotPropensitiesTimeSeries()
    >>> cmod.PlotAveragedSpeciesTimeSeries()
    >>> cmod.PlotWaitingtimeDistributions()
    >>> cmod.PlotSpeciesDistributions(bin_size = 3)
    >>> cmod.PrintSpeciesMeans()
    >>> cmod.PrintSpeciesDeviations()
    >>> cmod.ShowOverview()  
    >>> cmod.ShowSpecies()
    """
    def __init__(self,Method='Direct',File = 'CellDivision.psc',dir = None,sim_mode = 'generations',end=3,IsInteractive=True):
        print("Welcome to the Cell Division simulation module")        
        if os.sys.platform != 'win32':
            output_dir = os.path.join(os.path.expanduser('~'),'Stochpy',)
            temp_dir = os.path.join(os.path.expanduser('~'),'Stochpy','temp',)
            if dir == None:
                dir = os.path.join(os.path.expanduser('~'),'Stochpy','pscmodels')
        else:
            output_dir = os.path.join(os.getenv('HOMEDRIVE')+os.path.sep,'Stochpy',)
            temp_dir = os.path.join(os.getenv('HOMEDRIVE')+os.path.sep,'Stochpy','temp',)
            if dir == None:
                dir = os.path.join(os.getenv('HOMEDRIVE')+os.path.sep,'Stochpy','pscmodels')

        self.output_dir = output_dir
        self.model_dir = dir       
        self.temp_dir = temp_dir
        self.StochSim = StochSim.SSA(Method,File,dir,Mode = 'steps',IsTrackPropensities=False)        
        self.StochSim._IsCellDivision=True
        self.sim_mode = sim_mode.lower()
        self.sim_steps = 10**50
        self.sim_time  = 10**50
        if self.sim_mode == 'generations':
             self.sim_generations = end
        elif self.sim_mode == 'time':
             self.sim_time = end
        elif self.sim_mode == 'steps':
             self.sim_steps = end
        else: 
             self.sim_generations = 3
             
        self._IsBetaDistribution = False
        self._IsAnalyzedExtant = False
        self._IsModeSetByUser = False
        self._IsEndSetByUser = False
        if IsInteractive:
          try: 
              Analysis.plt.ion()    # Set on interactive pylab environment
          except Exception as er:
              print(er)
        else:
          try: 
              Analysis.plt.ioff()   # Set on interactive pylab environment
          except Exception as er:
              print(er)             
        
        self.HasCellDivisionParameters = np.zeros(5)    # Collects of each setting whether it has been set.
        self.SetDefaultParameters()

    def Method(self, method):
        """
        Set stochastic simulation algorithm to be used.
        
        Input:
         - *method* (string)
        """
        self.StochSim.Method(method)
        self.data_stochsim = None
        self.data_stochsim_grid = None
        self.data_stochsim_celldivision = None

    def Timesteps(self,s):
        """
        Timesteps(s)
        
        Set the number of time steps to be generated for each trajectory
        
        Input:
         - *s* (integer)
        """      
        try:
            self.sim_steps = abs(int(s))            
            self.sim_generations = 10**50
            self.sim_time = 10**50
            self.sim_mode = 'steps'
            print("Info: The number of time steps is: {0:d}".format(self.sim_steps) )
            self._IsEndSetByUser = True
            self._IsModeSetByUser = True
        except ValueError:
            raise ValueError("The number of time steps must be an integer")

    def Endtime(self,t):
        """
        Endtime(t)
        
        Set the end time of the exact realization of the Markov jump process
        
        Input:
         - *t* (float)
        """    
        try:
            self.sim_time = abs(float(t))
            self.sim_generations = 10**50
            self.sim_steps = 10**50            
            self.sim_mode = 'time'            
            print("Info: The simulation end time is: {0:f}".format(self.sim_time) )
            self._IsEndSetByUser = True
            self._IsModeSetByUser = True
        except ValueError:
            raise ValueError("The end time must be an integer or a float")           
        
    def Generations(self,g):
        """
        Endtime(t)
        
        Set the end time of the exact realization of the Markov jump process
        
        Input:
         - *t* (float)
        """
        try:
            self.sim_generations = int(abs(float(g)))
            self.sim_steps = 10**50
            self.sim_time = 10**50            
            self.sim_mode = 'generations'
            print("Info: The numbers of generations is set to: {0:d}".format(self.sim_generations) )
            self._IsEndSetByUser = True
            self._IsModeSetByUser = True
        except ValueError:
            raise ValueError("The end time must be an integer or a float")
    
    def Mode(self,sim_mode='generations'):
        """
        Set mode for a stochastic simulation.
        
        Input:
         - *sim_mode* [default = 'generations'] (string) 'time','steps', 'generations'
        """
        self.sim_mode = sim_mode.lower()        
        if self.sim_mode not in ['generations','steps','time']:
            print("*** WARNING ***: Mode '{0}' not recognized using: 'generations', thus 3 generations will be modeled".format(sim_mode) )
            self.sim_mode = 'generations'
            self.sim_generations = 3
            self.sim_steps = 10**50
            self.sim_time = 10**50        
        self._IsModeSetByUser = True             
    
    def Trajectories(self,n):
        """
        Set the number of trajectories to be generated
              
        Input:
         - *n* (int)
        """
        self.StochSim.Trajectories(n)
    
    def Model(self,File,dir = None,IsSetDefault=True): 
        """
        Give the model, which is used to do stochastic simulations on

        Input:
         - *File* filename.psc (string)
         - *dir* [default = None] the directory where File lives (string)
         - *IsSetDefault* [default = True]
        """   
        self.StochSim.Model(File,dir)
        self.HasCellDivisionParameters = np.zeros(5)
        if IsSetDefault:
            self.SetDefaultParameters()
            print('Please mind that the Cell Division parameters are reset to the default settings.')
        
    def ChangeParameter(self, parameter, value):
        """
        ChangeParameter(parameter,value)  
        
        Change parameter value   
        
        Input:
         - *parameter* (string)
         - *value* (float)
        """
        self.StochSim.ChangeParameter(parameter, value)
        #Reset volume dependencies of propensity formula
        self.SetVolumeDependencies(self._IsVolumeDependent, self._VolumeDependencies, self._SpeciesExtracellular)
        
    def ChangeInitialSpeciesAmount(self, species, value):
        """
        ChangeInitialSpeciesAmount(species,value)     
        
        Change initial species Amount
        
        Input:
         - *species* (string)
         - *value* (float)
        """
        self.StochSim.ChangeInitialSpeciesAmount(species, value)        
        self.SetVolumeDependencies(self._IsVolumeDependent, self._VolumeDependencies, self._SpeciesExtracellular)  #Reset volume dependencies of propensity formula
        
    def GetTrajectoryData(self,n=1):
        """ 
        Switch to another trajectory, by default, the last trajectory is accesible      
       
        Input:
         - *n* [default = 1] (int)
        """ 
        self.StochSim.GetTrajectoryData(n) 
        self.data_stochsim = copy.copy(self.StochSim.data_stochsim)
        try:      
            file_in = open(os.path.join(self.temp_dir,'{0}{1:d}_CD.dat'.format(self.StochSim.model_file,n)),'rb')
            self.data_stochsim_celldivision = pickle.load(file_in)
            file_in.close()
        except IOError:
            raise IOError("Trajectory {0:d} does not exist".format(n))                          
    
    def DumpTrajectoryData(self,n):
        """ 
        DumpTrajectoryData(n)
        
        Input:
         - *n* (integer)
        """ 
        self.StochSim.DumpTrajectoryData(n)        
        if n == self.data_stochsim_celldivision.simulation_trajectory:       
            filename_out = os.path.join(self.temp_dir,'{0}{1:d}_CD.dat'.format(self.StochSim.model_file,n))          
            f = open(filename_out,'wb')            
            pickle.dump(self.data_stochsim_celldivision,f)   
            f.close()
        else:
            print("Error: Trajectory {0} is currently not selected/ does not exist".format(n))
            
    def SetSeeding(self,UseSeed=True):
         """ Set Seeding """
         self.StochSim.SetSeeding(UseSeed)
    
    def SetDelayParameters(self, delay_distributions, nonconsuming_reactions = None):
        """
        Input delayed model parameters. This function subsequently parses the delay input and assigns it to the SSA method. 
        
        Example: 
        SetDelayParameters(delay_distributions = {'R1':('fixed',3), 'R2':('gamma',5,1)}, nonconsuming_reactions = ['R2'])
          - Reaction 'R1' will get a delay of 3 seconds and reaction 'R2' a random delay from a gamma distr with shape=5 and scale=1.
          - Reaction 'R1' will be a consuming reaction, and 'R2' a nonconsuming reaction.
        
        Inputs:
          - *delay_distributions* (dictionary)
              * Dictionary of reaction name (or index) as key and distribution as value.
          - *nonconsuming_reactions* (list) [default = None]
              * Reaction names or indices of the given delayed reactions that are nonconsuming (subset of reactions given in *delay_distributions*. 
                All other delayed reactions given in *delay_distributions* are considered consuming.
                Consuming and nonconsuming reactions are defined according to Xiaodong Cai (2007), "Exact stochastic simulation of coupled chemical reactions with delays", J.Phys. Chem. 126:124108.

          Value of *delay_distributions* can be any distribution of numpy.random, e.g.:
          - ('gamma', p1,p2) = np.random.gamma(p1,p2) #Where p1 is the shape parameter and p2 the scale parameter.
          - ('exponential', p1) = np.random.exponential(p1) #Where p1 is the scale parameter (NOT the rate).
          - ('uniform', lower, upper) = np.random.uniform(0,lower,upper)        
        """
        self.StochSim.SetDelayParameters(delay_distributions, nonconsuming_reactions)
    
    def SetPutativeReactionTimes(self, distributions): 
        """
        Sets the single molecule putative reaction times distribution.
        
        Inputs:
          - *distributions* (dictionary)
              * Dictionary of reaction name (or index) as key and distribution as value.
          
          Value of *distributions* can be any distribution of numpy.random, e.g.:
          - ('gamma', p1,p2) = np.random.gamma(p1,p2) #Where p1 is the shape parameter and p2 the scale parameter.
          - ('exponential', p1) = np.random.exponential(p1) #Where p1 is the scale parameter (NOT the rate).
          - ('uniform', lower, upper) = np.random.uniform(0,lower,upper)
        """   
        self.StochSim.SetPutativeReactionTimes(distributions)
        self._IsManualReactionTime = np.zeros(self.StochSim.SSA.n_reactions)
        for i in list(self.StochSim.putative_reaction_times):
            self._IsManualReactionTime[i] = 1
       
    def Reload(self):
        """ Reload the entire model again. Useful if the model file has changed"""
        self.StochSim.Reload()
        self.data_stochsim = None
        self.data_stochsim_grid = None
        self.data_stochsim_celldivision = None

    def SetDefaultParameters(self):
        """
        Set default parameters: growth rate, growth type, initial volume, and volume distributions        
              
        With default phi_beta_mean (2) this gives a symmetrical narrow distribution around 2 on [1.5-2.5].
        Beta Distributions make sure that distributions of daughter and mother cell volumes do not overlap
        """
        self.SetGrowthFunction(1.0, 'exponential')
        self.SetInitialVolume(1.0)               
        self.SetVolumeDistributions( ('beta',5,5), ('beta',2,2), 2)
                       
        self.SetVolumeDependencies(True)        
        self.SetExactDividingSpecies([])
        self.SetNonDividingSpecies([])
        
    def SetGrowthFunction(self, growth_rate, growth_type = 'exponential'):
        """
        Input:
         - *growth_rate* (float)
         - *growth_type* (string) [default = 'exponential', alternative = 'linear']
        """
        try:
            self.sim_growth_rate = float(growth_rate)          
        except ValueError:
            raise ValueError("The growth rate must be an integer or a float")
            
        if growth_type.lower() == 'exponential':
            self.Vt_codestring = "self._current_volume = {0:f} * np.exp( {1:f}*( self.sim_t - {2:f} ) )" # needs V0, growth rate, t_division
            self.IDT_func = lambda v_start, v_end: np.log(v_end/v_start)/self.sim_growth_rate            
            self.sim_growth_type = 'exponential'
        elif growth_type.lower() == 'linear':
            self.Vt_codestring = "self._current_volume = {0:f} + {1:f} *( self.sim_t - {2:f} )" # needs V0, growth rate, t_division
            self.IDT_func = lambda v_start, v_end: (v_end - v_start)/self.sim_growth_rate
            self.sim_growth_type = 'linear'
        else:
            raise Warning("Growth type '{0}' not recognized, use 'exponential' or 'linear'.".format(growth_type) )
        
        print( "Info: The {0} growth rate is: {1}".format(self.sim_growth_type, self.sim_growth_rate) )
        self.HasCellDivisionParameters[0] = 1        
    
    def SetInitialVolume(self, initial_volume):
        """
        Set initial volume
        
        Input:
         - initial_volume (float)         
        """
        try:
            self.sim_initial_volume = abs(float(initial_volume))
            self.HasCellDivisionParameters[1] = 1
        except ValueError:
            raise ValueError("The initial volume must be a positive integer or float")
        
    def SetVolumeDistributions(self, phi, K, phi_beta_mean = False):
        """
        Input:
         - *phi* (list) Specifies the distribution of the cell volume at which the mother cell divides.
         - *K* (list) The number from this distribution is multiplied with the mother cell volume to get volume of daughter 1.          
                      Vdaughter = Vmother * K
                      Note: This distribution needs to have a symmetrical distribution with a mean of 0.5, otherwise one will create a bias for one daughter
         - *phi_beta_mean* (float) only if phi is a beta distribution, then it is added to the random number from *phi_distr*
              
        The *phi* and *K* distributions can be any distribution of numpy.random, e.g.:
         - ('gamma', p1,p2) = np.random.gamma(p1,p2) #Where p1 is the shape parameter and p2 the scale parameter.
         - ('exponential', p1) = np.random.exponential(p1) #Where p1 is the scale parameter (NOT the rate).
         - ('uniform', lower, upper) = np.random.uniform(0,lower,upper)
         Fixed values for *phi* and *K* are also possible, e.g.:
         - phi = ('fixed', 2) and K = ('fixed',0.5) creates a lineage with cells that grow from a volume of 1 to 2.
        """               
        # Save settings for k solver
        self._phi_tuple = phi
        self._K_tuple = K              
        if phi[0].lower() == 'beta' and K[0].lower() == 'beta':            
            assert phi_beta_mean != False, "Beta distribution requires setting the *phi_beta_mean* argument"            
            assert phi_beta_mean  > 1.0, "The specified *phi_beta_mean* must be at least 1.0."
            self.phi_shift = phi_beta_mean - 0.5
            self.phi_distribution = lambda x,y: np.random.__dict__['beta'](x,y) + self.phi_shift
            self.phi_parameters = phi[1::] 
            self.K_distribution =  lambda x,y: (np.random.__dict__['beta'](x,y) * (self.phi_shift-1) + 1)/(self.phi_shift+1) # When all default on [0.4 - 0.6]
            self.K_parameters = K[1::]            
            self._IsBetaDistribution = True
        else:            
            if phi[0].lower() == 'beta':
                print("K is not both beta distributed, the specific growth rate will not be calculated.")
                self.phi_shift = phi_beta_mean - 0.5
                self.phi_distribution = lambda x,y: np.random.__dict__['beta'](x,y) + self.phi_shift
                self.phi_parameters = phi[1::]   
            else:
                print("Phi and K are not beta distributed, the specific growth rate will not be calculated.")
                self.phi_distribution, self.phi_parameters = MakeDistributionFunction(phi)
            self.K_distribution, self.K_parameters = MakeDistributionFunction(K)
            self._IsBetaDistribution = False           
            
        self.HasCellDivisionParameters[2] = 1
        
    def SetVolumeDependencies(self, IsVolumeDependent, VolumeDependencies = [], SpeciesExtracellular = []):
        """ 
        Set volume dependency of reactions. 
        
        Input:
         - *IsVolumeDependent* (boolean)
         - *VolumeDependencies* (list or True) User specified which reaction are volume dependent and with which order 
              = Approximation for fast reactions, because volume only updated after a reaction has fired.
              - If not specified, the algorithm will try to determine the volume dependency, depending on the order of the reaction:
                  - Order = number of reactants minus the extracellular species among those reactants (the latter are not affected by cell volume)
              - If only reaction name is specified, it by default assumes second order reactions (propensity/V)
              e.g.:
                - ['R2',R3'] --> Reactions R2 and R3 are second order reactions
                - [('R2',4), ('R3',3)] --> R2 is fourth order (propensity/V**3) and R3 is third order (propensity/V**2)
                   
         - *SpeciesExtracellular* (list of str) Species that are not inside the cell and should therefore not be divided upon cell division 
        """        
        assert isinstance(IsVolumeDependent, bool), "IsVolumeDependent argument must be a boolean (True/False)"
        # Save settings for reset of dependencies at .ChangeInitialSpeciesAmount and .ChangeParameter
        self._IsVolumeDependent    = IsVolumeDependent
        self._VolumeDependencies   = VolumeDependencies
        self._SpeciesExtracellular = SpeciesExtracellular
        
        if IsVolumeDependent:
            if isinstance(SpeciesExtracellular,str): 
                SpeciesExtracellular = [SpeciesExtracellular]
            try:
                self._species_extracellular_indices = [self.StochSim.SSA.species_names.index(x) for x in SpeciesExtracellular]
                self._species_extracellular = [x for x in SpeciesExtracellular]
            except ValueError:
                raise Warning("{0} is not a species name. Try one of: {1}".format(x, self.StochSim.SSA.species_names) )
                
            volume_propensities = self._BuildPropVolumeDependencies(VolumeDependencies, SpeciesExtracellular)
            if self.StochSim._IsNRM: 
                # Rebuild propensity codes
                self.StochSim.SSA.parse.BuildPropensityCodes( volume_propensities ) 
                self.StochSim.SSA.propensity_codes = self.StochSim.SSA.parse.propensity_codes
            else: 
                self.StochSim.SSA.propensities = volume_propensities
            
            self._IsPropensitiesVolumeDependent = True           
            
        else:
            self.Reload() # This resets propensities, but it should not remove all other settings!
            print("Info: your model is reloaded and therefore the propensities are reset.")
            self._IsPropensitiesVolumeDependent = False
        self.HasCellDivisionParameters[3] = 1
        
    def SetExactDividingSpecies(self, species):
        """
        Set species (as list of names) that are volume dependent, but divide equally (after replication).
        
        Input:
         - *species* (list)
        """
        if isinstance(species,str): 
            species = [species]
        assert isinstance(species,list), "Argument *species* must be a string or a list of strings"
        try:
            self.exact_species_indices = [self.StochSim.SSA.species_names.index(x) for x in species]
        except ValueError:
            raise Warning("{0} is not a species name. Try one of: {1}".format(x, self.StochSim.SSA.species_names) ) 
        
        self.HasCellDivisionParameters[4] = 1   
    
    def SetNonDividingSpecies(self, species):    
        """
        Set species (as list of names) that are volume dependent, but do not divide.
        
        Input:
         - *species* (list)
        """
        if isinstance(species,str): 
            species = [species]
        assert isinstance(species,list), "Argument *species* must be a string or a list of strings"    
        try:
            self.non_dividing_species_indices = [self.StochSim.SSA.species_names.index(x) for x in species]
        except ValueError:
            raise Warning("{0} is not a species name. Try one of: {1}".format(x, self.StochSim.SSA.species_names) )
    
    def _BuildPropVolumeDependencies(self, reactions_order, extracellular_species):
        """
        Returns propensity formulas with volume dependency inserted.
        Either using user specified orders or by determining the order from number of reactants.
        
        Input: 
         - *reactions_order* Dictionary or list of tuples with reaction name and the order. e.g. {'R1':2}. If no order is specified, it will be 2.
         - *extracellular_species* Species not affected by cell volume
        """
        self._HasVolumeDependencies = np.zeros( self.StochSim.SSA.n_reactions )
        propensities = copy.deepcopy(self.StochSim.SSA.parse.propensities) #Load initial propensities from the parse
        if reactions_order:
            print(reactions_order)
            indices_order = convertInput2IndicesAndValues(reactions_order, self.StochSim.SSA.rate_names, default_value = 2)
            for reaction_index, order in indices_order:
                if order >= 2:
                    #Add volume dependency according to /V**(order-1)
                    propensities[reaction_index] = '({0})/self._current_volume**({1})'.format(propensities[reaction_index], order-1)          
                    self._HasVolumeDependencies[reaction_index] = 1
        
        else: #Adds the divide by V according to the number of reactants (=order of the reaction)            
            for i,r_id in enumerate(self.StochSim.SSA.rate_names):
                allreagents = self.StochSim.SSA.parse.Mod.__nDict__[r_id]['AllReagents']  # 26-09-2014
                reactants = [x for x in allreagents if x[1] < 0]  #filter(lambda x: x[1] < 0, allreagents) Python 3.x
                n_reactants = sum([abs(sp[1]) for sp in reactants])

                #Remove the number of extracellular ligands in reactants:
                order = n_reactants - len( set.intersection(set(reactants), set(extracellular_species)) ) #Number of overlapping species of reactants and extracellular
                if order >= 2: # No or one reactants, so propensity is not volume dependent (and don't change it)
                    #Add volume dependency according to /V**(order-1)                    
                    propensities[i] = '({0})/self._current_volume**({1})'.format(propensities[i], order-1)
                    self._HasVolumeDependencies[i] = 1
            print("Info: The volume dependency is automatically implemented, but note that extracellular species have to be set specifically")
        return propensities   

    def DoCellDivisionStochSim(self, mode = False, end = False, method = False, trajectories = False, IsTrackPropensities = False, species_selection = None, rate_selection = None, IsOnlyLastTimepoint = False):
        """ 
        Do stochastic simulations with cell growth and cell divisions.
        
        Input:
         - *mode* (str)
            - 'generations' [default]
            - 'time'
            - 'steps'
         - *end* (int) [default = None]
            - Number of generations (default = 3) or steps to take (default = 1000).
         - *method* (str) [default = False]
         - *trajectories* (int) [default = 1]
         - *IsTrackPropensities* (boolean)
         - *rate_selection* [default = None] List of names of rates to store. This saves memory space and prevents Memory Errors when propensities propensities are tracked
         - *species_selection* [default = None] List of names of species to store. This saves memory space and prevents Memory Errors (occurring at ~15 species).    
         - *IsOnlyLastTimepoint* [default = False]         
        """        
        if not self.HasCellDivisionParameters.all():
            raise AttributeError("Not all Cell Division Parameters were set.")
        
        if species_selection and isinstance(species_selection,str):   
            species_selection = [species_selection]
        if species_selection and isinstance(species_selection,list): 
            for s_id in species_selection:
                assert s_id in self.StochSim.SSA.species_names, "Species {0} is not in the model or earlier specified species selection".format(s_id)

        self.StochSim.IsTrackPropensities = IsTrackPropensities       
        if rate_selection and isinstance(rate_selection,str):   
            rate_selection = [rate_selection]
            self.StochSim.IsTrackPropensities = True
        if rate_selection and isinstance(rate_selection,list): 
            for r_id in rate_selection:
                assert r_id in self.StochSim.SSA.rate_names, "Reaction {0} is not in the model or earlier specified reaction selection".format(r_id)
            self.StochSim.IsTrackPropensities = True
      
        if mode != False:
            self.Mode(sim_mode = mode)             
            self._IsModeSetByUser = False
        elif mode == False and self.sim_mode != 'generations' and not self._IsModeSetByUser:
            self.Mode('generations')
            
        if end != False:            
            if self.sim_mode == 'generations':
                self.Generations(end)
                self._IsEndSetByUser = False
            elif self.sim_mode == 'steps':
                self.Timesteps(end)
                self._IsEndSetByUser = False 
            elif self.sim_mode == 'time':
                self.Endtime(end)
                self._IsEndSetByUser = False
            self._IsModeSetByUser = False    
        elif end == False and self.sim_generations != 3 and not self._IsEndSetByUser:
            self.Generations(3)
         
        if method != False: 
            self.StochSim.Method(method)
            self.StochSim._MethodSetBy = "DoStochSim"
        elif method == False and self.StochSim.sim_method_name != "Direct" and self.StochSim._MethodSetBy == "DoStochSim":
            self.StochSim.Method("Direct")
 
        if trajectories != False: 
            self.StochSim.Trajectories(trajectories)
            self.StochSim._IsTrajectoriesSetByUser = False
        elif trajectories == False and self.StochSim.sim_trajectories != 1 and not self.StochSim._IsTrajectoriesSetByUser:
            self.StochSim.Trajectories(1)           
         
        if self.StochSim.IsTrackPropensities and self.StochSim.sim_method_name in ['FastSingleMoleculeMethod','SingleMoleculeMethod']:
            print("*** WARNING ***: Propensities cannot be tracked with the single molecule method")
            self.StochSim.IsTrackPropensities = False
                   
        self.StochSim._IsFixedIntervalMethod = False        
        self.StochSim.HAS_AVERAGE = False   
        self._IsAnalyzedExtant = False
         
        self.data_stochsim = IntegrationStochasticDataObj()
        self.data_stochsim_grid = RegularGridDataObj()     
        self.data_stochsim_celldivision = IntegrationStochasticCellDivisionObj()                          
        self.StochSim.DeleteTempfiles()  # Delete '.dat' files        
        self.StochSim.data_stochsim_grid = RegularGridDataObj()            
        if self.StochSim.sim_trajectories == 1: 
            print("Info: 1 trajectory is generated")
        else:            
            print("Info: {0:d} trajectories are generated".format(self.StochSim.sim_trajectories) )
            print("Info: Time simulation output of the trajectories is stored at {0:s} in directory: {1:s}".format(self.StochSim.model_file[:-4]+'(traj).dat',self.StochSim.temp_dir) )
         
        self.CalculateSpecificGrowthRate(IsDebug = False) # generates self.sim_specific_growth_rate
               
        # Delayed Method
        if self.StochSim._IsDelayedMethod and self.StochSim.HAS_DELAY_PARAMETERS:
            # Pass delay parameters to delayed SSA implementation.
            self.StochSim.SSA.distr_functions        = copy.copy(self.StochSim.delay_distributions)
            self.StochSim.SSA.distr_parameters       = copy.copy(self.StochSim.delay_distr_parameters)
            self.StochSim.SSA.reactions_Consuming    = copy.copy(self.StochSim.delayed_consuming)
            self.StochSim.SSA.reactions_NonConsuming = copy.copy(self.StochSim.delayed_nonconsuming)
        elif self.StochSim._IsDelayedMethod: # No delay parameters set.
            raise AttributeError("No delay parameters have been set for the model '{0:s}'. Please first use the function .SetDelayParameters().".format(self.StochSim.model_file) ) #7-1-2014 exit if no delay parameters            
        
        # Single Molecule Method
        if self.StochSim._IsSingleMoleculeMethod: 
            if not self.StochSim.HAS_PUTATIVE_REACTION_TIMES:
                raise Warning("No distributions have been set for the model '{0:s}'. Please first use the function .SetPutativeReactionTimes().".format(self.StochSim.model_file) ) #7-1-2014 exit if no delay parameters
                 
            if self.StochSim.sim_method_name == "FastSingleMoleculeMethod" and 2 in [self.StochSim.SSA.order[j] for j in list(self.StochSim.putative_reaction_times)]:
                print("Info: Second order is not supported by the fast Single Molecule Method. Switching to the full Single Molecule Method.")
                self.StochSim.Method('SingleMoleculeMethod')
            
            voldep_And_manualfiringtime = self._HasVolumeDependencies * self._IsManualReactionTime
            if voldep_And_manualfiringtime.any():
                raise Warning("Non-exponential putative firing times in the Single Molecule Method cannot be volume dependent ({0}).\nChange the volume dependency with .SetVolumeDependencies().".format([self.StochSim.SSA.rate_names[i] for i in range(self.StochSim.SSA.n_reactions) if voldep_And_manualfiringtime[i] >= 1]) )
                
            # Pass delay parameters to Single Molecule SSA implementation.
            self.StochSim.SSA.distr_functions  = copy.copy(self.StochSim.putative_reaction_times)
            self.StochSim.SSA.distr_parameters = copy.copy(self.StochSim.putative_reaction_times_distr_parameters)                    

            #If Single Molecule Method, set exponential distributions to reactions not specified in StochSim.putative_reaction_times
            if self.StochSim.sim_method_name == 'SingleMoleculeMethod':
                self.StochSim.SSA.auto_exponential_reactions = []                
                for j in range(self.StochSim.SSA.n_reactions):
                    if j not in self.StochSim.SSA.distr_functions:                       # Don't replace already assigned distributions.
                        self.StochSim.SSA.distr_functions[j] = np.random.exponential
                        self.StochSim.SSA.distr_parameters[j] = np.nan                   # 31-03-2014 To be specified at start of simulation (self.SSA.EvaluatePropensities)
                        self.StochSim.SSA.auto_exponential_reactions.append(j)           # 31-03-2014                                                 
            
        progressBar = Progress_bar(cycles_total = self.StochSim.sim_trajectories, done_msg = 'time')
        for self.StochSim._current_trajectory in range(1,self.StochSim.sim_trajectories+1):            
            
            self.StochSim.settings = StochSim.SSASettings(X_matrix = self.StochSim.SSA.X_matrixinit,timesteps = self.sim_steps,starttime = 0,endtime = 0,istrackpropensities = self.StochSim.IsTrackPropensities, speciesselection=species_selection, rateselection = rate_selection, isonlylasttimepoint=IsOnlyLastTimepoint,useseed=self.StochSim._UseSeed)                           
            if self.StochSim._UseSeed:                # necessary to get correct seeding of each generation
                np.random.seed(5)
          
            self._volume_mother = []
            self._volume_daughter = []          
            self._volume_daughter_notselected = []    # The daughter that is not chosen
            self._species_mother = []
            self._species_daughter= []   
            self._interdivision_times = []                           
            self._generation_timesteps = []
            self._ages = []                           # For every time step the age of the generation.          
                                    
            # Generate first mother cell volume at division.
            self._next_end_volume = self.phi_distribution(*self.phi_parameters)        
            
            assert self._next_end_volume >= self.sim_initial_volume, "The initial volume ({0}) is larger than the drawn mother volume. Please choose a smaller initial volume.".format( self.sim_initial_volume)
            
            #Run generations       
            self.StochSim.SSA.timestep = 1   
            self._current_generation = 0 
            self._next_start_volume = self.sim_initial_volume
            while self._current_generation < self.sim_generations:
                self._current_generation += 1
                #0 The Division volume of current cell is already generated at division.
                self._current_start_volume = self._next_start_volume
                self._current_end_volume = self._next_end_volume
                
                #1.1 Calculate Interdivision Time
                self._current_IDT = self.IDT_func(self._current_start_volume, self._current_end_volume)
                assert self._current_IDT >= 0, "The interdivision time is negative. Daughter volume = {0}, mother volume = {1}.".format(self._current_start_volume, self._current_end_volume)
                
                #1.2 Do SSA, end = IDT, mode = 'time'
                self._ExecuteVolumeSSA()                 
                # Save age data of current generation 
                self._GetAges()                
               
                endtime_current_generation = self.StochSim.SSA.sim_t
                endtime_complete_generation = self.StochSim.settings.starttime + self._current_IDT  # Time reached if generation completed.                
                if endtime_current_generation >= endtime_complete_generation:                       # Only divide if new IDT (age) is reached and not at max generations
                    self._interdivision_times.append( self._current_IDT )                           # Save IDT of previous generation
                    self._volume_mother.append( self._current_end_volume )                          # This volume is reached at division
                    
                    if self._current_generation < self.sim_generations:
                        self._Divide()                                                              # Divide volumes, species and chooses daughter to follow
                        self._volume_daughter.append( self._next_start_volume )                     # Next generation is started with this start volume
                        
                        if not self.StochSim.SSA.IsSpeciesSelection:
                            self.StochSim.SSA.sim_output.append(self._output_after_division)
                        else:
                            self.StochSim.SSA.sim_output.append([self._output_after_division[i] for i in self.StochSim.SSA.species_output_indices])
                        ### Set settings for new simulation ### 
                        self.StochSim.settings.starttime += self._current_IDT
                        self.StochSim.settings.X_matrix = copy.copy(self.StochSim.SSA.X_matrix)                    
                        
                        # Keep V_output in synchrony with sim_output
                        self.StochSim.SSA.V_output.append( self._next_start_volume )# Division happens instantaneous; at same time point mother volume and daughter volume.                        
                else:   
                    break  # Either end_steps or end_time is reached, no division            

            if self.sim_mode != 'generations':
                self._interdivision_times.append( self._current_IDT ) # Add last IDT, of not completed generation
                                       
            self.StochSim.FillDataStochsim()
            self.StochSim.data_stochsim.setVolume(self.StochSim.SSA.V_output)                     
            self.StochSim.data_stochsim.setSpeciesConcentrations(self._species_extracellular_indices)                       
            
            self._GetDeterministicData()
            self.FillDataStochSimCellDivision()
            
            if self.StochSim.sim_trajectories == 1: 
                print("Number of time steps {0:d}, End time {1:f}, Completed Generations: {2:d}".format(self.StochSim.SSA.timestep, self.StochSim.SSA.sim_t, len(self._volume_mother)))
            elif self.StochSim.sim_trajectories > 1:
                self.DumpTrajectoryData(self.StochSim._current_trajectory)                      
            progressBar.update()
        self.StochSim.sim_trajectories_done = copy.copy(self.StochSim.sim_trajectories)     
        self.StochSim._IsSimulationDone = True
        self.data_stochsim = copy.copy(self.StochSim.data_stochsim)              
        try: 
            self.StochSim.plot = Analysis.DoPlotting(self.data_stochsim.species_labels,self.StochSim.SSA.rate_names,self.StochSim.plot.plotnum)
        except: 
            self.StochSim.plot = Analysis.DoPlotting(self.data_stochsim.species_labels,self.StochSim.SSA.rate_names)          
            
    def _GetDeterministicData(self):
        """
        Generate deterministic ages, time, volume after generating a trajectory
        
        hard coded to about 10**6, 5*10**6, or 10**7 data points
        """
        completed_generations = len(self._volume_mother)
        #print(completed_generations)
        if not completed_generations:         # no generation finished, 1000 for both for a nice plot
            age_steps = 10**3
            generation_steps = 10**3
        elif completed_generations <= 1000:    # 1 < generations <= 1000
            generation_steps = 10**3
            age_steps = 10**6/completed_generations   
        elif completed_generations <= 10.000:  # 1000 < generations <= 10000
            generation_steps = 10**2
            age_steps = 10**6/completed_generations          
        elif completed_generations <= 100.000: # 10000 < generations <= 100000
            age_steps = 5*10**6/completed_generations
            generation_steps = 10**2
        else:                                  # generations < 100000
            age_steps = 10**7/completed_generations
            generation_steps = 10
        
        max_age = max(self._interdivision_times)
            
        self._time_deterministic = []    
        self._volume_deterministic = []    
        self._ages_deterministic = []

        start_volumes = [self.sim_initial_volume] + self._volume_daughter
        if completed_generations == len(self._interdivision_times):   
            end_times = self._interdivision_times
        elif completed_generations < len(self._interdivision_times):
            endtime_current_generation = self.StochSim.SSA.sim_t    
            end_times = self._interdivision_times[:-1] + [endtime_current_generation - sum(self._interdivision_times[:-1])]
        else:           
           raise Warning("This should not happen!")

        t1 = 0
        for v1,t2 in zip(start_volumes,end_times):
            #print(t1,t1+t2)
            generation_times = np.linspace(t1,t1+t2,generation_steps).tolist()
            t1 += t2    
            self._time_deterministic += generation_times # identical to 10 digits or so
            
            generation_ages = np.linspace(0,t2,age_steps*t2/max_age).tolist()
            self._ages_deterministic += generation_ages            
            
            if self.sim_growth_type == 'exponential': 
                generation_volumes = list(v1*np.exp(self.sim_growth_rate*np.linspace(0,t2,generation_steps))) # exponential growth    
            elif self.sim_growth_type == 'linear':
                generation_volumes = list(v1 + self.sim_growth_rate*np.linspace(0,t2,generation_steps))
            else:
                raise Warning("This growth type '{0}' is not supported".format(self.sim_growth_type))
            self._volume_deterministic += generation_volumes

    def _GetAges(self):
        """
        Calculates cell age from (total) time output.
        
        *** For internal use only ***        
        """
        marker = len(self._ages)                                                        # Number of time steps already processed saved.
        starttime_generation = sum( self._interdivision_times )                         # Time up to start of this generation.
        simt_generation = self.StochSim.SSA.sim_output[marker:]                         # Output of the current generation
        cell_ages = [ output[0] - starttime_generation for output in simt_generation ]  # Calculate cell ages: For every output, select time and subtract start time of the generation
        self._generation_timesteps.append( len(cell_ages) )
        self._ages.extend(cell_ages)

    def _ExecuteVolumeSSA(self):
        """
        Performs an execute of the SSA until certain end values (end_time or end_steps). 
               
        *** For internal use only ***
        """
        # Reset the volume code with current parameters        
        self.StochSim.settings.volume_code = self.Vt_codestring.format(self._current_start_volume, self.sim_growth_rate, sum(self._interdivision_times))

        self.StochSim.settings.endtime += self._current_IDT
        if self.StochSim.settings.endtime > self.sim_time:           # Apparently this generation the time will exceed the given end time
            self.StochSim.settings.endtime = self.sim_time
        
        # Run a generation or until end_steps or end time is reached # hard coded to the Direct (Volume) SSA        
        if self.StochSim.settings.starttime and self.StochSim.IsTrackPropensities:
            self.StochSim.SSA.IsInit = True
            self.StochSim.SSA.volume_code = self.StochSim.settings.volume_code
            self.StochSim.SSA.Propensities()    
                  
            output_step = self.StochSim.SSA.sim_a_mu.tolist()
            output_step.insert(0,self.StochSim.SSA.sim_t)
            if self.StochSim.SSA.IsRateSelection:
                output_step = [output_step[j] for j in self.StochSim.SSA.rate_output_indices]
            self.StochSim.SSA.propensities_output.append(output_step) 

        self.StochSim.SSA.Execute(self.StochSim.settings,IsStatusBar=False)   
        
    def _Divide(self, n = 0):
        """ 
        Divides the volume, chooses daughter to follow and divides the species according to daughter volume.
        
        *** For internal use only ***
        """
        # 2 Divide volume according to K
        V_daughter1 = self._current_end_volume * self.K_distribution(*self.K_parameters)
        V_daughter2 = self._current_end_volume - V_daughter1
        
        # 3 Choose daughter to follow, based on volume. The larger the volume, the larger the probability to be chosen.
        self._next_end_volume = self.phi_distribution(*self.phi_parameters) # Volume of mother cell that one of the daughters will grow to.        
        delta_t = self.IDT_func(V_daughter2, self._next_end_volume) - self.IDT_func(V_daughter1, self._next_end_volume) # Positive = volume 1 larger, Negative = volume 1 smaller        
        P_daughter1 = np.exp(delta_t * self.sim_specific_growth_rate)/(1+np.exp(delta_t * self.sim_specific_growth_rate)) 
        
        is_daughter1 = np.random.binomial(n = 1, p = P_daughter1)       # = 1 (with prob P_daughter1) or 0       
        if is_daughter1:
            self._next_start_volume = V_daughter1
            self._volume_daughter_notselected.append( V_daughter2 )     # Save the daughter that is not selected
        else:
            self._next_start_volume = V_daughter2
            self._volume_daughter_notselected.append( V_daughter1 )
        
        # Do not continue if the daughter volume is larger than the next mother volume. # 04-02-2014        
        if self._next_start_volume > self._next_end_volume:          
            assert n < 20, "Cannot find valid end volume for next generation" # solves potential infinite loop
            print("Rejected daughter volume {0}. The cell division SSA is no longer exact.".format(self._next_start_volume) )
            # Try again to divide. Draws new partitioning K and mother volume.
            self._Divide( n + 1 )                                       # n counts number of tries to get a valid mother volume
            self._volume_daughter_notselected.pop()                     # Remove last appended (wrong) value # 7-04-2014
            return None                                                 # Breaks from current _Divide()      # 7-04-2014
        
        self._species_mother.append(self.StochSim.SSA.sim_output[-1][1:-1])
        
        # 4.1 Divide species
        volume_fraction = self._next_start_volume / self._current_end_volume
        for j in range(self.StochSim.SSA.n_species):        # divide each species between two cells, weighted by volume            
            species_amount = self.StochSim.SSA.X_matrix[j]
            if j in self._species_extracellular_indices:    # species is not in the cell and should not divide
                self.StochSim.SSA.X_matrix[j] = species_amount
            elif j in self.non_dividing_species_indices:    # non-dividing intracellular species
                self.StochSim.SSA.X_matrix[j] = species_amount             
            elif j in self.exact_species_indices:           # exact partitioning                                 
                if species_amount:
                    if species_amount%2:
                       self.StochSim.SSA.X_matrix[j] = np.floor(species_amount/2) + np.random.binomial(1,0.5)   
                    else:
                       self.StochSim.SSA.X_matrix[j] = species_amount/2
            else:
                if species_amount:                          # value is non-zero, to avoid errors
                    self.StochSim.SSA.X_matrix[j] = np.random.binomial(species_amount, volume_fraction)     # New generation will start with this X_matrix

        # Replace last time point with species amounts after division in StochSim.SSA
        self._output_after_division = self.StochSim.SSA.X_matrix.tolist()
        self._output_after_division += [amount for amount in self.StochSim.SSA.fixed_species_amount]     
        if self.StochSim.SSA.__aDict__ != {}:
            self.AssignmentRules()
            self._output_after_division += [value for value in self.StochSim.SSA.assignment_species]                    
               
        t_division = self.StochSim.settings.endtime # round( self.StochSim.settings.endtime*10**8)/10**8
        self._output_after_division.insert(0, t_division )
        self._output_after_division.append(np.NAN)      # no reaction occurs at cell division       
        
        if self.StochSim.SSA.IsSpeciesSelection:    
            self._species_daughter.append([self._output_after_division[i] for i in self.StochSim.SSA.species_output_indices[1:-1]])
        else:
            self._species_daughter.append(self._output_after_division[1:-1])
        
        # 4.2 Divide delayed species
        if self.StochSim._IsDelayedMethod:
            pending_delayed = copy.copy(self.StochSim.SSA.Tstruct[1:-1])          # All pending delayed reactions at cell division (excluding the 'inits' at start and end)
            if len(pending_delayed) != 0:              
                number_inherited = np.random.binomial(len(pending_delayed), volume_fraction)                
            else:
                number_inherited = 0
            inherited_delayed = random.sample(pending_delayed, number_inherited)  # Sampling without replacement
            #print('mother delayed:', len(pending_delayed))
            #print('daughter delayed:', len(inherited_delayed))
            self.StochSim.SSA.Tstruct = [(0, np.nan)] + inherited_delayed + [(np.inf, np.nan)]
            self.StochSim.SSA.Tstruct.sort()
   
    def CalculateSpecificGrowthRate(self, n_trapezoidal = 20, IsDebug = True):
        """
        Calculates the specific growth rate from the mother volume distribution (phi) and partitioning distribution (K).
        The specific growth rate is retrieved by numerically solving equation 20 of Painter and Marr [1] for k. For a fast calcuation, the trapezoidal rule is used for integration and the Secant method for solving the equation.
        
        [1] Painter P.R. and Marr A.G. (1968), "Mathematics of microbial populations", Annu. Rev. Microbiol. 22:519-548.
        
        Input: 
         - *n_trapezoidal* (integer) [default = 20] Number of subintervals used for integration with the composite trapezoidal rule.
         - *IsDebug* (boolean) [default = True] With IsDebug True, the script checks calculated specific growth rate. This takes some time. For a 'silent' calculation, set IsDebug False.
        """ 
        # If exponential growth, then specific growth rates equals the volume growth rate. No calculation needed.
        if self.sim_growth_type == 'exponential':
            self.sim_specific_growth_rate = self.sim_growth_rate
            return self.sim_specific_growth_rate
        
        # Other growth types, calculate specific growth rate.
        if self._IsBetaDistribution:
            print("Info: Starting calculation of specific growth rate...")
            sys.stdout.flush()
            
            Solver = k_solver()
            Solver.set_model(distr_phi = self._phi_tuple, distr_K = self._K_tuple, shift = self.phi_shift,
                             growth_rate = self.sim_growth_rate, growth_type = self.sim_growth_type)
            Solver.set_integration_param(n_trapezoidal, doquad = False, lim_quad = 8)            
            if IsDebug:
                self.sim_specific_growth_rate = Solver.Solve_k()
            else:
                t1 = time.time()
                self.sim_specific_growth_rate = Solver.Get_k(init_guess = self.sim_growth_rate)
                t2 = time.time()
                print("Time taken to calculate the specific growth rate:", t2-t1)                
        else:
            print("Info: Cannot calculate specific growth rate without beta distributions.")
            print("Info: Setting specific_growth_rate = growth_rate.")
            self.sim_specific_growth_rate = self.sim_growth_rate           
 
    def AnalyzeExtantCells(self, n_bins_age = 15, n_bins_IDT = 15, n_samples = 100000,integration_method= 'trapezoidal',lb =0.95,ub=1.05):
        """ 
        Obtains the species statistics for a population of extant cells. We use data binning and numerical integration to obtain a probability mass distribution of each species in the extant cell population.
        
        The right number of bins is very important for an accurate numerical integration. This function returns a warning message if the sum of probabilities (which should sum to 1) is outside the provided lower and upper bounds (defaults are 0.95 and 1.05, respectively).               

        Input:
          - *n_bins_age* (int) [default = 15] Number of bins for the binning of cell ages
          - *n_bins_IDT* (int) [default = 15] Number of bins for the binning of interdivision times
          - *n_samples* (int) [default = 100,000] Number of equally time spaced samples to take from the simulation.
          - *integration_method* (string) [default = 'trapezoidal]. We provide a 2D trapezoidal and a Riemann sum method for numerical integration. We prefer the 2D trapezodial method.
          - *lb* (float) lower accuracy bound 
          - *ub* (float) upper accuracy bound
        """  
        assert self.StochSim._IsSimulationDone, "Before analyzing, first do a stochastic simulation."        
        # Calculate k, if not calculated already.
        try:
            k = self.sim_specific_growth_rate
        except AttributeError: 
            print("Calculating the specific growth rate...")
            self.CalculateSpecificGrowthRate()
            k = self.sim_specific_growth_rate
        
        print("Info: Starting the analysis of the extant cell population...")
        sys.stdout.flush()
        for n in range(1,self.StochSim.sim_trajectories_done+1):
            if self.StochSim.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
                            
            # Prevent oversampling of the data. Max n_samples is the number of time steps.
            if self.data_stochsim.time.shape[0] < n_samples:
                n_samples = self.data_stochsim.time.shape[0]
                print("Resetting *n_samples* to {0:d}".format(n_samples) )                                
           
            self._ExtantSolver = ExtrapolateExtant(self.data_stochsim, self.data_stochsim_celldivision)

            self._ExtantSolver.make_full_IDT()
            self._ExtantSolver.sample_per_generation( n_samples = n_samples ) 
            # self._ExtantSolver.sample_fixedinterval( n_samples = n_samples )            # not necessary, less accurate
            self._ExtantSolver.bin_data( n_bins_IDT = n_bins_IDT,n_bins_age = n_bins_age )
            self._ExtantSolver.Calculate_ExtantCellCN( k = k,integration_method= integration_method )                       
                    
            D_means = {}
            D_stds = {}
            D_moments = {}
            L_probability_mass = []
            for i,s_id in enumerate(self.StochSim.sim_species_tracked):                 
                species_distribution = self._ExtantSolver.extant_species_pn[i]                
                x = np.array(sorted(species_distribution),dtype=int)                    
                p_x = np.array([species_distribution[x_i] for x_i in x])
                
                mu = (x*p_x).sum()
                mu_sq = (x**2*p_x).sum()
                var =  mu_sq - mu**2
                std = var**0.5
                L_probability_mass.append([x,p_x])     
                 
                D_means[s_id] = mu
                D_stds[s_id] = std
                  
                D_moments[s_id] = {}
                D_moments[s_id]['1'] = mu
                D_moments[s_id]['2'] = mu_sq
                D_moments[s_id]['3'] = (x**3*p_x).sum()
                D_moments[s_id]['4'] = (x**4*p_x).sum()            
                      
            self.data_stochsim_celldivision.setSpeciesExtantDistributions(L_probability_mass,D_means,D_stds,D_moments)            
            if self.StochSim.sim_trajectories_done > 1:
                self.DumpTrajectoryData(n)   
            
        print("Info: Successfully analyzed the extant cell species distribution")# (self.data_stochsim_celldivision.species_extant_distributions)")      
        self._IsAnalyzedExtant = True
        for n in range(1,self.StochSim.sim_trajectories_done+1):
            if self.StochSim.sim_trajectories_done > 1:
                self.GetTrajectoryData(n) 
            # For every species
            for i,extant_species_pn_sum in enumerate(self._ExtantSolver.extant_species_pn_sum):
                if extant_species_pn_sum < lb or extant_species_pn_sum > ub:
                    raise UserWarning("We found a sum of species probabilities {0:0.3f} in the extant cells which is not between the desired bounds ({1},{2}). Our advice is to specify a different number of bins for both age and interdivision times.".format(extant_species_pn_sum,lb,ub))    
                    
                    
    def GetAverageSpeciesExtantDistributions(self):
        """ Get average species distributions """      
        assert self.StochSim._IsSimulationDone, "Before printing distributions first do a stochastic simulation"
        assert self._IsAnalyzedExtant, "Before showing the means, calculate first the extant cell population"
        assert not self.StochSim._IsOnlyLastTimepoint, "Determining statistics is disabled when saving only the last time point"
        
        D_distributions = {}
        for s_id in self.StochSim.sim_species_tracked:
            D_distributions[s_id] = {}
        L_distributions_means = []
        L_distributions_standard_deviations = []
        for n in range(1,self.StochSim.sim_trajectories_done+1): 
            if self.StochSim.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            for i in range(len(self.StochSim.sim_species_tracked)):
                s_id = self.StochSim.sim_species_tracked[i]
                for m,s_amount in enumerate(self.data_stochsim_celldivision.species_extant_distributions[i][0]):
                    if not s_amount in list(D_distributions[s_id]):
                        D_distributions[s_id][s_amount] = []
                    D_distributions[s_id][s_amount].append(self.data_stochsim_celldivision.species_extant_distributions[i][1][m])
            
        for s_id in self.StochSim.sim_species_tracked:
            L_amount = list(D_distributions[s_id])  # for a given species 
            L_means = []
            L_stds = []   
            for s_amount in L_amount:
                while len(D_distributions[s_id][s_amount]) < (n-1):
                    D_distributions[s_id][s_amount].append(0)
                L_means.append(np.mean(D_distributions[s_id][s_amount]))
                L_stds.append(np.std(D_distributions[s_id][s_amount]))    
            L_distributions_means.append([L_amount,L_means]) 
            L_distributions_standard_deviations.append([L_amount,L_stds])
        self.data_stochsim_grid.setSpeciesExtantDistributionAverage(L_distributions_means,L_distributions_standard_deviations)                       
                        

    def PrintSpeciesExtantDistributions(self): 
        """ Print obtained distributions for each generated trajectory """      
        assert self.StochSim._IsSimulationDone, "Before printing distributions first do a stochastic simulation"
        assert self._IsAnalyzedExtant, "Before showing the means, calculate first the extant cell population"
        assert not self.StochSim._IsOnlyLastTimepoint, "Determining statistics is disabled when saving only the last time point"
        for n in range(1,self.StochSim.sim_trajectories_done+1):       
            if self.StochSim.sim_trajectories_done > 1:  
                self.GetTrajectoryData(n)
                
            for i,L_species_dist in enumerate(self.data_stochsim_celldivision.species_extant_distributions):
                print("Amount ({0:s})\tProbability".format(self.StochSim.sim_species_tracked[i]) )
                for m in range(len(L_species_dist[0])):
                    x = L_species_dist[0][m]
                    p_x = L_species_dist[1][m]
                    if not p_x < 0.001:
                        print("{0:d}\t{1:0.3f}".format(x,p_x))
                    else:
                        print("{0:d}\t{1:0.3e}".format(x,p_x))  
        
    def PrintSpeciesExtantMeans(self):
        """ Print the means of each species for the selected trajectory"""
        assert self.StochSim._IsSimulationDone, "Before showing the means, do a stochastic simulation first"      
        assert self._IsAnalyzedExtant, "Before showing the means, calculate first the extant cell population"
        assert not self.StochSim._IsOnlyLastTimepoint, "Determining statistics is disabled when saving only the last time point"
        print("Species\tMean")
        for s_id in self.data_stochsim_celldivision.species_labels:    
            mu = self.data_stochsim_celldivision.species_extant_means[s_id]            
            if not mu < 0.001:
                print("{0:s}\t{1:0.3f}".format(s_id,mu))   
            else:
                print("{0:s}\t{1:0.3e}".format(s_id,mu))   
    
    def PrintSpeciesExtantStandardDeviations(self):
        """ Print the means of each species for the selected trajectory"""
        assert self.StochSim._IsSimulationDone, "Before showing the means, do a stochastic simulation first"      
        assert self._IsAnalyzedExtant, "Before showing the means, calculate first the extant cell population"
        assert not self.StochSim._IsOnlyLastTimepoint, "Determining statistics is disabled when saving only the last time point"
        print("Species\tStandard Deviation")
        for s_id in self.data_stochsim_celldivision.species_labels:          
            std = self.data_stochsim_celldivision.species_extant_standard_deviations[s_id]
            if not std < 0.001:
                print("{0:s}\t{1:0.3f}".format(s_id,std))     
            else:
                print("{0:s}\t{1:0.3e}".format(s_id,std))    
                
    def PlotExtantSpeciesDistribution(self, species2plot = True, linestyle = 'solid', linewidth = 1,colors=None,title = 'StochPy Extant Cell Species Probability Mass Function',xlabel='Molecule number',ylabel='Probability Mass',IsLegend=True,legend_location='upper right'):   
        print("***DEPRECATION WARNING***: This function is replaced by PlotSpeciesExtantDistributions()'")
        self.PlotSpeciesExtantDistributions(species2plot = species2plot, linestyle = linestyle, linewidth = linewidth,colors=colors,title = title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location)        
        
    def PlotSpeciesExtantDistributions(self, species2plot = True, linestyle = 'solid', linewidth = 1,colors=None,title = 'StochPy Extant Cell Species Probability Mass Function',xlabel='Molecule number',ylabel='Probability Mass',IsLegend=True,legend_location='upper right',bin_size=1):
        """
        Plots the analyzed/extrapolated extant cell species number Probability Mass Function.
        
        Input:
         - *species2plot* [default = True) (list)          
         - *linestyle* [default = 'dotted'] (string)         
         - *linewidth* [default = 1] (float)
         - *colors* [default = None] (list)
         - *title* [default = 'StochPy Extant Cell Probability Mass Function'] (string)
         - *xlabel* [default = 'Volume'] (string)
         - *ylabel* [default = 'Probability Mass'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
         - *bin_size* [default=None] (integer)
        """ 
        assert Analysis._IsPlotting, "Install Matplotlib or use Export2file()"
        assert self._IsAnalyzedExtant, "Before plotting extant species distribution, first analyze the simulations (.AnalyzeExtantCells())."
            
        species2plot = self.StochSim._getSpecies2Plot(species2plot)        
        species2plot_indices = [self.StochSim.sim_species_tracked.index(d) for d in species2plot]        
        if colors == None:
            colors =  ['#0000FF','#00CC00','#FF0033','#FF00CC','#6600FF','#FFFF00','#000000','#CCCCCC',
                       '#00CCFF','#99CC33','#FF6666','#FF99CC','#CC6600','#003300','#CCFFFF','#9900FF','#CC6633','#FFD700','#C0C0C0']   
        
        Analysis.plt.figure(self.StochSim.plot.plotnum)                
        for n in range(1,self.StochSim.sim_trajectories_done+1):
            if self.StochSim.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
   
            self.StochSim.plot.Distributions(self.data_stochsim_celldivision.species_extant_distributions,species2plot,self.data_stochsim_celldivision.species_labels,n-1,linestyle,linewidth,colors,title,xlabel,ylabel,IsLegend,legend_location,bin_size)                 
        self.StochSim.plot.plotnum += 1   
        
    def PlotAverageSpeciesExtantDistributions(self,species2plot = True,linestyle = 'None',linewidth = 1,marker = 'o',colors = None,title = 'StochPy Average Species Distributions Plot (# of trajectories = )',xlabel='Species Amount',ylabel='Probability',IsLegend=True,legend_location = 'upper right',nstd=1): 
        """
        PlotAverageSpeciesDistributions(species2plot = True,linestyle = 'None',marker = 'o',colors = None,title = 'StochPy Average Species Distributions Plot (# of trajectories = )',xlabel='Species Amount',ylabel='Probability',IsLegend=True,legend_location='upper right',nstd=1)

        Plot the average species distributions For each species Amount, the mean and standard deviation are plotted      

        Input:
         - *species2plot* [default = True] as a list ['S1','S2']
         - *linestyle* [default = 'dotted'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = 'o'] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Average Time (# of trajectories = ... )' ] (string)
         - *xlabel* [default = 'Species Amount'] (string)
         - *ylabel* [default = 'Probability'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
         - *nstd* [default=1] (float)
        """
        assert Analysis._IsPlotting, "Install Matplotlib or use Export2file()"
        assert self._IsAnalyzedExtant, "Before plotting extant species distribution, first analyze the simulations (.AnalyzeExtantCells())."      
        if not self.data_stochsim_grid.HAS_AVERAGE_SPECIES_EXTANT_DISTRIBUTIONS:
            self.GetAverageSpeciesExtantDistributions()
        
        species2plot = self.StochSim._getSpecies2Plot(species2plot)                
        if '(# of trajectories = )' in title:
            title = title.replace('= ','= {0:d}'.format(self.StochSim.sim_trajectories_done))

        self.StochSim.plot.AverageDistributions(self.data_stochsim_grid.species_extant_distributions_means,self.data_stochsim_grid.species_extant_distributions_standard_deviations,nstd,species2plot,self.StochSim.sim_species_tracked,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location)
        self.StochSim.plot.plotnum+=1         
        
    def SumExtantSpeciesDistributions(self):
        """ 
        Use this function to test the sum of p(Nx=n). This sum should be (very) close to zero. If not, do AnalyzeExtantCells with a different number of age and IDT bins.        
        """
        for n in range(1,self.StochSim.sim_trajectories_done+1):
            if self.StochSim.sim_trajectories_done > 1:
                self.GetTrajectoryData(n) 
            # For every species
            for i,extant_species_pn_sum in enumerate(self._ExtantSolver.extant_species_pn_sum):
                print(self.StochSim.sim_species_tracked[i],"{0:0.3f}".format(extant_species_pn_sum))
        
    def ShowSpecies(self):
        """ Print the species of the model """
        self.StochSim.ShowSpecies()

    def ShowOverview(self):
        """ Print an overview of the current settings """
        self.StochSim.ShowOverview()
    
    def PlotInterdivisionTimeDistribution(self, bins=10, histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy IDT Probability Density Function',xlabel='Interdivision Time',ylabel='Probability Density',IsLegend=True,legend_location='upper right'): 
        """
        PlotInterdivisionTimeDistribution(nbins=10, histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy IDT Probability Density Function',xlabel='Interdivision Time',ylabel='Probability Density',IsLegend=True,legend_location='upper right')
        
        Plots Interdivision Time distribution (between cell divisions) for a certain *trajectories* or for 'all' trajectories together        
        
        Input:
         - *bins* [default = 10] (integer)
         - *histtype* [default = 'step'] (string)
         - *linestyle* [default = 'dotted'] (string)
         - *filled* [default = False] (boolean)
         - *linewidth* [default = 1] (float)
         - *colors* [default = None] (list)
         - *title* [default = 'StochPy IDT Probability Density Function'] (string)
         - *xlabel* [default = 'Interdivision Time'] (string)
         - *ylabel* [default = 'Probability Density'] (string)
         - *IsLegend* [default = True] (boolean)
        """         
        assert len(self._interdivision_times) > 1, "Not enough generations to plot an inter division time distribution"
        self._PlotVolume(plottype = "interdivision",bins= bins, histtype = histtype, linestyle = linestyle, filled = filled, linewidth = linewidth,colors=colors,title = title,xlabel=xlabel,ylabel=ylabel)
   
    def PlotVolumeMotherDistribution(self, bins=10, histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy Mother Cell Volume Probability Density Function',xlabel='Volume',ylabel='Probability Density'):
        """
        PlotVolumeMotherDistribution(bins=10, histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy Mother Cell Volume Probability Density Function',xlabel='Volume',ylabel='Probability Density')
        
        Plot the volume distribution of mother cells
        
        Input:
         - *bin_size* [default = 0.1] (float)
         - *histtype* [default = 'step'] (string)
         - *linestyle* [default = 'dotted'] (string)
         - *filled* [default = False] (boolean)
         - *linewidth* [default = 1] (float)
         - *colors* [default = None] (list)
         - *title* [default = 'StochPy Mother cell Volume Probability Density Function'] (string)
         - *xlabel* [default = 'Volume'] (string)
         - *ylabel* [default = 'Probability Density'] (string)
        """
        assert len(self._volume_mother) > 0, "Not enough generations to plot a mother volume distribution"
        self._PlotVolume(plottype = "mother",bins= bins, histtype = histtype, linestyle = linestyle, filled = filled, linewidth = linewidth,colors=colors,title = title,xlabel=xlabel,ylabel=ylabel)

    def PlotVolumeDaughterDistribution(self,bins= 10, trajectories = 'all', histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy Daughter Cell Volume Probability Density Function',xlabel='Volume',ylabel='Probability Density'):
        """
        PlotVolumeDaughterDistribution(bins= 10, histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy Daughter Cell Volume Probability Density Function',xlabel='Volume',ylabel='Probability Density')
        
        Plot the volume distribution of daughter cells
        
        Input:
         - *bins* [default = 0.1] (float)
         - *histtype* [default = 'step'] (string)
         - *linestyle* [default = 'dotted'] (string)
         - *filled* [default = False] (boolean)
         - *linewidth* [default = 1] (float)
         - *colors* [default = None] (list)
         - *title* [default = 'StochPy Daughter Cell Volume Probability Density Function'] (string)
         - *xlabel* [default = 'Volume'] (string)
         - *ylabel* [default = 'Probability Density'] (string)
        """
        assert len(self._volume_daughter) > 0, "Not enough generations to plot a daughter volume distribution"
        self._PlotVolume(plottype = "daughter",bins= bins, histtype = histtype, linestyle = linestyle, filled = filled, linewidth = linewidth,colors=colors,title = title,xlabel=xlabel,ylabel=ylabel)
        Analysis.plt.xlim(xmax=max(self.data_stochsim_celldivision.volume_mother))       
        
    def PlotCellAgeDistribution(self, bins=10, trajectories = 'all', histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy Cell Age Probability Density Function',xlabel='Cell Age',ylabel='Probability Density'):
        """
        PlotCellAgeDistribution(bins=10, histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy Cell Age Probability Density Function',xlabel='Volume',ylabel='Probability Density')
        
        Plot the volume distribution of daughter cells
        
        Input:
         - *bins [default = 10] (integer)
         - *histtype* [default = 'step'] (string)
         - *linestyle* [default = 'dotted'] (string)
         - *filled* [default = False] (boolean)
         - *linewidth* [default = 1] (float)
         - *colors* [default = None] (list)
         - *title* [default = 'StochPy Daughter cell Volume Probability Density Function'] (string)
         - *xlabel* [default = 'Volume'] (string)
         - *ylabel* [default = 'Probability Density'] (string)
        """        
        self._PlotVolume(plottype = "cellage",bins= bins, histtype = histtype, linestyle = linestyle, filled = filled, linewidth = linewidth,colors=colors,title = title,xlabel=xlabel,ylabel=ylabel)
            
    def _PlotVolume(self, plottype, bins=10, histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy Volume Probability Density Function',xlabel='Molecule number',ylabel='Probability Density'):
        """ 
        _PlotVolume(plottype, bins=10, histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy Volume Probability Density Function',xlabel='Molecule number',ylabel='Probability Density')
        
        Here, we can directly use the hist() function. This is not possible for e.g. time series data, where we have to take into account the irregular time points between consecutive firings of reactions. Species distributions can therefore not be directly be generated with the hist() function.
        
        continuous in time: cell age distribution
        discrete: mother cell volume, daughter cell volume, interdivision time. 
        
        *** For internal use only ***
        """
        assert Analysis._IsPlotting, "Install Matplotlib or use Export2file()"
        assert self.StochSim._IsSimulationDone, "Before plotting time simulation results first do a stochastic simulation"
        
        if colors == None:
            colors =  ['#0000FF','#00CC00','#FF0033','#FF00CC','#6600FF','#FFFF00','#000000','#CCCCCC',
                       '#00CCFF','#99CC33','#FF6666','#FF99CC','#CC6600','#003300','#CCFFFF','#9900FF','#CC6633','#FFD700','#C0C0C0']           
        
        Analysis.plt.figure(self.StochSim.plot.plotnum)        
        for n in range(1,self.StochSim.sim_trajectories_done+1):   
            if self.StochSim.sim_trajectories > 1:
                self.GetTrajectoryData(n)
                
            # We now use mid as alignment for the data
            if plottype.lower() == 'mother':
                data = self.data_stochsim_celldivision.volume_mother
                align='mid'
            elif plottype.lower() == 'daughter':
                data = self.data_stochsim_celldivision.volume_daughter_all
                align='mid'
            elif plottype.lower() in ['idt','interdivision']:
                data = self.data_stochsim_celldivision.interdivision_times
                align='mid'
            elif plottype.lower() in ['age','ages','cellage','cellages']:
                data = self.data_stochsim_celldivision.ages_deterministic
                align = 'mid'                     
         
            
            Analysis.plt.hist(data[:,0], bins= bins, normed = True, histtype = histtype, ls = linestyle, fill = filled, lw = linewidth, color = colors[n-1],align=align)   
        
        Analysis.plt.xlim(xmin=0)
        Analysis.plt.ylim(ymin=0)   
        
        self.StochSim.plot.plotnum += 1
        Analysis.plt.title(title)
        Analysis.plt.xlabel(xlabel)
        Analysis.plt.ylabel(ylabel)        
        
    def PlotSpeciesDaughterDistributions(self, bin_size=1, species2plot = True, histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy Daughter Cell Species Probability Mass Function',xlabel='Molecule number',ylabel='Probability Mass',IsLegend=True,legend_location='upper right'):
        """ 
        PlotSpeciesDaughterDistributions(bin_size=1, species2plot = True, histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy Daughter Cell Species Probability Mass Function',xlabel='Molecule number',ylabel='Probability Mass',IsLegend=True,legend_location='upper right')
        
        StochPy Daughter Cell Species Probability Mass Function
        
        Input:
         - *bin_size* [default = 0.1] (float)
         - *species2plot* [default = True) (list) 
         - *histtype* [default = 'step'] (string)
         - *linestyle* [default = 'dotted'] (string)
         - *filled* [default = False] (boolean)
         - *linewidth* [default = 1] (float)
         - *colors* [default = None] (list)
         - *title* [default = 'StochPy Daughter cell Volume Probability Mass Function'] (string)
         - *xlabel* [default = 'Volume'] (string)
         - *ylabel* [default = 'Probability Mass'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
        """
        assert len(self._species_mother) > 0, "Not enough generations to plot a daughter species distribution"
        self._PlotSpecies(plottype = "daughter",bin_size=bin_size, species2plot = species2plot, histtype = histtype, linestyle = linestyle, filled = filled, linewidth = linewidth,colors=colors,title = title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location)        
        
        species2plot = self.StochSim._getSpecies2Plot(species2plot)             
        max_copy_number = 0
        for s_id in species2plot:
            i = self.data_stochsim_celldivision.species_labels.index(s_id)
            max_i = max(self.data_stochsim_celldivision.species_mother[:,i])
            if max_i > max_copy_number:
                max_copy_number = max_i        
        Analysis.plt.xlim(xmax=max_i)    
        
    def PlotSpeciesMotherDistributions(self, bin_size=1, species2plot = True, histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy Mother Cell Species Probability Mass Function',xlabel='Molecule number',ylabel='Probability Mass',IsLegend=True,legend_location='upper right'):
        """ 
        PlotSpeciesMotherDistributions(bin_size=1, species2plot = True, histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy Mother Cell Species Probability Mass Function',xlabel='Molecule number',ylabel='Probability Mass',IsLegend=True,legend_location='upper right')
        
        StochPy Mother Cell Species Probability Mass Function
        
        Input:
         - *bin_size* [default = 0.1] (float)
         - *species2plot* [default = True) (list) 
         - *histtype* [default = 'step'] (string)
         - *linestyle* [default = 'dotted'] (string)
         - *filled* [default = False] (boolean)
         - *linewidth* [default = 1] (float)
         - *colors* [default = None] (list)
         - *title* [default = 'StochPy Mother cell Volume Probability Mass Function'] (string)
         - *xlabel* [default = 'Volume'] (string)
         - *ylabel* [default = 'Probability Mass'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
        """        
        assert len(self._species_mother) > 0, "Not enough generations to plot a mother species distribution"
        self._PlotSpecies(plottype = "mother",bin_size=bin_size, species2plot = species2plot, histtype = histtype, linestyle = linestyle, filled = filled, linewidth = linewidth,colors=colors,title = title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location)
        
    def _PlotSpecies(self, plottype, bin_size=1, species2plot = True, histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy Daughter cell Species Probability Mass Function',xlabel='Molecule number',ylabel='Probability Mass',IsLegend=True,legend_location='upper right'):
        """ 
        _PlotSpecies(plottype, bin_size=1, species2plot = True, histtype = 'step', linestyle = 'solid', filled = False, linewidth = 1,colors=None,title = 'StochPy Daughter cell Species Probability Mass Function',xlabel='Molecule number',ylabel='Probability Mass',IsLegend=True,legend_location='upper right')
        
        *** For internal use only ***
        """
        assert Analysis._IsPlotting, "Install Matplotlib or use Export2file()"
        assert self.StochSim._IsSimulationDone, "Before plotting time simulation results first do a stochastic simulation"
            
        species2plot = self.StochSim._getSpecies2Plot(species2plot)
        
        species2plot_indices = [self.StochSim.sim_species_tracked.index(d) for d in species2plot]        
        if colors == None:
            colors =  ['#0000FF','#00CC00','#FF0033','#FF00CC','#6600FF','#FFFF00','#000000','#CCCCCC',
                       '#00CCFF','#99CC33','#FF6666','#FF99CC','#CC6600','#003300','#CCFFFF','#9900FF','#CC6633','#FFD700','#C0C0C0']   
        
        
        Analysis.plt.figure(self.StochSim.plot.plotnum)
        for n in range(1,self.StochSim.sim_trajectories_done+1):   
            if self.StochSim.sim_trajectories > 1:
                self.GetTrajectoryData(n)
            
            if plottype.lower() == 'mother':
                data = self.data_stochsim_celldivision.species_mother
            else:
                data = self.data_stochsim_celldivision.species_daughter
           
            for j,s_index in enumerate(species2plot_indices):
                if len(species2plot_indices) == 1:
                    j = n-1                
                dat_min = data[:,s_index].min() 
                dat_max = data[:,s_index].max()
                n_bins = 1 + (dat_max-dat_min) /bin_size # Just take one trajectory as reference
                L_bin_edges = np.linspace(dat_min-bin_size/2.0,dat_max+bin_size/2.0,n_bins+1)       
                Analysis.plt.hist(data[:,s_index], L_bin_edges, normed = True, histtype = histtype, ls = linestyle, fill = filled, lw = linewidth, color = colors[j])
               
        Analysis.plt.xlim(xmin=0)
        Analysis.plt.ylim(ymin=0,ymax = 1)       
        
        self.StochSim.plot.plotnum += 1        
        Analysis.plt.title(title)
        Analysis.plt.xlabel(xlabel)
        Analysis.plt.ylabel(ylabel)  
        if IsLegend:
            Analysis.plt.legend(species2plot,numpoints=1,frameon=True,loc=legend_location)
        
    def PlotVolumeTimeSeries(self,n_events2plot = 10000,linestyle = 'solid', linewidth = 1,marker = '',colors = None,title = 'StochPy Volume Time Series Plot', xlabel = 'Time', ylabel = 'Volume'):
        """
        PlotVolumeTimeSeries(n_events2plot = 10000,linestyle = 'solid', linewidth = 1,marker = '',colors = None,title = 'StochPy Volume Time Series Plot', xlabel = 'Time', ylabel = 'Volume')
        
        StochPy Volume Time Series Plot
        
        Input:
         - *n_events2plot* [default = 10000] (integer)       
         - *linestyle* [default = 'solid'] (string)       
         - *linewidth* [default = 1] (float)
         - *marker* [default = ''] (string)
         - *colors* [default = None] (list)
         - *title* [default = 'StochPy Volume Time Series Plot'] (string)
         - *xlabel* [default = 'Volume'] (string)
         - *ylabel* [default = 'Probability Mass'] (string)        
        """
        assert Analysis._IsPlotting, "Install matplotlib or use Export2file()"
        assert self.StochSim._IsSimulationDone, "Before plotting time simulation results first do a stochastic simulation"        
        if str(n_events2plot).lower() == 'all':
            n_events2plot = self.data_stochsim.simulation_timesteps       
                
        Analysis.plt.figure(self.StochSim.plot.plotnum)        
        if colors == None: 
            colors = self.StochSim.plot.colors    
        
        for n in range(1,self.StochSim.sim_trajectories_done+1):   
            if self.StochSim.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            Arr_volume = Analysis.getDataForTimeSimPlot(self.data_stochsim_celldivision.getVolumeDeterministic())
            Analysis.plt.plot(Arr_volume [:,0],Arr_volume[:,1], marker, ls = linestyle, lw = linewidth, color = colors[n-1])  
             
        Analysis.plt.title(title)
        Analysis.plt.xlabel(xlabel)
        Analysis.plt.ylabel(ylabel)
        self.StochSim.plot.plotnum+=1            

    def PlotSpeciesTimeSeries(self,plottype = 'amounts',n_events2plot = 10000,species2plot = True,linestyle = 'solid',linewidth = 1,marker = '',colors = None,title = 'StochPy Species Time Series Plot',xlabel='Time',ylabel='Copy Number',IsLegend=True,legend_location='upper right'):
        """
        PlotSpeciesTimeSeries(plottype = 'amounts',n_events2plot = 10000,species2plot = True,linestyle = 'solid',linewidth = 1, marker = '',colors = None,title = 'StochPy Species Time Series Plot',xlabel='Time',ylabel='Copy Number',IsLegend=True,legend_location='upper right')
        
        Plot time simulation output for each generated trajectory. 
        
        
        Default: PlotSpeciesTimeSeries() plots time simulation for each species amounts. Note that also species concentrations can be plotted.

        Input:
         - *plottype* [default = 'amounts'] alternative is 'concentrations'
         - *n_events2plot* [default = 10000] (integer)
         - *species2plot* [default = True] as a list ['S1','S2'] 
         - *linestyle* [default = 'solid'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = ''] ('v','o','s',',','*','.')
         - *colors* [default = None] (list)
         - *title* [default = 'StochPy Species Time Series Plot']  (string)
         - *xlabel* [default = 'Time'] (string)
         - *ylabel* [default = 'Copy Number'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string)
        """     
        assert Analysis._IsPlotting, "Install matplotlib or use Export2file()"
        assert self.StochSim._IsSimulationDone, "Before plotting time simulation results first do a stochastic simulation"
        assert not self.StochSim._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        species2plot = copy.copy(self.StochSim._getSpecies2Plot(species2plot))
        if str(n_events2plot).lower() == 'all':
            n_events2plot = self.data_stochsim.simulation_timesteps
                
        for n in range(1,self.StochSim.sim_trajectories_done+1):   
            if self.StochSim.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            
            if plottype.lower() in ['concentration','concentrations']:               
                plot_data = self.data_stochsim.getSpeciesConcentrations()
                species_labels = copy.copy(self.data_stochsim.species_concentrations_labels)
                for s in self._species_extracellular:
                    if s in species2plot:
                         species2plot.remove(s)                                
                if ylabel == 'Copy Number': 
                     ylabel = 'Concentration'           
            elif plottype.lower() in ['amounts','amount','copy number','copy_number']: 
                plot_data = self.data_stochsim.getSpecies()                
                species_labels = copy.copy(self.data_stochsim.species_labels)
            else:
                raise Warning("{0} is not a valid plottype argument. Valid plottypes are 'concentrations' and 'amounts'".format(plottype) )            
            
            self.StochSim.plot.TimeSeries(plot_data,n_events2plot,species2plot,species_labels,n-1,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location)           
        self.StochSim.plot.plotnum += 1
    
    def PlotSpeciesVolumeTimeSeries(self,plottype ='amounts', n_events2plot = 10000,species2plot = True,linestyle = 'solid',linewidth = 1, marker = '',colors = None,title= 'StochPy Species Time Series and Volume Plot',xlabel = 'Time',ylabel = 'Copy Number',IsLegend = True,legend_location=1):
        """
        PlotSpeciesVolumeTimeSeries(plottype ='amounts', n_events2plot = 10000,species2plot = True,linestyle = 'solid',linewidth = 1, marker = '',colors = None,title= 'StochPy Species Time Series and Volume Plot',xlabel = 'Time',ylabel = 'Copy Number',IsLegend = True,legend_location=1)
        
        Plot time simulation output for each generated trajectory
        Default: PlotSpeciesTimeSeries() plots time simulation for each species

        Input:
         - *plottype* [default = 'amounts'] alternative is 'concentrations'
         - *n_events2plot* [default = 10000] (integer)
         - *species2plot* [default = True] as a list ['S1','S2'] 
         - *linestyle* [default = 'solid'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = ''] ('v','o','s',',','*','.')
         - *colors* [default = None] (list)
         - *title* [default = 'StochPy Species Time Series and Volume Plot']  (string)    
         - *xlabel* [default = 'Time'] (string)
         - *ylabel* [default = 'Copy Number'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string)   
        """
        assert Analysis._IsPlotting, "Install matplotlib or use Export2file()"
        assert self.StochSim._IsSimulationDone, "Before plotting time simulation results first do a stochastic simulation"
        assert not self.StochSim._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        #Make two subplots
        gs = Analysis.gridspec.GridSpec(2,1)
        plotnum = self.StochSim.plot.plotnum
        Analysis.plt.figure(plotnum);
        
        #Plot species in upper panel
        ax1 = Analysis.plt.subplot(gs[0])
        self.StochSim.plot.plotnum = plotnum
        self.PlotSpeciesTimeSeries(plottype,n_events2plot, species2plot, linestyle, linewidth, marker, colors,title,xlabel,ylabel,IsLegend=IsLegend,legend_location=legend_location)
        Analysis.plt.xlabel('')
        
        #Plot volume in lower panel
        ax2 = Analysis.plt.subplot(gs[1])
        self.StochSim.plot.plotnum = plotnum
        self.PlotVolumeTimeSeries(n_events2plot,linestyle, linewidth, marker, colors,title='',xlabel=xlabel)    
        
           
    def PlotSpeciesDistributions(self,species2plot = True, linestyle = 'solid',linewidth = 1, colors=None,title = 'StochPy Species Probability Mass Function',xlabel='Number of Molecules',ylabel='Probability',IsLegend=True,legend_location='upper right',bin_size=1):
        """
        PlotSpeciesDistributions(species2plot = True, linestyle = 'solid',linewidth = 1, colors=None,title = 'StochPy Species Probability Mass Function',xlabel='Number of Molecules',ylabel='Probability',IsLegend=True,bin_size=1)
        
        Plots the PDF for each generated trajectory
        Default: PlotSpeciesDistributions() plots PDF for each species

        Input:
         - *species2plot* [default = True] as a list ['S1','S2']
         - *linestyle* [default = 'dotted'] (string)
         - *linewidth* [default = 1] (float)
         - *colors* (list)
         - *title* [default = 'StochPy Species Probability Mass Function'] (string)     
         - *xlabel* [default = 'Number of Molecules'] (string)
         - *ylabel* [default = 'Probability'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
         - *bin_size* [default=1] (integer)
        """     
        self.StochSim.PlotSpeciesDistributions(species2plot=species2plot,linestyle=linestyle,linewidth=linewidth,colors=colors,title=title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location,bin_size=bin_size)
                
    def PlotPropensitiesTimeSeries(self,n_events2plot = 10000,rates2plot = True,linestyle = 'solid',linewidth = 1,marker = '',colors = None,title = 'StochPy Propensities Time Series Plot',xlabel='Time',ylabel='Propensity',IsLegend=True,legend_location='upper right'):
        """
        PlotPropensitiesTimeSeries(n_events2plot = 10000,rates2plot = True,linestyle = 'solid',marker = '',colors = None,title = 'StochPy Propensities Time Series Plot',xlabel='Time',ylabel='Propensity',IsLegend=True,legend_location='upper right')
        
        Plot time simulation output for each generated trajectory

        Default: PlotPropensitiesTimeSeries() plots propensities for each species

        Input:
         - *n_events2plot* [default = 10000] (integer)
         - *rates2plot* [default = True]: species as a list ['S1','S2']
         - *marker* [default = ''] ('v','o','s',',','*','.')
         - *linestyle* [default = 'solid']: dashed, dotted, and solid (string)
         - *linewidth* [default = 1] (float)
         - *colors* [default = None] (list)
         - *title* [default = 'StochPy Propensities Time Series Plot'] (string)
         - *xlabel* [default = 'Time'] (string)
         - *ylabel* [default = 'Propensity'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string)   
        """
        self.StochSim.PlotPropensitiesTimeSeries(n_events2plot=n_events2plot,rates2plot=rates2plot,linestyle=linestyle,linewidth=linewidth,marker=marker,colors=colors,title=title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location)
        
    def PlotPropensitiesDistributions(self,rates2plot = True, linestyle = 'solid',linewidth = 1,colors=None,title = 'StochPy Propensities Probability Mass Function',xlabel='Propensity',ylabel='Probability',IsLegend=True,legend_location = 'upper right',bin_size=1):
        """
        PlotPropensitiesDistributions(self,rates2plot = True, linestyle = 'solid',linewidth = 1,colors=None,title = 'StochPy Propensities Probability Mass Function',xlabel='Propensity',ylabel='Probability',IsLegend=True,bin_size=1)
        
        Plots the PDF for each generated trajectory

        Default: PlotPropensitiesDistributions() plots PDF for each species

        Input:
         - *species2plot* [default = True] as a list ['S1','S2']
         - *linestyle* [default = 'dotted'] (string)
         - *linewidth* [default = 1] (float)
         - *colors* (list)
         - *title* [default = 'StochPy Propensities Probability Mass Function'] (string)     
         - *xlabel* [default = 'Propensity'] (string)
         - *ylabel* [default = 'Probability'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
         - *bin_size* [default=1] (integer)
        """
        self.StochSim.PlotPropensitiesDistributions(rates2plot=rates2plot,linestyle=linestyle,linewidth=linewidth,colors=colors,title=title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,bin_size=bin_size)   

    def GetWaitingtimes(self):
        """ Get for each reaction the waiting times """ 
        self.StochSim.GetWaitingtimes()
        self.data_stochsim = copy.copy(self.StochSim.data_stochsim)        

    def PlotWaitingtimesDistributions(self,rates2plot = True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Event Waiting times Plot',xlabel=r'inter-event time $t$',ylabel='Probability Density',IsLegend=True,legend_location='upper right'):
        """
        PlotWaitingtimesDistributions(rates2plot = True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Waiting times Plot',xlabel='inter-event time t',ylabel='Probability Density')
        
        Plot event waiting time distributions
        
        default: PlotWaitingtimesDistributions() plots waiting times for all rates
      
        Input:
         - *rates2plot* [default = True]  as a list of strings ["R1","R2"]
         - *linestyle* [default = 'None'] dashed, dotted, dash_dot, and solid (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = 'o'] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Event Waiting times Plot'] (string)
         - *xlabel* [default = 'inter-event time t'] (string)
         - *ylabel* [default = 'Probability Density'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string)   
        """     
        self.StochSim.PlotWaitingtimesDistributions(rates2plot=rates2plot,linestyle=linestyle,linewidth=linewidth,marker=marker,colors=colors,title=title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location)

    def GetRegularGrid(self,n_samples=250):
        """
        GetRegularGrid(n_samples=250)
        
                
        The Gillespie method generates data at irregular time points. However, it is possible to output data on a fixed regular time grid where the user can specify the resolution of the grid (n_samples).  
        
        We use a higher number of default samples, because we expect more stochasticity due to explicit modeling of cell divisions
       
        Input:
         - *n_samples* [default = 250] (integer)
        """    
        self.StochSim.GetRegularGrid(n_samples)        
        self.StochSim.data_stochsim_grid.setSpeciesConcentrations(self._species_extracellular_indices)
        (self.StochSim.data_stochsim_grid.species_concentrations_means,self.StochSim.data_stochsim_grid.species_concentrations_standard_deviations) = Analysis.GetAverageResults(self.StochSim.data_stochsim_grid.species_concentrations)
        self.data_stochsim_grid = copy.copy(self.StochSim.data_stochsim_grid)           
        
    def PlotAverageVolumeTimeSeries(self,linestyle = '', linewidth = 1,marker = 'o',color = 'blue',title = 'StochPy Volume Time Series Plot', xlabel = 'Time', ylabel = 'Volume',nstd=1):
        """
        PlotVolumeTimeSeries(n_events2plot = 10000,linestyle = 'solid', linewidth = 1,marker = '',colors = None,title = 'StochPy Volume Time Series Plot', xlabel = 'Time', ylabel = 'Volume')
        
        StochPy Volume Time Series Plot
        
        Input:             
         - *linestyle* [default = 'solid'] (string)       
         - *linewidth* [default = 1] (float)
         - *marker* [default = ''] (string)
         - *color* (string)
         - *title* [default = 'StochPy Volume Time Series Plot'] (string)
         - *xlabel* [default = 'Volume'] (string)
         - *ylabel* [default = 'Probability Mass'] (string)        
        """
        assert Analysis._IsPlotting, "Install matplotlib or use Export2file()"
        assert self.StochSim._IsSimulationDone, "Before plotting time simulation results first do a stochastic simulation"        
        if not self.StochSim.HAS_AVERAGE: 
            print("*** WARNING ***: No regular grid is created yet. Use GetRegularGrid(n_samples) if averaged results are unsatisfactory (e.g. more or less 'samples')")
            self.GetRegularGrid()  
        
        if '(# of trajectories = )' in title:
            title = title.replace('= ','= {0:d}'.format(self.sim_trajectories_done))    
        
        plotnum = self.StochSim.plot.plotnum
        Analysis.plt.figure(plotnum);
            
        Analysis.plt.errorbar(self.data_stochsim_grid.time,self.data_stochsim_grid.volume_means[0],yerr = nstd*self.data_stochsim_grid.volume_standard_deviations[0],ls=linestyle,lw=linewidth,marker=marker,color=color)

        Analysis.plt.title(title)
        Analysis.plt.xlabel(xlabel)
        Analysis.plt.ylabel(ylabel)
        self.StochSim.plot.plotnum+=1 
        
    def PlotAverageSpeciesVolumeTimeSeries(self,plottype ='amounts', species2plot = True,linestyle = 'solid',linewidth = 1, marker = '',colors = None,title= 'StochPy Species Time Series and Volume Plot',xlabel = 'Time', ylabel = 'Copy Number', IsLegend = True,legend_location=1,nstd=1): 
        """
        PlotAverageSpeciesVolumeTimeSeries(plottype ='amounts', species2plot = True,linestyle = 'solid',linewidth = 1, marker = '',colors = None,title= 'StochPy Species Time Series and Volume Plot',xlabel = 'Time', ylabel = 'Copy Number', IsLegend = True,legend_location=1,nstd=1)
        
        Plot time simulation output for each generated trajectory
        Default: PlotSpeciesTimeSeries() plots time simulation for each species

        Input:
         - *plottype* [default = 'amounts'] alternative is 'concentrations'         
         - *species2plot* [default = True] as a list ['S1','S2'] 
         - *linestyle* [default = 'solid'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = ''] ('v','o','s',',','*','.')
         - *colors* [default = None] (list)
         - *title* [default = 'StochPy Species Time Series and Volume Plot']  (string)    
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string)   
        """
        assert Analysis._IsPlotting, "Install matplotlib or use Export2file()"
        assert self.StochSim._IsSimulationDone, "Before plotting time simulation results first do a stochastic simulation"   
        assert not self.StochSim._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        #Make two subplots
        gs = Analysis.gridspec.GridSpec(2,1)
        plotnum = self.StochSim.plot.plotnum
        Analysis.plt.figure(plotnum);
        
        #Plot species in upper panel
        ax1 = Analysis.plt.subplot(gs[0])
        self.StochSim.plot.plotnum = plotnum
        self.PlotAverageSpeciesTimeSeries(plottype,species2plot, linestyle, linewidth, marker, colors,title,xlabel,ylabel,IsLegend=IsLegend,legend_location=legend_location,nstd=nstd)
        Analysis.plt.xlabel('')
        
        #Plot volume in lower panel
        ax2 = Analysis.plt.subplot(gs[1])
        self.StochSim.plot.plotnum = plotnum
        self.PlotAverageVolumeTimeSeries(linestyle, linewidth, marker, title='',nstd=nstd)              
        
    def PlotAverageSpeciesTimeSeries(self,plottype='amounts',species2plot = True,linestyle = 'None',linewidth = 1,marker = 'o',colors = None,title = 'StochPy Average Species Time Series Plot (# of trajectories = )',xlabel='Time',ylabel='Copy Number',IsLegend=True,legend_location='upper right',nstd=1): 
        """
        PlotAverageSpeciesTimeSeries(species2plot = True,linestyle = 'None',marker = 'o',colors = None,title = 'StochPy Average Species Time Series Plot (# of trajectories = )',xlabel='Time',ylabel='Copy Number',IsLegend=True,nstd=1)
        
        Plot the average time simulation result. For each time point, the mean and standard deviation are plotted 
        
        Input:
         - *plottype* [default = 'amounts'] alternative is 'concentrations'          
         - *species2plot* [default = True] as a list ['S1','S2']
         - *linestyle* [default = 'dotted'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = 'o'] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Average Time (# of trajectories = ... )' ] (string)
         - *xlabel* [default = 'Time'] (string)
         - *ylabel* [default = 'Copy Number'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string)   
         - *nstd* [default=1] (float)
        """ 
        assert Analysis._IsPlotting, "Install matplotlib or use Export2file()"  
        assert self.StochSim._IsSimulationDone, "Before plotting time simulation results first do a stochastic simulation"   
        assert not self.StochSim._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        
        if not self.StochSim.HAS_AVERAGE: 
            print("*** WARNING ***: No regular grid is created yet. Use GetRegularGrid(n_samples) if averaged results are unsatisfactory (e.g. more or less 'samples')")
            self.GetRegularGrid()                      
        species2plot = copy.copy(self.StochSim._getSpecies2Plot(species2plot))        
        if '(# of trajectories = )' in title:
            title = title.replace('= ','= {0:d}'.format(self.StochSim.sim_trajectories_done))            
            
        if plottype.lower() in ['concentration','concentrations']:               
            means = copy.copy(self.data_stochsim_grid.species_concentrations_means)
            stds = copy.copy(self.data_stochsim_grid.species_concentrations_standard_deviations)
            for s in self._species_extracellular:
                if s in species2plot:
                     species2plot.remove(s)                                
            if ylabel == 'Copy Number': 
                 ylabel = 'Concentration'           
        elif plottype.lower() in ['amounts','amount','copy number','copy_number']: 
            means = copy.copy(self.data_stochsim_grid.species_means)
            stds = copy.copy(self.data_stochsim_grid.species_standard_deviations)        
        
        self.StochSim.plot.AverageTimeSeries(means,stds,self.data_stochsim_grid.time,nstd,species2plot,self.StochSim.sim_species_tracked,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location)
        self.StochSim.plot.plotnum+=1       

        
    def PlotAveragePropensitiesTimeSeries(self,rates2plot = True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Average Propensities Time Series Plot (# of trajectories = )',xlabel='Time',ylabel='Propensity',IsLegend=True,legend_location='upper right',nstd=1): 
        """
        PlotAveragePropensitiesTimeSeries(rates2plot = True,linestyle = 'None',marker = 'o',colors = None,title = 'StochPy Average Propensities Time Series Plot (# of trajectories = )',xlabel='Time',ylabel='Propensity',IsLegend=True,nstd=1)
        
        Plot the average propensities For each time point, the mean and standard deviation are plotted 
        
        Input:
         - *rates2plot* [default = True] as a list ['S1','S2']
         - *linestyle* [default = 'dotted'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = 'o'] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Average Propensities Plot (# of trajectories = ...)' ] (string)
         - *xlabel* [default = 'Time'] (string)
         - *ylabel* [default = 'Propensity'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string)   
         - *nstd* [default=1] (float
        """              
        self.StochSim.PlotAveragePropensitiesTimeSeries(rates2plot=rates2plot,linestyle=linestyle,linewidth=linewidth,marker=marker,colors=colors,title=title,xlabel=xlabel,ylabel=ylabel,legend_location=legend_location,nstd=nstd)          
        self.data_stochsim_grid = copy.copy(self.StochSim.data_stochsim_grid) 
        
    def PlotAverageSpeciesDistributions(self,species2plot = True,linestyle = 'None',linewidth = 1,marker = 'o',colors = None,title = 'StochPy Average Species Distributions Plot (# of trajectories = )',xlabel='Species Amount',ylabel='Probability',IsLegend=True,legend_location = 'upper right',nstd=1): 
        """
        PlotAverageSpeciesDistributions(species2plot = True,linestyle = 'None',marker = 'o',colors = None,title = 'StochPy Average Species Distributions Plot (# of trajectories = )',xlabel='Species Amount',ylabel='Probability',IsLegend=True,nstd=1)

        Plot the average species distributions For each species Amount, the mean and standard deviation are plotted      

        Input:
         - *species2plot* [default = True] as a list ['S1','S2']
         - *linestyle* [default = 'dotted'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = 'o'] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Average Time (# of trajectories = ... )' ] (string)
         - *xlabel* [default = 'Species Amount'] (string)
         - *ylabel* [default = 'Probability'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string)   
         - *nstd* [default=1] (float)
        """    
        self.StochSim.PlotAverageSpeciesDistributions(species2plot = species2plot,linestyle = linestyle,linewidth = linewidth,marker = marker,colors = colors,title = title, xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location,nstd=nstd)
        self.data_stochsim_grid = copy.copy(self.StochSim.data_stochsim_grid) 
        
    def PlotAverageSpeciesDistributionsConfidenceIntervals(self,species2plot=True,colors = None,title = 'StochPy Average Species Distributions Plot (# of trajectories = )',xlabel='Species Amount',ylabel='Probability',IsLegend=True,legend_location = 'upper right',nstd=1):
        """
        PlotAverageSpeciesDistributionsConfidenceIntervals(species2plot=True,colors = None,title = 'StochPy Average Species Distributions Plot (# of trajectories = )',xlabel='Species Amount',ylabel='Probability',IsLegend=True,nstd=1)
        
        Plot the average species distributions For each species Amount, the mean and standard deviation are plotted      

        Input:
         - *species2plot* [default = True] as a list ['S1','S2']
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Average Time (# of trajectories = ... )' ] (string)
         - *xlabel* [default = 'Species Amount'] (string)
         - *ylabel* [default = 'Probability'] (string)
         - *IsLegend* [default = True] (boolean)      
         - *legend_location* [default = 'upper right'] (string)   
         - *nstd* [default=1] (float
        """
        self.StochSim.PlotAverageSpeciesDistributionsConfidenceIntervals(species2plot=species2plot,colors = colors,title = title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location,nstd=nstd)
        self.data_stochsim_grid = copy.copy(self.StochSim.data_stochsim_grid) 

    def PlotAveragePropensitiesDistributions(self,rates2plot = True,linestyle = 'None',linewidth = 1,marker = 'o',colors = None,title = 'StochPy Average Propensities Distributions Plot (# of trajectories = )',xlabel='Propensity',ylabel='Probability',IsLegend=True,legend_location = 'upper right',nstd=1): 
        """
        PlotAveragePropensitiesDistributions(rates2plot = True,linestyle = 'None',marker = 'o',colors = None,title = 'StochPy Average Species Time Series Plot (# of trajectories = )',xlabel='Propensity',ylabel='Probability',IsLegend=True,nstd=1)

        Plot the average time simulation result. For each time point, the mean and standard deviation are plotted      

        Input:
         - *rates2plot* [default = True] as a list ['R1','R2']
         - *linestyle* [default = 'dotted'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = 'o'] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Average Time (# of trajectories = ... )' ] (string)
         - *xlabel* [default = 'Propensity'] (string)
         - *ylabel* [default = 'Probability'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string)   
         - *nstd* [default=1] (float
        """  
        self.StochSim.PlotAveragePropensitiesDistributions(rates2plot = rates2plot,linestyle = linestyle,linewidth = linewidth,marker = marker,colors = colors,title = title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location,nstd=nstd)
        self.data_stochsim_grid = copy.copy(self.StochSim.data_stochsim_grid) 
        
    def PlotAveragePropensitiesDistributionsConfidenceIntervals(self,rates2plot = True,colors = None,title = 'StochPy Average Propensities Distributions Plot (# of trajectories = )',xlabel='Propensity',ylabel='Probability',IsLegend=True,legend_location='upper right',nstd=1):        
        """
        PlotAveragePropensitiesDistributionsConfidenceIntervals(rates2plot = True,colors = None,title = 'StochPy Average Propensities Distributions Plot (# of trajectories = )',xlabel='Propensity',ylabel='Probability',IsLegend=True,nstd=1)

        Plot the average time simulation result. For each time point, the mean and standard deviation are plotted      

        Input:
         - *rates2plot* [default = True] as a list ['R1','R2']       
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Average Time (# of trajectories = ... )' ] (string)
         - *xlabel* [default = 'Propensity'] (string)
         - *ylabel* [default = 'Probability'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string)   
         - *nstd* [default=1] (float)
        """
        self.StochSim.PlotAveragePropensitiesDistributionsConfidenceIntervals(rates2plot = rates2plot,colors = colors,title = title, xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location,nstd=nstd)
        self.data_stochsim_grid = copy.copy(self.StochSim.data_stochsim_grid)        
        
    def PlotSpeciesAutocorrelations(self,nlags = -1,species2plot=True,linestyle = 'None',linewidth = 1,marker = 'o',colors = None,title = 'StochPy Species Autocorrelation Plot',xlabel=r'Lag ($\tau$)',ylabel='Auto-correlation',IsLegend=True,legend_location='upper right'):
        """
        PlotSpeciesAutocorrelations(species2plot=True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Species Autocorrelation Plot',xlabel='Lag',ylabel='Auto-correlation')
        
        Plot species autocorrelations
        
        Input:
         - *nlags* [default = -1] (integer) 1,2,3 ... -1 where 3 means calculate the autocorrelation for the first 3 lags and -1 for all lags  
         - *species2plot* [default = True] as a list ['S1','S2']
         - *linestyle* [default = 'dotted'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = 'o'] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Species Autocorrelation Plot'] (string)
         - *xlabel* [default = r'Lag ($\tau$)'] (string)
         - *ylabel* [default = 'Autocorrelation'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
        """
        self.StochSim.PlotSpeciesAutocorrelations(nlags = nlags,species2plot=species2plot,linestyle = linestyle,linewidth = linewidth, marker = marker,colors = colors,title = title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location)
        self.data_stochsim_grid = copy.copy(self.StochSim.data_stochsim_grid) 

    def PlotSpeciesAutocovariances(self,nlags = -1,species2plot=True,linestyle = 'None', linewidth = 1, marker = 'o',colors = None,title = 'StochPy Species Autocorrelation Plot',xlabel=r'Lag ($\tau$)',ylabel='Auto-correlation',IsLegend=True,legend_location='upper right'):
        """
        PlotSpeciesAutocovariances(species2plot=True,linestyle = 'None', linewidth = 1, marker = 'o',colors = None,title = 'StochPy Species Autocorrelation Plot',xlabel='Lag',ylabel='Auto-correlation')
        
        Plot species auto-covariances
        
        Input:
         - *nlags* [default = -1] (integer) 1,2,3 ... -1 where 3 means calculate the autocorrelation for the first 3 lags and -1 for all lags  
         - *species2plot* [default = True] as a list ['S1','S2']
         - *linestyle* [default = 'dotted'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = 'o'] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Species Autocorrelation Plot'] (string)
         - *xlabel* [default = r'Lag ($\tau$)'] (string)
         - *ylabel* [default = 'Autocorrelation'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
        """
        self.StochSim.PlotSpeciesAutocovariances(nlags = nlags,species2plot=species2plot,linestyle = linestyle,linewidth = linewidth, marker = marker,colors = colors,title = title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location)
        self.data_stochsim_grid = copy.copy(self.StochSim.data_stochsim_grid) 
        
    def PlotAverageSpeciesAutocorrelations(self,nlags=-1,species2plot = True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Average Species Autocorrelation Plot (# of trajectories = )',xlabel=r'Lag ($\tau$)',ylabel='Auto-correlation',IsLegend=True,legend_location='upper right',nstd=1): 
        """
        PlotAverageSpeciesAutocorrelations(species2plot = True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Species Autocorrelation Plot (# of trajectories = )')
        
        Plot the average time simulation result. For each time point, the mean and standard deviation are plotted       

        Input:
         - *nlags* [default = -1] (integer) 1,2,3 ... -1 where 3 means calculate the autocorrelation for the first 3 lags and -1 for all lags  
         - *species2plot* [default = True] as a list ['S1','S2']
         - *linestyle* [default = 'dotted'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)      
         - *marker* [default = 'o'] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Average Species Autocorrelation Plot (# of trajectories = ... )' ] (string)
         - *xlabel* [default = r'Lag ($\tau$)'] (string)
         - *ylabel* [default = 'Autocorrelation'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
        """        
        self.StochSim.PlotAverageSpeciesAutocorrelations(nlags = nlags,species2plot=species2plot,linestyle = linestyle,linewidth = linewidth, marker = marker,colors = colors,title = title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location,nstd=nstd)
        self.data_stochsim_grid = copy.copy(self.StochSim.data_stochsim_grid) 
        

    def PlotAverageSpeciesAutocovariances(self,nlags=-1,species2plot = True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Average Species Autocorrelation Plot (# of trajectories = )',xlabel=r'Lag ($\tau$)',ylabel='Auto-correlation',IsLegend=True,legend_location='upper right',nstd=1): 
        """
        PlotAverageSpeciesAutocovariances(species2plot = True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Species Autocorrelation Plot (# of trajectories = )')
        
        Plot the average time simulation result. For each time point, the mean and standard deviation are plotted       

        Input:

         - *nlags* [default = -1] (integer) 1,2,3 ... -1 where 3 means calculate the autocorrelation for the first 3 lags and -1 for all lags  
         - *species2plot* [default = True] as a list ['S1','S2']
         - *linestyle* [default = 'dotted'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = 'o'] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Average Species Autocorrelation Plot (# of trajectories = ... )' ] (string)
         - *xlabel* [default = r'Lag ($\tau$)'] (string)
         - *ylabel* [default = 'Autocorrelation'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
        """
        self.StochSim.PlotAverageSpeciesAutocovariances(nlags = nlags,species2plot=species2plot,linestyle = linestyle,linewidth = linewidth, marker = marker,colors = colors,title = title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location,nstd=nstd)
        self.data_stochsim_grid = copy.copy(self.StochSim.data_stochsim_grid) 
        
    def PlotPropensitiesAutocorrelations(self,nlags=-1,rates2plot=True,linestyle = 'None', linewidth = 1, marker = 'o',colors = None,title = 'StochPy Propensities Autocorrelation Plot',xlabel=r'Lag ($\tau$)',ylabel='Auto-correlation',IsLegend=True,legend_location='upper right'):
        """
        PlotPropensitiesAutocorrelations(rates2plot=True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Propensities Autocorrelation Plot',xlabel=r'Lag ($\tau$)',ylabel='Auto-correlation')
        
        Input:
         - *nlags* [default = -1] (integer) 1,2,3 ... -1 where 3 means calculate the autocorrelation for the first 3 lags and -1 for all lags  
         - *rates2plot* [default = True] as a list ['R1','R2']      
         - *linestyle* [default = 'dotted'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = ','] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = StochPy Propensities Autocorrelation Plot] (string)
         - *xlabel* [default = r'Lag ($\tau$)'] (string)
         - *ylabel* [default = 'Autocorrelation'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
        """
        self.StochSim.PlotPropensitiesAutocorrelations(nlags = nlags,rates2plot=rates2plot,linestyle = linestyle,linewidth = linewidth, marker = marker,colors = colors,title = title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location)
        self.data_stochsim_grid = copy.copy(self.StochSim.data_stochsim_grid)         
        
        
    def PlotPropensitiesAutocovariances(self,nlags=-1,rates2plot=True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Propensities Autocorrelation Plot',xlabel=r'Lag ($\tau$)',ylabel='Auto-correlation',IsLegend=True,legend_location='upper right'):
        """
        PlotPropensitiesAutocovariances(rates2plot=True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Propensities Autocovariance Plot',xlabel=r'Lag ($\tau$)',ylabel='Auto-covariance')

        
        Input:
         - *nlags* [default = -1] (integer) 1,2,3 ... -1 where 3 means calculate the autocorrelation for the first 3 lags and -1 for all lags  
         - *rates2plot* [default = True] as a list ['R1','R2']      
         - *linestyle* [default = 'dotted'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = ','] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = StochPy Propensities Autocorrelation Plot] (string)
         - *xlabel* [default = r'Lag ($\tau$)'] (string)
         - *ylabel* [default = 'Auto-correlation'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
        """
        self.StochSim.PlotPropensitiesAutocovariances(nlags = nlags,rates2plot=rates2plot,linestyle = linestyle,linewidth = linewidth, marker = marker,colors = colors,title = title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location)
        self.data_stochsim_grid = copy.copy(self.StochSim.data_stochsim_grid) 
        
    def PlotAveragePropensitiesAutocorrelations(self,nlags=-1,rates2plot = True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Propensities Autocorrelation Plot (# of trajectories = )',xlabel=r'Lag ($\tau$)',ylabel='Auto-correlation',IsLegend=True,legend_location='upper right',nstd=1): 
        """
        PlotAveragePropensitiesAutocorrelation(nlags=-1,rates2plot = True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Propensities Autocorrelation Plot (# of trajectories = )',xlabel=r'Lag ($\tau$)',ylabel='Auto-correlation',IsLegend=True,legend_location='upper right',nstd=1)
        
        Plot the average propensities autocorrelation result for different lags. For each lag, the mean and standard deviation are plotted       

        Input:
         - *nlags* [default = -1] (integer) 1,2,3 ... -1 where 3 means calculate the autocorrelation for the first 3 lags and -1 for all lags  
         - *rates2plot* [default = True] as a list ['R1','R2']      
         - *linestyle* [default = 'dotted'] dashed, solid, and dash_dot (string)
         - *marker* [default = ','] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = StochPy Average Time (# of trajectories = ... ) ] (string)
         - *xlabel* [default = r'Lag ($\tau$)'] (string)
         - *ylabel* [default = 'Autocorrelation'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
        """  
        self.StochSim.PlotAveragePropensitiesAutocorrelations(nlags = nlags,rates2plot=rates2plot,linestyle = linestyle,linewidth = linewidth, marker = marker,colors = colors,title = title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location,nstd=nstd)      
        self.data_stochsim_grid = copy.copy(self.StochSim.data_stochsim_grid)   
        
    def PlotAveragePropensitiesAutocovariances(self,nlags=-1,rates2plot = True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Propensities Autocorrelation Plot (# of trajectories = )',xlabel=r'Lag ($\tau$)',ylabel='Auto-correlation',IsLegend=True,legend_location='upper right',nstd=1): 
        """
        PlotAveragePropensitiesAutocorrelation(nlags=-1,rates2plot = True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Propensities Autocorrelation Plot (# of trajectories = )',xlabel=r'Lag ($\tau$)',ylabel='Auto-correlation',IsLegend=True,legend_location='upper right',nstd=1)
        
        Plot the average propensities autocorrelation result for different lags. For each lag, the mean and standard deviation are plotted

        Input:
         - *nlags* [default = -1] (integer) 1,2,3 ... -1 where 3 means calculate the autocorrelation for the first 3 lags and -1 for all lags  
         - *rates2plot* [default = True] as a list ['R1','R2']      
         - *linestyle* [default = 'dotted'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = ','] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = StochPy Average Time (# of trajectories = ... ) ] (string)
         - *xlabel* [default = r'Lag ($\tau$)'] (string)
         - *ylabel* [default = 'Autocorrelation'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
        """          
        self.StochSim.PlotAveragePropensitiesAutocovariances(nlags = nlags,rates2plot=rates2plot,linestyle = linestyle,linewidth = linewidth, marker = marker,colors = colors,title = title,xlabel=xlabel,ylabel=ylabel,IsLegend=IsLegend,legend_location=legend_location,nstd=nstd)        
        self.data_stochsim_grid = copy.copy(self.StochSim.data_stochsim_grid) 
      
    def PrintSpeciesMeans(self):
        """ Print the means of each species for the selected trajectory"""
        self.StochSim.PrintSpeciesMeans()

    def PrintSpeciesStandardDeviations(self):
        """ Print the standard deviations of each species for the selected trajectory"""      
        self.StochSim.PrintSpeciesStandardDeviations()
        
    def PrintPropensitiesMeans(self):
        """ Print the means of each species for the selected trajectory"""
        self.StochSim.PrintPropensitiesMeans()

    def PrintPropensitiesStandardDeviations(self):
        """ Print the standard deviations of each species for the selected trajectory"""      
        self.StochSim.PrintPropensitiesStandardDeviations()

    def Export2File(self,analysis='timeseries',datatype='species', IsAverage = False, directory=None):
        """
        Export2File(analysis='timeseries',datatype='species', IsAverage = False, directory=None)
        
        Write data to a text document     
    
        Input:
         - *analysis* [default = 'timeseries'] (string) options: timeseries, distribution, mean, std, autocorrelation, autocovariance
         - *datatype*  [default = 'species'] (string) options: species, propensities, waitingtimes
         - *IsAverage* [default = False] (boolean)   
         - *directory* [default = None] (string)
        """        
        self.StochSim.Export2File(analysis,datatype,IsAverage,directory)
        
    def ExportExtant2File(self,analysis='distribution',IsAverage = False, directory=None):
        """
        Export2File(analysis='distributions',IsAverage = False, directory=None)
        
        Write data to a text document     
    
        Input:
         - *analysis* [default = 'distribution'] (string) options: distribution, mean, std, autocorrelation, autocovariance        
         - *IsAverage* [default = False] (boolean)   
         - *directory* [default = None] (string)
        """        
        assert self.StochSim._IsSimulationDone, "Before plotting time simulation results first do a stochastic simulation"   
        assert not self.StochSim._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        assert self._IsAnalyzedExtant , "Before exporting extant species distributions to a file first analyze the extant cell population"        
        
        if directory == None:
            if not IsAverage:
                directory = os.path.join(self.output_dir,"{0:s}_{1:s}".format(self.StochSim.model_file,analysis))
            else:
                directory = os.path.join(self.output_dir,"{0:s}_{1:s}_{2:s}".format(self.StochSim.model_file,"average_extant",analysis))
        else:
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not IsAverage:
                directory = os.path.join(directory,"{0:s}_{1:s}".format(self.StochSim.model_file,analysis))  
            else:
                directory = os.path.join(directory,"{0:s}_{1:s}_{2:s}".format(self.StochSim.model_file,"average_extant",analysis))
        
        if analysis.lower() in ['distributions','distribution'] and not IsAverage:            
            for n in range(1,self.StochSim.sim_trajectories_done+1):       
                if self.StochSim.sim_trajectories_done > 1:  
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')  
                for i,L_species_dist in enumerate(self.data_stochsim_celldivision.species_extant_distributions):
                    file_out.write("Amount ({0:s})\tProbability\n".format(self.StochSim.sim_species_tracked[i]) )
                    for m in range(len(L_species_dist[0])):
                        x = L_species_dist[0][m]
                        p_x = L_species_dist[1][m]                        
                        file_out.write("{0:d}\t{1}\n".format(x,p_x))                                   
                file_out.close()
        elif analysis.lower() == 'mean' and not IsAverage: 
            for n in range(1,self.StochSim.sim_trajectories_done+1):       
                if self.StochSim.sim_trajectories_done > 1:  
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')  
                file_out.write("Species\tMean\n")                
                for s_id in self.StochSim.sim_species_tracked: 
                    file_out.write("{0:s}\t{1:f}\n".format(s_id,self.data_stochsim_celldivision.species_extant_means[s_id])) 
                file_out.close()
                print("Info: Species extant means output is successfully saved at: {0:s}".format(file_path) )
                
        elif analysis.lower() == 'std' and not IsAverage: 
            for n in range(1,self.StochSim.sim_trajectories_done+1):       
                if self.StochSim.sim_trajectories_done > 1:  
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')  
                file_out.write("Species\tStandard Deviation\n")                
                for s_id in self.StochSim.sim_species_tracked: 
                    file_out.write("{0:s}\t{1:f}\n".format(s_id,self.data_stochsim_celldivision.species_extant_standard_deviations[s_id])) 
                file_out.close()
                print("Info: Species extant standard deviations output is successfully saved at: {0:s}".format(file_path) )           

        elif analysis.lower() in ['distributions','distribution'] and IsAverage:            
            if not self.data_stochsim_grid.HAS_AVERAGE_SPECIES_EXTANT_DISTRIBUTIONS:
                self.GetAverageSpeciesExtantDistributions()
        
            file_path = '{0:s}.txt'.format(directory)
            file_out = open(file_path,'w')     
            for i,s_id in enumerate(self.StochSim.sim_species_tracked):
                file_out.write("Amount\t{0:s} (Mean)\t{0:s} (STD)\n".format(s_id) )   
                for m in range(len(self.data_stochsim_grid.species_extant_distributions_means[i][0])):
                    s_amount = self.data_stochsim_grid.species_extant_distributions_means[i][0][m] 
                    s_probability_mean = self.data_stochsim_grid.species_extant_distributions_means[i][1][m]
                    s_probability_std = self.data_stochsim_grid.species_extant_distributions_standard_deviations[i][1][m]
                    file_out.write("{0:0.0f}\t{1:f}\t{2:f}\n".format(s_amount,s_probability_mean,s_probability_std) )
                file_out.write("\n")                
            print("Info: Averaged species distributions output is successfully saved at: {0:s}".format(file_path) ) 
        else:
            raise UserWarning("No valid option specified. Nothing is exported. See help function (help(ExportExtant2File))")

    def FillDataStochSimCellDivision(self):
        """ 
        Fill the data_stochsim_celldivision object after generating a realization
        """         
        self.data_stochsim_celldivision.setSimulationInfo(self.StochSim.SSA.timestep,self.StochSim.SSA.sim_t,self.StochSim._current_trajectory) # added 05-08-2014
        self.data_stochsim_celldivision.setTime(self.StochSim.data_stochsim.time)            
        self.data_stochsim_celldivision.setAges(np.array(self._ages).astype('d'))
        self.data_stochsim_celldivision.setDeterministicData(self._time_deterministic,self._volume_deterministic,self._ages_deterministic)            
        if self._current_generation > 1:
            self.data_stochsim_celldivision.setInterdivisionTimes(np.array(self._interdivision_times).astype('d'),self._current_generation)    
            self.data_stochsim_celldivision.setVolumeMother(np.array(self._volume_mother).astype('d'))
            self.data_stochsim_celldivision.setVolumeDaughter(np.array(self._volume_daughter).astype('d'), np.array(self._volume_daughter_notselected).astype('d'))
            self.data_stochsim_celldivision.setSpeciesMother(np.array(self._species_mother).astype(np.uint32),self.StochSim.sim_species_tracked)
            self.data_stochsim_celldivision.setSpeciesDaughter(np.array(self._species_daughter).astype(np.uint32),self.StochSim.sim_species_tracked)               
            self.data_stochsim_celldivision.setGenerationTimesteps(np.array(self._generation_timesteps).astype('d'))              
        
            (L_probability_mass, D_means, D_stds,D_moments) = Analysis.GetDataDistributions(self.data_stochsim_celldivision.getSpeciesMother(),self.StochSim.sim_species_tracked)
            self.data_stochsim_celldivision.setSpeciesMotherDist(L_probability_mass,D_means,D_stds,D_moments)
            (L_probability_mass, D_means, D_stds,D_moments) = Analysis.GetDataDistributions(self.data_stochsim_celldivision.getSpeciesDaughter(),self.StochSim.sim_species_tracked)
            self.data_stochsim_celldivision.setSpeciesDaughterDist(L_probability_mass,D_means,D_stds,D_moments)            

            (L_probability_mass, D_means, D_stds,D_moments) = Analysis.GetDataDistributions(self.data_stochsim_celldivision.getVolumeMother(),['v'])
            self.data_stochsim_celldivision.setVolumeMotherDist(L_probability_mass,D_means,D_stds,D_moments)
            (L_probability_mass, D_means, D_stds,D_moments) = Analysis.GetDataDistributions(self.data_stochsim_celldivision.getVolumeDaughter(),['v'])
            self.data_stochsim_celldivision.setVolumeDaughterDist(L_probability_mass,D_means,D_stds,D_moments)   

        
class IntegrationStochasticCellDivisionObj(object):
    """
    This class is specifically designed to store the results of a stochastic time simulation
    It has methods for setting e.g. the Time, Labels, Species, and Volume data and
    getting e.g.  Time, Species,and Volume (including time) arrays. However, of more use:

    - getDataAtTime(time) the data generated at time point "time".
    - getDataInTimeInterval(time, bounds=None) more intelligent version of the above
      returns an array of all data points where: time-bounds <= time <= time+bounds
    """    
    time = None
    species_extant_distributions = None
    species_mother = None
    species_daughter = None
    volume_mother = None
    volume_daughter = None
    interdivision_times = None
    division_times = None
    ages = None
    generation_timesteps = None    
    species_labels = None
    xdata_labels = None
    time_label = 'Time'
    
    HAS_DETERMINISTIC = False
    HAS_TIME = False    
    HAS_SPECIES_MOTHER = False
    HAS_SPECIES_DAUGHTER = False
    HAS_AGES = False
    HAS_IDT = False
    HAS_DT = False
    HAS_GENERATION_TIMESTEPS = False
    HAS_VOLUME_MOTHER = False
    HAS_VOLUME_DAUGHTER = False    
    HAS_XDATA = False

    IS_VALID = True    
    TYPE_INFO = 'Stochastic'  
 

    def setSimulationInfo(self,timesteps,endtime,simulation_trajectory):
        """
        set Simulation Information
        
        Input:
         - *timesteps* (integer)
         - *endtime* (float)
         - *simulation_trajectory* (integer)
        """
        self.simulation_timesteps = timesteps
        self.simulation_endtime = endtime
        self.simulation_trajectory = simulation_trajectory
    
    def setInterdivisionTimes(self,idt,n_generations):
        """
        set the (inter)division times array
        
        Input:
         - *idt*
        """
        self.interdivision_times = idt.reshape(len(idt), 1)
        division_times = np.cumsum(idt, dtype = 'd') # [sum(idt[:i]) for i in range(1,n_generations+1)]
        self.division_times = division_times.reshape(len(division_times),1)
        HAS_IDT = True
        HAS_DT = True
        
    def setAges(self,ages):
        """
        set the ... ages array
        
        Input:
         - *ages*
        """
        self.ages = ages.reshape(len(ages),1)
        HAS_AGES = True
        
    def setGenerationTimesteps(self,timesteps):
        """
        set the generation timesteps array 
        
        Input:
         - *timesteps*
        """
        self.generation_timesteps = timesteps
        HAS_GENERATION_TIMESTEPS = True  
        
    def setSpeciesExtantDistributions(self,distributions,means,stds,moments):
        """
        Set the species array
        
        Input:
         - *distributions* (list)
         - *means* (dict)
         - *stds* (dict)
         - *moments* (dict)
        """
        self.species_extant_distributions = distributions
        self.species_extant_means = means
        self.species_extant_standard_deviations = stds
        self.species_extant_moments = moments
        self.HAS_SPECIES_EXTANT = True        
       
    def setSpeciesMother(self,species,lbls = None):
        """
        Set the species array
        
        Input:
         - *species* an array of species vs time data
         - *lbls* [default=None] a list of species labels
        """
        self.species_mother = species
        self.HAS_SPECIES_MOTHER = True
        if lbls != None:
            self.species_labels = lbls        
    
    def setSpeciesDaughter(self,species,lbls = None):
        """
        Set the species array
        
        Input:
         - *species* an array of species vs time data
         - *lbls* [default=None] a list of species labels
        """
        self.species_daughter = species
        self.HAS_SPECIES_DAUGHTER = True
        if lbls != None:
            self.species_labels = lbls
            
    def setVolumeMother(self,volume):
        """
        set the volume mother array
        
        Input:
         - *volume*
        """
        self.volume_mother = volume.reshape(len(volume), 1)
        self.HAS_VOLUME_MOTHER = True

    def setVolumeDaughter(self, volume_selected, volume_notselected):
        """
        set the volume daughter array
        
        Input:
         - *volume*
        """
        self.volume_daughter = volume_selected.reshape(len(volume_selected), 1)
        self.volume_daughter_notselected = volume_notselected.reshape(len(volume_notselected), 1)
        
        self.volume_daughter_all = np.concatenate((self.volume_daughter, self.volume_daughter_notselected))
        self.HAS_VOLUME_DAUGHTER = True         

    def setLabels(self, species):
        """
        Set the species
        
        Input:
         - *species* a list of species labels
        """
        self.species_labels = species

    def setTime(self, time, lbl=None):
        """
        Set the time vector

        Input:
         - *time* a 1d array of time points
         - *lbl* [default=None] is "Time" set as required
        """
        self.time = time.reshape(len(time), 1)
        self.HAS_TIME = True
        if lbl != None:
            self.time_label = lbl
            
    def setXData(self, xdata, lbls=None):
        """
        Sets an array of extra simulation data

        Input:
        - *xdata* an array of xdata vs time
        - *lbls* [default=None] a list of xdata labels
        """
        self.xdata = xdata
        self.HAS_XDATA = True
        if lbls != None:
            self.xdata_labels = lbls

    def setSpeciesMotherDist(self,distributions,means,stds,moments):
        """
        setSpeciesDist stuff for the determination of distributions
        
        Input:
         - *distributions* (list)
         - *means* (dictionary)
         - *stds* (dictionary)
         - *moments* (dictionary) 
        """
        self.species_mother_distributions = distributions
        self.species_mother_means = means
        self.species_mother_standard_deviations = stds
        self.species_mother_moments = moments

    def setSpeciesDaughterDist(self,distributions,means,stds,moments):
        """
        setSpeciesDist stuff for the determination of distributions
        
        Input:
         - *distributions* (list)
         - *means* (dictionary)
         - *stds* (dictionary)
         - *moments* (dictionary)
        """
        self.species_daughter_distributions = distributions
        self.species_daughter_means = means
        self.species_daughter_standard_deviations = stds
        self.species_daughter_moments = moments
        
    def setVolumeMotherDist(self,distributions,means,stds,moments):
        """
        setSpeciesDist stuff for the determination of distributions
        
        Input:
         - *distributions* (list)
         - *means* (dictionary)
         - *stds* (dictionary)
         - *moments* (dictionary)
        """
        self.volume_mother_distributions = distributions
        self.volume_mother_means = means
        self.volume_mother_standard_deviations = stds
        self.volume_mother_moments = moments

    def setVolumeDaughterDist(self,distributions,means,stds,moments):
        """
        setSpeciesDist stuff for the determination of distributions
        
        Input:
         - *distributions* (list)
         - *means* (dictionary)
         - *stds* (dictionary)
         - *moments* (dictionary)
        """
        self.volume_daughter_distributions = distributions
        self.volume_daughter_means = means
        self.volume_daughter_standard_deviations = stds
        self.volume_daughter_moments = moments

    def getTime(self, lbls=False):
        """
        Return the time vector

        Input:
         - *lbls* [default=False] return only the time array or optionally both the time array and time label
        """
        output = None
        if self.HAS_TIME:
            output = self.time.reshape(len(self.time),)
        if not lbls:
            return output
        else:
            return output, [self.time_label]
            
    def setDeterministicData(self,time,volume,ages):
        """
        Set the time and volume arrays
        
        Input:
         - *time* (list)
         - *volume* (list)
         - *ages* (list
        """
        self.time_deterministic = np.array(time,'d').reshape(len(time), 1)
        self.volume_deterministic = np.array(volume,'d').reshape(len(volume), 1)
        self.ages_deterministic = np.array(ages,'d').reshape(len(ages), 1)       
        self.HAS_DETERMINISTIC = True     

    def getSpeciesMother(self, lbls=False):
        """
        Return an array of time+species

        Input:
        - *lbls* [default=False] return only the time+species array or optionally both the data array and a list of column label
        """
        output = None
        if self.HAS_SPECIES_MOTHER:
            length = len(self.species_mother)           # 20-02 prevents unequal sized arrays in the hstack
            output = np.hstack((self.division_times[:length,:], self.species_mother))
            labels = [self.time_label]+self.species_labels
        else:
            output = self.division_times
            labels = [self.time_label]
        if not lbls:
            return output
        else:
            return output, labels
            
    def getSpeciesDaughter(self, lbls=False):
        """
        Return an array of time+species

        Input:
        - *lbls* [default=False] return only the time+species array or optionally both the data array and a list of column label
        """
        output = None
        if self.HAS_SPECIES_DAUGHTER:
            length = len(self.species_daughter)
            output = np.hstack((self.division_times[:length,:], self.species_daughter))
            labels = [self.time_label]+self.species_labels
        else:
            output = self.division_times
            labels = [self.time_label]
        if not lbls:
            return output
        else:
            return output, labels            

    def getVolumeDeterministic(self):
        """ Return an array of time+volume """        
        if self.HAS_DETERMINISTIC:
            #output = np.array(zip(self.time_deterministic, self.volume_deterministic))
            output = np.hstack((self.time_deterministic, self.volume_deterministic))
        else:
            output = self.time_determistic
        return output   
            
    def getVolumeMother(self):
        """ Return an array of time+volume """
        output = None
        if self.HAS_VOLUME_MOTHER:
            length = len(self.volume_mother)
            output = np.hstack((self.division_times[:length,:], self.volume_mother))          
        else:
            output = self.division_times      
        return output
        
    def getVolumeDaughter(self):
        """ Return an array of time+volume """
        output = None
        if self.HAS_VOLUME_DAUGHTER:
            length = len(self.volume_daughter)
            output = np.hstack((self.division_times[:length,:], self.volume_daughter))        
        else:
            output = self.division_times
        return output        

    def getDataAtTime(self, time):
        """
        Return all data generated at "time"

        Input:
         - *time* the required exact time point
        """        
        t = None
        sp = None        
        temp_t = self.time.reshape(len(self.time),)
        for tt in range(len(temp_t)):
            if temp_t[tt] == time:
                t = tt
                if self.HAS_AGES:
                    sp = self.ages.take([tt], axis=0)                
                break

        output = None
        if t is not None:
            output = np.array([[temp_t[t]]])
            if sp is not None:
                output = np.hstack((output,sp))            
        return output
        
    def getMotherDataAtDivisionTime(self, time):
        """
        Return all mother data generated at "time"

        Input:
         - *time* the required exact time point
        """        
        t = None
        spm = None        
        spd = None    
        vm = None    
        vd = None    
        temp_t = self.division_times.reshape(len(self.division_times),)
        for tt in range(len(temp_t)):
            if temp_t[tt] == time:
                t = tt
                if self.HAS_SPECIES_MOTHER:
                    spm = self.species_mother.take([tt], axis=0)
                if self.HAS_VOLUME_MOTHER:
                    vm = self.volume_mother.take([tt], axis=0)
                break

        output = None
        if t is not None:
            output = np.array([[temp_t[t]]])
            if spm is not None:
                output = np.hstack((output,spm))  
            if vm is not None:
                output = np.hstack((output,vm))          
     
        return output
        
    def getDaughterDataAtDivisionTime(self, time):
        """
        Return all daughter data generated at "time"

        Input:
         - *time* the required exact time point
        """
        t = None
        spm = None        
        spd = None    
        vm = None    
        vd = None    
        temp_t = self.division_times[:-1].reshape(len(self.division_times[:-1]),)
        for tt in range(len(temp_t)):
            if temp_t[tt] == time:
                t = tt
                if self.HAS_SPECIES_DAUGHTER:
                    spd = self.species_daughter.take([tt], axis=0)
                if self.HAS_VOLUME_DAUGHTER:
                    vd = self.volume_daughter.take([tt], axis=0)
                break

        output = None
        if t is not None:
            output = np.array([[temp_t[t]]])
            if spd is not None:
                output = np.hstack((output,spd))
            if vd is not None:
                output = np.hstack((output,vd))          
        return output        

    def getDataInTimeInterval(self, time, bounds=None):
        """
        Returns an array of all data in interval: time-bounds <= time <= time+bounds
        where bound defaults to step size

        Input:
         - *time* the interval midpoint
         - *bounds* [default=None] interval half span defaults to step size
        """
        temp_t = self.time.reshape(len(self.time),)
        if bounds == None:
            bounds = temp_t[1] - temp_t[0]
        c1 = (temp_t >= time-bounds)
        c2 = (temp_t <= time+bounds)
        print('Searching ({0}:{1}:{2})'.format(time-bounds, time, time+bounds))

        t = []
        sp = None
        ra = None
        for tt in range(len(c1)):
            if c1[tt] and c2[tt]:
                t.append(tt)
        output = None
        if len(t) > 0:
            output = self.time.take(t)
            output = output.reshape(len(output),1)
            if self.HAS_AGES and self.HAS_TIME:
                output = np.hstack((output, self.ages.take(t, axis=0)))
        return output
