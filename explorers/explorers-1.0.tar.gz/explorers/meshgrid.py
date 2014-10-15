from __future__ import print_function, division

import numbers
import random
import copy

from . import tools


class MeshBin(object):

    def __init__(self, cfg, coo, bounds):
        self.cfg      = cfg
        self.coo      = coo
        self.bounds   = bounds
        self.elements = []

    def add(self, e, metadata, counter):
        self.elements.append((counter, e, metadata))

    def __len__(self):
        return len(self.elements)

    def __iter__(self):
        for e in self.elements:
            yield e

    def draw(self, replace=True):
        idx = random.randint(0, len(self.elements) - 1)
        if replace:
            choice = self.elements[idx]
        else:
            choice = self.elements.pop(idx)
        return choice


class MeshGrid(object):
    """\
    Groups elements in bins and draw elements by choosing a bin at random.
    """

    BinClass = MeshBin

    def __init__(self, cfg, bounds):
        self.cfg = cfg
        assert all(isinstance(b_min, numbers.Real) and
                   isinstance(b_max, numbers.Real) for b_min, b_max in bounds)
        self.bounds = bounds
        self.res = self.cfg['res']
        if isinstance(self.res, numbers.Integral):
            self.res = len(bounds)*[self.res]
        assert (len(self.res) == len(bounds) and
                all(isinstance(e, numbers.Integral) for e in self.res))

        self.dim = len(bounds)
        self._bins = {None: self.BinClass(self.cfg, None, None)} # a bin for everything not inside the bounds
        self._size = 0
        self._nonempty_bins = []
        self._counter = 0 # uuid for points, != size

    def _coo(self, p):
        assert len(p) == self.dim
        coo = []
        for pi, (si_min, si_max), res_i in zip(p, self.bounds, self.res):
            if si_min == si_max:
                coo.append(0)
            else:
                coo.append(int((pi - si_min)/(si_max - si_min)*res_i))
                if pi == si_max:
                    coo[-1] == res_i - 1
            if si_min > pi or si_max < pi:
                return None
        return tuple(coo)

    def _bounds(self, coo):
        if coo is None:
            return None
        else:
            bounds = []
            for c_i, (si_min, si_max), res_i in zip(coo, self.bounds, self.res):
                divsize = (si_max - si_min)/res_i
                bounds.append((si_min + c_i*divsize, si_min + (c_i+1)*divsize))
            return bounds

    def __len__(self):
        return self._size

    def resize(self, bounds, res=None):
        elements = [e for bin_ in self._bins.values() for e in bin_]
        res = self.res if res is None else res
        cfg = copy.deepcopy(self.cfg)
        cfg['res'] = res

        self.__init__(cfg, bounds)
        for c, p, md in elements:
            self.add(p, metadata=md)

    def empty_bin(self, p):
        coo = self._coo(p)
        return not coo in self._bins

    def _add_to_coo(self, coo, p, metadata):
        if not coo in self._bins:
            self._bins[coo] = self.BinClass(self.cfg, coo, self._bounds(coo))
        bin_ = self._bins[coo]
        if len(bin_) == 0:
            self._nonempty_bins.append(bin_)
        bin_.add(p, metadata, self._counter)
        self._counter += 1

    def add(self, p, metadata=None):
        assert len(p) == self.dim
        coo = self._coo(p)
        self._add_to_coo(coo, p, metadata)
        self._size += 1
        return coo

    def draw(self, replace=True, metadata=False):
        """Draw uniformly between existing (non-empty) bins"""
        try:
            idx = random.randint(0, len(self._nonempty_bins) - 1)
        except ValueError:
            raise ValueError("can't draw from an empty meshgrid")
        c, e, md = self._nonempty_bins[idx].draw(replace=replace)
        if not replace:
            self._size -= 1
        if len(self._nonempty_bins[idx]) == 0:
            self._nonempty_bins.pop(idx)
        if metadata:
            return e, md
        else:
            return e

    def draw_bin(self):
        if len(self._nonempty_bins) == 0:
            raise ValueError("can't draw from an empty meshgrid")
        return random.choice(self._nonempty_bins)


class ExplorerMeshGrid(object):
    """A meshgrid that accepts and returns s_signals instead of s_vectors"""

    def __init__(self, cfg, s_channels, m_channels):
        self.m_channels = m_channels
        self.s_channels = s_channels

        s_bounds = [c.bounds for c in self.s_channels]
        self._meshgrid = MeshGrid(cfg, s_bounds)
        self._m_map = {}

    def add(self, s_signal, m_signal=None):
        s_vector = tools.to_vector(s_signal, self.s_channels)

        coo = self._meshgrid._coo(s_vector)
        self._meshgrid._add_to_coo(coo, s_signal, metadata=m_signal)
        self._meshgrid._size += 1

        if m_signal is not None:
            m_vector = tools.to_vector(m_signal, self.m_channels)
            self._m_map[m_vector] = self._meshgrid._bins[coo]

        return coo

    @property
    def bins(self):
        return self._meshgrid._bins

    @property
    def nonempty_bins(self):
        return self._meshgrid._nonempty_bins

    def draw(self, replace=True):
        s_signal, m_signal = self._meshgrid.draw(replace=replace, metadata=True)
        return s_signal, m_signal

    def draw_bin(self):
        return self._meshgrid.draw_bin()

    def s_signal2bin(self, s_signal):
        """\
        Return the bin which would contains point, if the bin is not empty.
        Return None otherwise.
        """
        s_vector = tools.to_vector(s_signal, self.s_channels)
        coo = self._meshgrid._coo(s_vector)
        try:
            return self._meshgrid._bins[coo]
        except KeyError:
            return None

    def __len__(self):
        return len(self._meshgrid)
