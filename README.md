# Urban Development Analytics Pipeline

End-to-end data analytics pipeline analyzing **833,978 building permit records** from the City of Chicago Open Data Portal (2018–2023), built as a freelance data analytics engagement.

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![SQL](https://img.shields.io/badge/SQL-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![Tableau](https://img.shields.io/badge/Tableau-Live%20Dashboard-E97627?style=flat&logo=tableau&logoColor=white)](https://public.tableau.com/app/profile/emad.kalantari/viz/ChicagoUrbanDevelopmentAnalytics/ChicagoUrbanDevelopmentAnalytics20182023)

---

## Live Dashboard

**[View Interactive Tableau Dashboard →](https://public.tableau.com/app/profile/emad.kalantari/viz/ChicagoUrbanDevelopmentAnalytics/ChicagoUrbanDevelopmentAnalytics20182023)**

---

## Project Overview

This project simulates a freelance analytics engagement for an urban planning stakeholder. Raw municipal permit data is ingested, cleaned, and transformed through a multi-stage pipeline to surface trends in construction activity, fee revenue, processing efficiency, and geographic distribution across Chicago's 50 wards.

The pipeline is fully automated and containerized — a single Docker command reproduces all outputs from raw data to final visualizations.

---

## Key Findings

| Metric | Value |
|---|---|
| Total permits analyzed | 238,496 (2018–2023 filtered) |
| Permit volume drop in 2020 | −20.7% (COVID impact) |
| Processing time increase 2018→2023 | 17.9 days → 25.9 days (+44%) |
| Peak fee revenue year | 2019 at $27.2M total |
| Average reported construction cost 2022 | $194,549 (vs $95,302 in 2018) |

---

## Architecture

```
Raw CSV (833,978 rows)
        │
        ▼
load_to_db.py
  - Strips $ symbols, parses fee columns
  - Loads into SQLite (permits_raw table)
  - Filters nulls → permits_clean table (819,820 rows)
        │
        ▼
sql_analysis.py
  - 8 SQL aggregation queries
  - Exports: permits_by_type, monthly_trend,
    yearly_summary, permits_by_ward_year,
    top_zip_by_fees, permits_by_status,
    permits_by_work_type, permits_by_review_type
        │
        ▼
pipeline.py
  - Python ETL: date parsing, feature engineering
  - Filters to 2018–2023, removes outliers
  - Produces 5 Matplotlib/Seaborn visualizations
  - Exports pipeline_summary.csv
        │
        ▼
export_dashboard_data.py
  - Builds permits_final.csv (dashboard-ready)
  - Adds derived columns: year, month, quarter,
    year_month, days_to_issue
        │
        ▼
Tableau Public
  - 4-view interactive dashboard
  - Monthly trend, permit types, geo map, KPIs
```

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Data ingestion | Python (Pandas) | Read, parse, clean raw CSV |
| Database | SQLite via SQLAlchemy | Store raw and clean tables |
| Data transformation | SQL | Aggregations, filtering, feature creation |
| Analysis & automation | Python (Pandas, NumPy) | ETL pipeline, feature engineering |
| Visualization | Matplotlib, Seaborn | Static chart generation |
| Dashboard | Tableau Public | Interactive stakeholder dashboard |
| Containerization | Docker, docker-compose | Reproducible pipeline execution |
| Version control | Git, GitHub | Source control and portfolio hosting |

---

## Visualizations

### Monthly Permit Trend (2018–2023)
![Monthly Trend](docs/visualizations/01_monthly_trend.png)

### Top Permit Types by Volume
![Permit Types](docs/visualizations/02_permit_types.png)

### Annual Volume vs Average Processing Time
![Yearly Overview](docs/visualizations/03_yearly_volume_vs_processing.png)

### Top 15 Wards by Total Fees Collected
![Fees by Ward](docs/visualizations/04_fees_by_ward.png)

### Processing Time Distribution by Year
![Processing Time](docs/visualizations/05_processing_time_by_year.png)

---

## Project Structure

```
urban-analytics-pipeline/
├── scripts/
│   ├── load_to_db.py               # Ingest raw CSV → SQLite database
│   ├── sql_analysis.py             # SQL aggregations → processed CSVs
│   ├── pipeline.py                 # Full ETL + visualization pipeline
│   ├── export_dashboard_data.py    # Export dashboard-ready CSV
│   ├── inspect_columns.py          # Column inspection utility
│   └── diagnose.py                 # Data quality diagnostic utility
├── data/
│   ├── raw/                        # Raw source data (not tracked in Git)
│   └── processed/                  # Cleaned and aggregated CSVs
├── notebooks/
│   └── 01_eda.ipynb                # Exploratory data analysis
├── docs/
│   └── visualizations/             # Pipeline output charts (PNG)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt                # Full local environment
└── requirements.docker.txt         # Minimal Docker environment
```

---

## How to Run

### Option 1 — Docker (recommended)

Clone the repo and add the dataset:

```bash
git clone https://github.com/emaadkalantarii/urban-analytics-pipeline.git
cd urban-analytics-pipeline
```

Download the dataset from the [Chicago Data Portal](https://data.cityofchicago.org/Buildings/Building-Permits/ydr8-5enu) and save it as:

```
data/raw/building_permits.csv
```

Then run the full pipeline:

```bash
docker-compose up
```

All outputs will appear in `data/processed/` and `docs/visualizations/`.

### Option 2 — Local Python (Windows)

```bash
git clone https://github.com/emaadkalantarii/urban-analytics-pipeline.git
cd urban-analytics-pipeline
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python scripts/load_to_db.py
python scripts/sql_analysis.py
python scripts/pipeline.py
python scripts/export_dashboard_data.py
```

---

## Dataset

| Field | Detail |
|---|---|
| Source | [City of Chicago — Building Permits](https://data.cityofchicago.org/Buildings/Building-Permits/ydr8-5enu) |
| Total records | 833,978 |
| Records after cleaning | 819,820 |
| Pipeline working range | 2018–2023 |
| License | Public domain — Chicago Open Data Portal |

---

## Pipeline Outputs

| File | Description |
|---|---|
| `permits_by_type.csv` | Permit counts and fees by permit type |
| `permits_by_ward_year.csv` | Ward-level breakdown by year |
| `monthly_trend.csv` | Monthly permit volume and fee totals |
| `yearly_summary.csv` | Year-over-year KPI summary |
| `top_zip_by_fees.csv` | Top 20 community areas by fee revenue |
| `permits_by_status.csv` | Distribution by permit status |
| `permits_by_work_type.csv` | Distribution by work type |
| `permits_by_review_type.csv` | Distribution by review type |
| `pipeline_summary.csv` | Final aggregated yearly summary |
| `permits_final.csv` | Full dashboard-ready dataset |
