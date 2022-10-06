





def load_tracker(gamma, file_with_json=str, Cpu=True):

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