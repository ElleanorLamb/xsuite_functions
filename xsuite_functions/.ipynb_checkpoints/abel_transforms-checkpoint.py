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

from xbeamfit import fitting # need ElleanorLamb/xbeamfit not yet on GitLab - crashing 
from xbeamfit import distributions 
import xbeamfit as xb 

import pandas as pd
from scipy import interpolate
from numpy import trapz
import scipy.integrate as integrate

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



############# find the area under an abel transform of a distribution between a certain sigma ##################


def calculate_particle_percentage(x_y, HV_fit_array, lower_sigma, upper_sigma):
    
    '''
    Inputs: 
    HV_fit_array: Fit of the horizontal or vertical profile, eg a q-gaussian ABOVE 0 
    x_y: array of the values in x or y for the fit
    lower_sigma: lower sigma bound for finding the population of particles
    upper_simga: upper bound for finding the population of the particles 
    
    Outputs: 
    df: dataframe with the original distribution, the x_y and the abel transform
    percentage_desired_limits: percentage of the distribution within the upper and lower bounds 
    '''
    # Inverse Abel transform the distribution using pyabel
    
    abel_transform =direct_transform(HV_fit_array, dr=np.diff(x_y)[0], direction="inverse", correction=True)        
    
    # make a dataframe 
    
    dt = {'r_n': x_y, 'fitted_distribution':HV_fit_array, 'inv_abel':abel_transform}
    df = pd.DataFrame(data=dt)
    
    # interpolate distribution 
    interp = interpolate.interp1d(df['r_n'], df['inv_abel'])
    
    x_y_new = np.arange(lower_sigma, upper_sigma, np.diff(x_y)[0] )
    curve_to_integrate = interp(x_y_new)   
    
    # integrate between the upper and lower bound 
    
    area_sigma = trapz(curve_to_integrate, dx=np.diff(x_y_new)[0])
    total_area = trapz(HV_fit_array, dx=np.diff(x_y_new)[0]) # should be 0.5 if normalised 

    percentage_desired_limits = (area_sigma/total_area)*100
    print('percentage in desired limit ', percentage_desired_limits, '%')
    
    return df, percentage_desired_limits


    
    
    
 
