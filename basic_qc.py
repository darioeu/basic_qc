import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from utils import *

'''
Script para control de calidad (Quality Control) básico de datos solares.
Este script puede:
    -Verificar integridad de los datos (Que no existan periodos donde no se haya hecho la adquisición de datos)
'''
# Parametro para medir el tiempo de corrida del programa
tic = datetime.now()


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
# dff = pd.DataFrame({"theta_z": zenith_angle_series_rad, "gon": gon_series, "dni": dni_series,
#                     "epsilon": epsilon_series, "delta": delta_series, "c_i": c_i_series})

zenith_angle_series_rad = file_df.solartime.apply(lambda date: sp.theta_z(date, lat=latitud))
zenith_angle_series_deg = np.rad2deg(zenith_angle_series_rad)
gon_series = file_df.solartime.apply(sp.gon)
dni_series = pd.Series(map(lambda irglo, irdif, theta_z_value: dir_nu(irglo, irdif, theta_z_value),
                           file_df.IRGLO, file_df.IRDIF, zenith_angle_series_rad))
epsilon_series = pd.Series(map(lambda irdif, dni_value, date: epsilon(irdif, dni_value, date, latitud), file_df.IRDIF,
                               dni_series, file_df.solartime))
delta_series = pd.Series(map(lambda irdif, theta_z_value, gon_value: delta(irdif, theta_z_value, gon_value, altitud),
                             file_df.IRDIF, zenith_angle_series_rad, gon_series))
c_i_series = pd.Series(map(lambda date: c_i_original(date, latitud=latitud, shadowband_width=b, shadowband_radius=r),
                           file_df.solartime))
sunrise_time_series = pd.Series(map(lambda date: sp.sunrise_time(date, lat=latitud), file_df.solartime))

cuts = pd.Series(map(lambda aa, bb, cc, dd: cut(aa, bb, cc, dd), zenith_angle_series_deg, c_i_series, epsilon_series,
                     delta_series))
correction_series = pd.Series(map(lambda cut_input: lebaron(cut_input), cuts))
dif_corrected = file_df.IRDIF * correction_series

# Límites físicos y extremadamente raros
ghi = file_df.loc[:, ["fecha", "IRGLO", "solartime"]]
dhi = file_df.loc[:, ["fecha", "IRDIF", "solartime"]]
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

# Fin del programa: se ejecuta parte final para conteo de corrida
toc = datetime.now()
run_time = toc - tic
print(f"Runtime: {run_time}")
