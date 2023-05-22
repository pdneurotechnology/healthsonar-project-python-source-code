import numpy as np
import pandas as pd


def calculate_entropy(list_values):
    counter_values = Counter(list_values).most_common()
    probabilities = [elem[1] / len(list_values) for elem in counter_values]
    entropy = scipy.stats.entropy(probabilities)

    return entropy


def calculate_statistics(list_values):
    n5 = np.nanpercentile(list_values, 5)
    n25 = np.nanpercentile(list_values, 25)
    n75 = np.nanpercentile(list_values, 75)
    n95 = np.nanpercentile(list_values, 95)
    median = np.nanpercentile(list_values, 50)
    mean = np.nanmean(list_values)
    std = np.nanstd(list_values)
    var = np.nanvar(list_values)
    rms = np.nanmean(np.sqrt(list_values**2))
    sk = skew(list_values)
    kur = kurtosis(list_values)

    return [n5, n25, n75, n95, median, mean, std, var, rms, sk, kur]


def calculate_crossings(list_values):
    no_zero_crossings = sum(np.diff(np.array(list_values) > 0, prepend=False))
    no_mean_crossings = sum(
        np.diff(np.array(list_values) > np.mean(list_values), prepend=False)
    )

    return [no_zero_crossings, no_mean_crossings]


def get_features_rsp(list_values):
    entropy = calculate_entropy(list_values)
    crossings = calculate_crossings(list_values)
    statistics = calculate_statistics(list_values)

    return [entropy] + crossings + statistics


def feature_extraction_rsp(recording, abn, chest, labels, durations):
    lengths = []
    fs = 32
    data = []
    labels_list = []
    for i, label in tqdm(enumerate(labels)):
        prev = 0

        try:
            segment = abn[prev : fs * durations[i - 1]]
            rsp = nk.signal_filter(segment, highcut=30)
            rsp_features_abn = get_features_rsp(rsp)
            segment = chest[prev : fs * durations[i - 1]]
            rsp = nk.signal_filter(segment, highcut=30)
            rsp_features_chest = get_features_rsp(rsp)
            data.append([rsp_features_abn, rsp_features_chest])
            prev = durations[i - 1]
            # print(data.shape)

        except ValueError:
            # print(i)
            data.append([[np.nan] * 14, [np.nan] * 14])
    data = np.array(data, dtype="float")

    return data


def calculate_entropies(segment):
    shannon = [EH.CondEn(segment)[1][0], EH.CondEn(segment)[2][0]]
    bubble = list(EH.BubbEn(segment)[0][0] + EH.BubbEn(segment)[1])
    attn = [EH.AttnEn(segment)[0]]
    dispersion = [i for i in EH.DispEn(segment)]

    return shannon + bubble + attn + dispersion


def create_features(segment):
    fs = 256  # ECG sample frequency
    hr_min = 20
    hr_max = 300
    data = []

    try:
        segment, _, _ = st.filter_signal(
            segment,
            ftype="FIR",
            band="bandpass",
            order=int(0.3 * fs),
            frequency=[3, 45],
            sampling_rate=fs,
        )

    except:
        data.append([np.nan] * 26)

        return data

    # Finding R peaks
    (rpeaks,) = hamilton_segmenter(segment, sampling_rate=fs)
    (rpeaks,) = correct_rpeaks(segment, rpeaks, sampling_rate=fs, tol=0.1)

    # Extracting feature
    # label = 0 if labels[i] == "N" else 1
    # if 40 <= len(rpeaks) <= 200:  # Remove abnormal R peaks
    rri_tm, rri = rpeaks[1:] / float(fs), np.diff(rpeaks, axis=-1) / float(fs)
    rri = medfilt(rri, kernel_size=3)
    edr_tm, edr = rpeaks / float(fs), segment[rpeaks]

    # Remove physiologically impossible HR signal
    if np.all(np.logical_and(60 / rri >= hr_min, 60 / rri <= hr_max)):
        entr = calculate_entropies(segment)

        try:
            rri_time_features, rri_frequency_features = time_domain(
                rri * 1000
            ), frequency_domain(rri, rri_tm)
            edr_frequency_features = frequency_domain(edr, edr_tm)
            data.append(
                [
                    rri_time_features["rmssd"],
                    rri_time_features["sdnn"],
                    rri_time_features["nn50"],
                    rri_time_features["pnn50"],
                    rri_time_features["mrri"],
                    rri_time_features["mhr"],
                    rri_frequency_features["vlf"]
                    / rri_frequency_features["total_power"],
                    rri_frequency_features["lf"]
                    / rri_frequency_features["total_power"],
                    rri_frequency_features["hf"]
                    / rri_frequency_features["total_power"],
                    rri_frequency_features["lf_hf"],
                    rri_frequency_features["lfnu"],
                    rri_frequency_features["hfnu"],
                    edr_frequency_features["vlf"]
                    / edr_frequency_features["total_power"],
                    edr_frequency_features["lf"]
                    / edr_frequency_features["total_power"],
                    edr_frequency_features["hf"]
                    / edr_frequency_features["total_power"],
                    edr_frequency_features["lf_hf"],
                    edr_frequency_features["lfnu"],
                    edr_frequency_features["hfnu"]
                    # label
                ]
            )
            # labels_list.append(label)

        except:
            data.append([np.nan] * 26)
            # labels_list.append("Nan")

    else:
        data.append([np.nan] * 26)
        # labels_list.append("Nan")

    return data


