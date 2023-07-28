import numpy as np
import solarpy as sp
from datetime import timedelta


def lng_to360(lng_input):
    if lng_input < 0:
        return abs(lng_input)
    elif 0 < lng_input < 180:
        return lng_input + 180


def standard2solar_time_modified(date, lng, lng_std):
    """
    solarpy.standar2solar_time() modified function from solarpy
    Solar time for a particular longitude, date and *standard* time.

    Parameters
    ----------
    date : datetime object
        standard (or local) time
    lng : float
        longitude, west position to the Prime Meridian in degrees (0º to 360º)
    lng_std: float
        standard longitude, west position to the Prime Meridian in degrees (0ª to 360ª)

    Returns
    -------
    solar time : datetime object
        solar time
    """
    sp.check_long(lng)

    # standard time
    t_std = date
    lng_360 = lng_to360(lng)
    lng_std_360 = lng_to360(lng_std)

    # displacement from standard meridian for that longitude
    delta_std_meridian = timedelta(minutes=(4 * (lng_std_360 - lng_360)))

    # eq. of time for that day
    e_param = timedelta(minutes=sp.eq_time(date))
    t_solar = t_std + delta_std_meridian + e_param
    return t_solar


def dir_nu(date, glo_h, dif_hu, latitude):
    zen = sp.theta_z(date, latitude)
    dir_nu_value = (glo_h - dif_hu) / np.cos(zen)
    return dir_nu_value


def epsilon(date, glo_h, dif_hu, latitude, longitude, longitude_std):
    solar_time = standard2solar_time_modified(date, longitude, longitude_std)
    sunrise = sp.sunrise_time(solar_time, latitude)
    sunset = sp.sunset_time(solar_time, latitude)
    dir_nu_value = dir_nu(date, glo_h, dif_hu, latitude)
    if sunrise < solar_time < sunset:
        epsilon_value = (dif_hu + dir_nu_value) / dif_hu
    else:
        epsilon_value = np.nan
    return epsilon_value


def delta(date,  dif_hu, latitude, elevation):
    zen = sp.theta_z(date, latitude)
    delta_value = dif_hu * sp.air_mass_kastenyoung1989(np.rad2deg(zen), elevation) / sp.gon(date)
    return delta_value


def c_i_original(date, latitude, shadowband_width, shadowband_radius):
    phi = np.deg2rad(latitude)
    t_0 = sp.sunset_hour_angle(date, latitude)
    b = shadowband_width
    r = shadowband_radius
    declination = sp.declination(date)
    c_i_value = 1 / (1 - (2 * b) / (np.pi * r) * ((np.cos(declination)) ** 3) * (
            np.sin(phi) * np.sin(declination * t_0) + np.cos(phi) * np.cos(declination) * np.sin(t_0)))
    return c_i_value


def cut(date, glo_h, dif_hu, latitude, longitude, longitude_std, shadowband_width, shadowband_radius, elevation):
    zenith = sp.theta_z(date, latitude)
    if 0 <= zenith <= 35:
        zenith_cut = 1
    elif 35 < zenith <= 50:
        zenith_cut = 2
    elif 50 < zenith <= 60:
        zenith_cut = 3
    elif 60 < zenith <= 90:
        zenith_cut = 4
    else:
        zenith_cut = np.nan
    geometric = c_i_original(date, latitude, shadowband_width, shadowband_radius)
    if 1 <= geometric <= 1.068:
        geometric_cut = 1
    elif 1.068 <= geometric <= 1.1:
        geometric_cut = 2
    elif 1.1 <= geometric <= 1.132:
        geometric_cut = 3
    elif 1.132 < geometric:
        geometric_cut = 4
    else:
        geometric_cut = np.nan
    epsilon_value = epsilon(date, glo_h, dif_hu, latitude, longitude, longitude_std)
    if 0 <= epsilon_value <= 1.253:
        epsilon_cut = 1
    elif 1.253 <= epsilon_value <= 2.134:
        epsilon_cut = 2
    elif 2.134 <= epsilon_value <= 5.980:
        epsilon_cut = 3
    elif 5.980 < epsilon_value:
        epsilon_cut = 4
    else:
        epsilon_cut = np.nan
    delta_value = delta(date, dif_hu, latitude, elevation)
    if 0 <= delta_value <= 0.120:
        delta_cut = 1
    elif 0.120 <= delta_value <= 0.2:
        delta_cut = 2
    elif 0.2 <= delta_value <= 0.3:
        delta_cut = 3
    elif 0.3 < delta_value:
        delta_cut = 4
    else:
        delta_cut = np.nan
    return zenith_cut, geometric_cut, epsilon_cut, delta_cut


