# %%

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# %%
# Set up plotting.
# =============================================================================

sns.set(
    # rc={
    #     "figure.dpi": 300,
    #     "savefig.dpi": 300,
    # },
    style="ticks",
)

plt.style.use("dark_background")

# %%
# Load data.
# =============================================================================

# Path of the folder storing the compared data.
data_path = Path("/home/adam/Datasets/healthsonar-patients/cmp")

# Load the radar data and label the columns.
radar_data = pd.read_csv(
    Path(data_path, "005_radar_resp.csv"),
    names=["Timestamp", "Respiration"],
    sep=";",
)

# Convert the Unix timestamps to a different format.
radar_data["Timestamp"] = pd.to_datetime(radar_data["Timestamp"], unit="ms")

# Load the psg data.
psg_data = pd.read_csv(
    Path(data_path, "005_psg_resp.csv"),
    header=0,
    names=["Respiration"],
    sep=";",
)

# %%
# Data cleaning.
# =============================================================================

filter = radar_data.loc[:, "Respiration"] > -10000
radar_data = radar_data.loc[filter, :]

# %%
# Examine the data.
# =============================================================================

run = True

if run:
    a = 0
    b = -1

    x = radar_data["Timestamp"][a:b]
    y = radar_data["Respiration"][a:b]

    plt.plot(y)
    plt.xticks(rotation=30)
    plt.show()

    #
    #

    x = psg_data["Respiration"][a:b]

    plt.plot(x)
    plt.show()

    #
    #

    plt.hist(radar_data["Respiration"], bins=10)
    plt.show()

    plt.hist(psg_data["Respiration"], bins=10)
    plt.show()

# %%

# radar_data = radar_data[radar_data.index % 2 == 0]

a = radar_data["Respiration"]
print(a.describe().to_string())

print("\n")

b = psg_data["Respiration"]
print(b.describe().to_string())
