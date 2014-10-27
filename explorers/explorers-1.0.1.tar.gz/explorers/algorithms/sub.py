"""\
Pure random sensory explorer.
Needs motor and sensor boundaries.
"""
from __future__ import absolute_import, division, print_function
import random
import collections

import forest

from .. import conduits
from .. import explorer
from .. import tools


defcfg = explorer.defcfg._deepcopy()
defcfg.classname = 'explorers.SubExplorer'




class SubExplorer(explorer.Explorer):
    """\
    An explorer that support channels groups, and undeclared sensory channels.
    """

    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(SubExplorer, self).__init__(cfg, **kwargs)
        self.explorers = []

        assert all(len(self.cfg.weights[0]) == len(w_i) for w_i in self.cfg.weights)

        for i, _ in enumerate(self.cfg.weights[0]):
            ex_cfg = self.cfg['ex_{}'.format(i)]
            ex_cfg._update(self.cfg, overwrite=False, described_only=True)
            self.explorers.append(explorer.Explorer.create(ex_cfg, **kwargs))

    def explore(self):
        if (self.timecount >= self.cfg.eras[self.current_era]):
            self.current_era += 1

        idx = tools.roulette_wheel(self.cfg.weights[self.current_era])
        return self.explorers[idx].explore()

    def receive(self, exploration, feedback):

        self.timecount += 1
        self.obs_conduit.receive(feedback)
        for ex in self.explorers:
            ex.receive(feedback)
