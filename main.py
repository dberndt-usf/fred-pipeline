"""
main.py
--------
Lightweight orchestration script for the FRED data pipeline.

Steps:
1️⃣ Fetch data from the FRED API (GDP and DJIA)
2️⃣ Load curated CSVs into DuckDB
3️⃣ Run a few exploratory SQL queries
"""

from scripts.fred_fetch import fetch_fred_series
from scripts.duckdb_utils import (
    load_to_duckdb,
    list_tables,
    run_query,
    summarize_table
)
from scripts.duckdb_queries import (
    create_quarterly_tables,
    join_and_compute_correlations,
    preview_joined_data,
    rolling_correlation,
)
import pandas as pd
from pathlib import Path
import subprocess


def run_pipeline():
    print("\n🚀 Starting FRED data pipeline ...")

    # 1️⃣ Fetch data from FRED API (raw → curated)
    print("\n📡 Fetching data from FRED API ...")
    series_list = ["GDP", "DJIA"]  # add more later (e.g., SP500, CPI)
    fetch_fred_series(series_list, start_date="2010-01-01")

    # 2️⃣ Load curated CSVs into DuckDB
    print("\n🦆 Loading curated CSVs into DuckDB ...")
    db_path = "data/warehouse/fred.duckdb"
    load_to_duckdb(curated_dir="data/curated", db_path=db_path)

    # 3️⃣ List tables in the database
    print("\n📋 Tables in DuckDB:")
    print(list_tables(db_path))

    # 4️⃣ Preview GDP table
    print("\n📈 GDP summary:")
    print(summarize_table(db_path, "gdp"))

    # 5️⃣ Run a sample analytic query
    print("\n🧮 Sample analytic query:")
    query = """

        SELECT
            date,
            value AS gdp
        FROM gdp
        WHERE date >= '2015-01-01'
        ORDER BY date
        LIMIT 5;
    """
    df = run_query(db_path, query)
    print(df)

    create_quarterly_tables(db_path)

    corr_results = join_and_compute_correlations(db_path)
    print("\n📊 Correlation results:")
    print(corr_results)

    preview_joined_data(db_path)

    # Rolling correlation (4-quarter window)
    roll_df = rolling_correlation(db_path, window_size=4)
    print("\n📊 Rolling correlation results:")
    print(roll_df.head(5))
    print(roll_df.tail(5))

    print("\n✅ Pipeline completed successfully!\n")


def launch_streamlit():
    """Launch Streamlit dashboard after pipeline completion."""
    print("\n📊 Launching Streamlit dashboard ... (Ctrl+C to stop)")
    try:
        subprocess.run(["streamlit", "run", "scripts/streamlit_dash.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Streamlit dashboard closed by user.")
    except FileNotFoundError:
        print("\n⚠️ Streamlit not installed. Run 'pip install streamlit' to enable dashboard launch.")


if __name__ == "__main__":
    run_pipeline()

    # Ask user if they want to view the dashboard
    choice = input("\nWould you like to launch the Streamlit dashboard? (y/n): ").strip().lower()
    if choice == "y":
        launch_streamlit()
    else:
        print("✅ Pipeline complete. Dashboard launch skipped.")
