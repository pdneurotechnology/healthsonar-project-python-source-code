from collections import Counter

import neurokit2 as nk
import numpy as np
import pandas as pd
import scipy
from scipy.stats import kurtosis, skew


def calculate_entropy(list_values):
    counter_values = Counter(list_values).most_common()
    probabilities = [elem[1] / len(list_values) for elem in counter_values]
    entropy = scipy.stats.entropy(probabilities)

    return entropy


#
#


def calculate_statistics(list_values):
    n05 = np.nanpercentile(list_values, 5)
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

    return [n05, n25, n75, n95, median, mean, std, var, rms, sk, kur]


#
#


def calculate_crossings(list_values):
    no_zero_crossings = sum(np.diff(np.array(list_values) > 0, prepend=False))
    no_mean_crossings = sum(
        np.diff(np.array(list_values) > np.mean(list_values), prepend=False)
    )

    return [no_zero_crossings, no_mean_crossings]


#
#


def get_features_rsp(list_values):
    entropy = calculate_entropy(list_values)
    crossings = calculate_crossings(list_values)
    statistics = calculate_statistics(list_values)

    return [entropy] + crossings + statistics


#
#


def feature_extraction_rsp(recording, chest, labels, durations):
    fs = 32
    data = []
    lengths = []
    labels_list = []

    for i, label in enumerate(labels):
        prev = 0

        try:
            segment = chest[prev : fs * durations[i - 1]]

            # Uses a Butterworth filter by default.
            rsp = nk.signal_filter(segment, highcut=30)
            rsp_features_chest = get_features_rsp(rsp)

            data.append([rsp_features_chest])
            prev = durations[i - 1]

        # We get a ValueError for events with a duration of 0.
        except ValueError:
            data.append([[np.nan] * 14])

    data = np.array(data, dtype="float")

    return data
