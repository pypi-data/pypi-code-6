"""Reuse generators, that yield order to reuse"""

from __future__ import print_function, division, absolute_import
import random
import numbers

from . import s_reusegen
from ..m_rand import RandomMotorExplorer


algorithms = {'random'        : s_reusegen.RandomReuse,
              'sensor_uniform': s_reusegen.SensorUniformReuse,
              'pickone'       : s_reusegen.PickOneReuse}

defcfg = RandomMotorExplorer.defcfg._deepcopy()
defcfg._describe('reuse.algorithm', instanceof=str, default='sensor_uniform',
                 docstring='name of the reuse algorithm to use')
defcfg._describe('reuse.discount', instanceof=numbers.Real, default=1.0,
                 docstring='how much the ratio decrease with each reuse')
defcfg.classname = 'explorers.ReuseExplorer'


for algorithm in algorithms.values():
    defcfg._update(algorithm.defcfg)


class ReuseExplorer(RandomMotorExplorer):
    """A reuse explorer"""

    defcfg = defcfg

    def __init__(self, cfg, datasets=(), **kwargs):
        super(ReuseExplorer, self).__init__(cfg)
        assert len(datasets) == 1 # for the moment...
        self.reuse_generator = algorithms[cfg.reuse.algorithm](cfg, datasets[0])

    def _explore(self):
        try:
            m_signal = next(self.reuse_generator)
            return {'m_signal': m_signal, 'from': 'reuse'}
        except StopIteration:
            return None

    @property
    def diversity(self):
        return len(self.reuse_generator._meshgrid.self._nonempty_bins)
