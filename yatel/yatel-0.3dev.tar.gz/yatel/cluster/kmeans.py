#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY in return.


# =============================================================================
# DOCS
# =============================================================================

"""The Yatel kmeans algorithm clusters a network's environments, using as
dimensions the haplotypes which exists in each environment or arbitrary values
computed over them.

For more information about kmeans:

- `Scipy Doc <http://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans.html>`_
- `KMeans in wikipedia <http://en.wikipedia.org/wiki/K-means_clustering>`_

"""

# =============================================================================
# IMPORTS
# =============================================================================

import numpy as np
from scipy.cluster import vq

from yatel import db


# =============================================================================
# KMEANS
# =============================================================================

def kmeans(nw, envs, k_or_guess,
           whiten=False, coordc=None, *args, **kwargs):
    """Performs k-means on a set of all environments defined by `fact_attrs`
    of a network.

    Parameters
    ----------
    nw : `yatel.db.YatelNetwork`
        Network source of environments to classify.
    envs : iterable of `yatel.dom.Environments` or dicts
        Represents all the environments to be clustered.
    k_or_guess : int or ndarray
        The number of centroids to generate. A code is assigned
        to each centroid, which is also the row index of the
        centroid in the code_book matrix generated.

        The initial k centroids are chosen by randomly
        selecting observations from the observation matrix.
        Alternatively, passing a k by N array specifies the
        initial k centroids.
    whiten : bool
        execute ``scipy.cluster.vq.whiten`` function over the
        observation array before executing subjacent *scipy kmeans*.
    coordc : None or callable
        If `coordc` is ``None`` generates use `hap_in_env_coords`
        function. Otherwise `coordc` must be a callable with
        2 arguments:

        - `nw` network source of environments to classify.
        - `env` the environment to calculate the coordinates

        and must return an array of coordinates for the given
        network environment.
    args : arguments for scipy kmeans
    kwargs : keywords arguments for scipy kmeans

    Returns
    -------
    coodebook : an array kxn of k centroids
        A k by N array of k centroids. The i’th
        centroid codebook[i] is represented with the
        code i.
        The centroids and codes generated represent
        the lowest distortion seen, not necessarily
        the globally minimal distortion.
    distortion : the value of the distortion
        The distortion between the observations
        passed and the centroids generated.


    Examples
    --------
    >>> from yatel import nw
    >>> from yatel.cluster import kmeans
    >>> nw = db.YatelNetwork('memory', mode=db.MODE_WRITE)
    >>> nw.add_elements([dom.Haplotype(1), dom.Haplotype(2), dom.Haplotype(3)])
    >>> nw.add_elements([dom.Fact(1, att0=True, att1=4),
    ...                  dom.Fact(2, att0=False),
    ...                  dom.Fact(2, att0=True, att2="foo")])
    >>> nw.add_elements([dom.Edge(12, 1, 2),
    ...                  dom.Edge(34, 2, 3),
    ...                  dom.Edge(1.25, 3, 1)])
    >>> nw.confirm_changes()
    >>> kmeans.kmeans(nw, nw.enviroments(["att0", "att2"]), 2)
    (array([[1, 0, 0],
           [0, 1, 0]]),
     0.0,
     (({u'att0': True, u'att2': None},),
      ({u'att0': False, u'att2': None}, {u'att0': True, u'att2': u'foo'})))

    >>> calc = lambda nw, env: [stats.average(nw, env), stats.std(nw, env)]
    >>> kmeans.kmeans(nw, ["att0", "att2"], 2, coordc=calc)
    (array([[ 23.   ,  11.   ],
           [  6.625,   5.375]]),
     0.0)

    """
    obs = nw2obs(nw, envs, coordc=coordc)
    codebook, distortion = vq.kmeans(obs=obs, k_or_guess=k_or_guess,
                                     *args, **kwargs)
    return codebook, distortion


# =============================================================================
# SUPPORT
# =============================================================================

def hap_in_env_coords(nw, env):
    """Generates the coordinates for the kmeans algorithm
    with the existences of haplotypes in the environment.

    Parameters
    ----------
    nw : yatel.db.YatelNetwork
    env : a collection of dict or yatel.dom.Enviroment

    Returns
    -------
    array : arrays of arrays
        The returned coordinates has M elements
        (M is the number of haplotypes in the network)
        with same order of ``yatel.db.YatelNetwork.haplotypes_ids`` function
        with 2 posible values:

        - **0** if the haplotype doesn´t exist in the environment.
        - **0** if the haplotype exist in the environment.

    """
    haps_id = [hap.hap_id for hap in nw.haplotypes()]
    ehid = [hap.hap_id for hap in nw.haplotypes_by_environment(env=env)]
    haps_id.sort()
    ehid.sort()
    return [int(hid in ehid) for hid in haps_id]


def nw2obs(nw, envs, whiten=False, coordc=None):
    """Converts any given environments defined by `fact_attrs`
    of a network to an observation matrix to cluster with subjacent *scipy kmeans*

    Parameters
    ----------

    nw : yatel.db.YatelNetwork
        Network source of environments to classify.
    envs : iterable of yatel.dom.Enviroment or dicts
        Represent all the environment to be clustered.
    whiten : bool
        execute `scipy.cluster.vq.whiten` function over the
        observation array before executing subjacent *scipy kmeans*.
    coordc : None or callable
        If coordc is ``None`` generates use `hap_in_env_coords`
        function. Otherwise `coordc` must be a callable with
        2 arguments:

        - `nw` network source of environments to classify.
        - `env` the environment to calculate the coordinates

        and must return an array of coordinates for the given
        network environment.

    Returns
    -------
    obs : a vector of envs
        Each I'th row of the M by N array is an observation
        vector of the I'th environment of `envs`.

    Examples
    --------
    >>> from yatel import nw
    >>> from yatel.cluster import kmeans
    >>> nw = db.YatelNetwork('memory', mode=db.MODE_WRITE)
    >>> nw.add_elements([dom.Haplotype(1), dom.Haplotype(2), dom.Haplotype(3)])
    >>> nw.add_elements([dom.Fact(1, att0=True, att1=4),
    ...                  dom.Fact(2, att0=False),
    ...                  dom.Fact(2, att0=True, att2="foo")])
    >>> nw.add_elements([dom.Edge(12, 1, 2),
    ...                  dom.Edge(34, 2, 3),
    ...                  dom.Edge(1.25, 3, 1)])
    >>> nw.confirm_changes()
    >>> kmeans.nw2obs(nw, nw.enviroments(["att0", "att2"]))
    array([[1, 0, 0],
           [0, 1, 0],
           [0, 1, 0]])


    """
    if not isinstance(nw, db.YatelNetwork):
        msg = "nw must be 'yatel.db.YatelNetwork' instance"
        raise TypeError(msg)
    coordc = hap_in_env_coords if coordc is None else coordc
    mtx = []
    for env in envs:
        row = coordc(nw, env)
        mtx.append(row)
    obs = np.array(mtx)
    if whiten:
        obs = vq.whiten(obs)
    return obs


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print(__doc__)
