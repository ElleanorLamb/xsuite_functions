
import numpy as np 
import math 
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import matplotlib.pyplot as plt
from time import time
import sys
from abel.direct import direct_transform
from abel.tools.analytical import GaussianAnalytical

from xbeamfit import fitting
from xbeamfit import distributions 

import json

import numpy as np
import scipy as sp
import pandas as pd
import sys


import xbeamfit as xb 

from scipy import interpolate
from numpy import trapz
import scipy.integrate as integrate


from xsuite_functions import abel_transforms as ab 

'''
Example to show a distributiun from a fitted experiment transformed with the Abel transform. Then 
the percentage of particles within a sigma range is found.
'''

# make a q-Gaussian distribution 


r = np.linspace(0,20,1000) 

q_gauss = xb.distributions.qGauss(r, mu=0, A=1, b=0.5, q=1.1) # this is the observed profile 
#gauss_test = xb.distributions.Gaussian(r,A=1,mu=0,sig=1)


# Abel transform 

df, perc = ab.calculate_particle_percentage(r,q_gauss,lower_sigma=2,upper_sigma=3)

print(perc)



