"""\
Meshgrid goal explorer
"""
from __future__ import absolute_import, division, print_function
import random
import numbers
import collections

from .. import tools
from .. import meshgrid
from .. import Explorer


defcfg = Explorer.defcfg._deepcopy()
defcfg._describe('res', instanceof=(numbers.Integral, collections.Iterable),
                 docstring='resolution of the meshgrid')
defcfg._describe('n_perturbations', instanceof=numbers.Integral,
                 docstring='number of perturbations per new bins')
defcfg._describe('m_disturb', instanceof=numbers.Real,
                 docstring='percentage of range for the perturbation')
defcfg.classname = 'explorers.MotorDisturbExplorer'


class MotorDisturbExplorer(Explorer):
    """\
    Goal explorer that only sets goal in non-empty cells of the meshgrid.
    """
    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(MotorDisturbExplorer, self).__init__(cfg)
        self.m_disturb = tuple(self.cfg['m_disturb']*(c_i.bounds[1]-c_i.bounds[0])
                               for c_i in self.m_channels)
        self._meshgrid = meshgrid.MeshGrid(self.cfg, [c.bounds for c in self.s_channels])
        self._seeds  = []
        self._seed_count = []


    def _explore(self):
        if len(self._seeds) == 0:
            m_signal = tools.random_signal(self.m_channels)
        else:
            m_signal = self._seeds[-1]
            m_vector = tools.to_vector(m_signal, self.m_channels)
            # we draw the perturbation inside legal values, rather than clamp it afterward
            m_disturbed = [random.uniform(max(v_i - d_i, c_i.bounds[0]),
                                          min(v_i + d_i, c_i.bounds[1]))
                           for v_i, d_i, c_i in zip(m_vector, self.m_disturb, self.m_channels)]
            m_signal = tools.to_signal(m_disturbed, self.m_channels)

            self._seed_count[-1] += 1
            if self._seed_count[-1] >= self.cfg['n_perturbations']:
                self._seeds.pop()
                self._seed_count.pop()

        return {'m_signal': m_signal}

    def receive(self, exploration, feedback):
        super(MotorDisturbExplorer, self).receive(exploration, feedback)
        coo = self._meshgrid.add(tools.to_vector(feedback['s_signal'], self.s_channels), exploration['m_signal'])
        cell = self._meshgrid._bins[coo]
        if len(cell) == 1: # new cell
            self._seeds.append(exploration['m_signal'])
            self._seed_count.append(0)
