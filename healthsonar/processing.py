import logging as log
from typing import List

import pandas as pd


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
