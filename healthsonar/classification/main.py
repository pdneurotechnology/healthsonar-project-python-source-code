# %%

from pathlib import Path

import features as features
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# =============================================================================

plt.style.use("dark_background")

data_path = Path("/home/adam/Datasets/healthsonar-patients/")

rsps = ["PAT001_RSP.npy"]
event_files = ["HSP001.csv"]
folders = ["PAT001"]

#
#


for folder, event in zip(folders, event_files):
    chest = np.loadtxt(Path(data_path, "data", folder, "chest.txt"))
    event_df = pd.read_csv(Path(data_path, "data", "events", event))

    durations = event_df["duration"].values
    labels = event_df["label"].values

    data_new = features.feature_extraction_rsp(
        "DATA", chest, labels, durations
    )

    np.save(str(Path(data_path, "data", folder, folder + "_RSP")), data_new)
    print(f"> Finished RSP features for patient: {folder}")

#
#

cols = [
    "entropy",
    "n05",
    "n25",
    "n75",
    "n95",
    "median",
    "mean",
    "std",
    "var",
    "rms",
    "sk",
    "kur",
    "no_zero_crossings",
    "no_mean_crossings",
    "peak frequency",
]

for folder, rsp in zip(folders, rsps):
    data_rsp = np.load(str(Path(data_path, "data", folder, rsp)))
    rsp_df = pd.DataFrame.from_records(
        data_rsp.reshape(
            (data_rsp.shape[0], data_rsp.shape[1] * data_rsp.shape[2])
        )
    )

    rsp_df.columns = cols
    rsp_df["event"] = event_df["label"].values

# %%

# plt.plot(chest[100000:110000])
# plt.show()

# %%

# rsp_df
# %%

for col in cols:
    print(col)
    plt.scatter(x=rsp_df.index, y=rsp_df[col], marker="x")
    plt.show()
