import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from lebaron.shadowband import *

'''
Script para corregir los datos de radiación difusa tomados con banda de sombra. Se emplea LeBaron para la corrección.
'''

# Parametro para medir el tiempo de corrida del programa
tic = datetime.now()

# Parámetros de geolocalización
latitud = -32.898   # Latitud del lugar (de -90 a 90, sur negativo)
longitud = -68.875  # Longitud del lugar (de -180 a 180, oeste negativo)
longitud_std = -45  # Longitud estándar (de -180 a 180, oeste negativo). Longitud del meridiano del lugar de referencia
altitud = 842  # msnm
b = 7.5  # Ancho de la banda (cm)
r = 30.8  # Radio de la banda (cm)

# Carga del archivo a analizar
file_path = f"../data/2022-minute-raw.csv"
file_df = pd.read_csv(file_path, sep=";")
# Parseo y reordenamiento del archivo cargado
# file_df["fecha"] = file_df.fecha.map(lambda fecha: pd.to_datetime(fecha, format="%d/%m/%Y %H:%M"))
file_df['fecha'] = pd.to_datetime(file_df['fecha'], format="%d/%m/%Y %H:%M")
file_df.sort_values(by=["fecha"], inplace=True)
file_df.reset_index(inplace=True)

# Cálculo de coeficietes de corrección de difusa por medio de LeBaron
measurements_list = [SolarMeasurement(date, ghi, dif, lat=latitud, lng=longitud, lng_std=longitud_std, altitude=altitud,
                                      shadowband_width=b, shadowband_radius=r) for date, ghi, dif
                     in zip(file_df["fecha"], file_df["IRGLO"], file_df["IRDIF"])]
lebaron_list = [solar_measurement.dif_correction_factor for solar_measurement in measurements_list]
corrected_dif = pd.Series(lebaron_list) * file_df["IRDIF"]
corrected_dif = [value if np.isnan(corrected_dif[index]) else corrected_dif[index] for index, value in
                 enumerate(file_df["IRDIF"])]

# Plot
# plt.plot(file_df["IRDIF"])
# plt.plot(corrected_dif)
# plt.show()

file_df["IRDIFc"] = corrected_dif
file_df.to_csv("2022-minute-dif_corrected.csv")

# measurements_series = pd.Series(map(lambda date, ghi, dif: SolarMeasurement(date, ghi, dif, lat=latitud, lng=longitud,
#                                                                             lng_std=longitud_std, altitude=altitud,
#                                                                             shadowband_width=b, shadowband_radius=r),
#                                     file_df["fecha"], file_df["IRGLO"], file_df["IRDIF"]))
# lebaron_series = measurements_series.map(lambda measurement: measurement.dif_correction_factor)

# # Límites físicos y extremadamente raros
# ghi = file_df.loc[:, ["fecha", "IRGLO", "solartime"]]
# dhi = file_df.loc[:, ["fecha", "IRDIF", "solartime"]]
# factor_series = pd.Series(map(lambda gon_value, theta_z_value: gon_factor(gon_value, theta_z_value), gon_series,
#                               zenith_angle_series_rad))
# ghi["upper_physical_limit"] = 1.5 * factor_series + 100
# ghi["upper_extreme_limit"] = 1.2 * factor_series + 50
# dhi["upper_physical_limit"] = 0.95 * factor_series + 50
# dhi["upper_extreme_limit"] = 0.75 * factor_series + 30
# physical_lower_limit = -4
# extreme_lower_limit = -2
# ghi.index = ghi.fecha
# dhi.index = dhi.fecha

# Fin del programa: se ejecuta parte final para conteo de corrida
toc = datetime.now()
run_time = toc - tic
print(f"Runtime: {run_time}")
