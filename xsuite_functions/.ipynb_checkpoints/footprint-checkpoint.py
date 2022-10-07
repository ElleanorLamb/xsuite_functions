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

def plot_footprint(qx,qy,coords_per_arc,title=str,):
    plot_object = plt.figure('FOOTPRINT')
    plt.suptitle(title)
    
    n = coords_per_arc

    points=8

    plt.scatter(q_x[0:n],q_y[0:n], label = '0.3 $\sigma$ ', s=points)
    plt.scatter(q_x[n:2*n],q_y[n:2*n], label = '1.0 $\sigma$ ',s=points)
    plt.scatter(q_x[2*n:3*n],q_y[2*n:3*n], label = '2.0 $\sigma$ ',s=points)
    plt.scatter(q_x[3*n:4*n],q_y[3*n:4*n], label = '3.0 $\sigma$', s=points)
    plt.scatter(q_x[4*n:5*n],q_y[4*n:5*n], label = '4.0 $\sigma$ ', s=points)
    plt.scatter(q_x[5*n:6*n],q_y[5*n:6*n], label = '5.0 $\sigma$ ', s=points)
    plt.scatter(q_x[6*n:7*n],q_y[6*n:7*n], label = '6.0 $\sigma$ ', s=points)

    for i in range(n):
        q_x_s1c = [q_x[0+i],q_x[n+i],q_x[2*n+i],q_x[3*n+i],q_x[4*n+i],q_x[5*n+i],q_x[6*n+i]]
        q_y_s1c = [q_y[0+i],q_y[n+i],q_y[2*n+i],q_y[3*n+i],q_y[4*n+i],q_y[5*n+i],q_y[6*n+i]]
        plt.plot(q_x_s1c,q_y_s1c,'darkgrey')



    plt.plot(q_x[0:n-1],q_y[0:n-1],color='darkgrey',)
    plt.plot(q_x[n:2*n-1],q_y[n:2*n-1],color='darkgrey',)
    plt.plot(q_x[2*n:3*n-1],q_y[2*n:3*n-1], color='darkgrey',)
    plt.plot(q_x[3*n:4*n-1],q_y[3*n:4*n-1], color='darkgrey',)
    plt.plot(q_x[4*n:5*n-1],q_y[4*n:5*n-1], color='darkgrey',)
    plt.plot(q_x[5*n:6*n-1],q_y[5*n:6*n-1],color='darkgrey',)
    plt.plot(q_x[6*n:7*n],q_y[6*n:7*n], color='darkgrey',)

    plt.ylabel('$Q_y$')
    plt.xlabel('$Q_x$')

    plt.tight_layout()
    plt.axis('equal');
    plt.xticks(rotation=45)
    plt.grid()
    plt.legend()
    
    return

################################################################################

def get_max_tune(x_n,y_n,tracker):
    '''
    input your tracker after the last track 
    returns all the maximum amplitude tunes in x and y for each particle

    '''
    
    tune_search = 6 # find 6 maxima along the spectrum 
    q_x = []
    for k in range(len(x)):
        naff_tune = NAFFlib.get_tunes_all(tracker.record_last_track.x[k].copy(),h)
        amp = []
        for i in range(tune_search):

            amp.append(np.abs(naff_tune[1][i]))

        for i in range(tune_search):      
            if amp[i]==np.max(amp):
                q_x.append(np.abs(naff_tune[0][i]))
    q_y = []
    for k in range(len(y)):
        naff_tune = NAFFlib.get_tunes_all(tracker.record_last_track.y[k].copy(),h)
        amp = []
        for i in range(tune_search):
            amp.append(np.abs(np.abs(naff_tune[1][i])))

        for i in range(tune_search):        
            if amp[i]==np.max(amp):
                q_y.append(np.abs(naff_tune[0][i]))
                
    return q_x, q_y


###########################################################

    