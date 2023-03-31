from collections import OrderedDict
import io

import numpy as np

def read(fname):
    """
    Reads the binary file given by fname produced by the 
    MPS4264 pressure scanner. Returns the time of 
    measurement and the pressure signals. The time is
    given in seconds from a given date, and should only
    be used to get the time delta between two measurements.

    Input:
        fname : (str) Path to the file created by the 
                pressure scanner.

    Output:
        time     : (ndarray, 1D) Timestamp for all 
                   measured values.
        pressure : (ndarray, 2D) Pressure value for 
                   all ports at all points in time.
                   First index is the pressure port,
                   second index is point in time.
    """

    with io.open(fname, 'rb') as fp:
        bin_data = fp.read()
    
    num_points = int(len(bin_data) / (4 * 87))
    pressure = np.zeros((num_points, 64), dtype=np.float32)
    time = np.zeros(num_points, dtype=np.float64)
    t0_buff = np.frombuffer(bin_data, offset= 8 * 4, count=2, dtype='int32')
    t0 = t0_buff[0] + t0_buff[1] * 1e-9
    for ind in range(num_points):
        start = (19 + 87 * ind) * 4
        pressure[ind, :] = np.frombuffer(bin_data, offset=start, count=64, dtype='float32')
        time_buff = np.frombuffer(bin_data, offset=start+256, count=2, dtype='int32')
        time[ind] = t0 + time_buff[0] + time_buff[1] * 1e-9

    return time, pressure.T


def read_full(fname):
    """
    Reads the binary file given by fname produced by the 
    MPS4264 pressure scanner. Returns a dictionary with 
    all the information stored by the pressure scanner.

    NOTE: This function reads all the data in the same 
          format as created. Recommended to use the 
          read(fname) function if only pressure and 
          time is of interest.

    Input:
        fname: (str) Path to the file created by the 
               pressure scanner.

    Output:
        data: (dict) Dictionary of all the data stored
              in the file in native precision. 
    """
    with io.open(fname, 'rb') as fp:
        bin_data = fp.read()
    
    num_points = int(len(bin_data) / (4 * 87))
    # Create storage
    data = OrderedDict()
    data['packet_type'] = np.zeros(num_points, dtype=np.int32)
    data['packet_size'] = np.zeros(num_points, dtype=np.int32)
    data['frame_number'] = np.zeros(num_points, dtype=np.int32)
    data['scan_type'] = np.zeros(num_points, dtype=np.int32)
    data['frame_rate'] = np.zeros(num_points, dtype=np.float32)
    data['valve_status'] = np.zeros(num_points, dtype=np.int32)
    data['units_index'] = np.zeros(num_points, dtype=np.int32)
    data['unit_conversion_factor'] = np.zeros(num_points, dtype=np.float32)
    data['PTP_scan_start_time_sec'] = np.zeros(num_points, dtype=np.int32)
    data['PTP_scan_start_time_ns'] = np.zeros(num_points, dtype=np.int32)
    data['external_trigger_time'] = np.zeros(num_points, dtype=np.uint32)
    data['temperatures'] = np.zeros((num_points, 8), dtype=np.float32)
    data['pressures'] = np.zeros((num_points, 64), dtype=np.float32)
    data['frame_time_sec'] = np.zeros(num_points, dtype=np.int32)
    data['frame_time_ns'] = np.zeros(num_points, dtype=np.int32)
    data['external_trigger_time_sec'] = np.zeros(num_points, dtype=np.int32)
    data['external_trigger_time_ns'] = np.zeros(num_points, dtype=np.int32)

    # Parse the binary data
    pos = 0
    for ind in range(num_points):
        buff = np.frombuffer(bin_data, offset=pos, count=4, dtype='int32')
        pos += 16
        data['packet_type'][ind] = buff[0]
        data['packet_size'][ind] = buff[1]
        data['frame_number'][ind] = buff[2]
        data['scan_type'][ind] = buff[3]
        
        data['frame_rate'][ind] = np.frombuffer(bin_data, offset=pos, 
                                                count=1, dtype='float32')
        pos += 4

        buff = np.frombuffer(bin_data, offset=pos, count=2, dtype='int32')
        pos += 8
        data['valve_status'][ind] = buff[0]
        data['units_index'][ind] = buff[1]

        data['unit_conversion_factor'][ind] = np.frombuffer(bin_data, offset=pos, 
                                                            count=1, dtype='float32')
        pos += 4

        buff = np.frombuffer(bin_data, offset=pos, count=2, dtype='int32')
        pos += 8
        data['PTP_scan_start_time_sec'][ind] = buff[0]
        data['PTP_scan_start_time_ns'][ind] = buff[1]

        data['external_trigger_time'][ind] = np.frombuffer(bin_data, offset=pos, 
                                                           count=1, dtype='uint32')
        pos += 1

        data['temperatures'][ind, :] = np.frombuffer(bin_data, offset=pos, 
                                                     count=8, dtype='float32')
        pos += 32

        data['pressures'][ind, :] = np.frombuffer(bin_data, offset=pos, 
                                                  count=64, dtype='float32')
        pos += 256

        buff = np.frombuffer(bin_data, offset=pos, count=4, dtype='int32')
        pos += 16
        data['frame_time_sec'][ind] = buff[0]
        data['frame_time_ns'][ind] = buff[1]
        data['external_trigger_time_sec'][ind] = buff[2]
        data['external_trigger_time_ns'][ind] = buff[3]
    
    data['temperatures'] = data['temperatures'].T
    data['pressures'] = data['pressures'].T

    return data