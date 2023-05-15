import json
import time


def create_log(message: str):
    """
    Create a log message.

    Parameters
    ----------
    message : str
        The message to log.
    """

    log = {
        "Message": message,
        "Timestamp": int(time.time()),
    }

    print(json.dumps(log))
