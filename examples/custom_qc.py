import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# File reading
file_df = pd.read_csv("../data/2022-minute-raw.csv", sep=";")
file_df['fecha'] = pd.to_datetime(file_df['fecha'], format="%d/%m/%Y %H:%M")
file_df.sort_values(by=["fecha"], inplace=True)
file_df.reset_index(inplace=True)

# ---------- Checking timestamps integrity ----------
complete_timestamps = set(pd.date_range(start=f"2022-01-01 00:00", end=f"2022-12-31 23:59", freq="min"))
file_timestamps = set(file_df.fecha)

# Checking for missing timestamps
missing_timestamps = complete_timestamps.difference(file_timestamps)
print(f"Found {len(missing_timestamps)} missing of {len(complete_timestamps)} timestamps"
      f" ({len(missing_timestamps)/len(complete_timestamps)* 100:.2f}%)")

# Checking for repeated timestamps
repeated_timestamps = file_df[file_df["fecha"].duplicated()]
print(f"Found {len(repeated_timestamps)} repeated timestamps"
      f" ({len(repeated_timestamps)/len(file_df['fecha']):.2f}%)")
missing_df = pd.DataFrame({"fecha": list(missing_timestamps), "ILGLO": np.nan, "IRGLO": np.nan, "ILDIF": np.nan,
                           "IRDIF": np.nan}, index=list(missing_timestamps))
full_df = pd.concat([file_df, missing_df]).sort_values(by=["fecha"])
full_df.reset_index()

# ----------

