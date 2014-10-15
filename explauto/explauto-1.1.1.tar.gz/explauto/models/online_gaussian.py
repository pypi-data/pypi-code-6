from numpy import zeros, dot
from ..exceptions import ExplautoBootstrapError

class OnlineGaussian(object):
    def __init__(self, learning_rate=None):
        """

        :params float learning_rate: used as a temperature decay term as proposed in:

        Online Learning of Single- and Multivalued Functions with an Infinite Mixture of Linear Experts
        Bruno Damas and Jose Santos-Victor
        Neural Computation 2013 25:11, 3044-3091
        (section 3.1 E-Step)
        """
        self.count = 0
        self.learning_rate = learning_rate
        if learning_rate is None:
            self.sumweight = 0
        else:
            self.sumweight = 1

    def update(self, x, weight_=1.):
        if self.count == 0:
            self.mean = zeros(len(x))
            self.M2 = zeros((len(x), len(x)))
        if self.learning_rate is None:
            weight = weight_
        else:
            weight =  weight_ * self.sumweight * (self.count+1) ** ( - self.learning_rate)
        temp = weight + self.sumweight
        delta = x - self.mean
        R = delta * weight / temp
        self.mean = self.mean + R
        self.M2 = self.M2 + self.sumweight * dot(delta.reshape(-1, 1), R.reshape(1, -1))  #Alternatively, M2 = M2 + weight * delta * (x-mean)
        self.sumweight = temp
        self.count += 1

    @property
    def covariance(self):
        if self.count < 2:
            raise ExplautoBootstrapError("at least two update(.) calls are necessary before estimation can be computed")
        variance_n = self.M2/self.sumweight
        variance = variance_n * self.count/(self.count - 1)
        return variance
