"""
duckdb_utils.py
---------------
Lightweight utility functions for working with DuckDB in the FRED pipeline.
"""

import duckdb
from pathlib import Path
import pandas as pd


def connect_duckdb(db_path: str = "data/warehouse/fred.duckdb"):
    """Create or connect to a DuckDB database."""
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(db_path)


def load_to_duckdb(curated_dir: str = "data/curated", db_path: str = "data/warehouse/fred.duckdb"):
    """
    Load all CSV files in the curated directory into DuckDB tables.

    Table name is derived from the CSV filename (without extension).
    """
    curated_path = Path(curated_dir)
    con = connect_duckdb(db_path)

    for csv_file in curated_path.glob("*.csv"):
        table_name = csv_file.stem
        print(f"📥 Loading {csv_file.name} into DuckDB as '{table_name}'...")
        con.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS
            SELECT * FROM read_csv_auto('{csv_file}');
        """)

    con.close()
    print("✅ All curated CSVs loaded into DuckDB.")


def list_tables(db_path: str = "data/warehouse/fred.duckdb") -> pd.DataFrame:
    """Return a DataFrame listing available tables."""
    con = connect_duckdb(db_path)
    df = con.execute("SHOW TABLES;").df()
    con.close()
    return df


def run_query(db_path: str, query: str) -> pd.DataFrame:
    """Execute an SQL query and return a DataFrame."""
    con = connect_duckdb(db_path)
    df = con.execute(query).df()
    con.close()
    return df


def summarize_table(db_path: str, table: str) -> pd.DataFrame:
    """Return basic descriptive statistics for a table."""
    query = f"SELECT MIN(date) AS start, MAX(date) AS end, COUNT(*) AS rows FROM {table};"
    return run_query(db_path, query)
