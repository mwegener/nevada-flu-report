"""
flu_report.config
Centralised constants and environment settings.
"""

from __future__ import annotations
from pathlib import Path
import os
from dotenv import load_dotenv

# ------------------------------------------------------------------
# Project-root helpers
# ------------------------------------------------------------------
# config.py lives in  src/flu_report/, so ../..  is the repository root
ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
DL_DIR   = ROOT / "downloads"

# Ensure the usual folders exist
DATA_DIR.mkdir(exist_ok=True)
DL_DIR.mkdir(exist_ok=True)

# ------------------------------------------------------------------
# .env  (never hard-code secrets; store them in the repo-root .env)
# ------------------------------------------------------------------
load_dotenv(ROOT / ".env", override=False)   # override=False keeps OS vars

ESSENCE_USER = os.getenv("ESSENCE_USER")
ESSENCE_PASS = os.getenv("ESSENCE_PASS")

REDCAP_TOKEN = os.getenv("REDCAP_TOKEN", "")
REDCAP_URL   = os.getenv("REDCAP_URL", "")

# Time-zone for any datetime operations
TZ = os.getenv("TZ", "America/Los_Angeles")
os.environ["TZ"] = TZ      # propagate to everything that obeys $TZ

# ------------------------------------------------------------------
# Date parameters (update once per season/report)
# ------------------------------------------------------------------
HIST_START_DATE = "03Oct2021"   # historic data anchor (Sunday)
SEASON_START    = "28Sep2025"   # first epi-week Sunday
SEASON_END      = "14Mar2026"   # last epi-week Saturday

