#!/usr/env/bin python
import pandas as pd

from numpy.random import RandomState

from trials_functions import expand, extend, add_block

class TrialsMaker(object):
    def __init__(self, seed=None, trials=None):
        """
        TrialsMakers are wrappers for pandas.DataFrames for making trial lists.
        
        :param seed: Seed random number generator. If `seed` is `None`, no
            randomization will occur.
        :type seed: int or None.
        :param trials: Object to be coerced to a `pandas.DataFrame`. If trials
            isn't set with the constructor, can be set with `set_trials`.
        :type trials: pandas.DataFrame, dict, list, or None
        """
        self.seed = RandomState(seed)
        self.set_trials(trials)
    
    def set_trials(self, trials):
        """
        Set the base trials for the trials maker.
        
        :param pandas.DataFrame trials: Trial list. 
        """
        self.trials = pd.DataFrame(trials)
    
    def expand(ratio, name, values=[1,0], sample=False):
        """
        Copy rows as necessary to satisfy the valid:invalid ratio.
        
        """
        self.trials = expand(self.trials, name, values, ratio, 
                             sample, self.seed)
    
    def extend(reps=None, max_length=None, rep_ix=None, row_ix=None):
        """
        Duplicate the unique trials for a total length less than the max.
        """
        self.trials = extend(self.trials, reps, max_length, rep_ix, row_ix)
    
    def add_block(size, name='block', start_at=0, id_col=None):
        """
        Create a new column for block.
        """
        self.trials = add_block(self.trials, size, name, start_at, id_col, seed)
