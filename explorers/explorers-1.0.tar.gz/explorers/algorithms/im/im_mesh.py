"""\
Meshgrid goal explorer
"""
from __future__ import absolute_import, division, print_function
import random
import numbers
import collections

from ... import conduits
from ... import tools
from ... import meshgrid
from ..  import s_rand
from .   import im_grid

defcfg = s_rand.defcfg._copy(deep=True)
defcfg._describe('res', instanceof=(numbers.Integral, collections.Iterable),
                 docstring='resolution of the meshgrid')
defcfg._describe('lim.classname', instanceof=str,
                 docstring='classname of interest model')
defcfg.classname = 'explorers.IMExplorer'


class IMExplorer(s_rand.RandomGoalExplorer):
    """\
    Necessitate a sensory bounded environement.
    """
    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(IMExplorer, self).__init__(cfg)
        self._meshgrid = im_grid.IMGrid(cfg, [c.bounds for c in self.s_channels])

    def _explore(self):
        # pick a random bin
        try:
            s_bin    = self._meshgrid.draw_bin()
            s_goal   = tools.random_signal(self.s_channels, s_bin.bounds)
            m_signal = self._inv_request(s_goal)
            return {'m_signal': m_signal, 's_goal': s_goal, 'from': 'goal.babbling.im'}
        except ValueError as e:
            return None

    def receive(self, exploration, feedback):
        # getting prediction before updating learners.
        prediction = exploration.get('s_prediction', None)
        if prediction is None:
            prediction = self._fwd_request(exploration['m_signal'])

        super(IMExplorer, self).receive(exploration, feedback)

        pred_vector = None
        if prediction is not None:
            pred_vector = tools.to_vector(prediction, self.s_channels)
        goal = feedback.get('s_goal', None)
        goal_vector = None
        if goal is not None:
            goal_vector = tools.to_vector(goal, self.s_channels)

        self._meshgrid.add(tools.to_vector(feedback['s_signal'], self.s_channels),
                           (tools.to_vector(exploration['m_signal'], self.m_channels),
                            tools.to_vector(feedback['s_signal'], self.s_channels),
                            pred_vector,
                            goal_vector))
