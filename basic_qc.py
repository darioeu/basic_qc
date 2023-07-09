import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import solarpy as sp

'''
Script para control de calidad (Quality Control) básico de datos solares.
Este script puede:
    -Verificar integridad de los datos (Que no existan periodos donde no se haya hecho la adquisición de datos)
'''
# Parametric para medir el tiempo de corrida del programa
tic = datetime.now()


def gon_factor(gon_value, theta_z_value):
    return gon_value * (np.cos(theta_z_value)) ** 1.2


def dir_nu(glo_h, dif_hu, theta_z_value):
    dir_nu_value = (glo_h - dif_hu) / np.cos(theta_z_value)
    return dir_nu_value


def epsilon(dif_hu, dni_value):
    epsilon_value = (dif_hu + dni_value) / dif_hu
    return epsilon_value


def delta(dif_hu, theta_z_value, gon_value):
    delta_value = dif_hu * sp.air_mass_kastenyoung1989(np.rad2deg(theta_z_value), altitud) / gon_value
    return delta_value


def c_i(date):
    phi = np.deg2rad(latitud)
    t_0 = sp.sunset_hour_angle(date, latitud)
    italic_delta = sp.declination(date)
    c_i_value = 1 / (1 - (2 * b) / (np.pi * r) * ((np.cos(italic_delta)) ** 3) * (
                np.sin(phi) * np.sin(italic_delta * t_0) + np.cos(phi) * np.cos(italic_delta) * np.sin(t_0)))
    return c_i_value


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
latitud = -32.898
longitud = -68.875
altitud = 842
b = 7.5  # Ancho de la banda
r = 30.8  # Radio de la banda
# Carga del archivo a analizar
file_path = "../2022-minute-raw.csv"
file_df = pd.read_csv(file_path, sep=";")
file_df['fecha'] = pd.to_datetime(file_df['fecha'], format="%d/%m/%Y %H:%M")
file_df["solartime"] = [standard2solar_time_modified(date, lng=abs(longitud), lng_std=45) for date in file_df.fecha]
file_df.sort_values(by=["fecha"], inplace=True)

# Chequeo de la integridad de los timestamp
complete_timestamps = set(pd.date_range(start="2022-01-01 00:00", end="2022-12-31 23:59", freq="min"))
file_timestamps = set(file_df.fecha)
missing_timestamps = complete_timestamps.difference(file_timestamps)
print(f"Faltan {len(missing_timestamps)} de {len(complete_timestamps)} timestamps")
missing_df = pd.DataFrame(
    {"fecha": list(missing_timestamps), "ILGLO": np.nan, "IRGLO": np.nan, "ILDIF": np.nan, "IRDIF": np.nan},
    index=list(missing_timestamps))
full_df = pd.concat([file_df, missing_df]).sort_values(by=["fecha"])
full_df.index = range(len(file_df) + len(missing_timestamps))

# Cálculo LeBaron
theta_z = [sp.theta_z(date, latitud) for date in file_df.solartime]  # Ángulo cenital
gon = [sp.gon(date) for date in file_df.solartime]  # Io: Irradiancia extraterrestre
dni = [dir_nu(irglo, irdif, theta_z_value) for irglo, irdif, theta_z_value in
       zip(file_df.IRGLO, file_df.IRDIF, theta_z)]
epsilon = [epsilon(irdif, dni_value) for irdif, dni_value in zip(file_df.IRDIF, dni)]
delta = [delta(irdif, theta_z_value, gon_value) for irdif, theta_z_value, gon_value in zip(file_df.IRDIF, theta_z, gon)]
c_i = [c_i(date) for date in file_df.solartime]

ghi = file_df.loc[:, ["fecha", "IRGLO", "solartime"]]
dhi = file_df.loc[:, ["fecha", "IRDIF", "solartime"]]

# Límites físicos y extremadamente raros
factor = np.array([gon_factor(gon_value, theta_z_value) for gon_value, theta_z_value in zip(gon, theta_z)])
ghi["upper_physical_limit"] = 1.5 * factor + 100
ghi["upper_extreme_limit"] = 1.2 * factor + 50
dhi["upper_physical_limit"] = 0.95 * factor + 50
dhi["upper_extreme_limit"] = 0.75 * factor + 30
physical_lower_limit = -4
extreme_lower_limit = -2
ghi.index = ghi.fecha
dhi.index = ghi.fecha

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
