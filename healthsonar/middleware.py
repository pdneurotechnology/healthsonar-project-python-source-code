import json
import logging as log
import sys
import time
from pathlib import Path

import pandas as pd

import processing as proc

# Define funtion
# =============================================================================


def input_to_output():
    input_json = sys.argv[1]
    df = pd.read_json(input_json)

    respiration_csv_path = Path(df.loc[:, "RespInputFile"].values[0])
    heart_rate_csv_path = Path(df.loc[:, "HRInputFile"].values[0])
    activity_csv_path = Path(df.loc[:, "ActivityInputFile"].values[0])
    output_json_path = Path(df.loc[:, "OutputObservationsFile"].values[0])

    if respiration_csv_path.is_file():
        respiration_log = {
            "Message": f"Parsed {respiration_csv_path.name}!",
            "Timestamp": int(time.time()),
        }
    else:
        respiration_log = {
            "Message": f"Could not find {respiration_csv_path.name}!",
            "Timestamp": int(time.time()),
        }

    #
    #

    if heart_rate_csv_path.is_file():
        heart_rate_log = {
            "Message": f"Parsed {heart_rate_csv_path.name}!",
            "Timestamp": int(time.time()),
        }
    else:
        heart_rate_log = {
            "Message": f"Could not find {respiration_csv_path.name}!",
            "Timestamp": int(time.time()),
        }

    #
    #

    if activity_csv_path.is_file():
        activity_log = {
            "Message": f"Parsed {activity_csv_path.name}!",
            "Timestamp": int(time.time()),
        }
    else:
        activity_log = {
            "Message": f"Could not find {respiration_csv_path.name}!",
            "Timestamp": int(time.time()),
        }

    # Print logs to terminal
    # =========================================================================

    print(json.dumps(respiration_log))
    print(json.dumps(heart_rate_log))
    print(json.dumps(activity_log))

    # Load data from the csvc files
    # =========================================================================

    respiration_df = pd.read_csv(respiration_csv_path)
    heart_rate_df = pd.read_csv(heart_rate_csv_path)
    activity_df = pd.read_csv(activity_csv_path)

    # Process data
    # =========================================================================

    data = proc.process_data(respiration_df, heart_rate_df, activity_df)

    # Create observation json
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

    # Write the dictionary to a json string
    observations_json = json.dumps(observations, indent=4)

    # Write observations json to file
    with open(output_json_path, "w") as f:
        f.write(observations_json)


# Call function
# =============================================================================


if __name__ == "__main__":
    input_to_output()
