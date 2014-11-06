# FIXME: Python 2 only!
# -*- coding: utf-8 -*-

import importlib    # for dynamic kernels
from os import path
from glob import glob

def makedefines(opts):
    return " ".join("-D %s=%s" % (k.upper(), v) for k, v in opts.items())

def loadkernel(name, **params):
    """Load kernel with parameters"""
    curdir = path.dirname(__file__)
    clkernel = glob(path.join(curdir, name + ".cl"))
    pykernel = glob(path.join(curdir, name + ".py"))
    if clkernel:
        with open(clkernel[0]) as f:
            kernelstr = f.read()
    elif pykernel:
        kmodule = importlib.import_module(__name__ + "." + name)
        kernelstr = kmodule.kernel(**params)
    else:
        raise Exception("Kernel '%s' not found" % name)
    return kernelstr, makedefines(params)
