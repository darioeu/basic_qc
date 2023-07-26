import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
from qcontrol import *
from shadowband import *

'''
Script para control de calidad (Quality Control) básico de datos solares.
Este script puede:
    -Verificar integridad de los datos (Que no existan periodos donde no se haya hecho la adquisición de datos)
'''
# Parametro para medir el tiempo de corrida del programa
tic = datetime.now()

# Parámetros de geolocalización
latitud = -32.898
longitud = -68.875
longitud_std = -45  # Longitud estándar 0 a 360 hacia el oeste (Longitud del lugar de referencia)
altitud = 842  # msnm
b = 7.5  # Ancho de la banda (cm)
r = 30.8  # Radio de la banda (cm)

# Carga del archivo a analizar
file_path = f"data/2022-minute.csv"
file_df = pd.read_csv(file_path, sep=";")
# Parseo y reordenamiento del archivo cargado
file_df['fecha'] = pd.to_datetime(file_df['fecha'], format="%d/%m/%Y %H:%M")
file_df["solartime"] = [standard2solar_time_modified(date, lng=abs(longitud),
                                                     lng_std=abs(longitud_std)) for date in file_df.fecha]
file_df.sort_values(by=["fecha"], inplace=True)
file_df.reset_index(inplace=True)

# Cálculo de coeficietes de corrección de difusa por medio de LeBaron
# measurements = [SolarMeasurement(date, ghi, dif, latitud, longitud, longitud_std, altitud, b, r) for date, ghi, dif in
#                 zip(file_df["fecha"], file_df["IRGLO"], file_df["IRDIF"])]
measurements_series = pd.Series(map(lambda date, ghi, dif: SolarMeasurement(date, ghi, dif, lat=latitud, lng=longitud,
                                                                            lng_std=longitud_std, altitude=altitud,
                                                                            shadowband_width=b, shadowband_radius=r),
                                    file_df["fecha"], file_df["IRGLO"], file_df["IRDIF"]))
# lebaron_list = [lebaron(measurement) for measurement in measurements]
lebaron_series = pd.Series(map(lambda measurement: lebaron(measurement), measurements_series))

# ---------- Control de calidad ----------

# Chequeo de la integridad de los timestamp
# complete_timestamps = set(pd.date_range(start=f"{year}-01-01 00:00", end=f"{year}-12-31 23:59", freq="min"))
# file_timestamps = set(file_df.fecha)
# missing_timestamps = complete_timestamps.difference(file_timestamps)
# print(f"Faltan {len(missing_timestamps)} de {len(complete_timestamps)} timestamps")
# missing_df = pd.DataFrame({"fecha": list(missing_timestamps), "ILGLO": np.nan, "IRGLO": np.nan, "ILDIF": np.nan,
#                            "IRDIF": np.nan}, index=list(missing_timestamps))
# full_df = pd.concat([file_df, missing_df]).sort_values(by=["fecha"])
# full_df.reset_index()

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
