"""\
Meshgrid goal explorer
"""
from __future__ import absolute_import, division, print_function
import sys
import random
import numbers
import collections

from .. import tools
from .. import meshgrid
from .s_rand import RandomGoalExplorer


defcfg = RandomGoalExplorer.defcfg._copy(deep=True)
defcfg._describe('res', instanceof=(numbers.Integral, collections.Iterable),
                 docstring='resolution of the meshgrid')
defcfg._describe('cutoff', instanceof=(numbers.Integral), default=sys.maxint,
                 docstring='the maximum number of elements a cell can have '
                           'before goals cease to be set in it.')

defcfg.classname = 'explorers.MeshgridGoalExplorer'


class MeshgridGoalExplorer(RandomGoalExplorer):
    """\
    Goal explorer that only sets goal in non-empty cells of the meshgrid.
    """
    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(MeshgridGoalExplorer, self).__init__(cfg)
        self._meshgrid = meshgrid.MeshGrid(self.cfg, [c.bounds for c in self.s_channels])

    def _explore(self):
        # pick a random bin
        s_bins = list(b for b in self._meshgrid._nonempty_bins if len(b) < self.cfg.cutoff)
        if len(s_bins) == 0:
            return None #s_goal = tools.random_signal(self.s_channels)
        else:
            s_bin = random.choice(s_bins)
            s_goal = tools.random_signal(self.s_channels, s_bin.bounds)

        m_signal = self._inv_request(s_goal)
        return {'m_signal': m_signal, 's_goal': s_goal, 'from': 'goal.babbling.mesh'}

    def receive(self, exploration, feedback):
        super(MeshgridGoalExplorer, self).receive(exploration, feedback)
        self._meshgrid.add(tools.to_vector(feedback['s_signal'], self.s_channels), exploration['m_signal'])
