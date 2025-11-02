# 🧮 FRED Data Pipeline

**A lightweight, end-to-end Python data pipeline** demonstrating the full data lifecycle:
fetching economic data from the [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/) API, 
curating and storing it locally, loading it into a DuckDB warehouse, 
and running analytic SQL queries — including multi-lag and rolling correlations between **GDP** and **DJIA**.

---

## 🎯 Learning Objectives

Students will learn how to:

1. **Extract** data from a REST API (FRED) using Python and `requests`.  
2. **Transform & curate** data from raw JSON to clean CSV.  
3. **Load & analyze** data in an embedded analytics database (DuckDB).  
4. **Explore correlations** between stock market and GDP data using SQL lag and window functions.  

---

## 🧱 Directory Structure

```
fred-pipeline/
├── data/
│   ├── raw/          # Raw JSON files from the API
│   ├── curated/      # Clean CSVs ready for analytics
│   └── warehouse/    # DuckDB database (.duckdb)
│
├── scripts/
│   ├── fred_fetch.py       # Fetches series from FRED API
│   ├── duckdb_utils.py     # Loads and queries DuckDB
│   └── duckdb_queries.py   # Analytic SQL (aggregations, lag, rolling correlation)
│
├── main.py           # Orchestration script (runs all pipeline stages)
├── .env              # Contains your FRED_API_KEY
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourname/fred-pipeline.git
   cd fred-pipeline
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv-pipe
   source .venv-pipe/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your FRED API key**

   Create a `.env` file at the project root:
   ```bash
   FRED_API_KEY=your_api_key_here
   ```

   Obtain your key from [FRED’s Developer Portal](https://fred.stlouisfed.org/docs/api/fred/).

---

## 🚀 Running the Pipeline

```bash
python main.py
```

This will:

1. Fetch **GDP** and **DJIA** data from FRED (`scripts/fred_fetch.py`)  
2. Save raw JSON and curated CSV files under `/data/`  
3. Load those CSVs into DuckDB (`scripts/duckdb_utils.py`)  
4. Create quarterly tables and compute:  
   - Same-quarter correlation  
   - 1-quarter lag correlation  
   - 2-quarter lag correlation  
   - 4-quarter rolling correlation  

---

## 📊 Sample Output

```
📊 Correlation results:
   corr_same_quarter  corr_lag1  corr_lag2
0             0.9510      0.9484      0.9442

📈 Rolling correlation (4-quarter window):
   quarter_start  rolling_corr
57    2024-04-01      0.896810
58    2024-07-01      0.910782
59    2024-10-01      0.922337
60    2025-01-01      0.971350
61    2025-04-01      0.172703
```

---

## 🧠 Pedagogical Notes

| Stage | Tool | Concept | Deliverable |
|-------|------|----------|--------------|
| **1️⃣ Extract** | Python + FRED API | REST, JSON, Environment Variables | `/data/raw/` |
| **2️⃣ Transform** | pandas | Data cleaning, CSV export | `/data/curated/` |
| **3️⃣ Load** | DuckDB | SQL table creation, in-process OLAP | `/data/warehouse/fred.duckdb` |
| **4️⃣ Analyze** | SQL analytics | Multi-lag correlation, rolling correlation | printed results |

---

## 🧩 Requirements

```
requests
pandas
python-dotenv
duckdb
```

*(Optional for visualization)*  
```
streamlit
```

---

## 💡 Next Steps

- Add **Streamlit dashboards** to visualize GDP vs DJIA and rolling correlations.  
- Include **more FRED series** (CPI, unemployment, Fed Funds Rate) for macro comparisons.  
- Integrate **MLflow** to track correlation results and model experiments.  


