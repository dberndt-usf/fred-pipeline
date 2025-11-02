# 🔍 Challenge: Adding the S&P 500 to the FRED Pipeline

## 🎯 Learning Objectives
This challenge reinforces the **modular design** of the FRED data pipeline, giving you practice extending ETL stages and analytic SQL logic.

You will add a **third dataset** (the S&P 500 Index) to the existing pipeline and compare its correlation with GDP alongside the Dow Jones Industrial Average (DJIA).

---

## 🧩 Steps

### **Step 1 – Identify the FRED Series**
Find the appropriate FRED series ID for the **S&P 500 Index**.  
Hint: It is `SP500` on the [FRED website](https://fred.stlouisfed.org/series/SP500).

### **Step 2 – Extend the FRED Fetch Module**
Modify `scripts/fred_fetch.py` to also fetch and save `SP500` data:
```python
fetch_fred_series("SP500", start_date="2010-01-01")
```
Save the curated CSV as:
```
data/curated/sp500.csv
```

### **Step 3 – Load into DuckDB**
Update `scripts/duckdb_utils.py` so the S&P 500 data loads into a new table:
```
CREATE OR REPLACE TABLE sp500 AS
SELECT * FROM read_csv_auto('data/curated/sp500.csv');
```

### **Step 4 – Add S&P 500 Queries**
In `scripts/duckdb_queries.py`, create a new quarterly aggregation and correlation query:
```sql
CREATE OR REPLACE TABLE sp500_quarterly AS
SELECT
    date_trunc('quarter', date) AS quarter_start,
    AVG(value) AS avg_sp500
FROM sp500
GROUP BY 1
ORDER BY 1;
```

Then compute correlations with GDP, similar to the DJIA section:
```sql
SELECT
    corr(gdp, avg_sp500) AS corr_sp500_same,
    corr(gdp, LAG(avg_sp500, 1) OVER (ORDER BY quarter_start)) AS corr_sp500_lag1
FROM gdp_quarterly
LEFT JOIN sp500_quarterly USING (quarter_start);
```

### **Step 5 – Update Streamlit Dashboard (Optional)**
Modify `scripts/streamlit_dash.py` to visualize the S&P 500 correlations alongside DJIA using color-coded lines or Streamlit tabs:
```python
st.line_chart(df.set_index("quarter_start")[["avg_djia", "avg_sp500"]])
```

---

## 🧠 Discussion Questions

- Which market index (DJIA or S&P 500) appears to **better anticipate GDP movements** over the last decade?  
- Does the **lag correlation** differ significantly between them?  
- How does the rolling correlation pattern compare between the two indices?  

---

## 📦 Deliverables

- Updated pipeline code (`fred_fetch.py`, `duckdb_utils.py`, and `duckdb_queries.py`)  
- Screenshot of your updated Streamlit dashboard  
- Short paragraph (3–4 sentences) interpreting your correlation results  

---

✅ **Extension Idea:** Add a dropdown in Streamlit that lets users select which index (DJIA or S&P 500) to analyze interactively.
