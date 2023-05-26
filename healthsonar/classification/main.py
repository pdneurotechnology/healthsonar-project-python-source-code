# %%

from pathlib import Path

import features as features
import numpy as np
import pandas as pd

# =============================================================================

data_path = Path("/home/adam/Datasets/healthsonar-patients/")

rsps = ["PAT001_RSP.npy"]
event_files = ["HSP001.csv"]
folders = ["PAT001"]


for folder, event in zip(folders, event_files):
    chest = np.loadtxt(Path(data_path, "psg", folder, "chest.txt"))
    df = pd.read_csv(Path(data_path, "psg", "Events", event))

    durations = df["duration"].values
    labels = df["label"].values

    data_new = features.feature_extraction_rsp(
        "DATA", chest, labels, durations
    )

    np.save(str(Path(data_path, folder + "_RSP")), data_new)
    print(f"Finished RSP features for patient: {folder}")

df = pd.DataFrame()

# for ecg, rsp, label in zip(ecgs, rsps, labels):
#     data = np.load(ecg)
#     temp_df = pd.DataFrame.from_records(
#         data.reshape((data.shape[0], data.shape[1] * data.shape[2]))
#     )

#     data_rsp = np.load(rsp)
#     temp_rsp_df = pd.DataFrame.from_records(
#         data_rsp.reshape(
#             (data_rsp.shape[0], data_rsp.shape[1] * data_rsp.shape[2])
#         )
#     )

#     labels_df = pd.read_csv(label)

#     temp = pd.concat([temp_df, temp_rsp_df], axis=1)
#     temp["label"] = labels_df["label"]
#     df = df.append(temp)

# df.to_csv("data_all.csv", index=False)
