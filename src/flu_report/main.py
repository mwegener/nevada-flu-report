"""
flu_report.main
Master pipeline to refresh all source data for the Nevada Flu Report.

Steps
─────
1. Run the FluView R script  (scripts/get_fluview_data.R)
2. Download ESSENCE CSVs     (flu_report.essence)
3. Scrape ILINet / Lab data  (flu_report.ilinet – Playwright)

All artefacts end up in  downloads/
"""

from __future__ import annotations
import asyncio, subprocess, sys, textwrap
from pathlib import Path
from datetime import datetime

from . import config, essence, ilinet   # local modules

ROOT        = config.ROOT
DL_DIR: Path = config.DL_DIR            # downloads/

# ------------------------------------------------------------------
# 1. Run the R FluView script
# ------------------------------------------------------------------
def run_fluview_r(year: int) -> None:
    """
    Call scripts/get_fluview_data.R in a subprocess.
    The R script writes CSVs to downloads/.
    """
    script = ROOT / "scripts" / "get_fluview_data.R"
    if not script.exists():
        print(f"⚠️  {script} not found – skipping FluView step.")
        return

    cmd = ["Rscript", "--vanilla", str(script), str(year)]
    print(f"\n▶ Running FluView R script for {year} …")
    try:
        subprocess.check_call(cmd)
        print("✓ FluView data downloaded")
    except subprocess.CalledProcessError as exc:
        print(f"✗ FluView script failed (exit {exc.returncode})")


# ------------------------------------------------------------------
# 2. Download ESSENCE CSVs
# ------------------------------------------------------------------
def run_essence_download() -> None:
    print("\n▶ Downloading ESSENCE datasets …")
    data_map = essence.download_all(as_dataframe=False)

    # Optional: write each dataset to CSV
    for key, rows in data_map.items():
        out = DL_DIR / f"{key}_{datetime.now():%Y%m%d_%H%M%S}.csv"
        if not rows:
            print(f"  {key:<20s} – 0 rows (skipped)")
            continue

        # pandas is convenient for quick CSV dump
        try:
            import pandas as pd
            pd.DataFrame(rows).to_csv(out, index=False)
            print(f"  {key:<20s} – {len(rows):>6,d} rows → {out.name}")
        except ImportError:
            print(f"  {key:<20s} – pandas missing; not saved.")


# ------------------------------------------------------------------
# 3. Scrape ILINet web portal
# ------------------------------------------------------------------
async def run_ilinet_scraper() -> None:
    print("\n▶ Scraping ILINet portal …")
    ili_path, lab_path = await ilinet.download_ilinet_data()
    if ili_path:
        print(f"✓ ILINet CSV  → {Path(ili_path).name}")
        print(f"✓ Lab CSV     → {Path(lab_path).name}")
    else:
        print("✗ ILINet scraper failed")


# ------------------------------------------------------------------
# Entrypoint
# ------------------------------------------------------------------
def main(year: int = 2025):
    DL_DIR.mkdir(exist_ok=True)
    print(f"📂 downloads directory: {DL_DIR.resolve()}\n")

    run_fluview_r(year)          # Step 1
    run_essence_download()       # Step 2
    asyncio.run(run_ilinet_scraper())   # Step 3

    print("\n✅ All data sources refreshed.")


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Refresh all Nevada Flu Report data.")
    ap.add_argument(
        "--year",
        type=int,
        default=datetime.now().year,
        help="Flu season ending year (e.g., 2025 means 2024–25 season)",
    )
    args = ap.parse_args()

    try:
        main(year=args.year)
    except KeyboardInterrupt:
        sys.exit("\nInterrupted by user")