# ------------------------------------------------------------------
# ESSENCE URLs  (FULL real URLs go here)
# ------------------------------------------------------------------
ESSENCE_URLS: dict[str, str] = {
    "ILI_counties"          : "https://essence.syndromicsurveillance.org/nssp_essence/api/tableBuilder/csv?geography=nv_carson%20city&geography=nv_churchill&geography=nv_clark&geography=nv_douglas&geography=nv_elko&geography=nv_esmeralda&geography=nv_eureka&geography=nv_humboldt&geography=nv_lander&geography=nv_lincoln&geography=nv_lyon&geography=nv_mineral&geography=nv_nye&geography=nv_pershing&geography=nv_storey&geography=nv_unknown&geography=nv_washoe&geography=nv_white%20pine&datasource=va_er&startDate=28Sep2025&medicalGroupingSystem=essencesyndromes&userId=8036&endDate=3Oct2026&percentParam=medicalGrouping&aqtTarget=TableBuilder&medicalGrouping=ili&geographySystem=region&detector=nodetectordetector&timeResolution=weekly&rowFields=timeResolution&rowFields=geographyregion&columnField=medicalGroupingessencesyndromes",
    "ILI_age"               :  "https://essence.syndromicsurveillance.org/nssp_essence/api/tableBuilder/csv?geography=nv&datasource=va_er&startDate=28Sep2025&medicalGroupingSystem=essencesyndromes&userId=8036&ageCDCILI=00-04&ageCDCILI=05-24&ageCDCILI=25-49&ageCDCILI=50-64&ageCDCILI=65-1000&endDate=3Oct2026&percentParam=medicalGrouping&aqtTarget=TableBuilder&medicalGrouping=ili&geographySystem=state&detector=nodetectordetector&timeResolution=weekly&rowFields=timeResolution&rowFields=ageCDCILI&columnField=medicalGroupingessencesyndromes",
    "flu_ED_counties"       :  "https://essence.syndromicsurveillance.org/nssp_essence/api/tableBuilder/csv?geography=nv_carson%20city&geography=nv_churchill&geography=nv_clark&geography=nv_douglas&geography=nv_elko&geography=nv_esmeralda&geography=nv_eureka&geography=nv_humboldt&geography=nv_lander&geography=nv_lincoln&geography=nv_lyon&geography=nv_mineral&geography=nv_nye&geography=nv_pershing&geography=nv_storey&geography=nv_unknown&geography=nv_washoe&geography=nv_white%20pine&datasource=va_er&startDate=28Sep2025&medicalGroupingSystem=essencesyndromes&userId=8036&endDate=3Oct2026&percentParam=ccddCategory&aqtTarget=TableBuilder&ccddCategory=cdc%20influenza%20dd%20v1&geographySystem=region&detector=nodetectordetector&timeResolution=weekly&rowFields=timeResolution&rowFields=geographyregion&columnField=ccddCategory",
    "RSV_demog"             : "https://essence.syndromicsurveillance.org/nssp_essence/api/tableBuilder/csv?geography=nv&datasource=va_er&startDate=28Sep2025&medicalGroupingSystem=essencesyndromes&sex=m&sex=f&userId=8036&cRaceEthNarrow=american%20indian%20or%20alaska%20native%20and%20non-hispanic&cRaceEthNarrow=asian%20and%20non-hispanic&cRaceEthNarrow=black%20or%20african%20american%20and%20non-hispanic&cRaceEthNarrow=multiracial/other%20and%20non-hispanic&cRaceEthNarrow=native%20hawaiian%20or%20other%20pacific%20islander%20and%20non-hispanic&cRaceEthNarrow=white%20and%20non-hispanic&cRaceEthNarrow=hispanic%20or%20latino&age=00-04&age=05-17&age=18-44&age=45-64&age=65-1000&endDate=3Oct2026&percentParam=noPercent&aqtTarget=TableBuilder&ccddCategory=cdc%20respiratory%20syncytial%20virus%20dd%20v1&geographySystem=state&detector=nodetectordetector&timeResolution=weekly&rowFields=age&rowFields=sex&rowFields=cRaceEthNarrow&columnField=ccddCategory",
    "RSV_county_percent"    : "https://essence.syndromicsurveillance.org/nssp_essence/api/tableBuilder/csv?geography=nv_carson%20city&geography=nv_churchill&geography=nv_clark&geography=nv_douglas&geography=nv_elko&geography=nv_esmeralda&geography=nv_eureka&geography=nv_humboldt&geography=nv_lander&geography=nv_lincoln&geography=nv_lyon&geography=nv_mineral&geography=nv_nye&geography=nv_pershing&geography=nv_storey&geography=nv_unknown&geography=nv_washoe&geography=nv_white%20pine&datasource=va_er&startDate=28Sep2025&medicalGroupingSystem=essencesyndromes&userId=8036&endDate=3Oct2026&percentParam=geography&aqtTarget=TableBuilder&ccddCategory=cdc%20respiratory%20syncytial%20virus%20dd%20v1&geographySystem=region&detector=nodetectordetector&timeResolution=weekly&rowFields=timeResolution&rowFields=geographyregion&columnField=ccddCategory",
   "RSV_ED_historic"        : "https://essence.syndromicsurveillance.org/nssp_essence/api/tableBuilder/csv?geography=nv&datasource=va_er&startDate=3Oct2021&medicalGroupingSystem=essencesyndromes&userId=8036&endDate=3Oct2026&percentParam=noPercent&aqtTarget=TableBuilder&ccddCategory=cdc%20respiratory%20syncytial%20virus%20dd%20v1&geographySystem=state&detector=nodetectordetector&timeResolution=weekly&rowFields=timeResolution&columnField=ccddCategory",
    "flu_ED_historic"       :  "https://essence.syndromicsurveillance.org/nssp_essence/api/tableBuilder/csv?geography=nv_carson%20city&geography=nv_churchill&geography=nv_clark&geography=nv_douglas&geography=nv_elko&geography=nv_esmeralda&geography=nv_eureka&geography=nv_humboldt&geography=nv_lander&geography=nv_lincoln&geography=nv_lyon&geography=nv_mineral&geography=nv_nye&geography=nv_pershing&geography=nv_storey&geography=nv_unknown&geography=nv_washoe&geography=nv_white%20pine&datasource=va_er&startDate=3Oct2021&medicalGroupingSystem=essencesyndromes&userId=8036&endDate=3Oct2026&percentParam=noPercent&aqtTarget=TableBuilder&ccddCategory=cdc%20influenza%20dd%20v1&geographySystem=region&detector=nodetectordetector&timeResolution=weekly&rowFields=timeResolution&rowFields=geographyregion&columnField=ccddCategory",
    "flu_demog"             : "https://essence.syndromicsurveillance.org/nssp_essence/api/tableBuilder/csv?geography=nv&datasource=va_er&startDate=28Sep2025&medicalGroupingSystem=essencesyndromes&sex=m&sex=f&userId=8036&ageCDCILI=00-04&ageCDCILI=05-24&ageCDCILI=25-49&ageCDCILI=50-64&ageCDCILI=65-1000&cRaceEthNarrow=american%20indian%20or%20alaska%20native%20and%20non-hispanic&cRaceEthNarrow=asian%20and%20non-hispanic&cRaceEthNarrow=black%20or%20african%20american%20and%20non-hispanic&cRaceEthNarrow=multiracial/other%20and%20non-hispanic&cRaceEthNarrow=native%20hawaiian%20or%20other%20pacific%20islander%20and%20non-hispanic&cRaceEthNarrow=white%20and%20non-hispanic&cRaceEthNarrow=hispanic%20or%20latino&endDate=3Oct2026&percentParam=noPercent&aqtTarget=TableBuilder&ccddCategory=cdc%20influenza%20dd%20v1&geographySystem=state&detector=nodetectordetector&timeResolution=weekly&rowFields=ageCDCILI&rowFields=sex&rowFields=cRaceEthNarrow&rowFields=timeResolution&columnField=ccddCategory"
}

# Keys whose URLs must keep HIST_START_DATE as their startDate
HISTORIC_KEYS = {"RSV_ED_historic", "flu_ED_historic"}

# ------------------------------------------------------------------
# Convenience: default download/output directory as Path
# ------------------------------------------------------------------
DOWNLOAD_DIR = DL_DIR          # keep a Path, not plain str