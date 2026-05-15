import os
import io                 # ← missing import
import requests
import pandas as pd
from dotenv import load_dotenv
from . import config

load_dotenv()

_TOKEN = os.getenv("REDCAP_TOKEN") or config.REDCAP_TOKEN
_URL   = os.getenv("REDCAP_URL")   or config.REDCAP_URL

def export_records(payload: dict) -> pd.DataFrame:
    """
    Call REDCap’s API and return the result as a pandas DataFrame.

    Parameters
    ----------
    payload : dict
        Additional POST fields (e.g., {'content': 'record', 'type': 'flat'}).

    Returns
    -------
    pandas.DataFrame
    """
    if not _TOKEN or not _URL:
        raise RuntimeError("REDCAP_TOKEN and/or REDCAP_URL are not set.")

    body = {
        "token": _TOKEN,
        "format": "csv",          # we expect CSV in the response
        "returnFormat": "csv"
    }
    body.update(payload)

    resp = requests.post(_URL, data=body, timeout=120)
    resp.raise_for_status()

    return pd.read_csv(io.StringIO(resp.text))