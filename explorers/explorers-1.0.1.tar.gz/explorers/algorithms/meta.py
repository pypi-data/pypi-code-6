"""\
Pure random sensory explorer.
Needs motor and sensor boundaries.
"""
from __future__ import absolute_import, division, print_function
import random
import collections
import numbers

import forest

from .. import conduits
from .. import explorer
from .. import tools


defcfg = explorer.defcfg._deepcopy()
defcfg.classname = 'explorers.MetaExplorer'
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels to generate random goal from')
defcfg._describe('eras', instanceof=collections.Iterable,
                 docstring='The end date of each era of orchestration')
defcfg._describe('weights', instanceof=collections.Iterable,
                 docstring='Relative weights of each explorer during each era. A list of weights per era.')
defcfg._describe('fallback', instanceof=(numbers.Integral), default=-1,
                 docstring='The explorer to fallback on if the chosen one returned None. Its value will be returned even if equal to None.')
#defcfg._branch('ex_0') # first explorer
#defcfg._branch('ex_1') # second explorer




class MetaExplorer(explorer.Explorer):
    """\
    An explorer to orchestrate other explorers.
    """

    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(MetaExplorer, self).__init__(cfg, **kwargs)
        self.timecount = 0
        self.current_era = 0
        self.explorers = []

        assert all(self.cfg.eras[i] != None or i == len(self.cfg.eras)-1 for i in range(len(self.cfg.eras)))
        assert all(len(self.cfg.weights[0]) == len(w_i) for w_i in self.cfg.weights)

        for i, _ in enumerate(self.cfg.weights[0]):
            ex_cfg = self.cfg['ex_{}'.format(i)]
            ex_cfg._setdefault('m_channels', self.cfg.m_channels)
            if 's_channels' in self.cfg:
                ex_cfg._setdefault('s_channels', self.cfg.s_channels)
            ex = explorer.Explorer.create(ex_cfg, **kwargs)
            self.exp_conduit.register(ex.receive)
            self.explorers.append(ex)

    def _explore(self):
        end_time = self.cfg.eras[self.current_era]
        if (end_time is not None and self.timecount >= end_time):
            self.current_era += 1

        idx = tools.roulette_wheel(self.cfg.weights[self.current_era])
        exploration = self.explorers[idx].explore()
        if exploration is None and self.cfg.fallback != -1:
            return self.explorers[self.cfg.fallback].explore()
        return exploration

    def receive(self, exploration, feedback):
        self.timecount += 1
        super(MetaExplorer, self).receive(exploration, feedback)
