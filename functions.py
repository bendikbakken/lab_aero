# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 12:06:53 2023

@author: bendi
"""

from fluid_prop import fluid_prop
from PS2_Q3_supp import x_port_up, y_port_up, x_port_low, y_port_low, P_Dist_upper, P_Dist_lower
from matplotlib import pyplot as plt
import numpy as np

def plot_airfoil(ax):
    """ Plotting the airfoil"""
    x_points_up  = np.hstack([0, x_port_up,  0.45])
    x_points_low = np.hstack([0, x_port_low, 0.45])
    y_points_up  = np.hstack([0, y_port_up,  0.0])
    y_points_low = np.hstack([0, y_port_low, 0.0])
    
    ax.plot(x_points_low, y_points_low, linewidth=2, color='k')
    ax.plot(x_points_up, y_points_up, linewidth=2, color='k')
    ax.axis('equal')

def plot_pressure_vectors(ax, x_port_up, y_port_up, x_port_low, y_port_low, P_Dist_upper, P_Dist_lower):
    """Calculating the positions of the airfoil geomety"""
    origin_upper = [x_port_up] + [y_port_up]
    origin_lower = [x_port_low] + [y_port_low]
    
    x_points_up  = np.hstack([0, x_port_up,  0.45])
    x_points_low = np.hstack([0, x_port_low, 0.45])
    y_points_up  = np.hstack([0, y_port_up,  0.0])
    y_points_low = np.hstack([0, y_port_low, 0.0])
    
    x_diff_up  = np.gradient(x_points_up)[1:-1]
    y_diff_up  = np.gradient(y_points_up)[1:-1]
    x_diff_low = np.gradient(x_points_low)[1:-1]
    y_diff_low = np.gradient(y_points_low)[1:-1]

    P_upper_y  = -P_Dist_upper*np.sin(-np.arctan2(y_diff_up, x_diff_up))
    P_upper_x  = -P_Dist_upper*np.cos(-np.arctan2(y_diff_up, x_diff_up))
    
    P_lower_y  = P_Dist_lower*np.sin(-np.arctan2(y_diff_low, x_diff_low))
    P_lower_x  = P_Dist_lower*np.cos(-np.arctan2(y_diff_low, x_diff_low))
    
    ax.plot(x_points_low, y_points_low, linewidth=2, color='k')
    ax.plot(x_points_up, y_points_up, linewidth=2, color='k')
    ax.axis('equal')

    ax.quiver(*origin_upper, P_upper_y, P_upper_x)
    ax.quiver(*origin_lower, P_lower_y, P_lower_x, pivot='tip')
    ax.set_xlim(-0.1,0.5)

# plot_airfoil()
# plot_pressure_vectors(x_port_up, y_port_up, x_port_low, y_port_low, P_Dist_upper, P_Dist_lower)

def calc_cl(x_port_up, y_port_up, x_port_low, y_port_low, P_Dist_upper, P_Dist_lower):
    """Calculating resultant vector"""
    U_inf = 14.8
    chord = 0.45
    alpha = 10*np.pi/180
    fluid_properties = fluid_prop(29,738)
    rho_air = fluid_properties[0]
    Cp_upper = P_Dist_upper/(0.5*U_inf**2*rho_air)
    Cp_lower = P_Dist_lower/(0.5*U_inf**2*rho_air)
    
    """Could have calculated gradient without endpoints, 
        but this gives higher order at the ends"""                       
    x_points_up  = np.hstack([0, x_port_up,  0.45])
    x_points_low = np.hstack([0, x_port_low, 0.45])
    y_points_up  = np.hstack([0, y_port_up,  0.0])
    y_points_low = np.hstack([0, y_port_low, 0.0])
    
    """Gradients are needed for the axial pressure coefficient"""
    dydx_up = np.gradient(y_points_up, x_points_up)[1:-1]
    dydx_low = np.gradient(y_points_low, x_points_low)[1:-1]
    
    """Calculating the normal and axial integrated pressure forces using np.trapz to
    numericallly estimate the integrals"""
    C_n = 1/chord*(np.trapz(Cp_lower, x_port_low) -\
                   np.trapz(Cp_upper, x_port_up))
    C_a = 1/chord*(np.trapz(Cp_upper*dydx_up, x_port_up) -\
                   np.trapz(Cp_lower*dydx_low, x_port_low))
    
    """Using these to calculate the lift and (pressure) drag."""
    C_l = C_n*np.cos(alpha) - C_a*np.sin(alpha)
    C_d = C_n*np.sin(alpha) + C_a*np.cos(alpha)

    return C_l


"""Using L' = C_l * q_inf * C"""

# L_section = C_l*0.5*rho_air*U_inf**2*chord
# print(f'b) The sectional lift is \nL\' = {round(L_section,2)} N/m')
# print(f'The sectional lift coefficient is\nC_l = {round(C_l,2)}')