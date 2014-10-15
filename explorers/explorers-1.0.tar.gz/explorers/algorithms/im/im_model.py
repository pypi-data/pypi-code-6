import numbers
import math
import sys

import numpy as np

import forest

from ... import tools


defcfg = forest.Tree()
defcfg._describe('classname', instanceof=str)
defcfg.classname = 'LocalInterestModel'

class LocalInterestModel(object):

    defcfg = defcfg._deepcopy()

    def __init__(self, cfg):
        self.cfg        = cfg
        self.cfg._update(self.defcfg, overwrite=False)
        self._uptodate  = False
        self._weight    = 0
        self.effects    = []
        self.preds      = []
        self.pred_error = []
        self.goals      = []
        self.goal_error = []

    @property
    def weight(self):
        if not self._uptodate:
            self._recompute()
        return self._weight

    def _recompute(self):
        """Method to compute the weight from the goal and prediction sequence."""
        self._uptodate = True

    def add_effect(self, effect, prediction=None):
        self.effects.append(effect)
        if prediction is not None:
            self.preds.append((effect, prediction))
        self._uptodate = False

    def add_goal(self, effect, goal):
        self.goals.append((effect, goal))
        self._uptodate = False



defcfg = defcfg._deepcopy()
defcfg.classname = 'PredictiveNoveltyMotivation'
defcfg._describe('C', instanceof=numbers.Real, docstring='', default=1.0)
defcfg._describe('pred_error.window', instanceof=numbers.Integral,
                 docstring='the number of error values to average on', default=sys.maxint)

class PredictiveNoveltyMotivation(LocalInterestModel):

    defcfg = defcfg._deepcopy()

    def prediction_error(self):
        for i in range(len(self.pred_error), len(self.preds)):
            effect, prediction = self.preds[i]
            self.pred_error.append(tools.vec_norm_sq(effect, prediction))
        return np.mean(self.pred_error[-self.cfg.pred_error.window:])

    def _recompute(self):
        if len(self.preds) > 0:
            self._weight = self.cfg.C*self.prediction_error()
        self._uptodate = True



defcfg = defcfg._deepcopy()
defcfg.classname = 'IntermediateLevelOfNoveltyMotivation'
defcfg._describe('C_2', instanceof=numbers.Real, docstring='', default=1.0)
defcfg._describe('pred_error_threshold', instanceof=numbers.Real,
                 docstring='The optimal error value', default=0.0)

class IntermediateLevelOfNoveltyMotivation(PredictiveNoveltyMotivation):

    defcfg = defcfg._deepcopy()

    def _recompute(self):
        if len(self.preds) > 0:
            self._weight = self.cfg.C*math.exp(-self.cfg.C_2*(self.prediction_error()-self.cfg.pred_error_threshold)**2)
        self._uptodate = True

