"""Reuse generators, that yield order to reuse"""

from __future__ import print_function, division, absolute_import
import random
import numbers
import collections

from ... import meshgrid
from ... import Explorer
from ... import tools


defcfg = Explorer.defcfg._deepcopy()
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels')
defcfg._describe('reuse.res', instanceof=(numbers.Integral, collections.Iterable),
                 docstring='resolution of the meshgrid')
defcfg.classname = 'explorers.GoalReuseExplorer'


class GoalReuseExplorer(Explorer):
    """A reuse explorer"""

    defcfg = defcfg

    def __init__(self, cfg, datasets=(), **kwargs):
        super(GoalReuseExplorer, self).__init__(cfg)
        assert len(datasets) == 1
        self._dataset = datasets[0]
        assert self.m_channels == self._dataset['m_channels'], '{} different from {}'.format(self.m_channels,
                                                                                             self._dataset['m_channels'])

        self.reuse_m_signals = set()
        self._reuse_meshgrid = meshgrid.ExplorerMeshGrid(self.cfg.reuse,
                                                         self._dataset['s_channels'],
                                                         self._dataset['m_channels'])
        for explo, feedback in self._dataset['explorations']:
            m_vector = tools.to_vector(explo['m_signal'], self.m_channels)
            self.reuse_m_signals.add(m_vector)

            self._reuse_meshgrid.add(feedback['s_signal'], m_signal=explo['m_signal'])

        self._meshgrid = meshgrid.ExplorerMeshGrid(self.cfg.reuse, self.s_channels, self.m_channels)
        self._bin_map = {}

    def _explore(self):
        if len(self._bin_map) == 0:
            return None
        else:
            m_signal = None
            while m_signal is not None:
                # take one of the non-empty bins
                bin_coo = random.choice(self._bin_map.keys())
                # look up the bins corresponding to it in the reuse meshgrid
                reuse_coo = random.choice(self._bin_map[bin_coo].keys())
                # choose one non-empty and draw a m_signal from it.
                try:
                    _, m_signal = self._reuse_meshgrid.bins[reuse_coo].draw(replace=False)
                except KeyError:
                    self._bin_map[bin_coo].pop(reuse_coo)
                    if len(self._bin_map[bin_coo]) == 0:
                        self._bin_map.pop(bin_coo)
                        if len(self._bin_map) == 0:
                            return None

            return {'m_signal': m_signal}

    def receive(self, exploration, feedback):
        super(GoalReuseExplorer, self).receive(exploration, feedback)

        # check if m_vector is in the reuse data
        m_vector = tools.to_vector(exploration['m_signal'], self.m_channels)
        if m_vector in self.reuse_m_signals:
            # if it is look up the corresponding bin
            reuse_coo = self._reuse_meshgrid._m_map[m_vector]

            # add this bin to the ancestor of of the current meshgrid bin.
            bin_coo = self._meshgrid.add(feedback['s_signal'], exploration['m_signal'])
            self._bin_map.setdefault(bin_coo, {})
            self._bin_map[bin_coo].setdefault(reuse_coo, 0)
            self._bin_map[bin_coo][reuse_coo] += 1
