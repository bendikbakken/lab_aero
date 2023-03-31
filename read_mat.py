from collections import OrderedDict

import h5py
import numpy as np

def read(fname, ofname=None):
    """
    Read in the .mat file (version 7.3 only) created 
    by the Matlab script used during the laboratory 
    exercise in TEP4160.

    The program change all indices from Matlab (index
    starting at 1) to Python (idex starting at 0) and
    deals with the row-major versus column-major arrays
    of Matlab and Python.

    The program can save the parsed data in separate 
    hdf5 file if desired.

    Input:
        fname  : (str) Path to the .mat file
        ofname : (str or None) Path to the output filename
                 if a hdf5 file with the parse content of 
                 the file is wanted. If ofname is None, 
                 there is no save. NOTE: This will 
                 overwrite existing content in the file!
                 Default: None
    Output:
        data   : (dict) Dictionary containing all the 
                 data fields in the .mat file
    """
    
    data = OrderedDict()
    with h5py.File(fname, 'r') as h5f:
        for key, group in h5f.items():
            if not isinstance(group, h5py.Group):
                tmp_data = group[...]
                if isinstance(tmp_data, (list, np.ndarray)):
                    # tmp_data = tmp_data.T
                    if len(tmp_data.shape) == 2 and tmp_data.shape[0] == 1:
                        tmp_data.shape = (tmp_data.shape[1],)
                    if len(tmp_data.shape) == 1 and tmp_data.shape[0] == 1:
                        tmp_data = tmp_data[0]
                if 'ind' in key:
                    # print('Assuming \'{:s}\' represents Matlab indices'.format(key))
                    ## Matlab is 1-indexed, Python is 0-indexed
                    tmp_data = (tmp_data - 1).astype(int)
                data[key] = tmp_data

    # Parse strings to str
    str_keys = ['Prefix', 'Re', 'savefilename']
    for key in str_keys:
        char_arr = [chr(letter) for letter in data[key].flatten()]
        data[key] = ''.join(char_arr)
  
    if ofname is not None:
        with h5py.File(ofname, 'w') as h5f:
            for key, value in data.items():
                h5f[key] = value

    return data