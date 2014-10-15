"""\
Meshgrid goal explorer
"""
from __future__ import absolute_import, division, print_function
import random
import numbers
import collections

from .. import conduits
from .. import tools
from .. import meshgrid
from . import s_mesh


defcfg = s_mesh.MeshgridGoalExplorer.defcfg._copy(deep=True)
defcfg._pop('cutoff')
defcfg.classname = 'explorers.UnreachGoalExplorer'


class UnreachGoalExplorer(s_mesh.MeshgridGoalExplorer):
    """\
    Necessitate a sensory bounded environement.
    """
    defcfg = defcfg

    def _choose_goal(self):
        guard = 0
        while guard < 100:
            s_goal = tools.random_signal(self.s_channels)
            s_vector = tools.to_vector(s_goal, self.s_channels)
            if self._meshgrid.empty_bin(s_vector):
                return s_goal
        return s_goal

    def _explore(self):
        # pick a random bin
        s_goal   = self._choose_goal()
        m_signal = self._inv_request(s_goal)
        return {'m_signal': m_signal, 's_goal': s_goal, 'from': 'goal.babbling.unreach'}
