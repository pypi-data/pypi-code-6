"""\
Restrict goal explorer
"""
from __future__ import absolute_import, division, print_function
import collections
import copy

from .. import Explorer


defcfg = Explorer.defcfg._copy(deep=True)
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels to generate random goal from')
defcfg._describe('manual_s_bounds', instanceof=collections.Iterable,
                 docstring='manually defined sensory boundaries')
defcfg.classname = 'explorers.RestrictGoalExplorer'
defcfg._branch('explorer')


class RestrictGoalExplorer(Explorer):
    """\
    Bound the environement.
    """
    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(RestrictGoalExplorer, self).__init__(cfg)
        s_channels = copy.deepcopy(self.cfg.s_channels)
        for c in s_channels:
            if c.name in self.cfg.manual_s_bounds:
                c.bounds = self.cfg.manual_s_bounds[c.name]

        self.cfg.s_channels = s_channels
        self.cfg.explorer.m_channels = self.cfg.m_channels
        self.cfg.explorer.s_channels = self.cfg.s_channels
        self.ex = Explorer.create(self.cfg.explorer, **kwargs)
        self.exp_conduit.register(self.ex.receive)

    def _explore(self):
        return self.ex.explore()
