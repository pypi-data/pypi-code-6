from ... import meshgrid
from ... import tools


class IMBin(meshgrid.MeshBin):

    def __init__(self, cfg, coo, bounds):
        super(IMBin, self).__init__(cfg, coo, bounds)
        self.lim = tools._load_class(self.cfg.lim.classname)(self.cfg.lim)

    @property
    def weight(self):
        return self.lim.weight

    def add(self, e, metadata, counter):
        super(IMBin, self).add(e, metadata, counter)
        order, effect, prediction, goal = metadata
        self.add_im(effect, prediction=prediction, goal=goal)

    def add_im(self, effect, prediction=None, goal=None):
        if tools.belongs(effect, self.bounds):
            self.lim.add_effect(effect, prediction=prediction)
        if tools.belongs(effect, self.bounds):
            self.lim.add_goal(effect, goal)


class IMGrid(meshgrid.MeshGrid):

    BinClass = IMBin

    def add(self, p, metadata=None):
        super(IMGrid, self).add(p, metadata=metadata)

        # adding to goal bin if necessary
        if metadata is not None:
            order, effect, prediction, goal = metadata
            if goal is not None:
                assert p == effect
                effect_coo = self._coo(effect)
                goal_coo = self._coo(goal)
                if effect_coo != goal_coo:
                    self._add_to_coo(goal_coo, p, metadata)

    def draw_bin(self):
        """weigthed draw between non-empty bins"""
        weights = [b.weight for b in self._nonempty_bins]
        if len(weights) == 0:
            raise ValueError("can't draw from an empty meshgrid")
        idx = tools.roulette_wheel(weights)
        return self._nonempty_bins[idx]

