from datetime import datetime, timedelta
import numpy as np
import solarpy as sp
import pandas as pd


class SolarMeasurement:
    def __init__(self, clock_datetime, glo_h, dif_hu, lat, lng, lng_std, altitude, shadowband_width, shadowband_radius):
        self.datetime = clock_datetime
        self.glo_h = glo_h
        self.dif_hu = dif_hu
        self.lat = lat  # latitude (-90 to 90) in degrees
        self.lng = lng  # longitude (-180 to 180) in degrees, west negative
        self.lng_std = lng_std  # standard longitude (-180 to 180 in degrees, west negative
        self.altitude = altitude
        self.shadowband_width = shadowband_width
        self.shadowband_radius = shadowband_radius
        self.solar_datetime = standard2solar_time_modified(self.datetime, self.lng, self.lng_std)
        self.sunrise = sp.sunrise_time(self.datetime, self.lat)
        self.sunset = sp.sunset_time(self.datetime, self.lat)
        self.zenithal_angle = sp.theta_z(self.solar_datetime, self.lat)     # In radians


def set_lng(lng_input):
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
    lng_360 = set_lng(lng)
    lng_std_360 = set_lng(lng_std)

    # displacement from standard meridian for that longitude
    delta_std_meridian = timedelta(minutes=(4 * (lng_std_360 - lng_360)))

    # eq. of time for that day
    e_param = timedelta(minutes=sp.eq_time(date))
    t_solar = t_std + delta_std_meridian + e_param
    return t_solar


def dir_nu(measurement):
    dir_nu_value = (measurement.glo_h - measurement.dif_hu) / np.cos(measurement.zenithal_angle)
    return dir_nu_value


def epsilon(measurement):
    dni_value = dir_nu(measurement)
    sunrise = measurement.sunrise
    sunset = measurement.sunset
    if sunrise < measurement.datetime < sunset:
        epsilon_value = (measurement.dif_hu + dni_value) / measurement.dif_hu
    else:
        epsilon_value = np.nan
    return epsilon_value


def delta(measurement):
    delta_value = measurement.dif_hu * sp.air_mass_kastenyoung1989(np.rad2deg(measurement.zenithal_angle),
                                                                   measurement.altitude) / sp.gon(measurement.datetime)
    return delta_value


def c_i_original(measurement):
    b_input = measurement.shadowband_width
    r_input = measurement.shadowband_radius
    phi = np.deg2rad(measurement.lat)
    t_0 = sp.sunset_hour_angle(measurement.datetime, measurement.lat)
    italic_delta = sp.declination(measurement.datetime)
    c_i_value = 1 / (1 - (2 * b_input) / (np.pi * r_input) * ((np.cos(italic_delta)) ** 3) * (
            np.sin(phi) * np.sin(italic_delta * t_0) + np.cos(phi) * np.cos(italic_delta) * np.sin(t_0)))
    return c_i_value


def cut(measurement):
    zenith_angle_input = np.rad2deg(measurement.zenithal_angle)
    geometric_input = c_i_original(measurement)
    epsilon_input = epsilon(measurement)
    delta_input = delta(measurement)
    if 0 <= zenith_angle_input <= 35:
        zenith_cut = 1
    elif 35 < zenith_angle_input <= 50:
        zenith_cut = 2
    elif 50 < zenith_angle_input <= 60:
        zenith_cut = 3
    elif 60 < zenith_angle_input <= 90:
        zenith_cut = 4
    else:
        zenith_cut = np.nan

    if 1 <= geometric_input <= 1.068:
        geometric_cut = 1
    elif 1.068 <= geometric_input <= 1.1:
        geometric_cut = 2
    elif 1.1 <= geometric_input <= 1.132:
        geometric_cut = 3
    elif 1.132 < geometric_input:
        geometric_cut = 4
    else:
        geometric_cut = np.nan

    if 0 <= epsilon_input <= 1.253:
        epsilon_cut = 1
    elif 1.253 <= epsilon_input <= 2.134:
        epsilon_cut = 2
    elif 2.134 <= epsilon_input <= 5.980:
        epsilon_cut = 3
    elif 5.980 < epsilon_input:
        epsilon_cut = 4
    else:
        epsilon_cut = np.nan

    if 0 <= delta_input <= 0.120:
        delta_cut = 1
    elif 0.120 <= delta_input <= 0.2:
        delta_cut = 2
    elif 0.2 <= delta_input <= 0.3:
        delta_cut = 3
    elif 0.3 < delta_input:
        delta_cut = 4
    else:
        delta_cut = np.nan
    return zenith_cut, geometric_cut, epsilon_cut, delta_cut


