 #! /usr/bin/env python
"""
Stochastic Simulation Module
============================

The main module of StochPy that provides all SSAs, delayed SSAs and single-molecule methods. 

Written by T.R. Maarleveld, Amsterdam, The Netherlands
E-mail: tmd200@users.sourceforge.net
Last Change: October 31, 2014
"""
############################ IMPORTS ################################
from __future__ import division, print_function, absolute_import

import sys,copy,time,os,subprocess,bisect,math,shutil
from io import BytesIO   

try:
    import pickle
except ImportError:
    import cPickle as pickle
    
try: 
    import numpy as np  
except ImportError:
    print("Make sure that the NumPy module is installed")
    print("This program does not work without NumPy")
    print("See http://numpy.scipy.org/ for more information about NumPy")
    sys.exit()

import stochpy
from . import Analysis
from .PyscesMiniModel import RegularGridDataObj
from .PyscesMiniModel import IntegrationStochasticDataObj
from ..tools.Progress_bar import Progress_bar
from ..tools.ParseDistributions import ParseDistributions,convertInput2Indices

try: 
    from . import InterfaceCain    
    IS_STOCHPY_CAIN = True
except ImportError: 
    IS_STOCHPY_CAIN = False
    
try: 
    from . import InterfaceStochKit
    from . import PSC2StochkitXML
    InterfaceStochKit.DeleteExistingData()
    IS_STOCHPY_KIT = True
except ImportError:
    IS_STOCHPY_KIT = False

class SSASettings():
    """   
    Input:
     - *X_matrix* (array)
     - *timesteps* (integer)
     - *starttime* (float)
     - *endtime* (float)
     - *istrackpropensities* (boolean)
     - *useseed* (boolean)
     
    """
    def __init__(self,X_matrix,timesteps,starttime,endtime,speciesselection,istrackpropensities,rateselection,isonlylasttimepoint,useseed):
        self.X_matrix = X_matrix
        self.timesteps = timesteps
        self.starttime = starttime
        self.endtime = endtime
        self.species_selection = speciesselection
        self.IsTrackPropensities = istrackpropensities
        self.rate_selection = rateselection
        self.IsOnlyLastTimepoint = isonlylasttimepoint
        self.UseSeed = useseed

############################ END IMPORTS ############################

