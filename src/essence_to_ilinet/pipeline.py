from __future__ import annotations
import os, csv, textwrap, datetime as dt, pathlib, asyncio, requests, pandas as pd
from typing import Dict
from playwright.async_api import async_playwright
from .facility_map import FACILITY_MAP   # ← long dict lives next door

ROOT      = pathlib.Path(__file__).resolve().parents[2]
OUTPUTS   = ROOT / "outputs"
DOWNLOADS = ROOT / "downloads"
ESSENCE_BASE = "https://essence.syndromicsurveillance.org"

# ------------------------------------------------------------------ #
# everything else identical to previous answer …
# ------------------------------------------------------------------ #

def run(start: str, end: str, facilities: str):  # <-- exported in __init__.py
    """High-level driver called by main.py and by importers."""
    # … see previous answer for full body …
    ...