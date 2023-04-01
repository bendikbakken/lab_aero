import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.interpolate
import fluid_prop
import functions as fnc

from PS2_Q3_supp import x_port_up, y_port_up, x_port_low, y_port_low

#plt.rcParams['text.usetex'] = True

import read_mat
import read_press_scan_binary as rpsb


def example_calculation(data_directory, group_name_prefix, alpha):
    """
    This is an example function that shows you how to extract data from
    the pressure scanner files and how to perform offset corrections
    """

    # Load the metadata as a dictionary
    meta = read_mat.read(data_directory + group_name_prefix + '_dataset.mat')

    # Find indices of the pressure port on the
    # upper and lower surface as well as loading
    # surface_points for the corresponding indices
    inds_lower = meta['lower_ind']
    inds_upper = meta['upper_ind']
    x_lower = meta['x_surf_low_real']
    x_upper = meta['x_surf_up_real']

    # Angles of attack
    alphas = np.asarray((meta['alphas']), dtype=int)

    # Get index in variable 'alphas' that matches the chosen AoA
    alpha_index = np.where(alphas == alpha)

    # Exctract times at which pre- and post-experiment offset measurements were done
    t_offset_1 = meta['t_stamp_0_1']
    t_offset_2 = meta['t_stamp_0_2']

    # Time at which data for chosen AoA was measured
    t_alpha = meta['t_stamp'][alpha_index]

    # Extract offset pressure measurements from pressure scanner files, split
    # data between upper and lower surfaces, and calculate their temporal means
    _, PS_offset1 = rpsb.read(data_directory + group_name_prefix + '_offset1.dat')
    _, PS_offset2 = rpsb.read(data_directory + group_name_prefix + '_offset2.dat')
    PS_lower_offset_1 = np.mean(PS_offset1[inds_lower, :], axis=1)
    PS_upper_offset_1 = np.mean(PS_offset1[inds_upper, :], axis=1)
    PS_lower_offset_2 = np.mean(PS_offset2[inds_lower, :], axis=1)
    PS_upper_offset_2 = np.mean(PS_offset2[inds_upper, :], axis=1)

    # Create a multivariate interpolant function for the pressure scanner offsets.
    # This is a function that returns (as an array) the linearly interpolated value of
    # the offset pressure for each pressure port at any time between the offset measurements
    # if we assume a linear drift. Separate interpolants are made for the upper and
    # lower surfaces (but we could have easily done this in one go if we didn't split the data earlier).
    PS_lower_interpolant = sp.interpolate.interp1d(
        np.array([t_offset_1, t_offset_2]),
        np.array([PS_lower_offset_1, PS_lower_offset_2]).T
    )

    PS_upper_interpolant = sp.interpolate.interp1d(
        np.array([t_offset_1, t_offset_2]),
        np.array([PS_upper_offset_1, PS_upper_offset_2]).T
    )

    # Extract pressure scanner data for the chosen angle of attack, split data 
    # between upper and lower surfaces, and calculate their temporal means
    _, p = rpsb.read(data_directory + group_name_prefix + '_a' + str(int(alphas[alpha_index])) + '.dat')
    PS_upper_alpha = np.mean(p[inds_upper, :], axis=1)
    PS_lower_alpha = np.mean(p[inds_lower, :], axis=1)

    # Subtract the interpolated offset at the time of the measurement
    # Use .T to make sure arrays have the same orientation
    PS_upper_alpha = PS_upper_alpha - PS_upper_interpolant(t_alpha).T
    PS_lower_alpha = PS_lower_alpha - PS_lower_interpolant(t_alpha).T

    # Extract pitot tube offset measurements and calculate their temporal means
    q_offset_1 = np.mean(meta['data_q_0_1'])
    q_offset_2 = np.mean(meta['data_q_0_2'])

    # Use normal (i.e. univariate) interpolation to calculate the pitot offset at the time of
    # lift measurement - assuming linear drift
    q_offset_alpha = np.interp(
        t_alpha,
        np.array([t_offset_1, t_offset_2]),
        np.array([q_offset_1, q_offset_2])
    )

    # Extract pitot tube voltage data for the chosen AoA, calculate temporal mean,
    # subtract the interpolated offset, and then convert to Pa using the conversion factor
    q_alpha = ((np.mean(meta['data_q_raw'][alpha_index, :])) - q_offset_alpha) * meta['Vqfactor']

    # Extract thermocouple data for the chosen AoA and calculate the temporal mean
    Temp_alpha = np.mean(meta['data_T_raw'][alpha_index, :])

    # Use normal (i.e. univariate) interpolation to calculate the atmospheric
    # pressure at the time of lift measurement - assuming linear drift
    P_atm_alpha = np.interp(
        t_alpha,
        np.array([t_offset_1, t_offset_2]),
        np.array([meta['Patm'], meta['Patm_end']])
    )

    # calculate fluid and flow properties
    rho_alpha, mu_alpha, _, _ = fluid_prop.fluid_prop(Temp_alpha, P_atm_alpha)
    nu_alpha = mu_alpha / rho_alpha
    U_alpha = np.sqrt(2 * q_alpha / rho_alpha)
    Re_c_alpha = U_alpha * meta['c'] / nu_alpha

    # Plot the pressure profile as -Cp
    fig, (ax, ax2) = plt.subplots(2,1,sharex=True)
    fig.dpi = 150
    ax.plot(x_upper, -PS_upper_alpha.T / q_alpha, '-ob', label=r'Upper surface', linewidth=1, markersize=4)
    ax.plot(x_lower, -PS_lower_alpha.T / q_alpha, '-or', label=r'Lower surface', linewidth=1, markersize=4)
    ax.set_title('$\\alpha= %s ^{\\circ}$' % alpha, fontsize=16)
    ax.legend(loc='lower right')
    ax.set_xlabel(r'$x/c$', fontsize=16)
    ax.set_ylabel(r'$-Cp$', fontsize=16)
    ax.set_xlim((0, 1))
    
    fnc.plot_pressure_vectors(ax2, x_port_up, y_port_up, x_port_low, y_port_low, PS_upper_alpha, PS_lower_alpha)
    plt.show()

    # print results
    print('alpha = {:2n}     [deg]'.format(alpha))
    print('q_inf = {:3.1f}   [Pa]'.format(float(q_alpha)))
    print('T_inf = {:2.1f}   [deg C]'.format(Temp_alpha))
    print('U_inf = {:2.2f}  [m/s]'.format(float(U_alpha)))
    print('Re_c = {:5.0f}  [-]\n'.format(float(Re_c_alpha)))


if __name__ == "__main__":
    data_directory = 'raw_data/'
    group_name_prefix = 'Group13_370k'
    alpha_list = [-8, -4,-6,-2,0,2,4,6,7,8,9,10,11,12,13,14,16,18]
    
    for alpha in alpha_list:    
        example_calculation(data_directory, group_name_prefix, alpha)
