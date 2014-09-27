import pyfde
from pyfde.bench import schewefel
from timeit import default_timer as timer

def benchit():
    solver = pyfde.Solver(schewefel, n_dim=10, n_pop=50, limits=(-500.,500.))
    solver.cr, solver.f = 0.5, 0.8
    best, fit = solver.run(n_it=1000)

if __name__ == "__main__":
    N_TIMES = 10

    init = timer()
    for _ in range(N_TIMES):
        benchit()
        end = timer()

    seconds = (end - init) / N_TIMES
    print("Time per run: {:.3f} seconds".format(seconds))