def set_dif_correction_factor(date, glo_h, dif_hu, latitude, longitude, longitude_std, shadowband_width,
                              shadowband_radius, elevation):
    lebaron_parameters = cut(date, glo_h, dif_hu, latitude, longitude, longitude_std, shadowband_width,
                             shadowband_radius, elevation)
    i = lebaron_parameters[0]
    j = lebaron_parameters[1]
    k = lebaron_parameters[2]
    el = lebaron_parameters[3]
    dif_correction_factor = None
    if k == 1 and el == 1:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.173
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.104
            elif j == 3:
                dif_correction_factor = 1.115
            elif j == 4:
                dif_correction_factor = 1.163
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.069
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.119
            elif j == 4:
                dif_correction_factor = 1.140
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.047
            elif j == 2:
                dif_correction_factor = 1.063
            elif j == 3:
                dif_correction_factor = 1.074
            elif j == 4:
                dif_correction_factor = 1.030
    elif k == 2 and el == 1:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.248
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.184
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.161
            elif j == 2:
                dif_correction_factor = 1.161
            elif j == 3:
                dif_correction_factor = 1.147
            elif j == 4:
                dif_correction_factor = 1.168
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.076
            elif j == 2:
                dif_correction_factor = 1.078
            elif j == 3:
                dif_correction_factor = 1.104
            elif j == 4:
                dif_correction_factor = 1.146
    elif k == 3 and el == 1:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.156
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.156
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.156
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.187
            elif j == 2:
                dif_correction_factor = 1.167
            elif j == 3:
                dif_correction_factor = 1.139
            elif j == 4:
                dif_correction_factor = 1.191
    elif k == 4 and el == 1:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.181
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 0.990
            elif j == 4:
                dif_correction_factor = 1.104
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.015
            elif j == 2:
                dif_correction_factor = 1.016
            elif j == 3:
                dif_correction_factor = 0.946
            elif j == 4:
                dif_correction_factor = 1.027
        elif i == 4:
            if j == 1:
                dif_correction_factor = 0.925
            elif j == 2:
                dif_correction_factor = 0.967
            elif j == 3:
                dif_correction_factor = 0.977
            elif j == 4:
                dif_correction_factor = 1.150
    elif k == 1 and el == 2:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.176
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.095
            elif j == 3:
                dif_correction_factor = 1.130
            elif j == 4:
                dif_correction_factor = 1.162
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.073
            elif j == 2:
                dif_correction_factor = 1.089
            elif j == 3:
                dif_correction_factor = 1.115
            elif j == 4:
                dif_correction_factor = 1.142
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.058
            elif j == 2:
                dif_correction_factor = 1.076
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.156
    elif k == 2 and el == 2:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.211
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.186
            elif j == 4:
                dif_correction_factor = 1.194
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.086
            elif j == 2:
                dif_correction_factor = 1.130
            elif j == 3:
                dif_correction_factor = 1.168
            elif j == 4:
                dif_correction_factor = 1.177
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.074
            elif j == 2:
                dif_correction_factor = 1.102
            elif j == 3:
                dif_correction_factor = 1.118
            elif j == 4:
                dif_correction_factor = 1.174
    elif k == 3 and el == 2:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.237
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.203
            elif j == 4:
                dif_correction_factor = 1.212
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.080
            elif j == 2:
                dif_correction_factor = 1.195
            elif j == 3:
                dif_correction_factor = 1.211
            elif j == 4:
                dif_correction_factor = 1.185
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.140
            elif j == 2:
                dif_correction_factor = 1.098
            elif j == 3:
                dif_correction_factor = 1.191
            elif j == 4:
                dif_correction_factor = 1.181
    elif k == 4 and el == 2:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.217
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.120
            elif j == 4:
                dif_correction_factor = 1.180
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.182
            elif j == 2:
                dif_correction_factor = 1.115
            elif j == 3:
                dif_correction_factor = 1.081
            elif j == 4:
                dif_correction_factor = 1.111
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.057
            elif j == 2:
                dif_correction_factor = 1.119
            elif j == 3:
                dif_correction_factor = 1.133
            elif j == 4:
                dif_correction_factor = 1.033
    elif k == 1 and el == 3:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.182
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.128
            elif j == 4:
                dif_correction_factor = 1.159
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.076
            elif j == 2:
                dif_correction_factor = 1.088
            elif j == 3:
                dif_correction_factor = 1.131
            elif j == 4:
                dif_correction_factor = 1.129
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.060
            elif j == 2:
                dif_correction_factor = 1.085
            elif j == 3:
                dif_correction_factor = 1.103
            elif j == 4:
                dif_correction_factor = 1.156
    elif k == 2 and el == 3:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.221
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.171
            elif j == 3:
                dif_correction_factor = 1.180
            elif j == 4:
                dif_correction_factor = 1.213
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.135
            elif j == 2:
                dif_correction_factor = 1.148
            elif j == 3:
                dif_correction_factor = 1.176
            elif j == 4:
                dif_correction_factor = 1.197
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.092
            elif j == 2:
                dif_correction_factor = 1.119
            elif j == 3:
                dif_correction_factor = 1.143
            elif j == 4:
                dif_correction_factor = 1.182
    elif k == 3 and el == 3:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.238
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.160
            elif j == 3:
                dif_correction_factor = 1.207
            elif j == 4:
                dif_correction_factor = 1.230
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.169
            elif j == 2:
                dif_correction_factor = 1.191
            elif j == 3:
                dif_correction_factor = 1.193
            elif j == 4:
                dif_correction_factor = 1.210
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.150
            elif j == 2:
                dif_correction_factor = 1.133
            elif j == 3:
                dif_correction_factor = 1.180
            elif j == 4:
                dif_correction_factor = 1.156
    elif k == 4 and el == 3:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.156
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.156
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.156
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.089
            elif j == 2:
                dif_correction_factor = 1.194
            elif j == 3:
                dif_correction_factor = 1.216
            elif j == 4:
                dif_correction_factor = 1.064
    elif k == 1 and el == 4:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.191
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.105
            elif j == 3:
                dif_correction_factor = 1.143
            elif j == 4:
                dif_correction_factor = 1.168
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.085
            elif j == 2:
                dif_correction_factor = 1.093
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.156
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.069
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.156
    elif k == 2 and el == 4:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.238
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.148
            elif j == 3:
                dif_correction_factor = 1.195
            elif j == 4:
                dif_correction_factor = 1.230
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.132
            elif j == 2:
                dif_correction_factor = 1.160
            elif j == 3:
                dif_correction_factor = 1.183
            elif j == 4:
                dif_correction_factor = 1.210
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.118
            elif j == 2:
                dif_correction_factor = 1.116
            elif j == 3:
                dif_correction_factor = 1.150
            elif j == 4:
                dif_correction_factor = 1.185
    elif k == 3 and el == 4:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.232
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.206
            elif j == 3:
                dif_correction_factor = 1.210
            elif j == 4:
                dif_correction_factor = 1.238
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.144
            elif j == 2:
                dif_correction_factor = 1.178
            elif j == 3:
                dif_correction_factor = 1.226
            elif j == 4:
                dif_correction_factor = 1.216
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.117
            elif j == 2:
                dif_correction_factor = 1.155
            elif j == 3:
                dif_correction_factor = 1.178
            elif j == 4:
                dif_correction_factor = 1.167
    elif k == 4 and el == 4:
        if i == 1:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.156
        elif i == 2:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.156
        elif i == 3:
            if j == 1:
                dif_correction_factor = 1.051
            elif j == 2:
                dif_correction_factor = 1.082
            elif j == 3:
                dif_correction_factor = 1.117
            elif j == 4:
                dif_correction_factor = 1.156
        elif i == 4:
            if j == 1:
                dif_correction_factor = 1.024
            elif j == 2:
                dif_correction_factor = 1.025
            elif j == 3:
                dif_correction_factor = 1.162
            elif j == 4:
                dif_correction_factor = 1.142
    return dif_correction_factor
