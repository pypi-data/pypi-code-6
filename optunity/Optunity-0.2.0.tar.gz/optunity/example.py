#!/usr/bin/env python

import optunity


def f(x, y):
    return -x ** 2 - y ** 2

pso_solver = optunity.make_solver('particle swarm', num_particles=10,
                              max_speed=1,  num_generations=10,
                              x=[-1, 1], y=[1, 3])

result, details = optunity.maximize(pso_solver, f)

cma_solver = optunity.make_solver('cma-es', num_generations=20,
                                  centroid={'x': 0, 'y': 0},
                                  sigma=1)

result, details = optunity.maximize(cma_solver, f)
