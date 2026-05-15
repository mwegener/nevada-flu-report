"""
Command-line entry point that mirrors `python -m flu_report.main`.
"""

from __future__ import annotations
import argparse
from .pipeline import run as run_essence_to_ilinet

def cli() -> None:
    ap = argparse.ArgumentParser(
        prog   = "python -m essence_to_ilinet",
        description = "Download ESSENCE data and upload to ILINet."
    )
    ap.add_argument("--start", required=True, help="Start date (e.g. 10Aug2025)")
    ap.add_argument("--end",   required=True, help="End   date (e.g. 28Feb2026)")
    ap.add_argument(
        "--facilities",
        default="geography=16435&",
        help="ESSENCE facility query string (default: demo single facility)",
    )
    args = ap.parse_args()

    run_essence_to_ilinet(
        start=args.start,
        end=args.end,
        facilities=args.facilities,
    )

if __name__ == "__main__":  # pragma: no cover
    cli()