"""\
Meshgrid motor explorer
"""
from __future__ import absolute_import, division, print_function
import random
import numbers
import collections

from .. import conduits
from .. import tools
from .. import meshgrid
from . import m_rand


defcfg = m_rand.defcfg._copy(deep=True)
defcfg._describe('res', instanceof=(numbers.Integral, collections.Iterable),
                 docstring='resolution of the meshgrid')
defcfg.classname = 'explorers.MeshgridMotorExplorer'


class MeshgridMotorExplorer(m_rand.RandomMotorExplorer):
    """\
    Necessitate a sensory bounded environement.
    """
    defcfg = defcfg

    def __init__(self, cfg, **kwargs):
        super(MeshgridMotorExplorer, self).__init__(cfg)
        self._meshgrid = meshgrid.MeshGrid(self.cfg, [c.bounds for c in self.m_channels], cfg.res)

    def _explore(self):
        # pick a random bin
        if len(self._meshgrid._nonempty_bins) == 0:
            m_signal = tools.random_signal(self.m_channels)
        else:
            m_bin = random.choice(self._meshgrid._nonempty_bins)
            m_signal = tools.random_signal(self.m_channels, bounds=m_bin.bounds)

        return {'m_signal': m_signal, 'from': 'motor.babbling.mesh'}

    def receive(self, exploration, feedback):
        super(MeshgridMotorExplorer, self).receive(exploration, feedback)
        self._meshgrid.add(tools.to_vector(exploration['m_signal'], self.m_channels), feedback['s_signal'])
