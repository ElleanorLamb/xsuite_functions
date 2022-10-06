import xobjects as xo
import xtrack as xt
import xpart as xp
import xdeps as xd
from xdeps.madxutils import MadxEval



import pyarrow 
import pandas as pd
from matplotlib import pyplot as plt 
import numpy as np


import json
import scipy as sp
import math

import conda

from scipy.constants import c as speed_c
from scipy.constants import e as qe
from scipy.constants import m_p



def load_tracker(gamma, file_with_json=str, Cpu=True):
    """
    args ; gamma, file sting, Cpu true or false
    outputs ; tracker, context, part_ref
    
    """

    with open(file_with_json,'r') as fid:
        loaded_dct = json.load(fid)
        
    line = xt.Line.from_dict(loaded_dct)

    line.particle_ref = xp.Particles(mass0=xp.PROTON_MASS_EV, q0=1,
                        gamma0=gamma)
    
    part_ref = line.particle_ref 

    if Cpu == True:
        context = xo.context.Cpu
    else:
        context = xo.context.Cupy
        
    
    tracker = xt.Tracker(line=line, _context=context,)
    
    return tracker, context, part_ref