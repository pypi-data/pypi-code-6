# -*- coding: utf-8 -*-
"""Kiwi: a tool to combine gene-set analyses with biological networks.
:author: Francesco Gatto and Leif Väremo, 2014
:email: gatto@chalmers.se varemo@chalmers.se
:affiliation: Department of Biological Engineering, Chalmers, Göteborg, Sweden"""


import argparse 
import itertools
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import os
import warnings