from datetime import timedelta
import numpy as np
import solarpy as sp


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
        self.declination = sp.declination(self.datetime)
        self.solar_datetime = self.standard2solar_time_modified()
        self.sunrise = sp.sunrise_time(self.datetime, self.lat)
        self.sunset = sp.sunset_time(self.datetime, self.lat)
        self.sunset_hour_angle = sp.sunset_hour_angle(self.datetime, self.lat)
        self.zenithal_angle = sp.theta_z(self.solar_datetime, self.lat)  # In radians
        self.dir_nu = (self.glo_h - self.dif_hu) / np.cos(self.zenithal_angle)
        self.delta = self.dif_hu * sp.air_mass_kastenyoung1989(np.rad2deg(self.zenithal_angle),
                                                               self.altitude) / sp.gon(self.datetime)
        self.epsilon = None
        self.c_i = None
        self.lebaron_parameters = None
        self.dif_correction_factor = None
        self.set_epsilon()
        self.set_c_i()
        self.set_lebaron_parameters()
        self.set_dif_correction_factor()

    def set_epsilon(self):
        sunrise = self.sunrise
        sunset = self.sunset
        if sunrise < self.datetime < sunset:
            self.epsilon = (self.dif_hu + self.dir_nu) / self.dif_hu
        else:
            self.epsilon = np.nan

    def set_c_i(self):
        self.c_i = 1 / (1 - (2 * self.shadowband_width) / (np.pi * self.shadowband_radius) *
                        ((np.cos(self.declination)) ** 3) *
                        (np.sin(np.deg2rad(self.lat)) *
                         np.sin(self.declination * self.sunset_hour_angle) +
                         np.cos(np.deg2rad(self.lat)) * np.cos(self.declination) * np.sin(self.sunset_hour_angle)))

    def set_lebaron_parameters(self):
        zenith_angle_deg = np.rad2deg(self.zenithal_angle)
        if 0 <= zenith_angle_deg <= 35:
            zenith_cut = 1
        elif 35 < zenith_angle_deg <= 50:
            zenith_cut = 2
        elif 50 < zenith_angle_deg <= 60:
            zenith_cut = 3
        elif 60 < zenith_angle_deg <= 90:
            zenith_cut = 4
        else:
            zenith_cut = np.nan

        if 1 <= self.c_i <= 1.068:
            geometric_cut = 1
        elif 1.068 <= self.c_i <= 1.1:
            geometric_cut = 2
        elif 1.1 <= self.c_i <= 1.132:
            geometric_cut = 3
        elif 1.132 < self.c_i:
            geometric_cut = 4
        else:
            geometric_cut = np.nan

        if 0 <= self.epsilon <= 1.253:
            epsilon_cut = 1
        elif 1.253 <= self.epsilon <= 2.134:
            epsilon_cut = 2
        elif 2.134 <= self.epsilon <= 5.980:
            epsilon_cut = 3
        elif 5.980 < self.epsilon:
            epsilon_cut = 4
        else:
            epsilon_cut = np.nan

        if 0 <= self.delta <= 0.120:
            delta_cut = 1
        elif 0.120 <= self.delta <= 0.2:
            delta_cut = 2
        elif 0.2 <= self.delta <= 0.3:
            delta_cut = 3
        elif 0.3 < self.delta:
            delta_cut = 4
        else:
            delta_cut = np.nan
        self.lebaron_parameters = (zenith_cut, geometric_cut, epsilon_cut, delta_cut)

    def set_dif_correction_factor(self):
        i = self.lebaron_parameters[0]
        j = self.lebaron_parameters[1]
        k = self.lebaron_parameters[2]
        el = self.lebaron_parameters[3]
        if k == 1 and el == 1:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.173
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.104
                elif j == 3:
                    self.dif_correction_factor = 1.115
                elif j == 4:
                    self.dif_correction_factor = 1.163
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.069
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.119
                elif j == 4:
                    self.dif_correction_factor = 1.140
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.047
                elif j == 2:
                    self.dif_correction_factor = 1.063
                elif j == 3:
                    self.dif_correction_factor = 1.074
                elif j == 4:
                    self.dif_correction_factor = 1.030
        elif k == 2 and el == 1:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.248
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.184
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.161
                elif j == 2:
                    self.dif_correction_factor = 1.161
                elif j == 3:
                    self.dif_correction_factor = 1.147
                elif j == 4:
                    self.dif_correction_factor = 1.168
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.076
                elif j == 2:
                    self.dif_correction_factor = 1.078
                elif j == 3:
                    self.dif_correction_factor = 1.104
                elif j == 4:
                    self.dif_correction_factor = 1.146
        elif k == 3 and el == 1:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.156
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.156
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.156
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.187
                elif j == 2:
                    self.dif_correction_factor = 1.167
                elif j == 3:
                    self.dif_correction_factor = 1.139
                elif j == 4:
                    self.dif_correction_factor = 1.191
        elif k == 4 and el == 1:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.181
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 0.990
                elif j == 4:
                    self.dif_correction_factor = 1.104
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.015
                elif j == 2:
                    self.dif_correction_factor = 1.016
                elif j == 3:
                    self.dif_correction_factor = 0.946
                elif j == 4:
                    self.dif_correction_factor = 1.027
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 0.925
                elif j == 2:
                    self.dif_correction_factor = 0.967
                elif j == 3:
                    self.dif_correction_factor = 0.977
                elif j == 4:
                    self.dif_correction_factor = 1.150
        elif k == 1 and el == 2:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.176
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.095
                elif j == 3:
                    self.dif_correction_factor = 1.130
                elif j == 4:
                    self.dif_correction_factor = 1.162
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.073
                elif j == 2:
                    self.dif_correction_factor = 1.089
                elif j == 3:
                    self.dif_correction_factor = 1.115
                elif j == 4:
                    self.dif_correction_factor = 1.142
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.058
                elif j == 2:
                    self.dif_correction_factor = 1.076
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.156
        elif k == 2 and el == 2:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.211
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.186
                elif j == 4:
                    self.dif_correction_factor = 1.194
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.086
                elif j == 2:
                    self.dif_correction_factor = 1.130
                elif j == 3:
                    self.dif_correction_factor = 1.168
                elif j == 4:
                    self.dif_correction_factor = 1.177
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.074
                elif j == 2:
                    self.dif_correction_factor = 1.102
                elif j == 3:
                    self.dif_correction_factor = 1.118
                elif j == 4:
                    self.dif_correction_factor = 1.174
        elif k == 3 and el == 2:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.237
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.203
                elif j == 4:
                    self.dif_correction_factor = 1.212
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.080
                elif j == 2:
                    self.dif_correction_factor = 1.195
                elif j == 3:
                    self.dif_correction_factor = 1.211
                elif j == 4:
                    self.dif_correction_factor = 1.185
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.140
                elif j == 2:
                    self.dif_correction_factor = 1.098
                elif j == 3:
                    self.dif_correction_factor = 1.191
                elif j == 4:
                    self.dif_correction_factor = 1.181
        elif k == 4 and el == 2:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.217
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.120
                elif j == 4:
                    self.dif_correction_factor = 1.180
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.182
                elif j == 2:
                    self.dif_correction_factor = 1.115
                elif j == 3:
                    self.dif_correction_factor = 1.081
                elif j == 4:
                    self.dif_correction_factor = 1.111
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.057
                elif j == 2:
                    self.dif_correction_factor = 1.119
                elif j == 3:
                    self.dif_correction_factor = 1.133
                elif j == 4:
                    self.dif_correction_factor = 1.033
        elif k == 1 and el == 3:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.182
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.128
                elif j == 4:
                    self.dif_correction_factor = 1.159
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.076
                elif j == 2:
                    self.dif_correction_factor = 1.088
                elif j == 3:
                    self.dif_correction_factor = 1.131
                elif j == 4:
                    self.dif_correction_factor = 1.129
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.060
                elif j == 2:
                    self.dif_correction_factor = 1.085
                elif j == 3:
                    self.dif_correction_factor = 1.103
                elif j == 4:
                    self.dif_correction_factor = 1.156
        elif k == 2 and el == 3:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.221
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.171
                elif j == 3:
                    self.dif_correction_factor = 1.180
                elif j == 4:
                    self.dif_correction_factor = 1.213
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.135
                elif j == 2:
                    self.dif_correction_factor = 1.148
                elif j == 3:
                    self.dif_correction_factor = 1.176
                elif j == 4:
                    self.dif_correction_factor = 1.197
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.092
                elif j == 2:
                    self.dif_correction_factor = 1.119
                elif j == 3:
                    self.dif_correction_factor = 1.143
                elif j == 4:
                    self.dif_correction_factor = 1.182
        elif k == 3 and el == 3:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.238
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.160
                elif j == 3:
                    self.dif_correction_factor = 1.207
                elif j == 4:
                    self.dif_correction_factor = 1.230
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.169
                elif j == 2:
                    self.dif_correction_factor = 1.191
                elif j == 3:
                    self.dif_correction_factor = 1.193
                elif j == 4:
                    self.dif_correction_factor = 1.210
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.150
                elif j == 2:
                    self.dif_correction_factor = 1.133
                elif j == 3:
                    self.dif_correction_factor = 1.180
                elif j == 4:
                    self.dif_correction_factor = 1.156
        elif k == 4 and el == 3:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.156
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.156
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.156
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.089
                elif j == 2:
                    self.dif_correction_factor = 1.194
                elif j == 3:
                    self.dif_correction_factor = 1.216
                elif j == 4:
                    self.dif_correction_factor = 1.064
        elif k == 1 and el == 4:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.191
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.105
                elif j == 3:
                    self.dif_correction_factor = 1.143
                elif j == 4:
                    self.dif_correction_factor = 1.168
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.085
                elif j == 2:
                    self.dif_correction_factor = 1.093
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.156
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.069
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.156
        elif k == 2 and el == 4:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.238
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.148
                elif j == 3:
                    self.dif_correction_factor = 1.195
                elif j == 4:
                    self.dif_correction_factor = 1.230
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.132
                elif j == 2:
                    self.dif_correction_factor = 1.160
                elif j == 3:
                    self.dif_correction_factor = 1.183
                elif j == 4:
                    self.dif_correction_factor = 1.210
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.118
                elif j == 2:
                    self.dif_correction_factor = 1.116
                elif j == 3:
                    self.dif_correction_factor = 1.150
                elif j == 4:
                    self.dif_correction_factor = 1.185
        elif k == 3 and el == 4:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.232
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.206
                elif j == 3:
                    self.dif_correction_factor = 1.210
                elif j == 4:
                    self.dif_correction_factor = 1.238
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.144
                elif j == 2:
                    self.dif_correction_factor = 1.178
                elif j == 3:
                    self.dif_correction_factor = 1.226
                elif j == 4:
                    self.dif_correction_factor = 1.216
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.117
                elif j == 2:
                    self.dif_correction_factor = 1.155
                elif j == 3:
                    self.dif_correction_factor = 1.178
                elif j == 4:
                    self.dif_correction_factor = 1.167
        elif k == 4 and el == 4:
            if i == 1:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.156
            elif i == 2:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.156
            elif i == 3:
                if j == 1:
                    self.dif_correction_factor = 1.051
                elif j == 2:
                    self.dif_correction_factor = 1.082
                elif j == 3:
                    self.dif_correction_factor = 1.117
                elif j == 4:
                    self.dif_correction_factor = 1.156
            elif i == 4:
                if j == 1:
                    self.dif_correction_factor = 1.024
                elif j == 2:
                    self.dif_correction_factor = 1.025
                elif j == 3:
                    self.dif_correction_factor = 1.162
                elif j == 4:
                    self.dif_correction_factor = 1.142

    def standard2solar_time_modified(self):
        """
        solarpy.standar2solar_time() modified function from solarpy
        Solar time for a particular longitude, date and *standard* time.

        Parameters
        ----------
        self.datetime : datetime object
            standard (or local) time
        self.lng : float
            longitude, west position to the Prime Meridian in degrees (0º to 360º)
        self.lng_std: float
            standard longitude, west position to the Prime Meridian in degrees (0ª to 360ª)

        Returns
        -------
        solar time : datetime object
            solar time
        """
        sp.check_long(self.lng)

        # standard time
        t_std = self.datetime
        lng_360 = self.set_lng_360(self.lng)
        lng_std_360 = self.set_lng_360(self.lng_std)

        # displacement from standard meridian for that longitude
        delta_std_meridian = timedelta(minutes=(4 * (lng_std_360 - lng_360)))

        # eq. of time for that day
        e_param = timedelta(minutes=sp.eq_time(self.datetime))
        t_solar = t_std + delta_std_meridian + e_param
        return t_solar

    @staticmethod
    def set_lng_360(lng_input):
        if lng_input < 0:
            return abs(lng_input)
        elif 0 < lng_input < 180:
            return lng_input + 180
