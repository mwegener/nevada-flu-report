import re
from . import config

_DATE_RX = re.compile(r"(startDate|endDate)=[0-9A-Za-z]+")

def patch_dates(url: str, start: str, end: str) -> str:
    """Replace startDate=… and endDate=… inside an ESSENCE URL."""
    def _sub(m):
        key = m.group(1)
        return f"{key}={end if key=='endDate' else start}"
    return _DATE_RX.sub(_sub, url)

def build_essence_url_map() -> dict[str, str]:
    out = {}
    for key, raw in config.ESSENCE_URLS.items():
        if key in config.HISTORIC_KEYS:
            out[key] = patch_dates(raw,
                                   config.HIST_START_DATE,
                                   config.SEASON_END)
        else:
            out[key] = patch_dates(raw,
                                   config.SEASON_START,
                                   config.SEASON_END)
    return out