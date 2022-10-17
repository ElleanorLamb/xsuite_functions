from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals



import numpy as np 
import math 
import matplotlib.pyplot as plt
from time import time

import xbeamfit as xb

from abel.direct import direct_transform
from abel.tools.analytical import GaussianAnalytical

from xbeamfit import fitting # need ElleanorLamb/xbeamfit 
from xbeamfit import distributions 
import xbeamfit as xb 

#################### create a gaussian and forward transform ##################

def forward_transform_Gaussian(start, end, steps,A ,mu, sigma):

    ''' 
    Creates a 1D Gaussian, transforms it via the forward Abel transform,
    mu = average
    sigma = sigma
    A = Gaussian amplitude parameter
    '''
    
    r = np.linspace(start,end,steps) # input range

    gauss = []
    for i in range(len(r)):
        gauss.append(xb.distributions.Gaussian(r[i] ,A,mu,sigma))
    forward_transform = direct_transform(qgauss, dr=np.diff(r)[0], direction="forward", correction=True)

    return r, forward_transform, gauss
    

################### create a q-Gaussian and abel forward transform ###################3

def forward_transform_qGaussian(start, end, steps, mu, q, b, A,correction=True):
    ''' 
    Creates a 1D q-Gaussian, transforms it via the forward Abel transform
    
    x=input of q gaussian
    mu=average
    q = gGaussian q-parameter
    b = qGaussian b parameter 
    A = qGaussian amplitude parameter
    '''
    
    r = np.linspace(start,end,steps) # input range

    qgauss = []
    for i in range(len(r)):
        qgauss.append(xb.distributions.qGauss(r[i],mu,q,b,A))
    forward_transform = direct_transform(qgauss, dr=np.diff(r)[0], direction="forward", correction=correction)
    
    return r, forward_transform, qgauss


################# inverse abel transfrom ################

def inverse_transform(r,forward_transform,correction=True):
    return direct_transform(forward_transform,  dr=np.diff(r)[0], direction="inverse", correction=correction)


 