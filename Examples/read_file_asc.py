# niky.bruchon@cern.ch
# 2022-11-02
# data on dfs
# fils on 
# https://dfs.cern.ch/dfs/Departments/AB/Groups/dropbox/Sterbini


def read_file(file_path, logger):
    """Loads data from file"""
    import numpy as np
    from pathlib import Path

    error_flag = False
    fid = open(file_path, 'r')
    if fid == -1:
        errstr = 'Cannot open the file: ' + file_path
        print(errstr)
        error_flag = True
    else:
        # Read header
        from_scope = {'delta_t_traces': '---', 'first_trigger': '---', 'tr_offset': []}
        for header_long, line in enumerate(fid):
            aux = line.split('* Date:  ')
            if len(aux) != 1:
                aux = aux[1]
                aux = aux.rstrip("\n")
                from_scope['date'] = aux

            aux = line.split('* Time:  ')
            if len(aux) != 1:
                aux = aux[1]
                aux = aux.rstrip("\n")
                from_scope['time'] = aux

            aux = line.split('* Time between traces:  ')
            if len(aux) != 1:
                aux = aux[1]
                aux = aux.rstrip("\n")
                if aux == '---':
                    continue
                from_scope['delta_t_traces'] = int(aux[0])

            aux = line.split('* First trigger:  ')
            if len(aux) != 1:
                aux = aux[1]
                aux = aux.rstrip("\n")
                if aux == '---':
                    continue
                from_scope['first_trigger'] = float(aux[0])

            aux = line.split('* Time interval per data point (sec):  ')
            if len(aux) != 1:
                aux = aux[1]
                from_scope['delta_t_pts'] = float(aux)

            aux = line.split('* Horizontal fastframe length:  ')
            if len(aux) != 1:
                aux = aux[1]
                from_scope['h_frame_length'] = int(aux)

            aux = line.split('* Number of frames:  ')
            if len(aux) != 1:
                aux = aux[1]
                n_frames = int(aux)
                from_scope['n_frames'] = n_frames

            aux = line.split('* Number of data points:  ')
            if len(aux) != 1:
                aux = aux[1]
                from_scope['n_data_pts'] = int(aux)

            aux = line.split('* Acquire mode:  ')
            if len(aux) != 1:
                aux = aux[1]
                aux = aux.rstrip("\n")
                from_scope['acq_mode'] = aux

            aux = line.split('* Filter:  ')
            if len(aux) != 1:
                aux = aux[1]
                aux = aux.rstrip("\n")
                from_scope['filter'] = aux

            aux = line.split('* Trigger holdoff time:  ')
            if len(aux) != 1:
                aux = aux[1]
                aux = aux.rstrip("\n")
                from_scope['tr_hold_off'] = aux

            aux = line.split('* Vertical scale (V/div):  ')
            if len(aux) != 1:
                aux = aux[1]
                from_scope['v_scale'] = float(aux)

            aux = line.split('* Vertical position (div):  ')
            if len(aux) != 1:
                aux = aux[1]
                from_scope['v_pos'] = float(aux)

            aux = line.split('* Input coupling:  ')
            if len(aux) != 1:
                aux = aux[1]
                aux = aux.rstrip("\n")
                from_scope['in_coupl'] = aux

            aux = line.split('* Input impedance:  ')
            if len(aux) != 1:
                aux = aux[1]
                aux = aux.rstrip("\n")
                from_scope['in_imp'] = aux

            aux = line.split('* Vertical bandwidth:  ')
            if len(aux) != 1:
                aux = aux[1]
                from_scope['v_bandwidth'] = float(aux)

            aux = line.split('* Scale Factor (dB):  ')
            if len(aux) != 1:
                aux = aux[1]
                from_scope['att_db'] = float(aux)

            aux = line.split('* Trigger offset (index sec):  ')
            if len(aux) != 1:
                aux = aux[1]
                aux = aux.split()
                from_scope['tr_offset'].append(float(aux[1]))
                header_end = header_long
                if len(from_scope['tr_offset']) == from_scope['n_frames']:
                    break
        fid.close()
        from_scope['tr_offset'] = np.array(from_scope['tr_offset'])

        # Read both numpy and ascii files
        if Path(file_path[:-3] + 'npy').exists():
            data = np.load(file_path[:-3] + 'npy')
        else:
            data = pd.read_csv(file_path, skiprows=header_end + 2, header=None)
            # This is for some old files where the zeros were not loaded properly
            data.replace({'0.000E+': '0'}, inplace=True)
            data = data.iloc[:, 0].astype(float)
            data = data.to_numpy()

        from_scope['acquired'] = np.reshape(data, (int(from_scope['h_frame_length']),
                                                    int(from_scope['n_frames'])), order='F')

        #if not error_flag:
        #    from_scope = Acquisition.add_timescale(from_scope, logger)

    return from_scope


from matplotlib import pyplot as plt
aux=read_file('MD_133.asc', 'MD_133.npy')

plt.plot(aux['acquired'][:,0])
plt.show()