def lebaron(measurement):
    cut_input = cut(measurement)
    i = cut_input[0]
    j = cut_input[1]
    k = cut_input[2]
    el = cut_input[3]
    correction = None
    if k == 1 and el == 1:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.173
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.104
            elif j == 3:
                correction = 1.115
            elif j == 4:
                correction = 1.163
        elif i == 3:
            if j == 1:
                correction = 1.069
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.119
            elif j == 4:
                correction = 1.140
        elif i == 4:
            if j == 1:
                correction = 1.047
            elif j == 2:
                correction = 1.063
            elif j == 3:
                correction = 1.074
            elif j == 4:
                correction = 1.030
    elif k == 2 and el == 1:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.248
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.184
        elif i == 3:
            if j == 1:
                correction = 1.161
            elif j == 2:
                correction = 1.161
            elif j == 3:
                correction = 1.147
            elif j == 4:
                correction = 1.168
        elif i == 4:
            if j == 1:
                correction = 1.076
            elif j == 2:
                correction = 1.078
            elif j == 3:
                correction = 1.104
            elif j == 4:
                correction = 1.146
    elif k == 3 and el == 1:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 3:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 4:
            if j == 1:
                correction = 1.187
            elif j == 2:
                correction = 1.167
            elif j == 3:
                correction = 1.139
            elif j == 4:
                correction = 1.191
    elif k == 4 and el == 1:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.181
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 0.990
            elif j == 4:
                correction = 1.104
        elif i == 3:
            if j == 1:
                correction = 1.015
            elif j == 2:
                correction = 1.016
            elif j == 3:
                correction = 0.946
            elif j == 4:
                correction = 1.027
        elif i == 4:
            if j == 1:
                correction = 0.925
            elif j == 2:
                correction = 0.967
            elif j == 3:
                correction = 0.977
            elif j == 4:
                correction = 1.150
    elif k == 1 and el == 2:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.176
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.095
            elif j == 3:
                correction = 1.130
            elif j == 4:
                correction = 1.162
        elif i == 3:
            if j == 1:
                correction = 1.073
            elif j == 2:
                correction = 1.089
            elif j == 3:
                correction = 1.115
            elif j == 4:
                correction = 1.142
        elif i == 4:
            if j == 1:
                correction = 1.058
            elif j == 2:
                correction = 1.076
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
    elif k == 2 and el == 2:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.211
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.186
            elif j == 4:
                correction = 1.194
        elif i == 3:
            if j == 1:
                correction = 1.086
            elif j == 2:
                correction = 1.130
            elif j == 3:
                correction = 1.168
            elif j == 4:
                correction = 1.177
        elif i == 4:
            if j == 1:
                correction = 1.074
            elif j == 2:
                correction = 1.102
            elif j == 3:
                correction = 1.118
            elif j == 4:
                correction = 1.174
    elif k == 3 and el == 2:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.237
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.203
            elif j == 4:
                correction = 1.212
        elif i == 3:
            if j == 1:
                correction = 1.080
            elif j == 2:
                correction = 1.195
            elif j == 3:
                correction = 1.211
            elif j == 4:
                correction = 1.185
        elif i == 4:
            if j == 1:
                correction = 1.140
            elif j == 2:
                correction = 1.098
            elif j == 3:
                correction = 1.191
            elif j == 4:
                correction = 1.181
    elif k == 4 and el == 2:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.217
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.120
            elif j == 4:
                correction = 1.180
        elif i == 3:
            if j == 1:
                correction = 1.182
            elif j == 2:
                correction = 1.115
            elif j == 3:
                correction = 1.081
            elif j == 4:
                correction = 1.111
        elif i == 4:
            if j == 1:
                correction = 1.057
            elif j == 2:
                correction = 1.119
            elif j == 3:
                correction = 1.133
            elif j == 4:
                correction = 1.033
    elif k == 1 and el == 3:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.182
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.128
            elif j == 4:
                correction = 1.159
        elif i == 3:
            if j == 1:
                correction = 1.076
            elif j == 2:
                correction = 1.088
            elif j == 3:
                correction = 1.131
            elif j == 4:
                correction = 1.129
        elif i == 4:
            if j == 1:
                correction = 1.060
            elif j == 2:
                correction = 1.085
            elif j == 3:
                correction = 1.103
            elif j == 4:
                correction = 1.156
    elif k == 2 and el == 3:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.221
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.171
            elif j == 3:
                correction = 1.180
            elif j == 4:
                correction = 1.213
        elif i == 3:
            if j == 1:
                correction = 1.135
            elif j == 2:
                correction = 1.148
            elif j == 3:
                correction = 1.176
            elif j == 4:
                correction = 1.197
        elif i == 4:
            if j == 1:
                correction = 1.092
            elif j == 2:
                correction = 1.119
            elif j == 3:
                correction = 1.143
            elif j == 4:
                correction = 1.182
    elif k == 3 and el == 3:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.238
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.160
            elif j == 3:
                correction = 1.207
            elif j == 4:
                correction = 1.230
        elif i == 3:
            if j == 1:
                correction = 1.169
            elif j == 2:
                correction = 1.191
            elif j == 3:
                correction = 1.193
            elif j == 4:
                correction = 1.210
        elif i == 4:
            if j == 1:
                correction = 1.150
            elif j == 2:
                correction = 1.133
            elif j == 3:
                correction = 1.180
            elif j == 4:
                correction = 1.156
    elif k == 4 and el == 3:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 3:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 4:
            if j == 1:
                correction = 1.089
            elif j == 2:
                correction = 1.194
            elif j == 3:
                correction = 1.216
            elif j == 4:
                correction = 1.064
    elif k == 1 and el == 4:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.191
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.105
            elif j == 3:
                correction = 1.143
            elif j == 4:
                correction = 1.168
        elif i == 3:
            if j == 1:
                correction = 1.085
            elif j == 2:
                correction = 1.093
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 4:
            if j == 1:
                correction = 1.069
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
    elif k == 2 and el == 4:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.238
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.148
            elif j == 3:
                correction = 1.195
            elif j == 4:
                correction = 1.230
        elif i == 3:
            if j == 1:
                correction = 1.132
            elif j == 2:
                correction = 1.160
            elif j == 3:
                correction = 1.183
            elif j == 4:
                correction = 1.210
        elif i == 4:
            if j == 1:
                correction = 1.118
            elif j == 2:
                correction = 1.116
            elif j == 3:
                correction = 1.150
            elif j == 4:
                correction = 1.185
    elif k == 3 and el == 4:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.232
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.206
            elif j == 3:
                correction = 1.210
            elif j == 4:
                correction = 1.238
        elif i == 3:
            if j == 1:
                correction = 1.144
            elif j == 2:
                correction = 1.178
            elif j == 3:
                correction = 1.226
            elif j == 4:
                correction = 1.216
        elif i == 4:
            if j == 1:
                correction = 1.117
            elif j == 2:
                correction = 1.155
            elif j == 3:
                correction = 1.178
            elif j == 4:
                correction = 1.167
    elif k == 4 and el == 4:
        if i == 1:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 2:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 3:
            if j == 1:
                correction = 1.051
            elif j == 2:
                correction = 1.082
            elif j == 3:
                correction = 1.117
            elif j == 4:
                correction = 1.156
        elif i == 4:
            if j == 1:
                correction = 1.024
            elif j == 2:
                correction = 1.025
            elif j == 3:
                correction = 1.162
            elif j == 4:
                correction = 1.142
    return correction


# year = 2021
# latitud = -32.898
# longitud = -68.875
# altitud = 842  # msnm
# b = 7.5  # Ancho de la banda (cm)
# r = 30.8  # Radio de la banda (cm)

# # Carga del archivo a analizar
# file_path = r"G:\Otros ordenadores\INAHE-02\inahe\estacion emi\datos\script_tratamiento\data\2021-minute-raw.csv"
# file_df = pd.read_csv(file_path, sep=";")
# file_df['fecha'] = pd.to_datetime(file_df['fecha'], format="%d/%m/%Y %H:%M")
# file_df.sort_values(by=["fecha"], inplace=True)
#
# measurements = [SolarMeasurement(date, ghi, dif, latitud, longitud, -45, altitud, b, r) for date, ghi, dif in zip(file_df["fecha"], file_df["IRGLO"], file_df["IRDIF"])]
# lebaron_list = [lebaron(measurement) for measurement in measurements]
# file_df.reset_index(inplace=False)