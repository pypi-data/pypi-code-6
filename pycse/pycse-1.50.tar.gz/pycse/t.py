from scipy.integrate import odeint

k = -1

def f(y, x):
    return -k * y

print(odeint(f, 1, [0, 1]))
