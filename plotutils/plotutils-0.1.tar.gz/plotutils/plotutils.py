"""
A module with various plotting utilities

"""

import numpy as np
import matplotlib.pyplot as plt
import os,os.path,shutil

def setfig(fig=None,**kwargs):
    """
    Sets figure to 'fig' and clears; if fig is 0, does nothing (e.g. for overplotting)

    if fig is None (or anything else), creates new figure
    
    I use this for basically every function I write to make a plot.  I give the function
    a "fig=None" kw argument, so that it will by default create a new figure.
    """
    if fig:
        plt.figure(fig,**kwargs)
        plt.clf()
    elif fig==0:
        pass
    else:
        plt.figure(**kwargs)

