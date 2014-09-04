import numpy as np 
from censored_regression import CensoredLasso
def test_simple_regression():
    X = np.loadtxt("X.txt")
    Y = np.loadtxt("Y.txt")
    C = np.loadtxt("C.txt").astype('bool')
    w = np.loadtxt("w.txt")

    model = CensoredLasso(fit_intercept = False)
    model.fit(X,Y,C)
    assert np.mean(np.abs(model.predict(X)[~C] - Y[~C])) < 0.1
    assert np.mean(np.abs(model.coef_ - w)) < 0.1, \
        "Expected %s but got %s" % (w, model.coef_)
