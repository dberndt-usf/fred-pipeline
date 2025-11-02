"""
fred.py
--------
Fetch time series data from the Federal Reserve Economic Data (FRED) API.

Usage:
    python fred/fred.py --series GDP --start 2010-01-01 --end 2025-01-01
"""

import os
import json
import requests
import pandas as pd
from datetime import datetime
from pathlib import Path
import argparse
from dotenv import load_dotenv

# ------------------------------------
# Load environment variables
# ------------------------------------
# Automatically read .env file in project root
load_dotenv()

FRED_API_BASE = "https://api.stlouisfed.org/fred/series/observations"
DEFAULT_DATA_DIR = Path("data")
DEFAULT_RAW_DIR = DEFAULT_DATA_DIR / "raw"
DEFAULT_CURATED_DIR = DEFAULT_DATA_DIR / "curated"


def get_fred_api_key() -> str:
    """Retrieve FRED API key from environment variables."""
    api_key = os.getenv("FRED_API_KEY")
    if not api_key:
        raise ValueError("FRED_API_KEY not found. Please set it in your .env file.")
    return api_key


def fetch_fred_series(series_list, start_date=None, end_date=None, save=True):
    """
    Fetch multiple FRED series and return as dictionary of DataFrames.

    Parameters
    ----------
    series_list : list[str]
        List of FRED series IDs (e.g., ["GDP", "DJIA"])
    start_date : str, optional
        Start date (YYYY-MM-DD)
    end_date : str, optional
        End date (YYYY-MM-DD)
    save : bool
        Whether to save raw JSON and curated CSV files

    Returns
    -------
    dict[str, pd.DataFrame]
        Mapping series_id → DataFrame(date, value)
    """
    api_key = get_fred_api_key()
    DEFAULT_RAW_DIR.mkdir(parents=True, exist_ok=True)
    DEFAULT_CURATED_DIR.mkdir(parents=True, exist_ok=True)

    all_data = {}

    for series_id in series_list:
        params = {
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
        }
        if start_date:
            params["observation_start"] = start_date
        if end_date:
            params["observation_end"] = end_date

        print(f"📡 Fetching {series_id} from FRED...")
        response = requests.get(FRED_API_BASE, params=params)
        response.raise_for_status()
        data = response.json()

        # Save raw JSON
        if save:
            raw_path = DEFAULT_RAW_DIR / f"{series_id.lower()}_raw.json"
            with open(raw_path, "w") as f:
                json.dump(data, f, indent=2)
            print(f"💾 Saved raw JSON: {raw_path}")

        # Convert to DataFrame
        obs = data.get("observations", [])
        df = pd.DataFrame(obs)[["date", "value"]]
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df["date"] = pd.to_datetime(df["date"])
        df.dropna(subset=["value"], inplace=True)

        # Save curated CSV
        if save:
            csv_path = DEFAULT_CURATED_DIR / f"{series_id.lower()}.csv"
            df.to_csv(csv_path, index=False)
            print(f"💾 Saved curated CSV: {csv_path}")

        all_data[series_id] = df

    return all_data


# ------------------------------------
# CLI interface
# ------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch FRED economic data series")
    parser.add_argument("--series", nargs="+", required=True, help="FRED series IDs")
    parser.add_argument("--start", type=str, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, help="End date (YYYY-MM-DD)")
    args = parser.parse_args()

    fetch_fred_series(args.series, start_date=args.start, end_date=args.end)
