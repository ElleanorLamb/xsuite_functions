import numpy as np 
import scipy as sp 

#################### centre the distribution ################# 

def centre_beam(x, px): # find the average of the beam and move it to 0,0
    x_centre = []
    px_centre = []
    
    
    x_avg = np.average(x)
    x_centre = x - x_avg

    px_avg = np.average(px)
    px_centre = px - px_avg

    return x_centre,px_centre 


################## calculate the emittance of a normalised distribution ###################

def calculate_emittance(x,px): # assumes normalised coordinates 
    
    emittance=[]
      
    x_sq = np.multiply(x,x)
    xpx = x*px
    x_sq = np.multiply(x,x)
    px_sq = np.multiply(px,px)
    xsq_avg = np.mean(x_sq)
    pxsq_avg = np.mean(px_sq)
    mult_avg = np.mean(xpx)
    

    emittance = (np.sqrt((xsq_avg*pxsq_avg)-(mult_avg**2)))
    return emittance


################## calculate the normalised emittance of a normalised distribution ####################

def normalise_emittance(x,px,gamma): # assumes normalised coordinates 
    
    ''' 
    x ; 1D numpy array
    px ; 1D numpy array
    gamma ; nominal machine energy/rest mass energy of the charged particle
    '''
    
    emit = calculate_emittance(x,px)
    normalised_emit = emit * gamma * np.sqrt((gamma**2-1)/gamma**2)
    return normalised_emit 



################### the single value decomposition to find alpha, beta, ex ###################
def SVD_AlphaBeta(x,px):
    '''Taken from https://arxiv.org/pdf/2006.10661.pdf, P. Belanger implementation  '''
    
    U,s,V= np.linalg.svd([x,px])         #SVD
    
    N = np.dot(U,np.diag(s))
    theta = np.arctan(-N[0,1]/N[0,0])    #AngleofR(theta)
    co=np.cos(theta) ; si=np.sin(theta)
    
    R = [[co,si],[-si,co]]   
    X = np.dot(N,R)                      #Floquetupto1/det(USR)
    
    beta = np.abs(X[0,0]/X[1,1])
    alpha = X[1,0]/X[1,1]
    
    # dropped
    ex =s[0]*s[1]/(len(x)/2.)            #emit=det(S)/(n/2)
    
    return alpha,beta

###################  Transfer coordinates of distribution in phase space #########################
def phys2norm(x,px,alpha=None,beta=None,SVD=False):
    ''' Taken from P. Belanger'''
    
    if SVD:
        alpha,beta = SVD_AlphaBeta(x,px)
        
    #N0 = [[1/np.sqrt(beta),0],[alpha/np.sqrt(beta), np.sqrt(beta)]]
    x_n  = x/np.sqrt(beta)
    px_n = alpha*x/np.sqrt(beta) + px*np.sqrt(beta)
    
    return x_n,px_n

def norm2phys(x_n,px_n,alpha=None,beta=None):
    
    ''' Taken from P. Belanger'''

    x    = x_n*np.sqrt(beta)
    px   = -alpha*x_n/np.sqrt(beta) + px_n/np.sqrt(beta)
    
    return x, px
##############################################################
