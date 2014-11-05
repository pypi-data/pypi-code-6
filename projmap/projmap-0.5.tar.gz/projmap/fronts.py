"""
W. D. Nowlin, Jr., 1995: On the meridional extent and fronts of the Antarctic 
Circumpolar Current, Deep-Sea Res. I, 42, 641-673.

stf   subtropical front
saf   subantarctic front
pf    polar front
saccf southern antarctic circumpolar current front'
sbdy  southern boundary
"""
import os

import numpy as np
import pylab as pl
from scipy.spatial import cKDTree

def load(name):
        """Plot fronts in the Southern Ocean """
        if not name in ['saf', 'stf', 'saccf', 'pf', 'sbdy']:
            raise ValueError, "Unknown front name."

        basedir = os.path.dirname(os.path.abspath(__file__))
        frontdir = os.path.join(basedir, "data")

        data = np.genfromtxt(os.path.join(frontdir, name + '.txt'))
        return data[:,0],data[:,1]


def allfronts():

    loni = np.arange(-180,180,0.1)
    latmat = np.zeros((len(loni),7))
    latmat[:,0] = -70
    latmat[:,6] = -30
    for n,fr in enumerate([ 'sbdy', 'saccf', 'pf', 'saf', 'stf']):
        lon,lat = load(fr)
        latmat[:,n+1] = np.interp(loni, lon, lat)
    return loni, latmat


def index(lon,lat):

    loni, latmat = allfronts()
    ivec = np.searchsorted(loni,lon)

    index = []
    for i in np.arange(len(lon)):
        ipos = np.searchsorted(latmat[ivec[i],:],lat[i], side="left") - 1
        index.append((lat[i]                  - latmat[ivec[i], ipos]) /
                     (latmat[ivec[i], ipos+1] - latmat[ivec[i], ipos]) + ipos)
    return np.array(index)
    
    #lonmat = loni[:,np.newaxis] + latmat*0
    #imat = np.arange(7)[np.newaxis,:] + latmat*0
    #kd = cKDTree(np.vstack((lonmat.flat, latmat.flat)).T)    
    


    #sbdy:  -64.0
    #saccf: -62.4
    #pf:    -56.4
    #saf:   -51.9
    #stf:   -47.1


def indplot(lon, lat, val, text):

    ind = index(lon, lat)
    pl.clf()
    pl.subplot(1,2,1)
    pl.scatter(val,lat)
    pl.ylabel("Latitude")
    pl.xlabel(text)

    pl.subplot(1,2,2)
    pl.scatter(val, ind)
    pl.yticks([1,2,3,4,5],['sbdy', 'saccf', 'pf', 'saf', 'stf'])
    pl.xlabel(text)
    

    
