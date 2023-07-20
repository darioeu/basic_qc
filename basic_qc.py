import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import solarpy as sp
from lebaron import lebaron

'''
Script para control de calidad (Quality Control) básico de datos solares.
Este script puede:
    -Verificar integridad de los datos (Que no existan periodos donde no se haya hecho la adquisición de datos)
'''
# Parametro para medir el tiempo de corrida del programa
tic = datetime.now()


def gon_factor(gon_value, theta_z_value):
    return gon_value * (np.cos(theta_z_value)) ** 1.2


def dir_nu(glo_h, dif_hu, theta_z_value):
    dir_nu_value = (glo_h - dif_hu) / np.cos(theta_z_value)
    return dir_nu_value


def epsilon(dif_hu, dni_value, date):
    sunrise = sp.sunrise_time(date, latitud)
    sunset = sp.sunset_time(date, latitud)
    if sunrise < date < sunset:
        epsilon_value = (dif_hu + dni_value) / dif_hu
    else:
        epsilon_value = np.nan
    return epsilon_value


def delta(dif_hu, theta_z_value, gon_value):
    delta_value = dif_hu * sp.air_mass_kastenyoung1989(np.rad2deg(theta_z_value), altitud) / gon_value
    return delta_value


def c_i_original(date):
    phi = np.deg2rad(latitud)
    t_0 = sp.sunset_hour_angle(date, latitud)
    italic_delta = sp.declination(date)
    c_i_value = 1 / (1 - (2 * b) / (np.pi * r) * ((np.cos(italic_delta)) ** 3) * (
            np.sin(phi) * np.sin(italic_delta * t_0) + np.cos(phi) * np.cos(italic_delta) * np.sin(t_0)))
    return c_i_value


def cut(zenith_angle_input, geometric_input, epsilon_input, delta_input):
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

    # displacement from standard meridian for that longitude
    delta_std_meridian = timedelta(minutes=(4 * (lng_std - lng)))

    # eq. of time for that day
    e_param = timedelta(minutes=sp.eq_time(date))
    t_solar = t_std + delta_std_meridian + e_param

    return t_solar


# Parámetros de geolocalización
year = 2021
latitud = -32.898
longitud = -68.875
altitud = 842  # msnm
b = 7.5  # Ancho de la banda (cm)
r = 30.8  # Radio de la banda (cm)

# Carga del archivo a analizar
file_path = f"data/{year}-minute-raw.csv"
file_df = pd.read_csv(file_path, sep=";")
file_df['fecha'] = pd.to_datetime(file_df['fecha'], format="%d/%m/%Y %H:%M")
file_df["solartime"] = [standard2solar_time_modified(date, lng=abs(longitud), lng_std=45) for date in file_df.fecha]
file_df.sort_values(by=["fecha"], inplace=True)
file_df.reset_index(inplace=True)

# Chequeo de la integridad de los timestamp
# complete_timestamps = set(pd.date_range(start=f"{year}-01-01 00:00", end=f"{year}-12-31 23:59", freq="min"))
# file_timestamps = set(file_df.fecha)
# missing_timestamps = complete_timestamps.difference(file_timestamps)
# print(f"Faltan {len(missing_timestamps)} de {len(complete_timestamps)} timestamps")
# missing_df = pd.DataFrame({"fecha": list(missing_timestamps), "ILGLO": np.nan, "IRGLO": np.nan, "ILDIF": np.nan,
#                            "IRDIF": np.nan}, index=list(missing_timestamps))
# full_df = pd.concat([file_df, missing_df]).sort_values(by=["fecha"])
# full_df.reset_index()

# Cálculo LeBaron

