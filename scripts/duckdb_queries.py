"""
duckdb_queries.py
-----------------
Analytic SQL queries for exploring relationships between GDP and stock market data.
Includes same-quarter, 1-quarter, and 2-quarter lag correlations.
"""

from scripts.duckdb_utils import run_query


def create_quarterly_tables(db_path: str):
    """Aggregate daily DJIA data to quarterly and standardize GDP to quarters."""
    print("\n🧮 Creating quarterly summary tables...")

    # DJIA quarterly averages
    run_query(db_path, """
        CREATE OR REPLACE TABLE djia_quarterly AS
        SELECT
            date_trunc('quarter', date) AS quarter_start,
            AVG(value) AS avg_djia
        FROM djia
        GROUP BY 1
        ORDER BY 1;
    """)

    # GDP quarterly (dates are already quarterly)
    run_query(db_path, """
        CREATE OR REPLACE TABLE gdp_quarterly AS
        SELECT
            date_trunc('quarter', date) AS quarter_start,
            value AS gdp
        FROM gdp
        ORDER BY 1;
    """)

    print("✅ Quarterly tables created (djia_quarterly, gdp_quarterly).")


def join_and_compute_correlations(db_path: str):
    """
    Join quarterly GDP and DJIA data, compute lagged correlations.
    Returns a DataFrame with same-quarter, 1-quarter, and 2-quarter lag correlations.
    """
    print("\n🔗 Joining tables and computing correlations ...")

    # Create joined table with multiple lags
    run_query(db_path, """
        CREATE OR REPLACE TABLE joined AS
        SELECT
            g.quarter_start,
            g.gdp,
            dq.avg_djia,
            LAG(dq.avg_djia, 1) OVER (ORDER BY g.quarter_start) AS djia_lead1,
            LAG(dq.avg_djia, 2) OVER (ORDER BY g.quarter_start) AS djia_lead2
        FROM gdp_quarterly g
        LEFT JOIN djia_quarterly dq USING (quarter_start)
        WHERE dq.avg_djia IS NOT NULL
        ORDER BY g.quarter_start;
    """)

    # Compute correlations
    result = run_query(db_path, """
        SELECT
            corr(gdp, avg_djia)   AS corr_same_quarter,
            corr(gdp, djia_lead1) AS corr_lag1,
            corr(gdp, djia_lead2) AS corr_lag2
        FROM joined;
    """)

    return result


def preview_joined_data(db_path: str, limit: int = 10):
    """Return a small sample of the joined dataset for inspection."""
    query = f"""
        SELECT * FROM joined
        ORDER BY quarter_start
        LIMIT {limit};
    """
    df = run_query(db_path, query)
    print("\n📊 Joined table preview:")
    print(df)
    return df


def rolling_correlation(db_path: str, window_size: int = 4):
    """
    Compute rolling (moving) correlation between GDP and DJIA over N-quarter windows.
    Returns a DataFrame with quarter_start and rolling_corr columns.
    """

    print(f"\n📈 Computing rolling {window_size}-quarter correlation ...")

    query = f"""
        SELECT
            quarter_start,
            corr(gdp, avg_djia) OVER (
                ORDER BY quarter_start
                ROWS BETWEEN {window_size - 1} PRECEDING AND CURRENT ROW
            ) AS rolling_corr
        FROM joined
        ORDER BY quarter_start;
    """

    df = run_query(db_path, query)
    return df
