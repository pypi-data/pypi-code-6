from parsimony.estimators import ElasticNet
from sklearn.base import BaseEstimator


def make_grid(x, y, step=""):
    alphas = [1e-4, 1e-3, 1e-2, 0.1, 1., 10., 100., 1e3]
    ls = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
    grid = []
    for a in alphas:
        for l in ls:
            grid.append({"%s__l" % step: l,
                         "%s__alpha" % step: a})
    return grid


class EnetWrap(BaseEstimator, ElasticNet):

    def __init__(self, l=0., alpha=1., algorithm_params={},
                 penalty_start=0, mean=True):
        super(EnetWrap, self).__init__(l=l, alpha=alpha,
                                       algorithm_params=algorithm_params,
                                       penalty_start=penalty_start, mean=mean)
