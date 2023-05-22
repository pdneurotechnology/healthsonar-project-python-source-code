import json
from datetime import datetime

import numpy as np
import pandas as pd

event_files = [
    "HSP007_Events.txt",
    "HSP010_Events.txt",
    "HSP011_Events.txt",
    "HSP001_Events.txt",
    "HSP002_Events.txt",
    "HSP003_Events.txt",
    "HSP004_Events.txt",
    "HSP006_Events.txt",
    "HSP008_Events.txt",
    "HSP009_Events.txt",
    "HSP014_Events.txt",
]

for file in event_files:
    print(file)

    events = pd.read_csv(file, encoding="latin-1", sep="\t")
    events["TimeStart"] = (
        events["Time [hh:mm:ss]"]
        .apply(lambda x: x.split(" ")[0])
        .apply(pd.to_datetime)
    )
    events["TimeStart"] = events["TimeStart"].apply(
        lambda x: x + pd.to_timedelta(12, unit="h") if x.hour < 10 else x
    )
    events["TimeEnd"] = events.TimeStart + pd.to_timedelta(
        events["Duration[s]"], unit="s"
    )

    sorted_df = events.sort_values(by=["TimeStart", "TimeEnd"]).copy()

    labels = [
        "Apnea",
        "Apnea Central",
        "Apnea Mixed",
        "Apnea Obstructive",
        "Apnea Arousal",
        "Hypopnea",
        "Hypopnea Central",
        "Hypopnea Mixed",
        "Hypopnea Obstructive",
        "W",
        "N1",
        "N2",
        "N3",
        "R",
    ]

    df = sorted_df[sorted_df["Event"].isin(labels)].copy()

    first_date = df.iloc[0, -2]
    last_date = df.iloc[-1, -2]
    dates, lengs, temps = [], [], []
    starts_new = []
    labels_new = []
    durations_new = []

    flag = False

    for start in pd.date_range(first_date, last_date, freq="30s"):
        temp = df[
            (df["TimeStart"] >= start)
            & (df["TimeStart"] < start + pd.to_timedelta(30, unit="s"))
        ]

        labels_temp = temp.Event.values

        if len(temp) > 1:
            slots = temp.TimeStart.diff().values / np.timedelta64(1, "s")

            if flag:
                labels_new.append(labels_temp[0] + "-" + label_before)

                starts_new.append(end_before)
                labels_new.append(temp["Event"].values[0])
                durations_new.append(
                    temp["Duration[s]"].values[0] - duration_before
                )
                flag = False

            else:
                labels_new.append(labels_temp[0])
                durations_new.append(slots[1])
                starts_new.append(start)

            labels_new.append("-".join(labels_temp))
            slots2 = temp.TimeEnd.diff().values / np.timedelta64(1, "s")

            if slots2[1] < 0:
                durations_new.append(temp["Duration[s]"].values[1])
                starts_new.append(temp["TimeStart"].values[1])
                durations_new.append(abs(slots[1]))
                starts_new.append(temp["TimeEnd"].values[1])
                labels_new.append(labels_temp[0])
                flag = False

            else:
                starts_new.append(temp["TimeStart"].values[1])
                durations_new.append(temp["Duration[s]"].values[1] - slots2[1])
                flag = True
                label_before = labels_temp[1]
                duration_before = slots2[1]
                start_before = temp["TimeEnd"].values[0]
                end_before = temp["TimeEnd"].values[1]
                starts_new.append(start_before)
                durations_new.append(slots2[1])

        else:
            if flag:
                labels_new.append(labels_temp[0] + "-" + label_before)

                starts_new.append(end_before)
                labels_new.append(temp["Event"].values[0])
                durations_new.append(
                    temp["Duration[s]"].values[0] - duration_before
                )
                flag = False

            else:
                starts_new.append(temp["TimeStart"].values[0])
                labels_new.append(temp["Event"].values[0])
                durations_new.append(temp["Duration[s]"].values[0])

    filename = f"{file.split('_')[0]}_Starts_New.json"

    pd.DataFrame(
        {"label": labels_new, "duration": [int(i) for i in durations_new]}
    ).to_csv(f"{file.split('_')[0]}.csv")
