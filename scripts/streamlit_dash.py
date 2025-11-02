"""
streamlit_dash.py
----------------------
Interactive visualization of GDP–DJIA correlations.
"""

import sys
from pathlib import Path

# Ensure project root (fred-pipeline/) is on the Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
from scripts.duckdb_utils import run_query
from scripts.duckdb_queries import rolling_correlation

st.set_page_config(page_title="FRED GDP–DJIA Explorer", layout="wide")

st.title("📊 FRED Economic Data Dashboard")
st.caption("Analyzing correlations between GDP and the Dow Jones Industrial Average")

db_path = "data/warehouse/fred.duckdb"

# --- Query options
st.sidebar.header("Analysis Parameters")
window = st.sidebar.slider("Rolling correlation window (quarters):", 2, 8, 4)
show_data = st.sidebar.checkbox("Show data preview", value=False)

# --- Correlation summary
st.subheader("Lagged Correlation Summary")
corr_df = run_query(db_path, """
    SELECT
        corr(gdp, avg_djia)   AS corr_same_quarter,
        corr(gdp, djia_lead1) AS corr_lag1,
        corr(gdp, djia_lead2) AS corr_lag2
    FROM joined;
""")
st.dataframe(corr_df)

# --- Rolling correlation
st.subheader("Rolling Correlation Over Time")
roll_df = rolling_correlation(db_path, window_size=window)
st.line_chart(roll_df.set_index("quarter_start")["rolling_corr"])

# --- Data preview
if show_data:
    st.subheader("Joined Data (Quarterly)")
    df = run_query(db_path, "SELECT * FROM joined ORDER BY quarter_start;")
    st.dataframe(df)
