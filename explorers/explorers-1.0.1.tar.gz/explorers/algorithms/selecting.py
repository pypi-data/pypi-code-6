"""\
Pure random sensory explorer.
Needs motor and sensor boundaries.
"""
from __future__ import absolute_import, division, print_function
import random
import collections
import numbers

from .. import Explorer
from .. import tools
from .. import meshgrid


defcfg = Explorer.defcfg._deepcopy()
defcfg.classname = 'explorers.SelectExplorer'
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels to generate random goal from')
defcfg._describe('res', instanceof=(numbers.Integral, collections.Iterable),
                 docstring='resolution of the meshgrid')
defcfg._describe('window', instanceof=(numbers.Integral, collections.Iterable),
                 docstring='how much into the past to consider')
defcfg._describe('random_ratio', instanceof=numbers.Real,
                 docstring='how often explorers are choosen regardless of weight')
defcfg._describe('head_start', instanceof=numbers.Integral, default=1,
                 docstring='how much fake diversity hit to attribute at the beginning')
defcfg._describe('base_weights', instanceof=(collections.Iterable),
                 docstring='how often explorers are choosen regardless of weight, relative to one another')
defcfg._describe('fallback', instanceof=(numbers.Integral), default=-1,
                 docstring='The explorer to fallback on if the chosen one returned None. Its value will be returned even if equal to None.')
defcfg._describe('weight_history', instanceof=bool, default=True,
                 docstring='Save the weight history')
#defcfg._branch('ex_0') # first explorer
#defcfg._branch('ex_1') # second explorer

class SelectExplorer(Explorer):
    """\
    An explorer to select other explorers based on the diversity (new cells) they discover
    """

    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(SelectExplorer, self).__init__(cfg, **kwargs)
        self._meshgrid = meshgrid.MeshGrid(self.cfg, [c.bounds for c in self.s_channels])
        self._diversities = tuple(collections.deque([1.0 for _ in range(self.cfg.head_start)], self.cfg.window)
                                  for _ in self.cfg.base_weights)

        self._random_weights = tuple(self.cfg.random_ratio*w/sum(self.cfg.base_weights)
                                     for w in self.cfg.base_weights)
        self.weight_history = []

        self.explorers = []
        self._explorer_map = {}
        for i, _ in enumerate(self.cfg.base_weights):
            ex_cfg = self.cfg['ex_{}'.format(i)]
            ex_cfg._setdefault('m_channels', self.cfg.m_channels)
            assert 's_channels' in self.cfg
            if 's_channels' in self.cfg:
                ex_cfg._setdefault('s_channels', self.cfg.s_channels)
            ex = Explorer.create(ex_cfg, **kwargs)
            self.exp_conduit.register(ex.receive)
            self.explorers.append(ex)
            self._explorer_map[ex.uuid] = self._diversities[i]

    @property
    def diversities(self):
        return tuple(sum(d)/max(1, len(d)) for d in self._diversities)

    @property
    def weights(self):
        return tuple((1-self.cfg.random_ratio)*sum(dw)/max(1, len(dw)) + rw for rw, dw
                     in zip(self._random_weights, self._diversities))

    def _explore(self):
        weights = self.weights
        idx = tools.roulette_wheel(weights)
        if self.cfg.weight_history:
            self.weight_history.append(weights)
        # if random.random() < self.cfg.random_ratio:
        #     idx = tools.roulette_wheel(self.cfg.base_weights)
        # else:
        #     idx = tools.roulette_wheel(self.diversities)

        exploration = self.explorers[idx].explore()
        if exploration is None and self.cfg.fallback != -1:
            return self.explorers[self.cfg.fallback].explore()
        return exploration

    def receive(self, exploration, feedback):
        super(SelectExplorer, self).receive(exploration, feedback)
        coo = self._meshgrid.add(tools.to_vector(feedback['s_signal'], self.s_channels), exploration['m_signal'])
        cell = self._meshgrid._bins[coo]
        if len(cell) == 1: # new cell
            self._explorer_map[exploration['uuid']].append(1.0)
        else:
            self._explorer_map[exploration['uuid']].append(0.0)