# zenith_angle_series_rad = [sp.theta_z(date, lat=latitud) for date in file_df.solartime]
# gon_series = [sp.gon(date) for date in file_df.solartime]
# dni_series = [dir_nu(irglo, irdif, theta_z_value) for irglo, irdif, theta_z_value in zip(file_df.IRGLO, file_df.IRDIF,
#                                                                                          zenith_angle_series_rad)]
# epsilon_series = [epsilon(irdif, dni_value, date) for irdif, dni_value, date in zip(file_df.IRDIF, dni_series,
#                                                                                     file_df.solartime)]
# delta_series = [delta(irdif, theta_z_value, gon_value) for irdif, theta_z_value, gon_value in
#                 zip(file_df.IRDIF, zenith_angle_series_rad, gon_series)]
# c_i_series = [c_i(date) for date in file_df.solartime]

# dff = pd.DataFrame({"theta_z": zenith_angle_series_rad, "gon": gon_series, "dni": dni_series, "epsilon": epsilon_series,
#                     "delta": delta_series, "c_i": c_i_series})

zenith_angle_series_rad = file_df.solartime.apply(lambda date: sp.theta_z(date, lat=latitud))
zenith_angle_series_deg = np.rad2deg(zenith_angle_series_rad)
gon_series = file_df.solartime.apply(sp.gon)
dni_series = pd.Series(map(lambda irglo, irdif, theta_z_value: dir_nu(irglo, irdif, theta_z_value),
                           file_df.IRGLO, file_df.IRDIF, zenith_angle_series_rad))
epsilon_series = pd.Series(map(lambda irdif, dni_value, date: epsilon(irdif, dni_value, date), file_df.IRDIF,
                               dni_series, file_df.solartime))
delta_series = pd.Series(map(lambda irdif, theta_z_value, gon_value: delta(irdif, theta_z_value, gon_value),
                             file_df.IRDIF, zenith_angle_series_rad, gon_series))
c_i_series = file_df.solartime.apply(c_i_original)
sunrise_time_series = pd.Series(map(lambda date: sp.sunrise_time(date, lat=latitud), file_df.solartime))

cuts = pd.Series(map(lambda aa, bb, cc, dd: cut(aa, bb, cc, dd), zenith_angle_series_deg, c_i_series, epsilon_series,
                     delta_series))
correction_value = [lebaron(cut) for cut in cuts]

file_df["zenith_angle"] = zenith_angle_series_deg
file_df["sunrise_time"] = sunrise_time_series
file_df["epsilon"] = epsilon_series

ghi = file_df.loc[:, ["fecha", "IRGLO", "solartime"]]
dhi = file_df.loc[:, ["fecha", "IRDIF", "solartime"]]

# Límites físicos y extremadamente raros
factor_series = pd.Series(map(lambda gon_value, theta_z_value: gon_factor(gon_value, theta_z_value), gon_series,
                              zenith_angle_series_rad))
ghi["upper_physical_limit"] = 1.5 * factor_series + 100
ghi["upper_extreme_limit"] = 1.2 * factor_series + 50
dhi["upper_physical_limit"] = 0.95 * factor_series + 50
dhi["upper_extreme_limit"] = 0.75 * factor_series + 30
physical_lower_limit = -4
extreme_lower_limit = -2
ghi.index = ghi.fecha
dhi.index = dhi.fecha

# Límites de comparación


# # Ploteo GHI
# plt.plot(ghi.IRGLO, "k")
# plt.plot(ghi.upper_extreme_limit, "g-")
# plt.plot(ghi.upper_physical_limit, "r-")
# plt.legend(["GHI medida", "Límite extremo", "Límite físico"])
# plt.show()

# # Ploteo DHI
# plt.plot(dhi.IRDIF, "c")
# plt.plot(dhi.upper_extreme_limit, "g-")
# plt.plot(dhi.upper_physical_limit, "r-")
# plt.legend(["DHI medida", "Límite extremo", "Límite físico"])
# plt.show()

# Fin del programa: se ejecuta parte final para conteo de corrida
toc = datetime.now()
run_time = toc - tic
print(f"Runtime: {run_time}")
