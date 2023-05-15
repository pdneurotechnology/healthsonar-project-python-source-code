# README

You will only update the `processing.py` file, by adding the processing code inside the `process_data` function. This function already parses the relevant data from the raw data files into 3 dataframes. The results of the processing must be structured in the following way:

```python
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
```

Inside your processing script you can log into the terminal any message by calling the following function:

```python
log.create_log("This is a log message")
```

Said function creates a json message which includes the message and a Unix timestamp of the current time.