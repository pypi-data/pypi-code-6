from __future__ import print_function
import optunity
import optunity.parallel


def f(x, y):
    return x * y

s = optunity.solvers.GridSearch(x=[1,2,3], y=[1,2,3])
result = s.optimize(f)
result = s.optimize(f, pmap=optunity.parallel.pmap)


s = optunity.solvers.ParticleSwarm(5, 5, x=[1, 2], y=[0, 1])
result = s.optimize(f)

result2 = s.optimize(f, pmap=optunity.parallel.pmap)
