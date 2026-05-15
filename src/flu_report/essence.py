# src/flu_report/essence.py
"""
ESSENCE downloader utilities.
"""

from __future__ import annotations
import csv, io, os, requests
from pathlib import Path
from typing import Iterable, Mapping

import pandas as pd
from dotenv import load_dotenv

from . import config, utils

# ── Load credentials ────────────────────────────────────────────
load_dotenv()        # pick up ESSENCE_USER / ESSENCE_PASS from .env

_USERNAME = os.getenv("ESSENCE_USER", config.ESSENCE_USER)
_PASSWORD = os.getenv("ESSENCE_PASS", config.ESSENCE_PASS)

if not _USERNAME or not _PASSWORD:
    raise RuntimeError(
        "ESSENCE_USER / ESSENCE_PASS not found in environment or config."
    )

# ── Session wrapper ─────────────────────────────────────────────
class EssenceSession:
    """
    Re-usable HTTP session with Basic Auth for ESSENCE API calls.
    """

    def __init__(self, user: str = _USERNAME, pw: str = _PASSWORD) -> None:
        self.session = requests.Session()
        self.session.auth = (user, pw)
        self.session.headers.update({"User-Agent": "flu-report/1.0"})
        # You can add retry logic here if you like:
        # adapter = requests.adapters.HTTPAdapter(max_retries=3)
        # self.session.mount("https://", adapter)

    # ------------------------------------------------------------
    def fetch(self, url: str) -> str:
        """Return raw CSV text from ESSENCE."""
        resp = self.session.get(url, timeout=90)
        resp.raise_for_status()
        return resp.text

    # ------------------------------------------------------------
    def fetch_dicts(self, url: str) -> list[dict]:
        """Return parsed CSV rows as list-of-dicts (str keys)."""
        text = self.fetch(url)
        return list(csv.DictReader(io.StringIO(text)))

    # ------------------------------------------------------------
    def fetch_df(self, url: str) -> pd.DataFrame:
        """Return parsed CSV as a pandas DataFrame."""
        text = self.fetch(url)
        return pd.read_csv(io.StringIO(text))


# ── Convenience, single-shot helpers ────────────────────────────
_DEF_S = EssenceSession()   # module-level singleton

def fetch_csv(url: str) -> list[dict]:
    """One-off download; returns list-of-dicts."""
    return _DEF_S.fetch_dicts(url)

def fetch_df(url: str) -> pd.DataFrame:
    """One-off download; returns DataFrame."""
    return _DEF_S.fetch_df(url)


# ── Bulk download (used by main.py) ─────────────────────────────
def download_all(as_dataframe: bool = False) -> dict[str, Iterable]:
    """
    Download every URL in config.ESSENCE_URLS (after date patching).

    Returns:
        dict mapping key → rows (list[dict])  OR → DataFrame
        depending on `as_dataframe`.
    """
    urls: Mapping[str, str] = utils.build_essence_url_map()
    results: dict[str, Iterable] = {}

    for key, url in urls.items():
        print(f"→ {key:<18s}", end="", flush=True)
        try:
            results[key] = (
                _DEF_S.fetch_df(url) if as_dataframe else _DEF_S.fetch_dicts(url)
            )
            print("✓")
        except Exception as exc:
            print(f"✗  ({exc})")
            raise

    return results


# ── CLI for ad-hoc testing ─────────────────────────────────────
if __name__ == "__main__":
    from argparse import ArgumentParser

    ap = ArgumentParser(description="Download all ESSENCE datasets.")
    ap.add_argument("--df", action="store_true", help="return DataFrames")
    args = ap.parse_args()

    out = download_all(as_dataframe=args.df)
    for k, v in out.items():
        if args.df:
            print(f"{k}: {len(v):>6,d} rows")
        else:
            print(f"{k}: {len(v):>6,d} records")