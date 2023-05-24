import json
import logging as log
import sys
import time
from pathlib import Path
from typing import List

import pandas as pd
import processing as proc


def input_to_output():
    """
    Turn the data of a set of csv files into a dictionary of observations.
    """

    input_json = sys.argv[1]
    df = pd.read_json(input_json)

    respiration_csv_path = Path(df.loc[:, "RespInputFile"].values[0])
    heart_rate_csv_path = Path(df.loc[:, "HRInputFile"].values[0])
    activity_csv_path = Path(df.loc[:, "ActivityInputFile"].values[0])
    output_json_path = Path(df.loc[:, "OutputObservationsFile"].values[0])

    # Print logs to terminal.
    # =========================================================================

    if respiration_csv_path.is_file():
        log.create_log(f"Parsed {respiration_csv_path.name}!")
    else:
        log.create_log(f"Could not find {respiration_csv_path.name}!")

    if heart_rate_csv_path.is_file():
        log.create_log(f"Parsed {heart_rate_csv_path.name}!")
    else:
        log.create_log(f"Could not find {respiration_csv_path.name}!")

    if activity_csv_path.is_file():
        log.create_log(f"Parsed {activity_csv_path.name}!")
    else:
        log.create_log(f"Could not find {respiration_csv_path.name}!")

    # Load data from the csv files.
    # =========================================================================

    respiration_df = pd.read_csv(respiration_csv_path)
    heart_rate_df = pd.read_csv(heart_rate_csv_path)
    activity_df = pd.read_csv(activity_csv_path)

    # Process data.
    # =========================================================================

    data = proc.process_data(respiration_df, heart_rate_df, activity_df)

    # Create the observation's json.
    # =========================================================================

    observations = {
        "Timestamp": int(time.time()),
        "InputFiles": [
            str(respiration_csv_path),
            str(heart_rate_csv_path),
            str(activity_csv_path),
        ],
        "Version": "1.0",
        "Data": data,
    }

    # Write the dictionary to a json string.
    observations_json = json.dumps(observations, indent=4)

    # Write the observations to a json file.
    with open(output_json_path, "w") as f:
        f.write(observations_json)


def process_data(
    resp_df: pd.DataFrame, hr_df: pd.DataFrame, act_df: pd.DataFrame
) -> List[dict]:
    """
    Process data from three input files and return a dictionary of outputs.

    Parameters
    ----------
    resp_df : pd.DataFrame
        Dataframe containing respiration data.

    hr_df : pd.DataFrame
        Dataframe containing heart rate data.

    act_df : pd.DataFrame
        Dataframe containing activity data.

    Returns
    -------
    data : dict
        Dictionary of outputs.
    """

    # Add the processing code here and create an observations in the format
    # specified in the example below.

    #
    # Processing code goes here...
    #

    # You can create custom logs of the form:
    # log = {
    #     "Message": "This is a message",
    #     "Timestamp": int(time.time()),
    # }
    #
    # And print them to the terminal using:
    # log.create_log(log)

    # Create a log for example:
    message = "This is a message"
    log.create_log(message)

    # Example of output data
    data = [
        {"Code": "HR", "Value": 123, "Timestamp": 1234124512},
        {"Code": "RR", "Value": 123, "Timestamp": 1234124512},
        {"Code": "REC", "Value": 123, "Timestamp": 1234124512},
        {"Code": "APNEA", "Value": 123, "Timestamp": 1234124512},
        {"Code": "HYPOPNEA", "Value": 123, "Timestamp": 1234124512},
        {
            "Code": "SLEEP_STAGE_W",
            "Value": 123,
            "Timestamp": 1234124512,
        },
        {
            "Code": "SLEEP_STAGE_N1",
            "Value": 123,
            "Timestamp": 1234124512,
        },
        {
            "Code": "SLEEP_STAGE_N2",
            "Value": 123,
            "Timestamp": 1234124512,
        },
        {
            "Code": "SLEEP_STAGE_N3",
            "Value": 123,
            "Timestamp": 1234124512,
        },
        {
            "Code": "SLEEP_STAGE_R",
            "Value": 123,
            "Timestamp": 1234124512,
        },
    ]

    # Return a list of dictionaries.
    return data
