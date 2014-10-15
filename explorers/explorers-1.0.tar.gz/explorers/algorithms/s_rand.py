"""\
Pure random sensory explorer.
Needs motor and sensor boundaries.
"""
from __future__ import absolute_import, division, print_function
import random
import collections

import learners

from .. import conduits
from .. import explorer
from .. import tools


defcfg = explorer.defcfg._copy(deep=True)
defcfg._describe('s_channels', instanceof=collections.Iterable,
                 docstring='Sensory channels to generate random goal from')
defcfg._branch('learner')
defcfg.classname = 'explorers.RandomGoalExplorer'


class RandomGoalExplorer(explorer.Explorer):
    """\
    Just a random explorer
    Necessitate a sensory bounded environement.
    """
    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(RandomGoalExplorer, self).__init__(cfg)

        assert len(self.cfg.learner) > 0
        self.cfg.learner.m_channels = self.m_channels
        self.cfg.learner.s_channels = self.s_channels
        learners_list = [learners.Learner.create(self.cfg.learner)]

        for learner in learners_list:
            self.fwd_conduit.register(learner.fwd_request)
            self.inv_conduit.register(learner.inv_request)
            self.obs_conduit.register(learner.update_request)

    def _explore(self):
        s_goal = tools.random_signal(self.s_channels)
        m_signal = self._inv_request(s_goal)
        if m_signal is None:
            m_signal = tools.random_signal(self.m_channels)
        return {'m_signal': m_signal, 's_goal': s_goal, 'from': 'goal.babbling'}

    def _inv_request(self, s_goal):
        orders = self.inv_conduit.poll({'s_goal': s_goal,
                                        'm_channels': self.m_channels})
        return None if len(orders) == 0 else random.choice(orders)

    def _fwd_request(self, m_signal):
        predictions = self.fwd_conduit.poll({'m_signal': m_signal,
                                             's_channels': self.s_channels})
        return None if len(predictions) == 0 else random.choice(predictions)

