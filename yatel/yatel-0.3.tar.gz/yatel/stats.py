#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Statistic functions to calculate weight statistics over Yatel enviroments.

"""

#===============================================================================
# IMPORT
#===============================================================================

import collections

import numpy as np

from scipy import stats

from yatel import db


#===============================================================================
# BASIC POSITION STATS
#===============================================================================

def average(nw, env=None, **kwargs):
    """Compute the weighted average on a network.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.average(arr)


def median(nw, env=None, **kwargs):
    """Compute the median on a network.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.median(arr)


def percentile(nw, q, env=None, **kwargs):
    """Compute the q-th percentile of the network.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.percentile(arr, q)


def min(nw, env=None, **kwargs):
    """Return the minimum in a network.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.min(arr)


def max(nw, env=None, **kwargs):
    """Return the maximum in a network.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.max(arr)


def amin(nw, env=None, **kwargs):
    """Return the minimum in a network.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.amin(arr)


def amax(nw, env=None, **kwargs):
    """Return the maximum in a network.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.amax(arr)


def sum(nw, env=None, **kwargs):
    """Sum of the elements on the network.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.sum(arr)


def mode(nw, env=None, **kwargs):
    """Calculates mode on a network.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    cnt = collections.Counter(arr)
    value = np.max(cnt.values())
    n = cnt.values().count(value)
    return np.array(tuple(v[0] for v in cnt.most_common(n)))


#===============================================================================
# DISPERTION STATS
#===============================================================================

def var(nw, env=None, **kwargs):
    """Compute the variance of the network.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.var(arr)


def std(nw, env=None, **kwargs):
    """Compute the standard deviation of the network.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.std(arr)


def variation(nw, env=None, **kwargs):
    """Computes the coefficient of variation.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    return stats.variation(arr)

def range(nw, env=None, **kwargs):
    """Computes the distance between the maximum and minimum.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    return np.amax(arr) - np.amin(arr)


#===============================================================================
# KURTOSIS
#===============================================================================

def kurtosis(nw, env=None, **kwargs):
    """Computes the kurtosis (Fisher’s definition) of a network.

    Parameters
    ----------
    nw : :py:class:`yatel.db.YatelNetwork`
        Network to which apply the operation.
    env : :py:class:`yatel.dom.Enviroment` or dict like
        Environment for filtering.

    """
    arr = env2weightarray(nw, env=env, **kwargs)
    return stats.kurtosis(arr)


#===============================================================================
# SUPPORT
#===============================================================================

def weights2array(edges):
    """Create a **numpy.ndarray** with all the weights of 
    :py:class:`yatel.dom.Edge`
    
    """
    generator = (e.weight for e in edges)
    return np.fromiter(generator, float)


def env2weightarray(nw, env=None, **kwargs):
    """This function always return a **numpy.ndarray** with this conditions:

    - If ``nw`` is instance of **numpy.ndarray** the same array is returned.
    - If ``nw`` is instance of :py:class:`yatel.db.YatelNetwork` and an 
      environment is given return all the edges in this environment.
    - If ``nw`` is instance of :py:class:`yatel.db.YatelNetwork` and no 
      environment is given  then return all edges.
    - In the last case the function tries to convert ``nw`` to 
      **numpy.ndarray** instance.

    """
    env = dict(env) if env else {}
    env.update(kwargs)
    if isinstance(nw, np.ndarray):
        if env:
            msg = "if nw is numpy.ndarray you can't use environments"
            raise ValueError(msg)
        return nw
    elif isinstance(nw, db.YatelNetwork):
        if not env:
            return weights2array(nw.edges())
        return  weights2array(nw.edges_by_environment(env=env))
    else:
        return np.array(nw)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
