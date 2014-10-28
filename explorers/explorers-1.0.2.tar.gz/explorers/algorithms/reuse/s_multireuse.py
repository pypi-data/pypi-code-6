"""Reuse generators, that yield order to reuse"""

from __future__ import print_function, division, absolute_import

import numbers
import collections
import itertools

from ... import tools
from ... import meshgrid
from ... import Explorer
from .s_reuse import ReuseExplorer


defcfg = Explorer.defcfg._deepcopy()
defcfg.classname = 'explorers.MultiReuseExplorer'

defcfg._branch('reuse', value=ReuseExplorer.defcfg.reuse._deepcopy())
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels to generate random goal from')

defcfg._describe('pick_algorithm', instanceof=str, default='diversity',
                 docstring='how much the ratio decrease with each reuse')
defcfg._describe('res', instanceof=numbers.Integral,
                 docstring='the resolution of the meshgrid for the diversity count')


class MultiReuseExplorer(Explorer):
    """A reuse explorer"""

    defcfg = defcfg

    def __init__(self, cfg, datasets=(), **kwargs):
        super(MultiReuseExplorer, self).__init__(cfg)

        self.reusers    = {}
        self._meshgrids = {}
        for i, dataset in enumerate(datasets):
            ex_id = 'ex_{}'.format(i)
            try:
                cfg[ex_id]
            except KeyError:
                cfg._strict(strict=False)
                cfg[ex_id] = ReuseExplorer.defcfg._deepcopy()
                cfg._strict(strict=True)
                cfg[ex_id].reuse._update(cfg.reuse, overwrite=True)
                cfg[ex_id].m_channels = cfg.m_channels
            r = ReuseExplorer(cfg[ex_id], [dataset], **kwargs)
            self.reusers[r.uuid] = r
            self._meshgrids[r.uuid] = meshgrid.MeshGrid(self.cfg, [c.bounds for c in self.cfg.s_channels])
            self.exp_conduit.register(r.receive)


    def _explore(self):
        if len(self.reusers) == 0:
            return None
        if self.cfg.pick_algorithm == 'diversity':
            diversities = [max(1, len(self._meshgrids[r_uuid]._nonempty_bins)/max(1, len(self._meshgrids[r_uuid])))
                           for r_uuid in self.reusers.keys()]
        else :
            assert self.cfg.pick_algorithm == 'random'
            diversities = [1 for _ in self.reusers]
        idx = tools.roulette_wheel(diversities)
        r_uuid = next(itertools.islice(self.reusers.keys(), idx, idx+1))

        exploration = self.reusers[r_uuid].explore()
        if exploration is None:
            del self.reusers[r_uuid]
            return self.explore()
        return exploration

    def receive(self, exploration, feedback):
        super(MultiReuseExplorer, self).receive(exploration, feedback)

        try:
            s_vector = tools.to_vector(feedback['s_signal'], self.cfg.s_channels)
            self._meshgrids[exploration['uuid']].add(s_vector)
        except KeyError:
            pass
