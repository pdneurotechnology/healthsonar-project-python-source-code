import json
import sys
import time
from pathlib import Path

import pandas as pd

# Define funtion
# =============================================================================


def parse_files():
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
        "Data": [
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
        ],
    }

    observations_json = json.dumps(observations, indent=4)

    # Write observation json to file
    with open(output_json_path, "w") as f:
        f.write(observations_json)


# Call function
# =============================================================================


if __name__ == "__main__":
    parse_files()