def feature_extraction_new(
    recording,
    lead_1,
    lead_2,
    lead_3,
    lead_aVR,
    lead_aVL,
    lead_VF,
    labels,
    durations,
):
    data = []
    labels_list = []
    prev = 0

    for i, label in tqdm(enumerate(labels)):
        # for i in tqdm(range(len(labels)), desc=recording, file=sys.stdout):
        a = lead_1[prev : fs * durations[i - 1]]
        a = create_features(a)
        b = lead_1[prev : fs * durations[i - 1]]
        b = create_features(b)
        c = lead_1[prev : fs * durations[i - 1]]
        c = create_features(c)
        d = lead_1[prev : fs * durations[i - 1]]
        d = create_features(d)
        e = lead_1[prev : fs * durations[i - 1]]
        e = create_features(e)
        f = lead_1[prev : fs * durations[i - 1]]
        f = create_features(f)
        data.append([a, b, c, d, e, f])
        labels_list.append(label)
        prev = durations[i - 1]
    data = np.array(data, dtype="float")

    return data


ecgs = [
    "PAT 001.npy",
    "PAT 002.npy",
    "PAT 003.npy",
    "PAT 004.npy",
    "PAT 006.npy",
    "PAT 007.npy",
    "PAT 008.npy",
    "PAT 009.npy",
    "PAT 0010.npy",
    "PAT 0011.npy",
    "PAT 0014.npy",
]

rsps = [
    "PAT 001_RSP.npy",
    "PAT 002_RSP.npy",
    "PAT 003_RSP.npy",
    "PAT 004_RSP.npy",
    "PAT 006_RSP.npy",
    "PAT 007_RSP.npy",
    "PAT 008_RSP.npy",
    "PAT 009_RSP.npy",
    "PAT 0010_RSP.npy",
    "PAT 0011_RSP.npy",
    "PAT 0014_RSP.npy",
]

event_files = [
    "HSP001.csv",
    "HSP002.csv",
    "HSP003.csv",
    "HSP004.csv",
    "HSP006.csv",
    "HSP007.csv",
    "HSP008.csv",
    "HSP009.csv",
    "HSP010.csv",
    "HSP011.csv",
    "HSP014.csv",
]

fs = 256

folders = [
    "PAT 001",
    "PAT 002",
    "PAT 003",
    "PAT 004",
    "PAT 006",
    "PAT 007",
    "PAT 008",
    "PAT 009",
    "PAT 0010",
    "PAT 0011",
    "PAT 0014",
]


for folder, event in zip(folders, event_files):
    la = np.loadtxt(f"{folder}/ECG-LA.txt", skiprows=5)
    ll = np.loadtxt(f"{folder}/ECG-LL.txt", skiprows=5)
    ra = np.loadtxt(f"{folder}/ECG-RA.txt", skiprows=5)
    v1 = np.loadtxt(f"{folder}/ECG-V1.txt", skiprows=5)
    v2 = np.loadtxt(f"{folder}/ECG-V2.txt", skiprows=5)
    lead_1 = la - ra
    lead_2 = ll - ra
    lead_3 = ll - la
    lead_aVR = ra - (0.5) * (la + ll)
    lead_aVL = la - (0.5) * (ra + ll)
    lead_VF = ll - (0.5) * (ra + la)
    df = pd.read_csv(f"{event.split('_')[0]}.csv")
    durations = df["duration"].values
    labels = df["label"].values
    data_new = feature_extraction_new(
        "DATA",
        lead_1,
        lead_2,
        lead_3,
        lead_aVR,
        lead_aVL,
        lead_VF,
        labels,
        durations,
    )
    np.save(folder, data_new.reshape(data_new.shape[0], 6, 26))
    print(f"Finished ECG features for patient: {folder}")


for folder, event in zip(folders, event_files):
    act = np.loadtxt(f"Activity signals/{folder.split(' ')[1]}/Activity.txt")
    ch = np.loadtxt(f"{folder}/Chest.txt")
    df = pd.read_csv(event)
    durations = df["duration"].values
    labels = df["label"].values
    data_new = feature_extraction_rsp("DATA", act, ch, labels, durations)
    np.save(f"{folder}_RSP", data_new)
    print(f"Finished RSP features for patient: {folder}")

df = pd.DataFrame()

for ecg, rsp, label in zip(ecgs, rsps, labels):
    data = np.load(ecg)
    temp_df = pd.DataFrame.from_records(
        data.reshape((data.shape[0], data.shape[1] * data.shape[2]))
    )

    data_rsp = np.load(rsp)
    temp_rsp_df = pd.DataFrame.from_records(
        data_rsp.reshape(
            (data_rsp.shape[0], data_rsp.shape[1] * data_rsp.shape[2])
        )
    )

    labels_df = pd.read_csv(label)

    temp = pd.concat([temp_df, temp_rsp_df], axis=1)
    temp["label"] = labels_df["label"]
    df = df.append(temp)

df.to_csv("data_all.csv", index=False)
