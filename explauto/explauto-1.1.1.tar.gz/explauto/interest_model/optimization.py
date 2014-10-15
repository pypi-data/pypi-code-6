import cma
from numpy import zeros
from sklearn.preprocessing import StandardScaler


from .interest_model import InterestModel
from .competences import competence_dist
from ..utils import rand_bounds


class CmaOptimizer(InterestModel):
    def __init__(self, conf, expl_dims, measure=competence_dist):
        InterestModel.__init__(self, expl_dims)
        self.goal = None
        self.measure = measure
        self.conf = conf
        self.scaler = StandardScaler()
        self.scaler.fit(rand_bounds(conf.bounds[:, expl_dims], n=10000))
        self.opt = cma.CMAEvolutionStrategy(zeros(conf.m_ndims), 1., {'bounds': [-3, 3]})
        self.solutions = self.opt.ask()
        self.to_eval = len(self.solutions)
        self.costs = []

    def sample(self):
        if not self.to_eval:
            self.opt.tell(self.solutions, self.costs)
            self.costs = []
            self.solutions = self.opt.ask()
            self.to_eval = len(self.solutions)
        x = self.solutions[ - self.to_eval]
        self.to_eval -= 1
        return self.scaler.inverse_transform(x)


    def update(self, xy, ms):
        # print len(self.solutions), len(self.costs)
        if self.goal is None:
            raise AttributeError("You have to set a self.goal first")
        cost = - self.measure(self.goal, ms[self.conf.s_dims], dist_min=0.0)
        self.costs.append(cost)

interest_models = {'cma_optimization_beta': (CmaOptimizer,
                                         {'default': {}})}
