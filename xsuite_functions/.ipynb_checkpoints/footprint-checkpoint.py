from matplotlib import pyplot as plt 
import scipy as sp
import sys
import math
import json
import numpy as np
import NAFFlib
import xtrack as xt
import xpart as xp
import xobjects as xo
import pandas as pd

####################################################################

def generate_coordGrid(xRange,yRange,labels = ['x','y'],nPoints=100):
    '''
    
    Temporary function from BBfootprint change to BBfootprint installation after Philippe has implemented it 
    
    Distribute points uniformly on a 2D grid.
    -----------------------------------------
    Input:
        xRange : range of first coordinate
        yRange : range of second coordinate
        labels : labels to be used in the resulting dataframe
        nPoint : total number of points to generate (sqrt(nPoints) for each coordinate)
    Returns:
        coordinates: dataframe containing the distributed points
    '''

    if type(xRange) is list and type(yRange) is list:
        xVec = np.linspace(xRange[0],xRange[1],int(np.sqrt(nPoints)))
        yVec = np.linspace(yRange[0],yRange[1],int(np.sqrt(nPoints)))
    else:
        xVec = xRange
        yVec = yRange
        
    xx,yy = np.meshgrid(xVec,yVec)
    xx,yy = xx.flatten(),yy.flatten()

    return pd.DataFrame(dict(zip(labels,[xx,yy])))


####################################################################



def get_max_tune(x_n,y_n,tracker,tune_search=4):
    '''
    inputs 
    
    x_n, y_n the normalised coords numpy array of your particle distribution into the track
    your tracker after the last track 
    
    returns 
    q_x,q_y arrays ; all the maximum amplitude tunes in x and y for each particle

    '''
    
    q_x = []
    for k in range(len(x_n)):
        naff_tune = NAFFlib.get_tunes_all(tracker.record_last_track.x[k].copy(),h)
        amp = []
        for i in range(tune_search):

            amp.append(np.abs(naff_tune[1][i]))

        for i in range(tune_search):      
            if amp[i]==np.max(amp):
                q_x.append(np.abs(naff_tune[0][i]))
    q_y = []
    for k in range(len(y_n)):
        naff_tune = NAFFlib.get_tunes_all(tracker.record_last_track.y[k].copy(),h)
        amp = []
        for i in range(tune_search):
            amp.append(np.abs(np.abs(naff_tune[1][i])))

        for i in range(tune_search):        
            if amp[i]==np.max(amp):
                q_y.append(np.abs(naff_tune[0][i]))
                
    return q_x, q_y


###########################################################

    