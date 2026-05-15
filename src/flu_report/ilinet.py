"""
flu_report.ilinet
Automated login ➜ ESSENCE upload ➜ QA downloads
using Playwright (async API).

Environment variables that MUST be set:
  ILINET_USER           CDC ILINet username
  ILINET_PASS           CDC ILINet password
Optional overrides:
  ILINET_DOWNLOAD_DIR   folder for downloaded CSVs
"""

from playwright.async_api import async_playwright, TimeoutError as PWTimeout
from pathlib import Path
from datetime import datetime
import asyncio, os

# ── Configuration constants ─────────────────────────────────────
USERNAME = os.getenv("ILINET_USER")
PASSWORD = os.getenv("ILINET_PASS")
ILINET_LOGIN_URL      = "https://wwwn.cdc.gov/ILINet/Default.aspx"
SENTINEL_DOWNLOAD_URL = "https://wwwn.cdc.gov/ILINet/DownloadSentinel.aspx"
LAB_DOWNLOAD_URL      = "https://wwwn.cdc.gov/ILINet/LabData.aspx"

# Determine download folder
_raw = os.getenv("ILINET_DOWNLOAD_DIR", "")
if _raw:
    DOWNLOAD_DIR = Path(_raw)
else:
    # Walk up until repo root (the folder that contains *.Rproj OR .git)
    _here = Path(__file__).resolve().parent
    root  = _here
    while root != root.parent and not (root / ".git").exists():
        if any(root.glob("*.Rproj")):
            break
        root = root.parent
    DOWNLOAD_DIR = root / "downloads"

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
print(f"📁 Saving files to: {DOWNLOAD_DIR.absolute()}")

# ── Main async worker ───────────────────────────────────────────
async def download_ilinet_data():
    async with async_playwright() as p:
        browser  = await p.chromium.launch(headless=False, slow_mo=50)
        context  = await browser.new_context(accept_downloads=True)
        context.set_default_timeout(30_000)
        page     = await context.new_page()

        try:
            # 1 ─ Login
            await page.goto(ILINET_LOGIN_URL)
            await page.fill("#MainContent_Login1_UserName", USERNAME)
            await page.fill("#MainContent_Login1_Password", PASSWORD)
            await page.click("#MainContent_Login1_LoginButton")
            await page.wait_for_selector("#MainContent_linkEnhancedData", timeout=120_000)
            print("✓ Logged in")

            # 2 ─ Download Sentinel (ILI) data
            await page.goto(SENTINEL_DOWNLOAD_URL)
            await page.wait_for_load_state("networkidle")
            await page.wait_for_selector(
                "xpath=/html/body/div[3]/form/div[3]/div[1]/div[1]"
                "/div/div[2]/div[1]/div[1]/select",
                timeout=10_000
            )
            await page.select_option(
                "xpath=/html/body/div[3]/form/div[3]/div[1]/div[1]"
                "/div/div[2]/div[1]/div[1]/select",
                index=1
            )
            print("✓ Selected most recent season")
            await page.wait_for_timeout(1000)

            await page.wait_for_selector("#MainContent_linkAgeDownload", state="visible")
            async with page.expect_download(timeout=60_000) as dl_info:
                await page.click("#MainContent_linkAgeDownload")
            line_dl  = await dl_info.value
            line_name = f"ili_net_data_{datetime.now():%Y%m%d_%H%M%S}.csv"
            await line_dl.save_as(DOWNLOAD_DIR / line_name)
            print(f"✓ ILINet data saved as {line_name}")

            # 3 ─ Download Lab data
            await page.goto(LAB_DOWNLOAD_URL)
            await page.wait_for_load_state("networkidle")

            selectors_to_try = [
                "xpath=/html/body/div[3]/form/div[3]/div[1]/div[1]/div/div[2]/div[1]/div[1]/select",
                "select[name*='ddlSeason']",
                "[id*='ddlSeason']",
                "#MainContent_ddlSeason"
            ]
            season_select = None
            for sel in selectors_to_try:
                try:
                    await page.wait_for_selector(sel, timeout=3_000)
                    season_select = sel
                    break
                except PWTimeout:
                    continue
            if not season_select:
                selects = await page.query_selector_all("select")
                if selects:
                    season_select = "xpath=(//select)[1]"

            await page.select_option(season_select, index=1)
            print("✓ Selected most recent season (lab data)")
            await page.wait_for_timeout(2000)

            await page.wait_for_selector("#MainContent_LinkDownloadLabData", state="visible")
            async with page.expect_download(timeout=60_000) as dl_info:
                await page.click("#MainContent_LinkDownloadLabData")
            lab_dl   = await dl_info.value
            lab_name = f"lab_data_{datetime.now():%Y%m%d_%H%M%S}.csv"
            await lab_dl.save_as(DOWNLOAD_DIR / lab_name)
            print(f"✓ Lab data saved as {lab_name}")

            print(f"\nAll done! Files saved to: {DOWNLOAD_DIR}")
            return str(DOWNLOAD_DIR / line_name), str(DOWNLOAD_DIR / lab_name)

        except Exception as exc:
            print(f"✗ Error occurred: {exc}")
            return None, None
        finally:
            await context.close()
            await browser.close()

# ── Convenience CLI ─────────────────────────────────────────────
if __name__ == "__main__":
    asyncio.run(download_ilinet_data())