class SSA():
    """
    SSA(Method='Direct', File=None, dir=None, Mode='steps', End=1000, Trajectories=1, IsTrackPropensities=False)
    
    Input options:
     - *Method* [default = 'Direct'], Available methods: 'Direct', 'FirstReactionMethod','TauLeaping','Next Reaction Method'
     - *File* [default = ImmigrationDeath.psc]
     - *dir* [default = /home/user/stochpy/pscmodels/ImmigrationDeath.psc]
     - *Mode* [default = 'steps'] simulation for a total number of 'steps' or until a certain end 'time' (string)
     - *End* [default = 1000] end of the simulation (number of steps or end time)   (float)   
     - *Trajectories* [default = 1] (integer)   
     - *TrackPropensities* [default = False] (boolean)
    
    Usage (with High-level functions):
    >>> smod = stochpy.SSA()
    >>> help(smod)
    >>> smod.Model(File = 'filename.psc', dir = '/.../')
    >>> smod.Method('Direct')
    >>> smod.Reload()
    >>> smod.Trajectories(3)
    >>> smod.Timesteps(10000)
    >>> smod.DoStochSim()
    >>> smod.DoStochSim(end=1000,mode='steps',trajectories=5,method='Direct',IsTrackPropensities=True)
    >>> smod.PlotSpeciesTimeSeries()
    >>> smod.PlotPropensitiesTimeSeries()
    >>> smod.PlotAverageSpeciesTimeSeries()
    >>> smod.PlotWaitingtimesDistributions()
    >>> smod.PlotSpeciesDistributions(bin_size = 3)
    >>> smod.PrintSpeciesMeans()
    >>> smod.PrintSpeciesDeviations()
    >>> smod.PrintPropensitiesMeans()
    >>> smod.ShowOverview()
    >>> smod.ShowSpecies()
    >>> smod.DoTestsuite()
    """
    def __init__(self,Method='Direct',File='ImmigrationDeath.psc',dir=None,Mode='steps',End=1000,Trajectories=1,IsTrackPropensities=False,IsInteractive=True,UseSeed=False):
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
        
        self.model_file = File
        self.model_dir = dir
        self.output_dir = output_dir
        self.temp_dir = temp_dir    
        self.sim_end = End
        self.sim_mode = Mode
        self.sim_trajectories = Trajectories    
        self.IsTrackPropensities = IsTrackPropensities
        self._UseSeed = UseSeed
        self._IsSimulationDone = False
        self._IsFixedIntervalMethod = False        
        self._IsOnlyLastTimepoint = False
        self._IsTrajectoriesSetByUser = False
        self._MethodSetBy = "DoStochSim" #8-01-2014
        self._IsModeSetByUser = False
        self._IsEndSetByUser = False
        self._IsDeletePreviousSimulationData = True      
        self._IsCellDivision = False  
        self.HAS_AVERAGE = False
        self.HAS_DELAY_PARAMETERS = False #10-11-2013           
        self.HAS_PUTATIVE_REACTION_TIMES = False 
        self.species_amount_modifications = {}
        self.parameter_value_modifications = {}
        self.Method(Method)
        if IsInteractive:          
          try: 
              Analysis.plt.ion()   # Set on interactive pylab environment              
          except Exception as er:
              print(er)
        else:
          try: 
              Analysis.plt.ioff()  # Set on interactive pylab environment
          except Exception as er:
              print(er) 

    def SetSeeding(self,UseSeed=True):
        self._UseSeed = UseSeed
                            
    def Method(self,method):
        """
        Method(method)
        
        Input:
         - *method* (string)

        Select one of the following methods:    
         - *Direct*
         - *FirstReactionMethod* (FRM)
         - *NextReactionMethod* (NRM)
         - *TauLeaping*
         - *DelayedDirect*
         - *DelayedNextReactionMethod* (DelayedNRM)
         - *SingleMoleculeMethod* (SMM)
         - *FastSingleMoleculeMethod* (fSMM)
         
        Note: input must be a string --> 'Direct' (not case sensitive)
        """
        self._IsTauLeaping = False
        self._IsDelayedMethod = False
        self._IsSingleMoleculeMethod = False
        self._IsNRM = False        
        
        method = method.lower()         # Capital insensitive
        if method == 'direct':
            from ..implementations import DirectMethod
            self.sim_method = DirectMethod.DirectMethod
            print("Info: Direct method is selected to perform stochastic simulations.")
            self.sim_method_name = "Direct"
        elif method in ['firstreactionmethod','frm']:
            from ..implementations import FirstReactionMethod as FRM
            self.sim_method = FRM.FirstReactionMethod
            self.sim_method_name = "FirstReactionMethod"
            print("Info: First Reaction method is selected to perform stochastic simulations.")
        elif method == 'tauleaping':
            from ..implementations import TauLeaping
            self.sim_method = TauLeaping.OTL
            self.sim_method_name = "TauLeaping"
            print("Info: Optimized Tau-Leaping method is selected to perform stochastic simulations.")
            print("Info: User can change the 'epsilon' parameter with DoStochSim(epsilon = 0.01)")
            self._IsTauLeaping = True
        elif method in ['nextreactionmethod','nrm']:
            from ..implementations import NextReactionMethod as NRM
            self.sim_method = NRM.NextReactionMethod 
            print("Info: Next Reaction method is selected to perform stochastic simulations")
            self._IsNRM = True
            self.sim_method_name = "NextReactionMethod"
        elif method in ['delayeddirect','delayed']:
            from ..implementations import DelayedDirectMethod
            self.sim_method = DelayedDirectMethod.DelayedDirectMethod
            print("Info: Delayed Direct Method is selected to perform delayed stochastic simulations.")
            self.sim_method_name = "DelayedDirectMethod"
            self._IsDelayedMethod = True
        elif method in ['delayednextreactionmethod','delayednrm']:
            from ..implementations import DelayedNRM
            self.sim_method = DelayedNRM.DelayedNRM 
            print("Info: Delayed Next Reaction Method is selected to perform delayed stochastic simulations.")
            self.sim_method_name = "DelayedNextReactionMethod"
            self._IsDelayedMethod = True
            self._IsNRM = True       
        elif method in ['singlemoleculemethod','smm']:
            from ..implementations import SingleMoleculeMethod
            self.sim_method = SingleMoleculeMethod.SingleMoleculeMethod
            print("Info: full Single Molecule Method with support for second-order reactions, is selected to perform delayed stochastic simulations.")
            print("*** Warning: The Single Molecule Method assumes that each reaction is described with mass-action kinetics. Use the fSMM if there are non-linear rate equations ***")           
            self.sim_method_name = "SingleMoleculeMethod"            
            self._IsSingleMoleculeMethod = True            
        elif method in ['fastsinglemoleculemethod','fsmm']: 
            from ..implementations import FastSingleMoleculeMethod
            self.sim_method = FastSingleMoleculeMethod.FastSingleMoleculeMethod 
            print("Info: fast Single Molecule Method is selected to perform delayed stochastic simulations.")            
            self.sim_method_name = "FastSingleMoleculeMethod"
            self._IsNRM = True
            self._IsSingleMoleculeMethod = True
        else:
            print("*** WARNING ***: Only valid options are: 'Direct', 'FirstReactionMethod', 'NextReactionMethod','TauLeaping' or 'DelayedDirect', 'DelayedNRM' or 'SMM', 'fSMM'.")
            print("Info: By default, the Direct method is selected")
            from ..implementations import DirectMethod
            self.sim_method = DirectMethod.DirectMethod
            self.sim_method_name = "Direct"            
        
        self.SSA = self.sim_method(self.model_file,self.model_dir)
        for s in self.species_amount_modifications:
            self.ChangeInitialSpeciesAmount(s,self.species_amount_modifications[s])            
        for p in self.parameter_value_modifications: 
            self.ChangeParameter(p,self.parameter_value_modifications[p])
        
        self.data_stochsim = IntegrationStochasticDataObj()   
        self.data_stochsim_grid = RegularGridDataObj()   
        self._IsSimulationDone = False    
        self.HAS_AVERAGE = False   
        self._MethodSetBy = "User"        
      
    def Timesteps(self,s):
        """
        Timesteps(s)
        
        Set the number of time steps to be generated for each trajectory
        
        Input:
         - *s* (integer)
        """      
        try:
            self.sim_end  = abs(int(s))
            self.sim_mode = 'steps'            
            print("Info: The number of time steps is: {0:d}".format(self.sim_end))
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
            self.sim_end = abs(float(t))
            self.sim_mode = 'time'            
            print("Info: The simulation end time is: {0}".format(self.sim_end))
            self._IsEndSetByUser = True
            self._IsModeSetByUser = True
        except ValueError:
            raise ValueError("The end time must be an integer or a float")

    def Trajectories(self,n):
        """
        Trajectories(n)
        
        Set the number of trajectories to be generated
        
        Input:
         - *n* (integer)
        """
        if isinstance(n,int):  
            self.sim_trajectories = n
            self._IsTrajectoriesSetByUser = True
        else:
            raise TypeError("Integer argument expected, got {0}".format(type(n)))     

    def Reload(self):
        """ Reload the entire model again. Useful if the model file has changed """
        self.SSA.Parse(self.model_file,self.model_dir,IsTauLeaping = self._IsTauLeaping, IsNRM = self._IsNRM,IsDelayed = self._IsDelayedMethod, IsSMM = self._IsSingleMoleculeMethod)              
        self._IsSimulationDone = False   
        self.HAS_AVERAGE = False 
        self.data_stochsim = IntegrationStochasticDataObj()       
        self.data_stochsim_grid = RegularGridDataObj()  
        
        self.species_amount_modifications = {}
        self.parameter_value_modifications = {}
        self.sim_trajectories_done = None
        self._current_trajectory = None
        self.sim_species_tracked = None
        self.settings = None

    def Model(self,File,dir=None):
        """
        Model(File,dir=None)
        
        Select model for simulation
              
        Input:
         - *File* (string)
         - *dir* [default = None] (string)
        """      
        if self.HAS_DELAY_PARAMETERS:
            self.HAS_DELAY_PARAMETERS = False
            print('Info: Please mind that the delay parameters have to be set again.')
            self.delay_distr_parameters = None
            self.delay_distributions = None
            self.delayed_nonconsuming = None
            self.delayed_consuming = None
        if self.HAS_PUTATIVE_REACTION_TIMES:
            self.HAS_PUTATIVE_REACTION_TIMES = False
            print('Info: Please mind that the waiting time distributions have to be set again.')
            self._putative_reaction_times_distr_parameters = None
            self._putative_reaction_times = None  
        self.model_file = File
        if dir != None: 
            self.model_dir = dir
        self.Reload()       


    def Mode(self,sim_mode='steps'):
        """
        Mode(sim_mode='steps')
        
        Run a stochastic simulation for until `end` is reached. This can be either time steps or end time (which could be a *HUGE* number of steps).

        Input:
         - *sim_mode* [default = 'steps'] (string) 'time' or 'steps'      
        """
        self.sim_mode = sim_mode.lower()
        if self.sim_mode.lower() not in ['steps','time']:
            print("*** WARNING ***: Mode '{0}' not recognized using: 'steps'".format(sim_mode))
            self.sim_mode = 'steps'        
        self._IsModeSetByUser = True

    def GetTrajectoryData(self,n=1):
        """ 
        GetTrajectryData(n=1)
        
        Switch to another trajectory, by default, the last trajectory is accessible      
        
        Input:
         - *n* [default = 1] (integer)
        """ 
        if isinstance(n,int):
            try:      
                file_in = open(os.path.join(self.temp_dir,'{0}{1:d}.dat'.format(self.model_file,n)),'rb') # rb necessary for Python 3.x
                self.data_stochsim = pickle.load(file_in)
                file_in.close()
            except IOError:
                raise IOError("Trajectory {0:d} does not exist".format(n))                
        else:
            raise TypeError("Integer argument expected, got float")

    def DumpTrajectoryData(self,n):
        """ 
        DumpTrajectoryData(n)
        
        Input:
         - *n* (integer)
        """ 
        if isinstance(n,int):    
            if n == self.data_stochsim.simulation_trajectory:                        
                filename_out = os.path.join(self.temp_dir,'{0}{1:d}.dat'.format(self.model_file,n))                          
                f = open(filename_out,'wb')
                pickle.dump(self.data_stochsim,f)         
                f.close()
            else:
                print("Error: Trajectory {0} is currently not selected/ does not exist".format(n))
        else:
            raise TypeError("Integer argument expected, got float")
            
    def ChangeParameter(self,parameter,value):
        """
        ChangeParameter(parameter,value)  
        
        Change parameter value   
        
        Input:
         - *parameter* (string)
         - *value* (float)
        """
        IsKeyError = False
        if isinstance(parameter,str) and type(value) in [int,float,np.float64,np.float32]:   
            try:
                self.SSA.parse.Mod.__pDict__[parameter]['initial'] = float(value)               
            except KeyError:              
                print("Parameters are: {0}".format(list(self.SSA.parse.Mod.__pDict__)))
                IsKeyError = True
            if not IsKeyError: 
                self.SSA.parse.BuildReactions()
                self.SSA.propensities = copy.deepcopy(self.SSA.parse.propensities)
            if self._IsNRM: # 21-11-2013 For speed improved NRM.
                self.SSA.parse.BuildPropensityCodes()
                self.SSA.propensity_codes = copy.deepcopy(self.SSA.parse.propensity_codes)              
        else:
            print("Error: arguments parameter = string and value = float")
        
        self.parameter_value_modifications[parameter] = value

    def ChangeInitialSpeciesAmount(self,species,value):
        """
        ChangeInitialSpeciesAmount(species,value)     
        
        Change initial species Amount
        
        Input:
         - *species* (string)
         - *value* (float)
        """
        IsKeyError = False
        if isinstance(species,str) and type(value) in [int,float,np.float64,np.float32]:   
            try:
                self.SSA.parse.Mod.__sDict__[species]['initial'] = float(value)
            except KeyError:     
                print("Species are: {0}".format(list(self.SSA.parse.Mod.__sDict__)))
                IsKeyError = True              
            if not IsKeyError:
                if self.SSA.parse.Mod.__sDict__[species]['fixed']: # rebuild reactions and propensities
                    self.SSA.parse.BuildReactions()
                    self.SSA.propensities = copy.deepcopy(self.SSA.parse.propensities)
                self.SSA.parse.BuildX()     
                self.SSA.X_matrixinit = copy.deepcopy(self.SSA.parse.X_matrix.transpose()[0])
        else:
            print("Error: species argument must be a string and value argument must be a float or integer") 
        
        self.species_amount_modifications[species] = value        
    
        
    def DoStochKitStochSim(self,endtime=100,frames=10000,trajectories=False,IsTrackPropensities=False,customized_reactions=None,solver=None,keep_stats = False,keep_histograms = False):
        """
        DoStochKitStochSim(endtime=100,frames=10000,trajectories=False,IsTrackPropensities=False,customized_reactions=None,solver=None,keep_stats = False,keep_histograms = False)
        
        Do Stochastic simulations with StochKit in StochPy
        Make sure that the input file contains net stoichiometric coefficients
        
        Input:
         - *endtime* [default = 100] (float)
         - *frames* [default = 10000] (integer)
         - *trajectories* [default = False] (integer)
         - *IsTrackPropensities* [default = False] (boolean)
         - *customized_reactions* [default=None] (list of strings)
         - *solver* [default = None] (string)
         - *keep_states* [default = False] (boolean)
         - *keep_histograms* [default = False) (boolean)
        """
        assert IS_STOCHPY_KIT,"StochKit and/or InterfaceStochKit is not installed or the directories in InterfaceStochKit.ini are incorrect"        
        if IS_STOCHPY_KIT:               
            self.DeleteTempfiles() # Delete '.dat' files
            print("*** WARNING ***: Do not use net stoichiometric coefficients for fixed-interval output solvers. Use X > {2}  in stead of $pool > X")
            if isinstance(frames,int):            
                pass
            elif type(frames) in [float,np.float64,np.float32]:
                print("*** WARNING ***: 'frames' must be an integer rather than a float; float {0} is rounded to {1:d}".format(frames,int(frames)))
                frames = int(frames) 
            else:
                print("Error: 'frames' must be an integer")
                sys.exit()   
            
            self.data_stochsim = IntegrationStochasticDataObj()
            self.data_stochsim_grid = RegularGridDataObj()
            
            self._IsOnlyLastTimepoint = False
            self._IsFixedIntervalMethod = True
            self._IsSimulationDone = False
            self.IsTrackPropensities = IsTrackPropensities
            if self.IsTrackPropensities:
                self.sim_rates_tracked = copy.copy(self.SSA.rate_names) 
            self.HAS_AVERAGE = False          
            if trajectories != False:
                self.Trajectories(trajectories)             
                self._IsTrajectoriesSetByUser = False
            elif trajectories == False and self.sim_trajectories != 1 and not self._IsTrajectoriesSetByUser:
                    self.Trajectories(1)
            if customized_reactions != None:
                for r_id in customized_reactions:
                    r_index = self.SSA.rate_names.index(r_id)
                    self.SSA.parse.rate_eqs[r_index]['stochtype'] = 'customized'
                    
            assert not self.SSA.parse.Mod.__HAS_ASSIGNMENTS__, "StochKit solvers do not support assignments. Use the StochPy solvers DoStochSim()"          
   
            if solver == None:                  
                solver = InterfaceStochKit.STOCHKIT_SOLVER # use the default solver
            
            t1 = time.time()
            stochkit_model_filename = self.model_file.split('.')[0]+'_stochkit.xml'
            doc = PSC2StochkitXML.xml_createStochKitDoc(self.SSA)
            PSC2StochkitXML.xml_viewStochKitXML(doc,fname=os.path.join(self.temp_dir,stochkit_model_filename))          
            stochkit_model_filename_path = os.path.join(self.temp_dir, stochkit_model_filename)            
            stochkit_keep_stats = keep_stats
            stochkit_keep_histograms = keep_histograms
            stochkit_keep_trajectories = True
            stochkit_cmd = "-m {0} -t {1} -r {2} -i {3} --label -f".format(stochkit_model_filename_path,endtime,self.sim_trajectories ,frames)
            if not stochkit_keep_stats:
                stochkit_cmd += " --no-stats"
            if stochkit_keep_histograms:
                stochkit_cmd += " --keep-histograms"
            if stochkit_keep_trajectories:
                stochkit_cmd += " --keep-trajectories"
            stochkit_cmd += " --out-dir {0}".format(os.path.join(InterfaceStochKit.STOCHKIT_WORK_DIR,stochkit_model_filename))
            #print stochkit_cmd            
            if self.sim_trajectories == 1:                  
                print("Info: {0:d} trajectory is generated until t = {1} with {2:d} frames".format(self.sim_trajectories,endtime,frames))
            else:                  
                print("Info: {0:d} trajectories are generated until t = {1} with {2:d} frames".format(self.sim_trajectories,endtime,frames))    
            try: 
                solver_path = os.path.join(InterfaceStochKit.STOCHKIT_SOLVER_DIR, solver)                
                #rcode = subprocess.call([solver_path, stochkit_cmd]) 
                _string ='{0:s} {1:s}'.format(solver_path,stochkit_cmd)
                rcode = subprocess.call(_string.split())
                IsSimulation = True
            except Exception as er:
                print(er)
                print(solver_path)
                IsSimulation = False
                                     
            if IsSimulation:    
                t2 = time.time()    
                self.simulation_time = t2-t1              
                print("Info: Simulation time including compiling {0:1.5f}".format(self.simulation_time))
                if self.IsTrackPropensities:
                    print("Info: Parsing data to StochPy and calculating propensities and distributions ...")
                else:
                    print("Info: Parsing data to StochPy and calculating distributions ...")
                self.data_stochsim = InterfaceStochKit.GetStochKitOutput(stochkit_model_filename,self.SSA,self.model_file,endtime,self.sim_trajectories,frames,self.IsTrackPropensities)              
                self.sim_species_tracked = copy.copy(self.SSA.species_names)    
                self.sim_trajectories_done = copy.copy(self.sim_trajectories)
                try:
                    self.plot = Analysis.DoPlotting(self.data_stochsim.species_labels,self.SSA.rate_names,self.plot.plotnum)
                except:
                    self.plot = Analysis.DoPlotting(self.data_stochsim.species_labels,self.SSA.rate_names)
                self._IsSimulationDone = True
                print("Info: Data successfully parsed into StochPy")
       
    def DoCainStochSim(self,endtime=100,frames=10000,trajectories=False,solver="HomogeneousDirect2DSearch",IsTrackPropensities=False):
        """      
        DoCainStochSim(endtime=100,frames=10000,trajectories=False,solver="HomogeneousDirect2DSearch",IsTrackPropensities=False)
        
        Use Cain implementations for fixed-interval output stochastic simulations (www.cacr.caltech.edu/~sean/cain/DeveloperFile)
        Make sure that the input file contains net stoichiometric coefficients
        
        Input:
         - *endtime* [default = 100](float)
         - *frames* [default = 10000] (integer)
         - *trajectories* [default = False] (integer)
         - *solver* [default = HomogeneousDirect2DSearch] (string)
         - *IsTrackPropensities* [default = False] (boolean)
        """     
        assert IS_STOCHPY_CAIN, "InterfaceCain is not installed"      
        if IS_STOCHPY_CAIN:
            print("*** WARNING ***: Only mass-action kinetics can be correctly parsed by the Cain solvers")          
            self.DeleteTempfiles() # Delete '.dat' files
            print("*** WARNING ***: Do not use net stoichiometric coefficients for fixed-interval output solvers. Use X > {2} in stead of $pool > X")
            if isinstance(frames,int):
                pass
            elif type(frames) in [float,np.float64,np.float32]:
                print("*** WARNING ***: 'frames' must be an integer rather than a float; float {0} is rounded to {1:d}".format(frames,int(frames)))
                frames = int(frames) 
            else:
                print("Error: 'frames' must be an integer")
                sys.exit()             

            self.data_stochsim = IntegrationStochasticDataObj()
            self.data_stochsim_grid = RegularGridDataObj()         
        
            self._IsOnlyLastTimepoint = False
            self._IsFixedIntervalMethod = True
            self.IsTrackPropensities = IsTrackPropensities
            if self.IsTrackPropensities:
                self.sim_rates_tracked = copy.copy(self.SSA.rate_names)    
            self.HAS_AVERAGE = False  
            self._IsSimulationDone = False          
            if trajectories != False:
                self.Trajectories(trajectories)
                self._IsTrajectoriesSetByUser = False
            elif trajectories == False and self.sim_trajectories != 1 and not self._IsTrajectoriesSetByUser:
                self.Trajectories(1)
                      
            assert not self.SSA.parse.Mod.__HAS_EVENTS__, "Cain solvers do not support events. Use the StochPy solvers DoStochSim()"               
            assert not self.SSA.parse.Mod.__HAS_ASSIGNMENTS__, "Cain solvers do not support assignments. Use the StochPy solvers DoStochSim()"
            ### Parse model to CAIN ###
            mersenne_twister_data = InterfaceCain.getCainInputfile(self.SSA,endtime,frames,self.sim_trajectories)            
            cain_cmd_filename = 'cain_in.txt'
            cmd_file = open(os.path.join(self.temp_dir, cain_cmd_filename), 'rb')
            cain_cmd = cmd_file.read()
            cmd_file.close()
            ###########################
            
            try:
                if (os.sys.platform == 'win32') and (not solver.endswith('.exe')):
                    solver = solver.split('.')[0] + '.exe'                 
                solver_path = os.path.join(InterfaceCain.CAIN_SOLVER_PATH,solver)  
                proc = subprocess.Popen(os.path.join(InterfaceCain.CAIN_SOLVER_PATH,solver),stdin=subprocess.PIPE,stdout=subprocess.PIPE) 
                IsFoundSolver = True
            except Exception as er:
                print(er)
                print(solver_path)
                IsFoundSolver = False    
            
            if IsFoundSolver:
                if self.sim_trajectories == 1:                  
                    print("Info: {0:d} trajectory is generated until t = {1} with {2:d} frames".format(self.sim_trajectories,endtime,frames))
                else:                  
                    print("Info: {0:d} trajectories are generated until t = {1} with {2:d} frames".format(self.sim_trajectories,endtime,frames))
                t1 = time.time()     
                stdout_values = proc.communicate(cain_cmd)[0]              
                t2 = time.time() 
                self.simulation_time = t2-t1            
                print("Info: Simulation time {0:1.5f}".format(self.simulation_time))
                if self.IsTrackPropensities:
                    print("Info: Parsing data to StochPy and calculating propensities and distributions ...")
                else:
                    print("Info: Parsing data to StochPy and calculating distributions ...")                    
                
                self.data_stochsim = InterfaceCain.getCainOutput2StochPy(BytesIO(stdout_values).readlines() ,mersenne_twister_data,self.SSA,self.model_file,endtime,self.sim_trajectories,frames,self.IsTrackPropensities)              
                self.sim_species_tracked = copy.copy(self.SSA.species_names)    
                self.sim_trajectories_done = copy.copy(self.sim_trajectories)
                try: 
                    self.plot = Analysis.DoPlotting(self.data_stochsim.species_labels,self.SSA.rate_names,self.plot.plotnum)
                except:
                    self.plot = Analysis.DoPlotting(self.data_stochsim.species_labels,self.SSA.rate_names)
                self._IsSimulationDone = True
                print("Info: Data successfully parsed into StochPy")
    
    def DoStochSim(self,end=False,mode=False,method=False,trajectories=False,epsilon = 0.03,IsTrackPropensities=False, rate_selection = None, species_selection = None,IsOnlyLastTimepoint = False,critical_reactions=[],reaction_orders = False,species_HORs = False,species_max_influence = False):
        """
        DoStochSim(end=10, mode='steps', method='Direct', trajectories=1, epsilon=0.03,IsTrackPropensities=False,critical_reactions=[])

        Run a stochastic simulation for until `end` is reached. This can be either time steps or end time (which could be a *HUGE* number of steps).

        Input:
         - *end* [default=1000] simulation end (steps or time)
         - *mode* [default='steps'] simulation mode, can be one of:
           - *steps* (string) total number of steps to simulate
           - *time* (string) simulate until time is reached
         - *method* [default='Direct'] stochastic algorithm (Direct, FRM, NRM, TauLeaping)
         - *trajectories* [default = 1] number of trajectories
         - *epsilon* [default = 0.03] parameter for Tau-Leaping
         - *IsTrackPropensities* [default = False]
         - *rate_selection* [default = None] List of names of rates to store. This saves memory space and prevents Memory Errors when propensities propensities are tracked
         - *species_selection* [default = None] List of names of species to store. This saves memory space and prevents Memory Errors (occurring at ~15 species).
         - *IsOnlyLastTimepoint* [default = False]
         - *critical_reactions* [default = [] ] (list) ONLY for the tau-leaping method where the user can pre-define reactions that are "critical". Critical reactions can fire only once per time step.
         - *reaction_orders* [default = [] (list) ONLY for the tau-leaping method 
         - *species_HORs* [default = []  (list) ONLY for the tau-leaping method 
         - *species_max_influence* [default = []  (list) ONLY for the tau-leaping method 
        """
        if species_selection and isinstance(species_selection,str):   
            species_selection = [species_selection]
        if species_selection and isinstance(species_selection,list): 
            for s_id in species_selection:
                assert s_id in self.SSA.species_names, "Species {0} is not in the model or earlier specified species selection".format(s_id)
        
        self.IsTrackPropensities = IsTrackPropensities
        if rate_selection and isinstance(rate_selection,str):   
            rate_selection = [rate_selection]
            self.IsTrackPropensities = True
        if rate_selection and isinstance(rate_selection,list): 
            for r_id in rate_selection:
                assert r_id in self.SSA.rate_names, "Reaction {0} is not in the model or earlier specified reaction selection".format(r_id)
            self.IsTrackPropensities = True
               
        self._IsOnlyLastTimepoint = IsOnlyLastTimepoint
        if mode != False:
            self.Mode(sim_mode = mode) 
            self._IsModeSetByUser = False
        elif mode == False and self.sim_mode != 'steps' and not self._IsModeSetByUser:
            self.Mode('steps')
        if end != False:    
            if type(end) in [int,float,np.float64,np.float32]: 
                self.sim_end = end   
            else:
                print("*** WARNING ***: 'end' should be an integer or float\n 1000 is used by default")
                self.sim_end = 1000   
            self._IsEndSetByUser=False
        elif end == False and self.sim_end != 1000 and not self._IsEndSetByUser:
            self.sim_end = 1000

        self.data_stochsim = IntegrationStochasticDataObj()
        self.data_stochsim_grid = RegularGridDataObj()  
        
        if method != False: 
            self.Method(method)
            self._MethodSetBy = "DoStochSim"
        elif method == False and self.sim_method_name != "Direct" and self._MethodSetBy == "DoStochSim":
            self.Method("Direct")
        
        # If DoStochSim not called from DoDelayedStochSim, the method should never be delayed.
        if (self._IsDelayedMethod or self._IsSingleMoleculeMethod) and self._MethodSetBy != "Script": # 08-01-2014
            print("*** WARNING ***: ({0:s}) was selected. Switching to the normal Direct Method.".format(self.sim_method_name))
            self.Method('Direct')
            self._MethodSetBy = "DoStochSim"
        
        if reaction_orders != False:
            print("Info: reaction orders {0} replaced with {1}".format(self.SSA.parse.reaction_orders, reaction_orders))
            self.SSA.parse.reaction_orders = reaction_orders
        if species_HORs != False:
            self.SSA.parse.species_HORs = species_HORs
            print("Info: species HORs {0} replaced with {1}".format(self.SSA.parse.species_HORs, species_HORs))
        if species_max_influence != False:
            self.SSA.parse.species_max_influence = species_max_influence
            print("Info: species max influence {0} replaced with {1}".format(self.SSA.parse.species_max_influence, species_max_influence))
                
        if trajectories != False: 
            self.Trajectories(trajectories)                        
            self._IsTrajectoriesSetByUser = False
        elif trajectories == False and self.sim_trajectories != 1 and not self._IsTrajectoriesSetByUser:
            self.Trajectories(1)        
        
        self._IsFixedIntervalMethod = False      
        self.HAS_AVERAGE = False      
        if self._IsDeletePreviousSimulationData:
           self.DeleteTempfiles()  # Delete '.dat' files
      
        if self.sim_trajectories == 1:
            print("Info: 1 trajectory is generated")
        else:      
            print("Info: {0:d} trajectories are generated".format(self.sim_trajectories))
            print("Info: Time simulation output of the trajectories is stored at {0:s} in directory: {1:s}".format(self.model_file[:-4]+'(trajectory).dat',self.temp_dir))
        
        progressBar = Progress_bar(cycles_total = self.sim_trajectories, done_msg = 'time')  ##Progress bar addition## Shows Simulation time afterwards
        for self._current_trajectory in range(1,self.sim_trajectories+1):
            if self.sim_trajectories > 1:
               IsStatusBar = False
            else:
               IsStatusBar = True
               t1 = time.time() 
            
            if self.sim_mode.lower() == 'time':
                self.settings = SSASettings(X_matrix=self.SSA.X_matrixinit,timesteps=10**50,starttime=0,endtime=self.sim_end, speciesselection=species_selection,istrackpropensities=self.IsTrackPropensities,rateselection = rate_selection,isonlylasttimepoint=IsOnlyLastTimepoint,useseed = self._UseSeed)              
            elif self.sim_mode.lower() == 'steps':
                self.settings = SSASettings(X_matrix=self.SSA.X_matrixinit,timesteps=self.sim_end,starttime=0,endtime=10**50, speciesselection=species_selection,istrackpropensities=self.IsTrackPropensities,rateselection = rate_selection,isonlylasttimepoint=IsOnlyLastTimepoint,useseed = self._UseSeed)               
            else:
                print("*** WARNING ***: Simulation mode should be 'time' or 'steps'. Steps is done by default")
                self.settings = SSASettings(X_matrix=self.SSA.X_matrixinit,timesteps=self.sim_end,starttime=0,endtime=10**50, speciesselection=species_selection,istrackpropensities=self.IsTrackPropensities,rateselection = rate_selection,isonlylasttimepoint=IsOnlyLastTimepoint,useseed = self._UseSeed) 
                
            if self.sim_method_name.lower() == "tauleaping":    
                self.SSA.Execute(self.settings,IsStatusBar,epsilon,critical_reactions)
            else:
                self.SSA.Execute(self.settings,IsStatusBar)

            self.data_stochsim = IntegrationStochasticDataObj()         
                  
            self.FillDataStochsim()          
            if self.sim_trajectories == 1:
                print("Info: Number of time steps {0:d} End time {1}".format(self.SSA.timestep,self.SSA.sim_t))
            elif self.sim_trajectories > 1:                
                self.DumpTrajectoryData(self._current_trajectory)
                progressBar.update() #Progress bar addition, only for multiple trajectories#
               
        self._IsSimulationDone = True      
        self.sim_trajectories_done = copy.copy(self.sim_trajectories)
        try: 
            self.plot = Analysis.DoPlotting(self.data_stochsim.species_labels,self.sim_rates_tracked,self.plot.plotnum)
        except:
            self.plot = Analysis.DoPlotting(self.data_stochsim.species_labels,self.sim_rates_tracked)
        if IsStatusBar:
            t2 = time.time()          
            self.simulation_time = t2-t1
            print("Info: Simulation time {0:1.5f}".format(self.simulation_time))
        else:
            self.simulation_time = progressBar.end_time - progressBar.t1            
        if IsOnlyLastTimepoint:
            print('Info: not enough data points (are stored) to determine statistics.')        
            
    def SetDelayParameters(self, delay_distributions, nonconsuming_reactions = None):
        """
        Input delayed model parameters. This function subsequently parses the delay input and assigns it to the SSA method. 
        
        Example: 
        SetDelayParameters(delay_distributions = {'R1':('fixed',3), 'R2':('gamma',5,1)}, nonconsuming_reactions = ['R2'])
          - Reaction 'R1' will get a delay of 3 time units and reaction 'R2' a random delay from a gamma distr with shape=5 and scale=1.
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
        # Parse the distribution dictionary to two dictionaries. These have reaction indices as keys and values are resp. distribution functions and parameter lists.
        self.delay_distributions, self.delay_distr_parameters = ParseDistributions(delay_distributions, self.SSA.rate_names)  # use all rate names, because this is done before the simulation starts
        delayed_reactions = list(self.delay_distributions)        
        if nonconsuming_reactions == None:              # ==None to recognize 0 as reaction index.
            self.delayed_nonconsuming = []
            self.delayed_consuming = delayed_reactions  # All reactions consuming            
        else:                                           # Nonconsuming reactions supplied
            self.delayed_nonconsuming = convertInput2Indices(nonconsuming_reactions, self.SSA.rate_names)           
            self.delayed_nonconsuming = [r for r in self.delayed_nonconsuming if r in delayed_reactions] # Selects nonconsuming reactions that have a delay distribution.
            self.delayed_consuming = list(set(delayed_reactions) - set(self.delayed_nonconsuming)) # Selects consuming reactions by: all_reaction - nonconsuming     
                                        
        self.HAS_DELAY_PARAMETERS = True

    def DoDelayedStochSim(self, end=False, mode=False, method=False, trajectories=False, IsTrackPropensities=False, rate_selection = None, species_selection = None, IsOnlyLastTimepoint = False):
        """
        DoDelayedStochSim(end=100, mode='steps', method='DelayedDirect', trajectories=1, IsTrackPropensities=False, species_selection = None)    
        Run a stochastic simulation with delayed reactions until `end` is reached. This can be either time steps or end time (which could be a *HUGE* number of steps).

        Input:
         - *end* [default=1000] simulation end (steps or time)
         - *mode* [default='steps'] simulation mode, can be one of:
           - *steps* (string) total number of steps to simulate
           - *time* (string) simulate until time is reached
         - *method* [default='Delayeddirect'] stochastic algorithm (DelayedDirect, DelayedNRM)
         - *trajectories* [default = 1] number of trajectories
         - *IsTrackPropensities* [default = False]
         - *rate_selection* [default = None] List of names of rates to store. This saves memory space and prevents Memory Errors when propensities propensities are tracked
         - *species_selection* [default = None] List of names of species to store. This saves memory space and prevents Memory Errors (occurring at ~15 species).
         - *IsOnlyLastTimepoint* [default = False]
        """
        if method != False: 
            self.Method(method)
            self._MethodSetBy = "DoStochSim"
        elif self._MethodSetBy == "DoStochSim" and self.sim_method_name != "DelayedDirectMethod":
            self.Method("DelayedDirect")  # Default
        
        if not self._IsDelayedMethod:
            print("*** WARNING ***: an invalid method ({0}) was selected. Switching to the Delayed Direct Method.".format(self.sim_method_name))
            self.Method('DelayedDirect')  # = Default delayed method      
        
        if self.HAS_DELAY_PARAMETERS:
            # Pass delay parameters to delayed SSA implementation.
            self.SSA.distr_functions        = copy.copy(self.delay_distributions)
            self.SSA.distr_parameters       = copy.copy(self.delay_distr_parameters)
            self.SSA.reactions_Consuming    = copy.copy(self.delayed_consuming)
            self.SSA.reactions_NonConsuming = copy.copy(self.delayed_nonconsuming)
        else:
            raise AttributeError("No delay parameters have been set for the model '{0:s}'. Please first use the function .SetDelayParameters().".format(self.model_file)) #7-1-2014 exit if no delay parameters
        
        # Specify that delayed method is set by this script. Prevents DoStochSim to select other method.
        temp_MethodSetBy = self._MethodSetBy #Either "User" or "DoStochSim"
        self._MethodSetBy = "Script"    
        
        #Perform Stochastic Simulation with given settings and method selected in
        self.DoStochSim(end=end, mode=mode, method=False, trajectories=trajectories, IsTrackPropensities=IsTrackPropensities, rate_selection = rate_selection, species_selection = species_selection, IsOnlyLastTimepoint = IsOnlyLastTimepoint)
        
        # Reset to original value
        self._MethodSetBy = temp_MethodSetBy
        if IsOnlyLastTimepoint:
            print('Info: not enough data points (are stored) to determine statistics.')    
    
    def SetPutativeReactionTimes(self, distributions):
        """
        Sets the single molecule putative reaction times distribution. For use with DoSingleMoleculeStochSim().
        
        Inputs:
          - *distributions* (dictionary), Dictionary of reaction name (or index) as key and distribution as value.
          
          Value of *distributions* can be any distribution of numpy.random, e.g.:
          - ('gamma', p1,p2) = np.random.gamma(p1,p2) #Where p1 is the shape parameter and p2 the scale parameter.
          - ('exponential', p1) = np.random.exponential(p1) #Where p1 is the scale parameter (NOT the rate).
          - ('uniform', lower, upper) = np.random.uniform(0,lower,upper)
        """        
        self._putative_reaction_times, self._putative_reaction_times_distr_parameters = ParseDistributions(distributions, self.SSA.rate_names) 
        self.HAS_PUTATIVE_REACTION_TIMES = True
    
    def DoSingleMoleculeStochSim(self, end=False, mode=False, method=False, trajectories=False, species_selection = None, IsOnlyLastTimepoint = False):
        """
        DoSingleMoleculeStochSim(end=100, mode='steps', method='SingleMoleculeMethod', trajectories=1, IsTrackPropensities=False)         
        Run a single molecule stochastic simulation until `end` is reached. This can be either time steps or end time (which could be a *HUGE* number of steps).

        Input (similar to .DoStochSim()):
         - *end* [default=1000] simulation end (steps or time)
         - *mode* [default='steps'] simulation mode, can be one of:
           - *steps* (string) total number of steps to simulate
           - *time* (string) simulate until time is reached
         - *method* [default='SingleMoleculeMethod'] stochastic algorithm, can be one of:
           - SingleMoleculeMethod or SMM
           - FastSingleMoleculeMethod or fSMM
         - *trajectories* [default = 1] number of trajectories         
         - *species_selection* [default = None] List of names of species to store. This saves memory space and prevents Memory Errors.
         - *IsOnlyLastTimepoint* [default = False]
        """     
        # Check whether waiting time distributions were given.
        if not self.HAS_PUTATIVE_REACTION_TIMES:
            raise Warning("No distributions have been set for the model '{0:s}'. Please first use the function .SetPutativeReactionTimes().".format(self.model_file))
        
        if method != False: 
            self.Method(method)
            self._MethodSetBy = "DoStochSim"
        elif self._MethodSetBy == "DoStochSim" and self.sim_method_name != "FastSingleMoleculeMethod":
            self.Method("fSMM") # Default method
        
        if not self._IsSingleMoleculeMethod:
            print("*** WARNING ***: an invalid method ({0}) was selected. Switching to the fast Single Molecule Method.".format(self.sim_method_name))
            self.Method('fSMM')
        
        if self.sim_method_name == "FastSingleMoleculeMethod" and 2 in [self.SSA.parse.reaction_orders[j] for j in self._putative_reaction_times]:
            print("Info: Second-order reactions are not supported by the fSMM. Switching to the SMM.")
            self.Method('SMM') 

        # Pass delay parameters to SingleMolecule SSA implementation.
        self.SSA.distr_functions  = copy.copy(self._putative_reaction_times)
        self.SSA.distr_parameters = copy.copy(self._putative_reaction_times_distr_parameters)                    

        #If Single Molecule Method, set exponential distributions to reactions not specified in self._putative_reaction_times.
        if self.sim_method_name == 'SingleMoleculeMethod':# and len(self.SSA.distr_functions) < self.SSA.n_reactions:
            self.SSA.auto_exponential_reactions = []
            #print("\nUsing exponential waiting time distributions for:")          
            for j in range(self.SSA.n_reactions):
                if j not in self.SSA.distr_functions:                       # Don't replace already assigned distributions.
                    self.SSA.distr_functions[j] = np.random.exponential
                    self.SSA.distr_parameters[j] = np.nan                   # 31-03-2014 To be specified at start of simulation (self.SSA.EvaluatePropensities)
                    self.SSA.auto_exponential_reactions.append(j)           # 31-03-2014
       
        # Specify that delayed method is set by the script here. Prevents DoStochSim to select other method.
        temp_MethodSetBy = self._MethodSetBy # Either "User" or "DoStochSim"
        self._MethodSetBy = "Script"           
        
        if self.IsTrackPropensities:
            print("*** WARNING ***: Propensities cannot be tracked with the single molecule method")
            self.IsTrackPropensities = False
        
        self.DoStochSim(end=end, mode=mode, method=False, trajectories=trajectories, IsTrackPropensities=False, species_selection = species_selection, IsOnlyLastTimepoint = IsOnlyLastTimepoint)
        self._MethodSetBy = "DoStochSim"     # RESET
        
        # Reset to original value
        self._MethodSetBy = temp_MethodSetBy
        if IsOnlyLastTimepoint:
            print('Info: not enough data points (are stored) to determine statistics.')

    def DoCompleteStochSim(self, error = 0.001, size=100000,IsTrackPropensities=False, rate_selection=None, species_selection = None):
        """      
        DoCompleteStochSim(error = 0.001, size=100000,IsTrackPropensities=False)
        
        Do a stochastic simulation until the first four moments converge (in development, beta-status)
        
        Input:
         - *error* maximal allowed error [default = 0.001]
         - *size* (integer) number of steps before checking the first four moments [default = 100000]
         - *IsTrackPropensities* [default = False]
         - *rate_selection* [default = None] List of names of rates to store. This saves memory space and prevents Memory Errors when propensities propensities are tracked
         - *species_selection* [default = None] List of names of species to store. This saves memory space and prevents Memory Errors (occurring at ~15 species).         
        """
        if species_selection and isinstance(species_selection,str):   
            species_selection = [species_selection]
        if species_selection and isinstance(species_selection,list): 
            for s_id in species_selection:
                assert s_id in self.SSA.species_names, "Species {0} is not in the model or earlier specified species selection".format(s_id)
        
        self.IsTrackPropensities = IsTrackPropensities       
        if rate_selection and isinstance(rate_selection,str):   
            rate_selection = [rate_selection]
            self.IsTrackPropensities = True
        if rate_selection and isinstance(rate_selection,list): 
            for r_id in rate_selection:
                assert r_id in self.SSA.rate_names, "Reaction {0} is not in the model or earlier specified reaction selection".format(r_id)
            self.IsTrackPropensities = True

        self.Trajectories(1)                
        self._IsFixedIntervalMethod = False
        self.HAS_AVERAGE = False      
        self.DeleteTempfiles()    # Delete '.dat' files   
        
        self._current_trajectory = 1
        t1 = time.time()
        self.settings = SSASettings(X_matrix=self.SSA.X_matrixinit,timesteps=size,starttime=0,endtime=10**50, speciesselection=species_selection,istrackpropensities=self.IsTrackPropensities,rateselection = rate_selection,isonlylasttimepoint=False,useseed = self._UseSeed)      
        self.SSA.Execute(self.settings)     
        if self.settings.species_selection:   
            self.sim_species_tracked = [s_id for s_id in self.settings.species_selection]
        else:
            self.sim_species_tracked = copy.copy(self.SSA.species_names)           
                        
        (L_probability_mass, D_means, D_stds,D_moments) = Analysis.GetDataDistributions(self.SSA.sim_output,self.sim_species_tracked)      
        m1 = [np.array(list(D_moments[s_id].values())) for s_id in self.sim_species_tracked]      
        IsContinue = True
        print('Info: {0:d} time steps simulated'.format(size))
        n=1      
        while IsContinue:          
            self.settings = SSASettings(X_matrix=self.SSA.X_matrixinit,timesteps=size*(n+1),starttime=self.SSA.sim_t,endtime=10**50, speciesselection=species_selection,istrackpropensities=self.IsTrackPropensities,rateselection = rate_selection,isonlylasttimepoint=False,useseed = self._UseSeed)      
            self.SSA.Execute(self.settings)
            (L_probability_mass,D_means,D_stds,D_moments) = Analysis.GetDataDistributions(self.SSA.sim_output,self.sim_species_tracked)          
            m2 = [np.array(list(D_moments[s_id].values())) for s_id in self.sim_species_tracked] 
            max_total = 0
            for i in range(self.SSA.n_species): 
                max_s = abs(1-(m2[i]/m1[i])).max()
                if max_s > max_total:
                     max_total = max_s          
            m1 = copy.deepcopy(m2)  
            n+=1
            print('Info: {0:d} time steps simulated'.format(n*size))
            if max_total < error:
                IsContinue = False                  
        t2 = time.time()
        self.simulation_time = t2-t1
        print("Info: Simulation time {0:1.5f}".format(self.simulation_time))
        self.FillDataStochsim()
        self._IsSimulationDone = True
        self.sim_trajectories_done = copy.copy(self.sim_trajectories)
        try:
            self.plot = Analysis.DoPlotting(self.data_stochsim.species_labels,self.sim_rates_tracked,self.plot.plotnum)
        except:
            self.plot = Analysis.DoPlotting(self.data_stochsim.species_labels,self.sim_rates_tracked)            
            
    def _getSpecies2Plot(self,species2plot):
        """ *** For internal use only ***: this function determines the species for which we will plot something """
        if species2plot == True:
            species2plot = self.sim_species_tracked
        if isinstance(species2plot,str):
            species2plot = [species2plot]    
        for s_id in species2plot:          
            assert s_id in self.sim_species_tracked, "Species {0} is not in the model or earlier specified species selection".format(s_id)
        return species2plot    
        
    def _getRates2Plot(self,rates2plot):
        """ *** For internal use only ***: this function determines the reactions for which we will plot something """
        if rates2plot == True:
            rates2plot = self.sim_rates_tracked
        if isinstance(rates2plot,str):
            rates2plot = [rates2plot]    
        for r_id in rates2plot:
            assert r_id in self.sim_rates_tracked, "Reaction {0} is not in the model or earlier specified reaction selection".format(r_id)
        return rates2plot
               
    def PlotSpeciesTimeSeries(self,n_events2plot = 10000,species2plot = True,linestyle = 'solid',linewidth = 1,marker = '',colors = None,title = 'StochPy Species Time Series Plot',xlabel='Time',ylabel='Copy Number',IsLegend=True,legend_location='upper right'):
        """
        PlotSpeciesTimeSeries(n_events2plot = 10000,species2plot = True,linestyle = 'solid',linewidth = 1, marker = '',colors = None,title = 'StochPy Species Time Series Plot',xlabel='Time',ylabel='Copy Number',IsLegend=True,legend_location='upper right')
        
        Plot time simulation output for each generated trajectory
        Default: PlotSpeciesTimeSeries() plots time simulation for each species

        Input:
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
         - *legend_location* [default = 'upper right'] (string/integer)
        """      
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"
        assert self._IsSimulationDone, "Before plotting time simulation results first do a stochastic simulation"
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
           
        species2plot = self._getSpecies2Plot(species2plot)
                      
        if str(n_events2plot).lower() == 'all':
                n_events2plot = self.data_stochsim.simulation_timesteps        
        for n in range(1,self.sim_trajectories_done+1):    
            if self.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            self.plot.TimeSeries(self.data_stochsim.getSpecies(),n_events2plot,species2plot,self.data_stochsim.species_labels,n-1,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location) # Plot time sim
        self.plot.plotnum+=1

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
         - *legend_location* [default = 'upper right'] (string/integer)
        """
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"
        assert self._IsSimulationDone and self.IsTrackPropensities, "Before plotting propensities first do a stochastic simulation with tracking propensities (use the IsTrackPropensities flag in DoStochSim)"
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"        
        
        rates2plot = self._getRates2Plot(rates2plot)    
        
        if str(n_events2plot).lower() == 'all':
            n_events2plot = self.data_stochsim.simulation_timesteps
            
        for n in range(1,self.sim_trajectories_done+1): 
            if self.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            self.plot.TimeSeries(self.data_stochsim.getPropensities(),n_events2plot,rates2plot,self.sim_rates_tracked,n-1,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location)            
        self.plot.plotnum+=1

    def PlotSpeciesDistributions(self,species2plot = True, linestyle = 'solid',linewidth = 1,colors=None,title = 'StochPy Species Probability Mass Function',xlabel='Number of Molecules',ylabel='Probability',IsLegend=True,legend_location='upper right',bin_size=1):  
        """
        PlotSpeciesDistributions(species2plot = True, linestyle = 'solid',linewidth = 1,colors=None,title = 'StochPy Species Probability Mass Function',xlabel='Number of Molecules',ylabel='Probability',IsLegend=True,bin_size=1)
        
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
         - *bin_size* [default=None] (integer)
        """       
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"
        assert self._IsSimulationDone, "Before plotting species distributions first do a stochastic simulation"
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        
        species2plot = self._getSpecies2Plot(species2plot)  
        
        for n in range(1,self.sim_trajectories_done+1):   
            if self.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            self.plot.Distributions(self.data_stochsim.species_distributions,species2plot,self.data_stochsim.species_labels,n-1,linestyle,linewidth,colors,title,xlabel,ylabel,IsLegend,legend_location,bin_size)                    
        self.plot.plotnum += 1
        
                
    def PlotPropensitiesDistributions(self,rates2plot = True, linestyle = 'solid',linewidth = 1,colors=None,title = 'StochPy Propensities Probability Mass Function',xlabel='Propensity',ylabel='Probability',IsLegend=True,legend_location='upper right',bin_size=1):
        """
        PlotPropensitiesDistributions(self,rates2plot = True, linestyle = 'solid',linewidth = 1,colors=None,title = 'StochPy Propensities Probability Mass Function',xlabel='Propensity',ylabel='Probability',IsLegend=True,legend_location='upper right',bin_size=1)
        
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
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"
        assert self._IsSimulationDone and self.IsTrackPropensities, "Before plotting propensities first do a stochastic simulation with tracking propensities (use the IsTrackPropensities flag in DoStochSim)"  
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        
        rates2plot = self._getRates2Plot(rates2plot)    
        
        for n in range(1,self.sim_trajectories_done+1):    
            if self.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            self.plot.Distributions(self.data_stochsim.propensities_distributions,rates2plot,self.sim_rates_tracked,n-1,linestyle,linewidth,colors,title,xlabel,ylabel,IsLegend,legend_location,bin_size)
        self.plot.plotnum += 1
        
        
    def GetWaitingtimes(self):
        """ Get for each reaction the waiting times """      
        assert self._IsSimulationDone, "Before getting waiting times first do a stochastic simulation (and do not use the Tau-Leaping method)"         
        assert not self._IsTauLeaping, "Tau-Leaping method does not allow for calculation of waiting times"          
        assert not self._IsFixedIntervalMethod, "Fixed-interval output solvers do not allow for calculation of waiting times"
        assert not self._IsOnlyLastTimepoint, "Calculating waiting times is disabled when saving only the last time point"        
        
        for n in range(1,self.sim_trajectories_done+1): 
            if self.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            D_waitingtimes = Analysis.ObtainWaitingtimes(self.data_stochsim,self.SSA.rate_names) # hard coded for all reactions
            self.data_stochsim.setWaitingtimes(D_waitingtimes,self.SSA.rate_names)
            self.data_stochsim.setWaitingtimesMeans(self.data_stochsim.waiting_times,self.SSA.rate_names)        
            self.data_stochsim.setWaitingtimesStandardDeviations(self.data_stochsim.waiting_times,self.SSA.rate_names)
            if self.sim_trajectories_done > 1: # "store" the data, otherwise the added waiting times get lost again by opening via GetTrajectoryData
                self.DumpTrajectoryData(n)            
            
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
         - *legend_location* [default = 'upper right'] (string/integer)
        """    
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"
        assert not self._IsTauLeaping, "Tau-Leaping method does not allow for calculation of waiting times"
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        
        if (not self.data_stochsim.HAS_WAITINGTIMES) and (not self._IsTauLeaping):
            self.GetWaitingtimes()
            
        waitingtime_r_ids = list(self.data_stochsim.waiting_times)
        if rates2plot == True:
            rates2plot = np.sort(waitingtime_r_ids)
        else:
            rates2plot = self._getRates2Plot(rates2plot)
            for r_id in rates2plot:
                if r_id + '_Completion' in waitingtime_r_ids: # Automatically also select completion waiting times
                    rates2plot.append( r_id + '_Completion' )                             
        
        for n in range(1,self.sim_trajectories_done+1): 
            if self.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            self.plot.WaitingtimesDistributions(self.data_stochsim.waiting_times,rates2plot,n-1,linestyle,linewidth, marker,colors,title,xlabel,ylabel,IsLegend,legend_location)            
        self.plot.plotnum+=1
        
    def GetRegularGrid(self,n_samples=51):
        """
        GetRegularGrid(n_samples=51)              
        
        The Gillespie method generates data at irregular time points. This function puts the data on a fixed regular time grid of which the user can specify the resolution (n_samples). 
        
        For each trajectory, we use the same grid. This has the following consequences for the two type of simulation modes:
        - time: the end time of each trajectory is identical
        - time steps: the end time of each trajectory is different. We select the minimal end time of each of these simulations and ignore the period afterwards.
        
        Input:
         - *n_samples* [default = 51] (integer)
        """
        assert self._IsSimulationDone, "Before getting average data on a regular grid first do a stochastic simulation"        
        assert not self._IsOnlyLastTimepoint, "Generating a regular grid is disabled when saving only the last time point"
        
        ### Determine the number of samples ###
        if isinstance(n_samples,int):
            pass
        elif type(n_samples) in [float,np.float64,np.float32]:
            print("*** WARNING ***: 'n_samples' must be an integer rather than a float; float {0} is rounded to {1:d}".format(n_samples,int(n_samples)))
            n_samples = int(n_samples)
        elif n_samples == True:
            n_samples = int(self.data_stochsim.simulation_endtime)    
        else:
            raise TypeError("Argument of GetRegularGrid() must be an integer")               
        
        n_species = len(self.data_stochsim.species_labels)
        L_species = [[] for i in range(n_species)]
        if self._IsCellDivision:
           L_volumes = [[]]  # hard coded one sort of volume 
        if self.IsTrackPropensities:
            n_rates = len(self.sim_rates_tracked)
            L_propensities = [[] for j in range(n_rates)]
            self.data_stochsim_grid.propensities_autocorrelations = [[] for j in range(n_rates)]
        
        if self.sim_mode == 'time':
            sample_timepoints = np.linspace(0,self.sim_end,n_samples)            
        else: 
            L_simulation_endtimes = []
            for n in range(1,self.sim_trajectories_done+1): 
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                L_simulation_endtimes.append(self.data_stochsim.simulation_endtime)                             
            sample_timepoints = np.linspace(0,min(L_simulation_endtimes),n_samples)
        
        for n in range(1,self.sim_trajectories_done+1):               
            if self.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)           
            
            sample_indices = self.data_stochsim.time[:,0].searchsorted(sample_timepoints, side = 'right') - 1 # Get point before
            sampled_species = self.data_stochsim.species[sample_indices]        
            if self._IsCellDivision:                        
                sampled_volume = self.data_stochsim.volume[sample_indices]             
                
            ### Put data in grid files ### 
            for i in range(n_species):
                L_species[i].append(sampled_species[:,i])             
             
            if self.IsTrackPropensities:
                sample_propensities = self.data_stochsim.propensities[sample_indices]   
                for j in range(n_rates):
                    L_propensities[j].append(sample_propensities[:,j])     
            if self._IsCellDivision:
                L_volumes[0].append(sampled_volume[:,0])
                    
        self.data_stochsim_grid.setTime(sample_timepoints)                           
        self.data_stochsim_grid.setSpecies(L_species,self.sim_species_tracked)          
        (self.data_stochsim_grid.species_means,self.data_stochsim_grid.species_standard_deviations) = Analysis.GetAverageResults(self.data_stochsim_grid.species)
        if self.IsTrackPropensities:
            self.data_stochsim_grid.setPropensities(L_propensities) 
            (self.data_stochsim_grid.propensities_means,self.data_stochsim_grid.propensities_standard_deviations) = Analysis.GetAverageResults(self.data_stochsim_grid.propensities)
        if self._IsCellDivision:
            self.data_stochsim_grid.setVolume(L_volumes)
            (self.data_stochsim_grid.volume_means,self.data_stochsim_grid.volume_standard_deviations) = Analysis.GetAverageResults(self.data_stochsim_grid.volume)
        self.HAS_AVERAGE = True        

    def PlotAverageSpeciesTimeSeries(self,species2plot = True,linestyle = 'None',linewidth = 1,marker = 'o',colors = None,title = 'StochPy Average Species Time Series Plot (# of trajectories = )',xlabel='Time',ylabel='Copy Number',IsLegend=True,legend_location='upper right',nstd=1): 
        """
        PlotAverageSpeciesTimeSeries(species2plot = True,linestyle = 'None',marker = 'o',colors = None,title = 'StochPy Average Species Time Series Plot (# of trajectories = )',xlabel='Time',ylabel='Copy Number',IsLegend=True,legend_location='upper right',nstd=1)
        
        Plot the average time simulation result. For each time point, the mean and standard deviation are plotted 
        
        Input:
         - *species2plot* [default = True] as a list ['S1','S2']
         - *linestyle* [default = 'dotted'] dashed, solid, and dash_dot (string)
         - *linewidth* [default = 1] (float)
         - *marker* [default = 'o'] ('v','o','s',',','*','.')
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Average Time (# of trajectories = ... )' ] (string)
         - *xlabel* [default = 'Time'] (string)
         - *ylabel* [default = 'Copy Number'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
         - *nstd* [default=1] (float
        """
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"  
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        
        if not self.HAS_AVERAGE: 
            print("*** WARNING ***: No regular grid is created yet. Use GetRegularGrid(n_samples) if averaged results are unsatisfactory (e.g. more or less 'samples')")
            self.GetRegularGrid()        
        
        species2plot = self._getSpecies2Plot(species2plot)
                
        if '(# of trajectories = )' in title:
            title = title.replace('= ','= {0:d}'.format(self.sim_trajectories_done))
            
        self.plot.AverageTimeSeries(self.data_stochsim_grid.species_means,self.data_stochsim_grid.species_standard_deviations,self.data_stochsim_grid.time,nstd,species2plot,self.sim_species_tracked,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location)
        self.plot.plotnum+=1
            
    def PlotAverageSpeciesDistributions(self,species2plot = True,linestyle = 'None',linewidth = 1,marker = 'o',colors = None,title = 'StochPy Average Species Distributions Plot (# of trajectories = )',xlabel='Species Amount',ylabel='Probability',IsLegend=True,legend_location = 'upper right',nstd=1): 
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
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"  
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"        
        if not self.data_stochsim_grid.HAS_AVERAGE_SPECIES_DISTRIBUTIONS:
            self.GetAverageSpeciesDistributions()
        
        species2plot = self._getSpecies2Plot(species2plot)
                
        if '(# of trajectories = )' in title:
            title = title.replace('= ','= {0:d}'.format(self.sim_trajectories_done))

        self.plot.AverageDistributions(self.data_stochsim_grid.species_distributions_means,self.data_stochsim_grid.species_distributions_standard_deviations,nstd,species2plot,self.sim_species_tracked,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location)
        self.plot.plotnum+=1
             
    def PlotAverageSpeciesDistributionsConfidenceIntervals(self,species2plot=True,colors = None,title = 'StochPy Average Species Distributions Plot (# of trajectories = )',xlabel='Species Amount',ylabel='Probability',IsLegend=True,legend_location='upper right',nstd=1):
        """
        PlotAverageSpeciesDistributionsConfidenceIntervals(species2plot=True,colors = None,title = 'StochPy Average Species Distributions Plot (# of trajectories = )',xlabel='Species Amount',ylabel='Probability',IsLegend=True,legend_location='upper right',nstd=1)
        
        Plot the average species distributions For each species Amount, the mean and standard deviation are plotted      

        Input:
         - *species2plot* [default = True] as a list ['S1','S2']
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Average Time (# of trajectories = ... )' ] (string)
         - *xlabel* [default = 'Species Amount'] (string)
         - *ylabel* [default = 'Probability'] (string)
         - *IsLegend* [default = True] (boolean)   
         - *legend_location* [default = 'upper right'] (string/integer)   
         - *nstd* [default=1] (float
        """
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"  
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        if not self.data_stochsim_grid.HAS_AVERAGE_SPECIES_DISTRIBUTIONS:
            self.GetAverageSpeciesDistributions()
        
        species2plot = self._getSpecies2Plot(species2plot)
        
        if '(# of trajectories = )' in title:
            title = title.replace('= ','= {0:d}'.format(self.sim_trajectories_done))
            
        self.plot.AverageDistributionsCI(self.data_stochsim_grid.species_distributions_means,self.data_stochsim_grid.species_distributions_standard_deviations,nstd,species2plot,self.sim_species_tracked,colors,title,xlabel,ylabel,IsLegend,legend_location)    
        self.plot.plotnum+=1
             
    def PlotAveragePropensitiesDistributionsConfidenceIntervals(self,rates2plot = True,colors = None,title = 'StochPy Average Propensities Distributions Plot (# of trajectories = )',xlabel='Propensity',ylabel='Probability',IsLegend=True,legend_location='upper right',nstd=1):
        """
        PlotAveragePropensitiesDistributionsConfidenceIntervals(rates2plot = True,colors = None,title = 'StochPy Average Propensities Distributions Plot (# of trajectories = )',xlabel='Propensity',ylabel='Probability',IsLegend=True,legend_location='upper right',nstd=1)

        Plot the average time simulation result. For each time point, the mean and standard deviation are plotted      

        Input:
         - *rates2plot* [default = True] as a list ['R1','R2']       
         - *colors* [default =  None] (list)
         - *title* [default = 'StochPy Average Time (# of trajectories = ... )' ] (string)
         - *xlabel* [default = 'Propensity'] (string)
         - *ylabel* [default = 'Probability'] (string)
         - *IsLegend* [default = True] (boolean)
         - *legend_location* [default = 'upper right'] (string/integer)
         - *nstd* [default=1] (float)
        """
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"  
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        if not self.data_stochsim_grid.HAS_AVERAGE_PROPENSITIES_DISTRIBUTIONS:
            self.GetAveragePropensitiesDistributions()          

        rates2plot = self._getRates2Plot(rates2plot)    
        
        self.plot.AverageDistributionsCI(self.data_stochsim_grid.propensities_distributions_means,self.data_stochsim_grid.propensities_distributions_standard_deviations,nstd,rates2plot,self.sim_rates_tracked,colors,title,xlabel,ylabel,IsLegend,legend_location)
        self.plot.plotnum+=1
                
    def PlotAveragePropensitiesDistributions(self,rates2plot = True,linestyle = 'None',linewidth = 1,marker = 'o',colors = None,title = 'StochPy Average Propensities Distributions Plot (# of trajectories = )',xlabel='Propensity',ylabel='Probability',IsLegend=True,legend_location='upper right',nstd=1): 
        """
        PlotAveragePropensitiesDistributions(rates2plot = True,linestyle = 'None',marker = 'o',colors = None,title = 'StochPy Average Species Time Series Plot (# of trajectories = )',xlabel='Propensity',ylabel='Probability',IsLegend=True,legend_location='upper right',nstd=1)

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
         - *legend_location* [default = 'upper right'] (string/integer)
         - *nstd* [default=1] (float
        """  
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"  
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        if not self.data_stochsim_grid.HAS_AVERAGE_PROPENSITIES_DISTRIBUTIONS:
            self.GetAveragePropensitiesDistributions()
         
        rates2plot = self._getRates2Plot(rates2plot)    
                
        if '(# of trajectories = )' in title:
            title = title.replace('= ','= {0:d}'.format(self.sim_trajectories_done))

        self.plot.AverageDistributions(self.data_stochsim_grid.propensities_distributions_means,self.data_stochsim_grid.propensities_distributions_standard_deviations,nstd,rates2plot,self.sim_rates_tracked,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location)
        self.plot.plotnum+=1 
            
    def PlotAveragePropensitiesTimeSeries(self,rates2plot = True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Average Propensities Time Series Plot (# of trajectories = )',xlabel='Time',ylabel='Propensity',IsLegend=True,legend_location='upper right',nstd=1): 
        """
        PlotAveragePropensitiesTimeSeries(rates2plot = True,linestyle = 'None',marker = 'o',colors = None,title = 'StochPy Average Propensities Time Series Plot (# of trajectories = )',xlabel='Time',ylabel='Propensity',IsLegend=True,legend_location='upper right',nstd=1)
        
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
         - *legend_location* [default = 'upper right'] (string/integer)
         - *nstd* [default=1] (float
        """      
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"       
        assert self.IsTrackPropensities, "Before plotting propensities first do a stochastic simulation with tracking propensities (use the IsTrackPropensities flag in DoStochSim)"
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        
        if (not self.HAS_AVERAGE) and (self.IsTrackPropensities): 
            print("*** WARNING ***: No regular grid is created yet. Use GetRegularGrid(n_samples) if averaged results are unsatisfactory)")
            self.GetRegularGrid()      
            
        rates2plot = self._getRates2Plot(rates2plot)  
                
        if '(# of trajectories = )' in title:
            title = title.replace('= ','= {0:d}'.format(self.sim_trajectories_done))

        self.plot.AverageTimeSeries(self.data_stochsim_grid.propensities_means,self.data_stochsim_grid.propensities_standard_deviations,                   self.data_stochsim_grid.time,nstd,rates2plot,self.sim_rates_tracked,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location)
        self.plot.plotnum+=1  
            
    def GetAverageSpeciesDistributions(self):
        """ Get average species distributions """      
        assert self._IsSimulationDone, "Before getting average species distributions first do a stochastic simulation."         
        assert not self._IsOnlyLastTimepoint, "Calculating average species distributions is disabled when saving only the last time point"
        
        D_distributions = {}
        for s_id in self.sim_species_tracked:
            D_distributions[s_id] = {}
        L_distributions_means = []
        L_distributions_standard_deviations = []
        for n in range(1,self.sim_trajectories_done+1): 
            if self.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            for i in range(len(self.sim_species_tracked)):
                s_id = self.sim_species_tracked[i]
                for m,s_amount in enumerate(self.data_stochsim.species_distributions[i][0]):
                    if not s_amount in list(D_distributions[s_id]):
                        D_distributions[s_id][s_amount] = []
                    D_distributions[s_id][s_amount].append(self.data_stochsim.species_distributions[i][1][m])
            
        for s_id in self.sim_species_tracked:
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
        self.data_stochsim_grid.setSpeciesDistributionAverage(L_distributions_means,L_distributions_standard_deviations)          
        
    def GetAveragePropensitiesDistributions(self):
        """ Get average propensities distributions """
        assert (self._IsSimulationDone and self.IsTrackPropensities), "Before getting average propensities distributions first do a stochastic simulation (use the IsTrackPropensities flag in DoStochSim)." 
        assert not self._IsOnlyLastTimepoint, "Calculating average propensities distributions is disabled when saving only the last time point"         
        
        D_distributions = {}
        for r_id in self.sim_rates_tracked:
            D_distributions[r_id] = {}
        L_distributions_means = []
        L_distributions_standard_deviations = []
        for n in range(1,self.sim_trajectories_done+1): 
            if self.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            for j in range(len(self.sim_rates_tracked)):
                r_id = self.sim_rates_tracked[j]                
                for m,r_prop in enumerate(self.data_stochsim.propensities_distributions[j][0]):
                    if not r_prop in list(D_distributions[r_id]): 
                        D_distributions[r_id][r_prop] = []
                    D_distributions[r_id][r_prop].append(self.data_stochsim.propensities_distributions[j][1][m])
            
        for r_id in self.sim_rates_tracked:
            L_propensities = list(D_distributions[r_id])  # for a given species 
            L_means = []
            L_stds = []   
            for r_prop in L_propensities:
                while len(D_distributions[r_id][r_prop]) < (n-1):
                    D_distributions[r_id][r_prop].append(0)
                L_means.append(np.mean(D_distributions[r_id][r_prop]))
                L_stds.append(np.std(D_distributions[r_id][r_prop]))    
            L_distributions_means.append([L_propensities,L_means])
            L_distributions_standard_deviations.append([L_propensities,L_stds])
        self.data_stochsim_grid.setPropensitiesDistributionAverage(L_distributions_means,L_distributions_standard_deviations)            

    def GetSpeciesAutocorrelations(self,species2calc=True,n_samples=51):
        """
        GetSpeciesAutocorrelations(species2calc=True,n_samples=51)
        
        Input:
         - *species2calc* [default = True] as a list ['S1','S2']
         - *n_samples* (integer)
        """
        if (not self.HAS_AVERAGE) or n_samples != 51:
            self.GetRegularGrid(n_samples)        
        
        species2calc = self._getSpecies2Plot(species2calc)                             
        L_species_autocorrelations = [[] for i in range(len(self.sim_species_tracked))]
        
        for n in range(self.sim_trajectories_done):               
            for s_id in species2calc:                  
                s_index = self.sim_species_tracked.index(s_id)
                L_species_autocorrelations[s_index].append(Analysis.Autocorrelation(self.data_stochsim_grid.species[s_index][n]))  
            
        self.data_stochsim_grid.setSpeciesAutocorrelations(np.array(L_species_autocorrelations))
        
        (self.data_stochsim_grid.species_autocorrelations_means,
        self.data_stochsim_grid.species_autocorrelations_standard_deviations) = Analysis.GetAverageResults(L_species_autocorrelations)

    def GetSpeciesAutocovariances(self,species2calc=True,n_samples=51):
        """
        GetSpeciesAutocovariances(species2calc=True,n_samples=51)
        
        Input:
         - *species2calc* [default = True] as a list ['S1','S2']
         - *n_samples* (integer)
        """
        if (not self.HAS_AVERAGE) or n_samples != 51:
            self.GetRegularGrid(n_samples)
        
        species2calc = self._getSpecies2Plot(species2calc)
                             
        L_species_autocovariances = [[] for i in range(len(self.sim_species_tracked))]
       
        for n in range(self.sim_trajectories_done):                  
            for s_id in species2calc:
                s_index = self.sim_species_tracked.index(s_id)  
                L_species_autocovariances[s_index].append(Analysis.AutoCov(self.data_stochsim_grid.species[s_index][n]))  
                  
        self.data_stochsim_grid.setSpeciesAutocovariances(np.array(L_species_autocovariances))
        (self.data_stochsim_grid.species_autocovariances_means,
        self.data_stochsim_grid.species_autocovariances_standard_deviations) = Analysis.GetAverageResults(L_species_autocovariances)
            
    def GetPropensitiesAutocorrelations(self,rates2calc=True,n_samples=51):
        """
        GetPropensitiesAutocorrelations(rates2calc=True,n_samples=51)
        
        Input:
         - *rates2calc* [default = True] as a list ['R1','R2']     
         - *n_samples* (integer)
        """
        assert self.IsTrackPropensities, "Before plotting propensities first do a stochastic simulation with tracking propensities (use the IsTrackPropensities flag in DoStochSim)"           
        
        if (not self.HAS_AVERAGE) and n_samples != 51:
            self.GetRegularGrid(n_samples)          
        
        rates2calc = self._getRates2Plot(rates2calc)
        L_Propensities_autocorrelations = [[] for j in range(len(self.sim_rates_tracked))]
        
        for n in range(self.sim_trajectories_done):               
            for r_id in rates2calc:
                r_index = self.sim_rates_tracked.index(r_id)   
                L_Propensities_autocorrelations[r_index].append(Analysis.Autocorrelation(self.data_stochsim_grid.propensities[r_index][n]))
                    
        self.data_stochsim_grid.setPropensitiesAutocorrelations(np.array(L_Propensities_autocorrelations))
        self.data_stochsim_grid.propensities_autocorrelations_means, self.data_stochsim_grid.propensities_autocorrelations_standard_deviations = Analysis.GetAverageResults(self.data_stochsim_grid.propensities_autocorrelations)

    def GetPropensitiesAutocovariances(self,rates2calc=True,n_samples=51): 
        """
        GetPropensitiesAutocovariances(rates2calc=True,n_samples=51)

        Input:
         - *rates2calc* [default = True] as a list ['R1','R2']     
         - *n_samples* (integer)
        """
        assert self.IsTrackPropensities, "Before plotting propensities first do a stochastic simulation with tracking propensities (use the IsTrackPropensities flag in DoStochSim)"
        
        if (not self.HAS_AVERAGE) and n_samples != 51:
            self.GetRegularGrid(n_samples)
            
        rates2calc = self._getRates2Plot(rates2calc)

        L_Propensities_autocovariances = [[] for j in range(len(self.sim_rates_tracked))]              
        for n in range(self.sim_trajectories_done):                
            for r_id in rates2calc:
                r_index = self.sim_rates_tracked.index(r_id)   
                L_Propensities_autocovariances[r_index].append(Analysis.AutoCov(self.data_stochsim_grid.propensities[r_index][n]))
              
        self.data_stochsim_grid.setPropensitiesAutocovariances(np.array(L_Propensities_autocovariances))
        self.data_stochsim_grid.propensities_autocovariances_means, self.data_stochsim_grid.propensities_autocovariances_standard_deviations = Analysis.GetAverageResults(self.data_stochsim_grid.propensities_autocovariances)                      
                
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
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"     
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        if not self.data_stochsim_grid.HAS_SPECIES_AUTOCORRELATIONS:
            print("*** WARNING ***: Autocorrelations are not yet calculated. StochPy automatically calculates autocorrelations with pre-defined settings. You can use GetSpeciesAutocorrelations(species2calc=True,n_samples=51)")
            self.GetSpeciesAutocorrelations(species2calc = species2plot)
        
        species2plot = self._getSpecies2Plot(species2plot)
                
        for n in range(self.sim_trajectories_done):       
            self.plot.Autocorrelations(self.data_stochsim_grid.time[0:nlags],self.data_stochsim_grid.species_autocorrelations[:,n],   species2plot,self.sim_species_tracked,n,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location)
            
        self.plot.plotnum+=1
        
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
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"     
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        if not self.data_stochsim_grid.HAS_SPECIES_AUTOCOVARIANCES:
            print("*** WARNING ***: Autocovariances are not yet calculated. StochPy automatically calculates autocovariances with pre-defined settings. You can use GetSpeciesAutocovariances(species2calc=True,n_samples=51)")
            self.GetSpeciesAutocovariances(species2calc = species2plot)
        
        species2plot = self._getSpecies2Plot(species2plot)
            
        for n in range(self.sim_trajectories_done):     
            self.plot.Autocorrelations(self.data_stochsim_grid.time[0:nlags],self.data_stochsim_grid.species_autocovariances[:,n],     species2plot,self.sim_species_tracked,n,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location)            
        self.plot.plotnum+=1
           
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
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"     
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        
        if not self.data_stochsim_grid.HAS_SPECIES_AUTOCORRELATIONS:
            print("*** WARNING ***: Autocorrelations are not yet calculated. StochPy automatically calculates autocorrelations with pre-defined settings. You can use GetSpeciesAutocorrelations(species2calc=True,n_samples=51)")
            self.GetSpeciesAutocorrelations(species2calc = species2plot)
      
        species2plot = self._getSpecies2Plot(species2plot)    
            
        if '(# of trajectories = )' in title:
            title = title.replace('= ','= {0:d}'.format(self.sim_trajectories_done))
        
        self.plot.AverageTimeSeries(self.data_stochsim_grid.species_autocorrelations_means,self.data_stochsim_grid.species_autocorrelations_standard_deviations,self.data_stochsim_grid.time[0:nlags],nstd,species2plot,self.sim_species_tracked,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location)
        self.plot.plotnum+=1
        
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
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
             
        if not self.data_stochsim_grid.HAS_SPECIES_AUTOCOVARIANCES:
            print("*** WARNING ***: Autocovariances are not yet calculated. StochPy automatically calculates autocovariances with pre-defined settings. You can use GetSpeciesAutocovariances(species2calc=True,n_samples=51)")
            self.GetSpeciesAutocovariances(species2calc = species2plot)
      
        species2plot = self._getSpecies2Plot(species2plot)
            
        if '(# of trajectories = )' in title:
            title = title.replace('= ','= {0:d}'.format(self.sim_trajectories_done))
        
        self.plot.AverageTimeSeries(self.data_stochsim_grid.species_autocovariances_means,self.data_stochsim_grid.species_autocovariances_standard_deviations,
        self.data_stochsim_grid.time[0:nlags],nstd,species2plot,self.sim_species_tracked,linestyle,linewidth, marker,colors,title,xlabel,ylabel,IsLegend,legend_location)
        self.plot.plotnum+=1
            
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
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"     
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        
        if not self.data_stochsim_grid.HAS_PROPENSITIES_AUTOCORRELATIONS:
            print("*** WARNING ***: Autocorrelations are not yet calculated. StochPy automatically calculates autocorrelations with pre-defined settings. You can use GetPropensitiesAutocorrelations(rates2calc=True,n_samples=51)")
            self.GetPropensitiesAutocorrelations(rates2calc = rates2plot,n_samples=self.data_stochsim.simulation_endtime)
             
        rates2plot = self._getRates2Plot(rates2plot)    
                    
        for n in range(self.sim_trajectories_done):     
            self.plot.Autocorrelations(self.data_stochsim_grid.time[0:nlags],self.data_stochsim_grid.propensities_autocorrelations[:,n],rates2plot,self.sim_rates_tracked,n,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location)
        self.plot.plotnum+=1  
        
    def PlotPropensitiesAutocovariances(self,nlags=-1,rates2plot=True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Propensities Autocorrelation Plot',xlabel=r'Lag ($\tau$)',ylabel='Auto-correlation',IsLegend=True,legend_location='upper right'):
        """
        PlotPropensitiesAutocovariances(rates2plot=True,linestyle = 'None',linewidth = 1, marker = 'o',colors = None,title = 'StochPy Propensities Autocorrelation Plot',xlabel=r'Lag ($\tau$)',ylabel='Auto-correlation')

        
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
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"     
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        
        if not self.data_stochsim_grid.HAS_PROPENSITIES_AUTOCOVARIANCES:
            print("*** WARNING ***: Autocovariances are not yet calculated. StochPy automatically calculates autocovariances with pre-defined settings. You can use GetPropensitiesAutocovariances(rates2calc=True,n_samples=51)")
            self.GetPropensitiesAutocovariances(rates2calc = rates2plot,n_samples=self.data_stochsim.simulation_endtime)
             
        rates2plot = self._getRates2Plot(rates2plot)    
                    
        for n in range(self.sim_trajectories_done):     
            self.plot.Autocorrelations(self.data_stochsim_grid.time[0:nlags],self.data_stochsim_grid.propensities_autocovariances[:,n],rates2plot,self.sim_rates_tracked,n,linestyle,linewidth, marker,colors,title,xlabel,ylabel,IsLegend,legend_location)                        
        self.plot.plotnum+=1  

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
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"      
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
           
        if not self.data_stochsim_grid.HAS_PROPENSITIES_AUTOCORRELATIONS:
            print("*** WARNING ***: Autocorrelations are not yet calculated. StochPy automatically calculates autocorrelations with pre-defined settings. You can use GetPropensitiesAutocorrelations(rates2calc=True,n_samples=51)")
            self.GetPropensitiesAutocorrelations(rates2calc = rates2plot,n_samples=self.data_stochsim.simulation_endtime)
        
        rates2plot = self._getRates2Plot(rates2plot)
                    
        if '(# of trajectories = )' in title:
            title = title.replace('= ','= {0:d}'.format(self.sim_trajectories_done)) 

        self.plot.AverageTimeSeries(self.data_stochsim_grid.propensities_autocorrelations_means,self.data_stochsim_grid.propensities_autocorrelations_standard_deviations,                self.data_stochsim_grid.time[0:nlags],nstd,rates2plot,self.sim_rates_tracked,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location)
        self.plot.plotnum+=1

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
        assert stochpy._IsPlotting, "Install matplotlib or use Export2file()"         
        assert not self._IsOnlyLastTimepoint, "Plotting is disabled when saving only the last time point"
        
        if not self.data_stochsim_grid.HAS_PROPENSITIES_AUTOCOVARIANCES:
            print("*** WARNING ***: Autocovariances are not yet calculated. StochPy automatically calculates autocovariances with pre-defined settings. You can use GetPropensitiesAutocovariances(rates2calc=True,n_samples=51)")
            self.GetPropensitiesAutocovariances(rates2calc = rates2plot,n_samples=self.data_stochsim.simulation_endtime)
        
        rates2plot = self._getRates2Plot(rates2plot)
        if '(# of trajectories = )' in title:
            title = title.replace('= ','= {0:d}'.format(self.sim_trajectories_done))
        self.plot.AverageTimeSeries(self.data_stochsim_grid.propensities_autocovariances_means,self.data_stochsim_grid.propensities_autocovariances_standard_deviations,self.data_stochsim_grid.time[0:nlags],nstd,rates2plot,self.sim_rates_tracked,linestyle,linewidth,marker,colors,title,xlabel,ylabel,IsLegend,legend_location)
        self.plot.plotnum+=1

    def PrintSpeciesMeans(self):
        """ Print the means (3 decimals) of each species for the selected trajectory"""
        assert self._IsSimulationDone, "Before showing the means, do a stochastic simulation first"      
        assert not self._IsOnlyLastTimepoint, "Determining statistics is disabled when saving only the last time point"
        print("Species\tMean")
        for s_id in self.data_stochsim.species_labels:   
            mu = self.data_stochsim.species_means[s_id]         
            if not mu < 0.001:
                print("{0:s}\t{1:0.3f}".format(s_id,mu))   
            else:
                print("{0:s}\t{1:0.3e}".format(s_id,mu))           

    def PrintSpeciesStandardDeviations(self):
        """ Print the standard deviations (3 decimals) of each species for the selected trajectory"""  
        assert self._IsSimulationDone, "Before showing the standard deviations, do a stochastic simulation first"     
        assert not self._IsOnlyLastTimepoint, "Determining statistics is disabled when saving only the last time point"           
        print("Species\tStandard Deviation")
        for s_id in self.data_stochsim.species_labels:          
            std = self.data_stochsim.species_standard_deviations[s_id]
            if not std < 0.001:
                print("{0:s}\t{1:0.3f}".format(s_id,std))     
            else:
                print("{0:s}\t{1:0.3e}".format(s_id,std))    
                
    def PrintPropensitiesMeans(self): 
        """ Print the means of each propensity for the selected trajectory"""      
        assert (self.IsTrackPropensities and self._IsSimulationDone), "Before printing propensities first do a stochastic simulation with tracking propensities (use the IsTrackPropensities flag in DoStochSim)"      
        assert not self._IsOnlyLastTimepoint, "Determining statistics is disabled when saving only the last time point"
        print("Reaction\tMean")
        for r_id in self.sim_rates_tracked:
            mu = self.data_stochsim.propensities_means[r_id]
            if not mu < 0.001:
                print("{0:s}\t{1:0.3f}".format(r_id,mu))
            else:
                print("{0:s}\t{1:0.3e}".format(r_id,mu))

    def PrintPropensitiesStandardDeviations(self):
        """ Print the standard deviations of each propensity for the selected trajectory"""  
        assert (self.IsTrackPropensities and self._IsSimulationDone), "Before printing propensities first do a stochastic simulation with tracking propensities (use the IsTrackPropensities flag in DoStochSim)"    
        assert not self._IsOnlyLastTimepoint, "Determining statistics is disabled when saving only the last time point"           
        print("Reaction\tStandard Deviation")
        for r_id in self.sim_rates_tracked:            
            std = self.data_stochsim.propensities_standard_deviations[r_id]
            if not std < 0.001:
                print("{0:s}\t{1:0.3f}".format(r_id,std))     
            else:
                print("{0:s}\t{1:0.3e}".format(r_id,std))    

    def PrintWaitingtimesMeans(self):
        """ Print the waiting time means for the selected trajectory """      
        assert not self._IsTauLeaping, "Tau-Leaping method does not allow for calculation of waiting times"        
        if (not self.data_stochsim.HAS_WAITINGTIMES) and (not self._IsTauLeaping): 
            self.GetWaitingtimes()

        for n in range(1,self.sim_trajectories_done+1):     
            if self.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            print("Reaction\tMean")            
            for j,r_id in enumerate(self.SSA.rate_names):                  
                mu = self.data_stochsim.waiting_times_means[j]
                if not mu < 0.001:
                    print("{0:s}\t{1:0.3f}".format(r_id,mu))
                else:
                    print("{0:s}\t{1:0.3e}".format(r_id,mu))              
   
    def PrintWaitingtimesStandardDeviations(self):
        """ Print the waiting time standard deviations for the selected trajectory """
        assert not self._IsTauLeaping, "Tau-Leaping method does not allow for calculation of waiting times"    
        if (not self.data_stochsim.HAS_WAITINGTIMES) and (not self._IsTauLeaping): 
            self.GetWaitingtimes()
        for n in range(1,self.sim_trajectories_done+1):     
            if self.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            print("Reaction\tStandard deviation")            
            for j,r_id in enumerate(self.SSA.rate_names):                             
                std = self.data_stochsim.waiting_times_standard_deviations[j]
                if not std < 0.001:
                    print("{0:s}\t{1:0.3f}".format(s_id,std))     
                else:
                    print("{0:s}\t{1:0.3e}".format(s_id,std))
     
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
        if directory == None:
            if not IsAverage:
                directory = os.path.join(self.output_dir,"{0:s}_{1:s}_{2:s}".format(self.model_file,datatype,analysis))
            else:
                directory = os.path.join(self.output_dir,"{0:s}_{1:s}_{2:s}_{3:s}".format(self.model_file,"average",datatype,analysis))
        else:
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not IsAverage:
                directory = os.path.join(directory,"{0:s}_{1:s}_{2:s}".format(self.model_file,datatype,analysis))  
            else:
                directory = os.path.join(directory,"{0:s}_{1:s}_{2:s}_{3:s}".format(self.model_file,"average",datatype,analysis))
          
        if (datatype.lower() == 'species') and (analysis.lower() == 'timeseries') and (not IsAverage):
            assert self._IsSimulationDone, "Before exporting species time series to a file first do a stochastic simulation"          
            for n in range(1,self.sim_trajectories_done+1): 
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)	# Dir/Filename
                file_out = open(file_path,'w')
                file_out.write('# reactions: {0:d}\n'.format(len(self.SSA.rate_names)))
                file_out.write('Time')
                for s_id in self.data_stochsim.species_labels:
                    file_out.write('\t{0:s}'.format(s_id))
                
                if not self._IsTauLeaping:
                    file_out.write('\tFired Reaction')              
                file_out.write('\n')                                                       
                for m,timepoint in enumerate(self.data_stochsim.getSpecies()):
                    slist = [str(value) for value in timepoint]
                    line = "\t".join(slist) 
                    if not self._IsTauLeaping:
                        line += "\t {0}".format(self.data_stochsim.fired_reactions[m])
                    line += '\n'
                    file_out.write(line)                
                file_out.close()                
                print("Info: Species time series output is successfully saved at: {0:s}".format(file_path) )
                  
        elif (datatype.lower() == 'species') and (analysis.lower() in ['distributions','distribution'] ) and (not IsAverage):
            assert self._IsSimulationDone, "Before exporting species time series to a file first do a stochastic simulation"          
            for n in range(1,self.sim_trajectories_done+1):  
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')  
                for L_species_dist in self.data_stochsim.species_distributions:
                    file_out.write("Amount\tProbability\n")
                    for m in range(len(L_species_dist[0])):
                        file_out.write("{0}\t{1}\n".format(L_species_dist[0][m],L_species_dist[1][m]) ) 
                file_out.close()
                print("Info: Species distributions output is successfully saved at: {0:s}".format(file_path) )
                  
        elif  (datatype.lower() == 'species') and (analysis.lower() == 'autocorrelation') and (not IsAverage):
            if not self.data_stochsim_grid.HAS_SPECIES_AUTOCORRELATIONS:
                print("*** WARNING ***: Autocorrelations are not yet calculated. StochPy automatically calculates autocorrelations with pre-defined settings. You can use GetSpeciesAutocorrelations(species2calc=True,n_samples=51)")
                self.GetSpeciesAutocorrelations()          
             
            for n in range(1,self.sim_trajectories_done+1):
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')                  
                Arr_autocorrelations = self.data_stochsim_grid.species_autocorrelations[:,n-1]
                file_out.write('Lag (tau)')
                for i,L_acor in enumerate(Arr_autocorrelations):
                    file_out.write('\tAutocorrelation ({0:s})'.format(self.sim_species_tracked[i]) )
                file_out.write('\n')
                for m in range(len(self.data_stochsim_grid.time)-1):                   
                    file_out.write(str(self.data_stochsim_grid.time[m][0])) # lag                      
                    for acor in Arr_autocorrelations[:,m]:
                        file_out.write('\t{0:f}'.format(acor))
                    file_out.write('\n')                                              
                               
                file_out.close()
                print("Info: Species autocorrelation output is successfully saved at: {0:s}".format(file_path) )

        elif  (datatype.lower() == 'species') and (analysis.lower() == 'autocovariance') and (not IsAverage):
            if not self.data_stochsim_grid.HAS_SPECIES_AUTOCOVARIANCES:
                print("*** WARNING ***: Autocovariances are not yet calculated. StochPy automatically calculates autocovariances with pre-defined settings. You can use GetSpeciesAutocovariances(species2calc=True,n_samples=51)")
                self.GetSpeciesAutocovariances()          
            for n in range(1,self.sim_trajectories_done+1):
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')  
                Arr_autocovariances = self.data_stochsim_grid.species_autocovariances[:,n-1]
                file_out.write('Lag (tau)')
                for i,L_acov in enumerate(Arr_autocovariances):
                    file_out.write('\tAutocorrelation ({0:s})'.format(self.sim_species_tracked[i]) )
                file_out.write('\n')
                for m in range(len(self.data_stochsim_grid.time)-1):
                    file_out.write(str(self.data_stochsim_grid.time[m][0])) # lag
                    for acov in Arr_autocovariances[:,m]:
                        file_out.write('\t{0:f}'.format(acov) )
                    file_out.write('\n')                
                file_out.close()
                print("Info: Species autocovariance output is successfully saved at: {0:s}".format(file_path) )
                    
        elif (datatype.lower() == 'species') and (analysis.lower() == 'mean') and (not IsAverage):
            assert self._IsSimulationDone, "Before exporting species time series to a file first do a stochastic simulation"          
            for n in range(1,self.sim_trajectories_done+1):
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')                      
                file_out.write("Species\tMean\n")                
                for s_id in self.sim_species_tracked: 
                    file_out.write("{0:s}\t{1:f}\n".format(s_id,self.data_stochsim.species_means[s_id])) 
                file_out.close()
                print("Info: Species means output is successfully saved at: {0:s}".format(file_path) )
                    
        elif (datatype.lower() == 'species') and (analysis.lower() == 'std') and (not IsAverage):
            assert self._IsSimulationDone, "Before exporting species time series to a file first do a stochastic simulation"          
            for n in range(1,self.sim_trajectories_done+1):
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')                      
                file_out.write("Species\tStandard deviation\n")                
                for s_id in self.sim_species_tracked: 
                    file_out.write("{0:s}\t{1:f}\n".format(s_id,self.data_stochsim.species_standard_deviations[s_id]))               
                file_out.close()
                print("Info: Species standard deviations output is successfully saved at: {0:s}".format(file_path) )
                    
        elif (datatype.lower() == 'propensities') and  (analysis.lower() == 'timeseries') and (not IsAverage):       
            assert (self.IsTrackPropensities and self._IsSimulationDone), "Before exporting propensities time series to a file first do a stochastic simulation with tracking propensities (use the IsTrackPropensities flag in DoStochSim)"          
            for n in range(1,self.sim_trajectories_done+1):
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')  
                file_out.write('Time')
                for r_id in self.sim_rates_tracked:
                    file_out.write('\t{0:s}'.format(r_id) )
                file_out.write('\n')      
                for timepoint in self.data_stochsim.getPropensities(): 
                    slist = [str(value) for value in timepoint]
                    line = "\t".join(slist) 
                    line += '\n'
                    file_out.write(line)                
                file_out.close()
                print("Info: Propensities time series output is successfully saved at: {0:s}".format(file_path) )
                    
        elif (datatype.lower() == 'propensities') and (analysis.lower() in ['distributions','distribution'] ) and (not IsAverage):
            assert (self.IsTrackPropensities and self._IsSimulationDone), "Before exporting propensities distributions to a file first do a stochastic simulation with tracking propensities (use the IsTrackPropensities flag in DoStochSim)"          
            for n in range(1,self.sim_trajectories_done+1):
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')                
                for j,L_prop_dist in enumerate(self.data_stochsim.propensities_distributions):
                    file_out.write("Propensity ({0:s})\tProbability\n".format(self.sim_rates_tracked[j]) )
                    for k in range(len(L_prop_dist[0])):
                        file_out.write("{0}\t{1}\n".format(L_prop_dist[0][k],L_prop_dist[1][k]))                
                file_out.close()
                print("Info: Species distributions output is successfully saved at: {0:s}".format(file_path) )
                
        elif  (datatype.lower() == 'propensities') and (analysis.lower() == 'autocorrelation') and (not IsAverage):
            if not self.data_stochsim_grid.HAS_PROPENSITIES_AUTOCORRELATIONS:
                print("*** WARNING ***: Autocorrelations are not yet calculated. StochPy automatically calculates autocorrelations with pre-defined settings. You can use GetPropensitiesAutocorrelations(rates2calc=True,n_samples=51)")
                self.GetPropensitiesAutocorrelations(n_samples=self.data_stochsim.simulation_endtime)          
            for n in range(1,self.sim_trajectories_done+1):
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')  
                Arr_autocorrelations = self.data_stochsim_grid.propensities_autocorrelations[:,n-1]
                file_out.write('Lag (tau)')
                for j,L_acor in enumerate(Arr_autocorrelations):
                    file_out.write('\tAutocorrelation ({0:s})'.format(self.sim_rates_tracked[j]) )                 
                file_out.write('\n')
                for m in range(len(self.data_stochsim_grid.time)-1):
                    file_out.write(str(self.data_stochsim_grid.time[m][0])) # lag
                    for acor in Arr_autocorrelations[:,m]:
                        file_out.write('\t{0:f}'.format(acor) )
                    file_out.write('\n')                
                file_out.close()
                print("Info: Propensities autocorrelation output is successfully saved at: {0:s}".format(file_path) ) 

        elif  (datatype.lower() == 'propensities') and (analysis.lower() == 'autocovariance') and (not IsAverage):
            if not self.data_stochsim_grid.HAS_PROPENSITIES_AUTOCOVARIANCES:
                print("*** WARNING ***: Autocovariances are not yet calculated. StochPy automatically calculates autocovariances with pre-defined settings. You can use GetPropensitiesAutocovariances(rates2calc=True,n_samples=51)")
                self.GetPropensitiesAutocovariances(rates2calc = rates2plot,n_samples=self.data_stochsim.simulation_endtime)
            
            for n in range(1,self.sim_trajectories_done+1): 
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')  
                Arr_autocovariances = self.data_stochsim_grid.propensities_autocovariances[:,n-1]
                file_out.write('Lag (tau)')
                for j,L_acov in enumerate(Arr_autocovariances):
                    file_out.write('\tAutocovariance ({0:s})'.format(self.sim_rates_tracked[j]) )
                 
                file_out.write('\n')
                for m in range(len(self.data_stochsim_grid.time)-1):
                    file_out.write(str(self.data_stochsim_grid.time[m][0])) # lag
                    for acov in Arr_autocovariances[:,m]:
                        file_out.write('\t{0:f}'.format(acov))
                    file_out.write('\n')                    
                file_out.close()
                print("Info: Propensities autocovariance output is successfully saved at: {0:s}".format(file_path) )
                  
        elif (datatype.lower() == 'propensities') and  (analysis.lower() == 'mean') and (not IsAverage):        
            assert (self.IsTrackPropensities and self._IsSimulationDone), "Before exporting propensities means to a file first do a stochastic simulation with tracking propensities (use the IsTrackPropensities flag in DoStochSim)"          
            for n in range(1,self.sim_trajectories_done+1):                
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')                      
                file_out.write("Reaction\tMean\n")                
                for r_id in self.sim_rates_tracked: 
                    file_out.write("{0}\t{1}\n".format(r_id,self.data_stochsim.propensities_means[r_id]))                                    
                file_out.close()
                print("Info: Propensities means output is successfully saved at: {0:s}".format(file_path) )
                                    
        elif (datatype.lower() == 'propensities') and (analysis.lower() == 'std') and (not IsAverage):
            assert (self.IsTrackPropensities and self._IsSimulationDone), "Before exporting propensities standard deviations to a file first do a stochastic simulation with tracking propensities (use the IsTrackPropensities flag in DoStochSim)"                        
            for n in range(1,self.sim_trajectories_done+1):            
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')                      
                file_out.write("Reaction\tStandard deviation\n")                
                for r_id in self.sim_rates_tracked: 
                    file_out.write("{0}\t{1}\n".format(r_id,self.data_stochsim.propensities_standard_deviations[r_id]))                
                file_out.close()
                print("Info: Propensities standard deviations output is successfully saved at: {0:s}".format(file_path) )
                  
        elif (datatype.lower() == 'waitingtimes') and (analysis.lower() in ['distributions','distribution'] ) and (not IsAverage):          
            if (not self.data_stochsim.HAS_WAITINGTIMES):
                self.GetWaitingtimes()
            for n in range(1,self.sim_trajectories_done+1):   
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')
                for r_id in sorted(self.data_stochsim.waiting_times):
                    file_out.write("Waitingtimes\t{0:s}\n".format(r_id) )
                    L_waiting_times_r = self.data_stochsim.waiting_times[r_id]
                    for time in L_waiting_times_r:
                        file_out.write("{0:f}\n".format(time) )                
                file_out.close()
                print("Info: Waitingtimes distributions output is successfully saved at: {0:s}".format(file_path) )
                  
        elif (datatype.lower() == 'waitingtimes') and (analysis.lower() == 'mean') and (not IsAverage):
            if (not self.data_stochsim.HAS_WAITINGTIMES):
                self.GetWaitingtimes()          
            for n in range(1,self.sim_trajectories_done+1):              
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')                      
                file_out.write("Reaction\tMean\n")                
                for j,r_id in enumerate(self.SSA.rate_names): 
                    file_out.write("{0}\t{1}\n".format(r_id,self.data_stochsim.waiting_times_means[j]))                 
                file_out.close()
                print("Info: Waitingtimes means output is successfully saved at: {0:s}".format(file_path) )
                  
        elif (datatype.lower() == 'waitingtimes') and (analysis.lower() == 'std') and (not IsAverage):
            if (not self.data_stochsim.HAS_WAITINGTIMES):
                self.GetWaitingtimes()          
            for n in range(1,self.sim_trajectories_done+1):            
                if self.sim_trajectories_done > 1:
                    self.GetTrajectoryData(n)
                file_path = "{0:s}{1:d}.txt".format(directory,n)
                file_out = open(file_path,'w')                      
                file_out.write("Reaction\tStandard deviation\n")                
                for j,r_id in enumerate(self.SSA.rate_names): 
                    file_out.write("{0}\t{1}\n".format(r_id,self.data_stochsim.waiting_times_standard_deviations[j]))                                    
                file_out.close()
                print("Info: Waitingtimes means output is successfully saved at: {0:s}".format(file_path) )  
                   
        elif (datatype.lower() == 'species') and (analysis.lower() == 'timeseries') and (IsAverage):
            if not self.HAS_AVERAGE:
                print("*** WARNING ***: No regular grid is created yet. Use GetRegularGrid(n_samples) if averaged results are unsatisfactory (e.g. more or less 'points')")
                self.GetRegularGrid()          
            file_path = '{0:s}.txt'.format(directory)
            file_out = open(file_path,'w')
            file_out.write("t")
            for s_id in self.sim_species_tracked:
                file_out.write("\t{0:s} (Mean)\t{0:s} (STD)".format(s_id) )
            file_out.write("\n")
            means = np.transpose(self.data_stochsim_grid.species_means)
            stds = np.transpose(self.data_stochsim_grid.species_standard_deviations)                
            for i,t in enumerate(self.data_stochsim_grid.time): 
                file_out.write( str(t[0]) )  
                for j in range(len(self.data_stochsim_grid.species_means)):
                    file_out.write("\t{0:f}\t{1:f}".format(means[i][j],stds[i][j]) )
                file_out.write("\n")
            print("Info: Averaged species time series output is successfully saved at: {0:s}".format(file_path) )
            
        elif (datatype.lower() == 'propensities') and (analysis.lower() == 'timeseries') and (IsAverage):
            assert self.IsTrackPropensities, "Before exporting averaged propensities to a file first do a stochastic simulation with tracking propensities (use the IsTrackPropensities flag in DoStochSim)"
            if not self.HAS_AVERAGE and self.IsTrackPropensities:
                print("*** WARNING ***: No regular grid is created yet. Use GetRegularGrid(n_samples) if averaged results are unsatisfactory (e.g. more or less 'points')")
                self.GetRegularGrid()          
            file_path = '{0:s}.txt'.format(directory)
            file_out = open(file_path,'w')
            file_out.write("t")
            for r_id in self.sim_rates_tracked:
                file_out.write("\t{0:s} (Mean)\t{0:s} (STD)".format(r_id) )
            file_out.write("\n")
            means = np.transpose(self.data_stochsim_grid.propensities_means)
            stds = np.transpose(self.data_stochsim_grid.propensities_standard_deviations)                        
            for i,t in enumerate(self.data_stochsim_grid.time):
                file_out.write( str(t[0]) )
                for j in range(len(self.data_stochsim_grid.propensities_means)):
                    file_out.write("\t{0:f}\t{1:f}".format(means[i][j],stds[i][j]) )                   
                file_out.write("\n")                
            print("Info: Averaged propensities time series output is successfully saved at: {0:s}".format(file_path) )
            
        elif (datatype.lower() == 'species') and (analysis.lower() in ['distributions','distribution'] ) and (IsAverage):
            if not self.data_stochsim_grid.HAS_AVERAGE_SPECIES_DISTRIBUTIONS:              
                self.GetAverageSpeciesDistributions()          
            file_path = '{0:s}.txt'.format(directory)
            file_out = open(file_path,'w')             
            for i,s_id in enumerate(self.sim_species_tracked):
                file_out.write("Amount\t{0:s} (Mean)\t{0:s} (STD)\n".format(s_id) )   
                for m in range(len(self.data_stochsim_grid.species_distributions_means[i][0])):
                    s_amount = self.data_stochsim_grid.species_distributions_means[i][0][m] 
                    s_probability_mean = self.data_stochsim_grid.species_distributions_means[i][1][m]
                    s_probability_std = self.data_stochsim_grid.species_distributions_standard_deviations[i][1][m]
                    file_out.write("{0:0.0f}\t{1:f}\t{2:f}\n".format(s_amount,s_probability_mean,s_probability_std) )
                file_out.write("\n")                
            print("Info: Averaged species distributions output is successfully saved at: {0:s}".format(file_path) )
            
        elif (datatype.lower() == 'propensities') and (analysis.lower() in ['distributions','distribution'] ) and (IsAverage):
            if not self.data_stochsim_grid.HAS_AVERAGE_PROPENSITIES_DISTRIBUTIONS:
                self.GetAveragePropensitiesDistributions()
            file_path = '{0:s}.txt'.format(directory)
            file_out = open(file_path,'w')            
            for j,r_id in enumerate(self.sim_rates_tracked):
                file_out.write("Propensity\t{0:s} (Mean)\t{0:s} (STD)\n".format(r_id) )   
                for m in range(len(self.data_stochsim.propensities_distributions_means[j][0])):
                    r_prop = self.data_stochsim.propensities_distributions_means[j][0][m]
                    r_probability_mean = self.data_stochsim.propensities_distributions_means[j][1][m]
                    r_probability_std = self.data_stochsim.propensities_distributions_standard_deviations[j][1][m] 
                    file_out.write("{0}\t{1:f}\t{2:f}\n".format(r_prop,r_probability_mean,r_probability_std))
                file_out.write("\n")                
            print("Info: Averaged propensities distributions output is successfully saved at: {0:s}".format(file_path) )
            
        elif (datatype.lower() == 'species') and (analysis.lower() == 'autocorrelation') and (IsAverage):         
            if not self.data_stochsim_grid.HAS_SPECIES_AUTOCORRELATIONS:
                print("*** WARNING ***: Autocorrelations are not yet calculated. StochPy automatically calculates autocorrelations with pre-defined settings. You can use GetSpeciesAutocorrelations(species2calc=True,n_samples=51)")
                self.GetSpeciesAutocorrelations()
            
            file_path = '{0:s}.txt'.format(directory)
            file_out = open(file_path,'w')            
            for i,s_id in enumerate(self.sim_species_tracked):
                file_out.write(r'Lag ($\tau$)\t{0:s} (Mean)\t{0:s} (STD)\n'.format(s_id) )
                for j in range(len(self.data_stochsim_grid.species_autocorrelations_means[i])):
                    acor_mean = self.data_stochsim_grid.species_autocorrelations_means[i][j]
                    acor_std = self.data_stochsim_grid.species_autocorrelations_standard_deviations[i][j]                                     
                    file_out.write("{0:f}\t{0:f}\t{0:f}\n".format(self.data_stochsim_grid.time[j][0],acor_mean,acor_std) )
                file_out.write("\n")                
            print("Info: Averaged species autocorrelations output is successfully saved at: {0:s}".format(file_path) )
            
        elif (datatype.lower() == 'species') and (analysis.lower() == 'autocovariance') and (IsAverage):          
            if not self.data_stochsim_grid.HAS_SPECIES_AUTOCOVARIANCES:
                print("*** WARNING ***: Autocovariances are not yet calculated. StochPy automatically calculates autocovariances with pre-defined settings. You can use GetSpeciesAutocovariances(species2calc=True,n_samples=51)")
                self.GetSpeciesAutocovariances()
            
            file_path = '{0:s}.txt'.format(directory)
            file_out = open(file_path,'w')            
            for i,s_id in enumerate(self.sim_species_tracked):
                file_out.write(r'Lag ($\tau$)\t{0:s} (Mean)\t{0:s} (STD)\n'.format(s_id) )
                for j in range(len(self.data_stochsim_grid.species_autocovariances_means[i])):
                    acor_mean = self.data_stochsim_grid.species_autocovariances_means[i][j]
                    acor_std = self.data_stochsim_grid.species_autocovariances_standard_deviations[i][j]                                     
                    file_out.write("{0:f}\t{0:f}\t{0:f}\n".format(self.data_stochsim_grid.time[j][0],acor_mean,acor_std) )
                file_out.write("\n")               
            print("Info: Averaged species autocovariances output is successfully saved at: {0:s}".format(file_path) )
            
        elif (datatype.lower() == 'propensities') and (analysis.lower() == 'autocorrelation') and (IsAverage):          
            if not self.data_stochsim_grid.HAS_PROPENSITIES_AUTOCORRELATIONS:
                print("*** WARNING ***: Autocorrelations are not yet calculated. StochPy automatically calculates autocorrelations with pre-defined settings. You can use GetPropensitiesAutocorrelations(rates2calc=True,n_samples=51)")
                self.GetPropensitiesAutocorrelations()          
            file_path = '{0:s}.txt'.format(directory)
            file_out = open(file_path,'w')            
            for j,r_id in enumerate(self.sim_rates_tracked):
                file_out.write(r'Lag ($\tau$)\t{0:s} (Mean)\t{0:s} (STD)\n'.format(r_id) )   
                for m in range(len(self.data_stochsim_grid.propensities_autocorrelations_means[j])):
                    acor_mean = self.data_stochsim_grid.propensities_autocorrelations_means[j][m]
                    acor_std = self.data_stochsim_grid.propensities_autocorrelations_standard_deviations[j][m]
                    file_out.write("{0:f}\t{0:f}\t{0:f}\n".format(self.data_stochsim_grid.time[m][0],acor_mean,acor_std))
                file_out.write("\n")                
            print("Info: Averaged propensities autocorrelations output is successfully saved at: {0:s}".format(file_path) )

        elif (datatype.lower() == 'propensities') and (analysis.lower() == 'autocovariance') and (IsAverage):          
            if not self.data_stochsim_grid.HAS_PROPENSITIES_AUTOCOVARIANCES:
                print("*** WARNING ***: Autocovariances are not yet calculated. StochPy automatically calculates autocovariances with pre-defined settings. You can use GetPropensitiesAutocovariances(rates2calc=True,n_samples=51)")
                self.GetPropensitiesAutocovariances()
            
            file_path = '{0:s}.txt'.format(directory)
            file_out = open(file_path,'w')            
            for j,r_id in enumerate(self.sim_rates_tracked):
                file_out.write(r'Lag ($\tau$)\t{0:s} (Mean)\t{0:s} (STD)\n'.format(r_id) )
                for m in range(len(self.data_stochsim_grid.propensities_autocovariances_means[j])):
                    acor_mean = self.data_stochsim_grid.propensities_autocovariances_means[j][m]
                    acor_std = self.data_stochsim_grid.propensities_autocovariances_standard_deviations[j][m]  
                    file_out.write("{0:f}\t{0:f}\t{0:f}\n".format(self.data_stochsim_grid.time[m][0],acor_mean,acor_std))
                file_out.write("\n")                
            print("Info: Averaged propensities autocovariances output is successfully saved at: {0:s}".format(file_path) )

        else:
            raise UserWarning("No valid option specified. Nothing is exported. See help function (help(Export2File))")
            
    def Import2StochPy(self,filename,filedir,delimiter='\t'):
        """
        Can import time series data with the following format:
        
        Time S1 S2 S3 Fired Reactions
        0    1  0  1  nan
        1.5  0  0  2  1
        etc.
        
        or 
        
        Time S1 S2 S3
        0    1  0  1
        1.5  0  0  2
        etc.      
        
        In the future, this function will probably support more data types. We currently accept the default output of the Gillespie algorithm from which other data types can be derived.
        
        Input: 
         - *filename* (string)
         - *filedir* (string)
         - *delimiter* (string)
        """
        print("*** WARNING ***: In construction - This function currently accepts species time series data only!")        
        try:
            filepath = os.path.join(filedir,filename)
            file_in = open(filepath,'r') 
        except IOError:
            print("File path {0:s} does not exist".format(filepath) )
            sys.exit()
        
        L_sim_output = []
        L_data = file_in.readlines()
          
        nreactions = int(L_data[0].strip().split(':')[1])
        self.SSA.rate_names = []
        for r in range(1,nreactions+1):
            self.SSA.rate_names.append('R{0:d}'.format(r) )          

        print("Info: Reaction identifiers are unknown, StochPy created the following identifiers automatically:\t{0}".format(self.SSA.rate_names) )
        print("Info: Update 'smod.SSA.rate_names' if other identifiers are desired")                
        
        L_header = L_data[1].strip().split(delimiter)
        L_species_names = L_header[1:]      
        self._IsTauLeaping = False
        if L_header[-1] != 'Fired Reaction': # no fired reactions stored                    
            self._IsTauLeaping = True
        else:
            L_species_names.pop(-1)         
             
        for dat in L_data[2:]:
            fdat = [float(x) for x in dat.strip().split(delimiter)] # parse data and convert to float (is for some reason faster than integers ...)
            if not self._IsTauLeaping and not math.isnan(fdat[-1]):
               fdat[-1] = int(fdat[-1])                  
            L_sim_output.append(fdat)      
        self.SSA.sim_output = L_sim_output
        self.SSA.species_names = L_species_names
        self.SSA.timestep = len(L_sim_output)
        self.SSA.sim_t = L_sim_output[-1][0]

        self._current_trajectory = 1 # HARD CODED
        self.sim_trajectories_done = 1      
        self.IsTrackPropensities =  False
        self.data_stochsim = IntegrationStochasticDataObj()           
        self.FillDataStochsim(IsImport=True)     
        try:
            self.plot = Analysis.DoPlotting(self.data_stochsim.species_labels,self.SSA.rate_names,self.plot.plotnum)
        except:
            self.plot = Analysis.DoPlotting(self.data_stochsim.species_labels,self.SSA.rate_names)
        self._IsSimulationDone = True        
            
    def ShowSpecies(self):
        """ Print the species of the model """
        print(self.SSA.species_names)

    def ShowOverview(self):
        """ Print an overview of the current settings """
        print("Current Model:\t{0:s}".format(self.model_file) )
        if self.sim_mode == "steps": 
            print("Number of time steps:\t{0:d}".format(self.sim_end) )
        elif self.sim_mode == "time":
            print("Simulation end time:\t{0:1.2f}".format(self.sim_end) )
        print("Current Algorithm:\t{0:s}".format(self.sim_method) )
        print("Number of trajectories:\t{0:d}".format(self.sim_trajectories) )
        if self.IsTrackPropensities:
             print("Propensities are tracked")
        else:
             print("Propensities are not tracked")

    def DeleteTempfiles(self):
        """ Deletes all .dat files """
        for name in os.listdir(self.temp_dir):
            try:
                os.remove(os.path.join(self.temp_dir,name))
            except:
                dir2delete = os.path.join(self.temp_dir,name)
                shutil.rmtree(dir2delete, ignore_errors=True)

    def DoTestsuite(self,epsilon_ = 0.01,sim_trajectories=1000):
        """
        DoTestsuite(epsilon_ = 0.01,sim_trajectories=1000)
        
        Do "sim_trajectories" simulations until t=50 and print the interpolated result for t = 0,1,2,...,50
        
        Input:
         - *epsilon_* [default = 0.01]: useful for tau-Leaping simulations (float)
         - *sim_trajectories* [default = 1000]
        """      
        self.DoStochSim(mode='time',end=50,epsilon = epsilon_,trajectories = sim_trajectories)
        self.GetRegularGrid(n_samples = 51)
        self.PrintAverageSpeciesTimeSeries()        

    def FillDataStochsim(self,IsImport=False):
        """
        Put all simulation data in the data object data_stochsim
        
        Input:
         - *IsImport* (boolean) [False]
        """ 
        if not IsImport and self.settings.species_selection:   
            self.sim_species_tracked = [s_id for s_id in self.settings.species_selection]
        else:
            self.sim_species_tracked = copy.copy(self.SSA.species_names)
            
        if not IsImport and self.settings.rate_selection:
            self.sim_rates_tracked = [r_id for r_id in self.settings.rate_selection]
        else:
            self.sim_rates_tracked = copy.copy(self.SSA.rate_names)             
        
        (L_probability_mass,D_means,D_stds,D_moments) = Analysis.GetDataDistributions(self.SSA.sim_output,self.sim_species_tracked)    
        sim_dat = np.array(self.SSA.sim_output)   
        self.data_stochsim.setTime(sim_dat[:,0])
        self.data_stochsim.setSpeciesDist(L_probability_mass,D_means,D_stds,D_moments)
        
        if not self._IsTauLeaping:
            self.data_stochsim.setSpecies(sim_dat[:,1:-1].astype(np.uint32),self.sim_species_tracked) #28-11-2013
            self.data_stochsim.setFiredReactions(sim_dat[:,-1]) #.astype(np.uint16))
        else:
            self.data_stochsim.setSpecies(sim_dat[:,1:].astype(np.uint32),self.sim_species_tracked)
            
        self.data_stochsim.setSimulationInfo(self.SSA.timestep,self.SSA.sim_t,self._current_trajectory)
        if self.IsTrackPropensities:
            (L_probability_mass,D_means,D_stds,D_moments) = Analysis.GetDataDistributions(self.SSA.propensities_output,self.sim_rates_tracked)
            self.data_stochsim.setPropensitiesDist(L_probability_mass,D_means,D_stds,D_moments)
            self.data_stochsim.setPropensities(self.SSA.propensities_output,self.sim_rates_tracked)
            
    def PrintSpeciesTimeSeries(self):
        """ Print time simulation output for each generated trajectory """      
        assert self._IsSimulationDone, "Before printing time simulation results first do a stochastic simulation"      
        for n in range(1,self.sim_trajectories_done+1):
            if self.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            print('Time', "\t", end="")
            for s_id in self.sim_species_tracked:
                print(s_id,"\t",end="")
            print()
            for timepoint in self.data_stochsim.getSpecies():
                for value in timepoint:
                    print(value,"\t",end="")
                print()            

    def PrintPropensitiesTimeSeries(self):
        """ Print a time series of the propensities each generated trajectory """      
        assert (self.IsTrackPropensities and self._IsSimulationDone), "Before plotting a time series of propensities first do a stochastic simulation with tracking propensities (use the IsTrackPropensities flag in DoStochSim)"
        for n in range(1,self.sim_trajectories_done+1):   	
            if self.sim_trajectories_done > 1:        
                self.GetTrajectoryData(n)
            print('Time', "\t", end="")
            for r_id in self.sim_rates_tracked:
                print(r_id,"\t",end="")
            print()
            for timepoint in self.data_stochsim.getPropensities():
                for value in timepoint:               
                     print(value,"\t",end="")
                print()

    def PrintSpeciesDistributions(self):
        """ Print obtained distributions for each generated trajectory """      
        assert self._IsSimulationDone, "Before printing distributions first do a stochastic simulation"
        assert not self._IsOnlyLastTimepoint, "Determining statistics is disabled when saving only the last time point"
        for n in range(1,self.sim_trajectories_done+1):
            if self.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)
            for i,L_species_dist in enumerate(self.data_stochsim.species_distributions):
                print("Amount ({0:s})\tProbability".format(self.sim_species_tracked[i]) )
                for m in range(len(L_species_dist[0])):
                    x = L_species_dist[0][m]
                    p_x = L_species_dist[1][m]
                    if not p_x < 0.001:
                        print("{0:d}\t{1:0.3f}".format(x,p_x))
                    else:
                        print("{0:d}\t{1:0.3e}".format(x,p_x))          

    def PrintPropensitiesDistributions(self):
        """ Print obtained distributions for each generated trajectory """     
        assert (self.IsTrackPropensities and self._IsSimulationDone),"Before printing distributions first do a stochastic simulation"
        assert not self._IsOnlyLastTimepoint, "Determining statistics is disabled when saving only the last time point"
        for n in range(1,self.sim_trajectories_done+1):    
            if self.sim_trajectories_done > 1:  
                self.GetTrajectoryData(n)
            
            for j,L_prop_dist in enumerate(self.data_stochsim.propensities_distributions):
                print("Propensity ({0:s})\tProbability".format(self.sim_rates_tracked[j]) )
                for m in range(len(L_prop_dist[0])):                    
                    x = L_prop_dist[0][m]
                    p_x = L_prop_dist[1][m]
                    if not p_x < 0.001:
                        print("{0:d}\t{1:0.3f}".format(x,p_x))   
                    else:
                        print("{0:d}\t{1:0.3e}".format(x,p_x))                                           

    def PrintWaitingtimesDistributions(self):
        """ Print obtained waiting times """
        assert not self._IsTauLeaping, "Tau-Leaping method does not allow for calculation of waiting times"
        if (not self.data_stochsim.HAS_WAITINGTIMES) and (not self._IsTauLeaping):
            self.GetWaitingtimes()
        for n in range(1,self.sim_trajectories_done+1):   
            if self.sim_trajectories_done > 1:
                self.GetTrajectoryData(n)           
            for r_id in self.data_stochsim.waiting_times:
                print("Waiting times\t({0:s})".format(r_id) )
                waiting_times_r = self.data_stochsim.waiting_times[r_id]
                for wtime in waiting_times_r:
                    if not wtime < 0.001:
                        print("{0:0.3f}".format(wtime))   
                    else:
                        print("{0:0.3e}".format(wtime))                        

    def PrintAverageSpeciesTimeSeries(self):    
        """ Analyze the average output over all generated trajectories """
        if not self.HAS_AVERAGE:
            print("*** WARNING ***: No regular grid is created yet. Use GetRegularGrid(n_samples) if averaged results are unsatisfactory (e.g. more or less 'points')")
            self.GetRegularGrid()
        for s_id in self.data_stochsim.species_labels:              
            print("\t{0:s} (Mean)\t{0:s} (STD)".format(s_id),end="")
        print()
        L_means = np.transpose(self.data_stochsim_grid.species_means)
        L_stds = np.transpose(self.data_stochsim_grid.species_standard_deviations)        
        for i,t in enumerate(self.data_stochsim_grid.time): 
            print(t[0],end="")            
            for j in range(len(self.data_stochsim_grid.species_means)):                 
                mu = L_means[i][j]
                sigma = L_stds[i][j]
                if not mu < 0.001 and not sigma < 0.001:
                    print("\t{0:0.3f}\t{1:0.3f}".format(mu,sigma),end="") 
                elif not mu < 0.001:
                    print("\t{0:0.3f}\t{1:0.3e}".format(mu,sigma),end="")
                else:
                    print("\t{0:0.3e}\t{1:0.3e}".format(mu,sigma),end="")                                                     
            print()            
                
    def PrintAveragePropensitiesTimeSeries(self):
        """ Analyze the average output over all generated trajectories """
        assert self.IsTrackPropensities, "Before plotting propensities first do a stochastic simulation with tracking propensities (use the IsTrackPropensities flag in DoStochSim)"
        if (not self.HAS_AVERAGE) and (self.IsTrackPropensities):
            print("*** WARNING ***: No regular grid is created yet. Use GetRegularGrid(n_samples) if averaged results are unsatisfactory (e.g. more or less 'points')")
            self.GetRegularGrid()
        print("Time",end="")
        for r_id in self.sim_rates_tracked:
            print("\t{0:s} (Mean)\t{0:s} (STD)".format(r_id),end="")
        print()
        L_means = np.transpose(self.data_stochsim_grid.propensities_means)
        L_stds = np.transpose(self.data_stochsim_grid.propensities_standard_deviations)
        for i,t in enumerate(self.data_stochsim_grid.time): 
            print(t[0],end="")
            for j in range(len(self.data_stochsim_grid.propensities_means)):                 
                mu = L_means[i][j]
                sigma = L_stds[i][j]
                if not mu < 0.001 and not sigma < 0.001:
                    print("\t{0:0.3f}\t{1:0.3f}".format(mu,sigma),end="")   
                elif not mu < 0.001:
                    print("\t{0:0.3f}\t{1:0.3e}".format(mu,sigma),end="")   
                else:
                    print("\t{0:0.3e}\t{1:0.3e}".format(mu,sigma),end="")    
            print() 
