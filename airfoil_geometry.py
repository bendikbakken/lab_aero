###########################################################################
# This file contains the pressure tap coordinates of the NREL S826 airfoil
# model at NTNU that is used for the TEP4160 lab experiment. A set of
# pressure distribution data is also attached as part of the dataset
# required for Problem Set 2.
###########################################################################

import numpy as np

########################################################################### 

## surface pressure holes locations
#
# The units are in m; the LE is at the point [0,0]
#
# x_port_up  :  Upper ressure tap x-coord from the LE (19 taps in total)
# y_port_up  :  Upper ressure tap y-coord from the LE (19 taps in total)
# x_port_low :  Lower ressure tap x-coord from the LE (13 taps in total)
# y_port_low :  Lower ressure tap y-coord from the LE (13 taps in total)

x_port_up  = np.array([ 0.0002, 0.0042, 0.0100, 0.0154, 0.0211, 0.0349, 0.0487, 0.0627, 0.0763, 0.0910, 0.1113, 0.1516, 0.1946, 0.2375, 0.2802, 0.3228, 0.3651, 0.4071, 0.4276])
y_port_up  = np.array([ 0.0019, 0.0073, 0.0120, 0.0155, 0.0186, 0.0245, 0.0290, 0.0327, 0.0358, 0.0387, 0.0419, 0.0457, 0.0461, 0.0431, 0.0382, 0.0320, 0.0244, 0.0152, 0.0089])
x_port_low = np.array([ 0.0101, 0.0248, 0.0396, 0.0535, 0.0749, 0.0958, 0.1178, 0.1562, 0.1944, 0.2418, 0.2903, 0.3386, 0.3861])
y_port_low = np.array([ -0.0066, -0.0097, -0.0118, -0.0134, -0.0157, -0.0177, -0.0189, -0.0179, -0.0132, -0.0056, 0.0013, 0.0060, 0.0071])


## surface pressure holes location, measured in distance from leading edge
# These are distances measured ALONG the surface, they are NOT the x-coord
# of the pressure taps. 
#
# The units are millimetres.
#
# surf_up  :  Upper ressure tap distance along the surface from the LE (19 taps in total)
# surf_low :  Lower ressure tap distance along the surface from the LE (13 taps in total)

surf_up = np.array([1, 8.5, 16, 22.5, 29, 44, 58.5, 73, 87, 102, 122.5, 163, 206, 249, 292, 335, 378, 421, 442.5])
surf_low = np.array([12.5, 27.5, 42.5, 56.5, 78, 99, 121, 159.5, 198, 246, 295, 343.5, 391])
