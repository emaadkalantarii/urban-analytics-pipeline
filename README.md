# Urban Development Analytics Pipeline

A freelance end-to-end data analytics pipeline analyzing 830,000+ building permit records from the City of Chicago Open Data Portal (2018–2023).

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![SQL](https://img.shields.io/badge/SQL-SQLite-003B57?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![Tableau](https://img.shields.io/badge/Tableau-Public-E97627?style=flat&logo=tableau&logoColor=white)](https://public.tableau.com/app/profile/emad.kalantari/viz/ChicagoUrbanDevelopmentAnalytics/ChicagoUrbanDevelopmentAnalytics20182023)

---

## Live Dashboard

**[View Interactive Tableau Dashboard →](https://public.tableau.com/app/profile/emad.kalantari/viz/ChicagoUrbanDevelopmentAnalytics/ChicagoUrbanDevelopmentAnalytics20182023)**

---

## Project Overview

This project simulates a freelance data analytics engagement for an urban planning stakeholder. Starting from raw municipal data, the pipeline cleans, transforms, and aggregates permit records to surface trends in construction activity, fee revenue, processing efficiency, and geographic distribution across Chicago's 50 wards.

**Key findings:**
- Permit volume dropped 20.7% in 2020 (COVID impact) and did not fully recover through 2023
- Average processing time increased from 17.9 days (2018) to 25.9 days (2023) — a 44% slowdown
- Total fee revenue peaked in 2019 at $27.2M and declined to $20.9M by 2023
- Average reported construction cost rose sharply from $95K (2018) to $194K (2022)

---

## Architecture

Raw CSV (830K rows)
↓
load_to_db.py — cleans fee columns, loads into SQLite
↓
sql_analysis.py — 8 SQL aggregation queries → processed CSVs
↓
pipeline.py — Python ETL + 5 Matplotlib/Seaborn visualizations
↓
export_dashboard_data.py — dashboard-ready CSV
↓
Tableau Public — interactive 4-view dashboard

---

## Tech Stack

| Layer | Tool |
|---|---|
| Data ingestion | Python (Pandas), SQLite |
| Data transformation | SQL (SQLite), Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Dashboard | Tableau Public |
| Containerization | Docker, docker-compose |
| Version control | Git, GitHub |

---

## Visualizations

### Monthly Permit Trend (2018–2023)
![Monthly Trend](docs/visualizations/01_monthly_trend.png)

### Top Permit Types by Volume
![Permit Types](docs/visualizations/02_permit_types.png)

### Annual Volume vs Processing Time
![Yearly Overview](docs/visualizations/03_yearly_volume_vs_processing.png)

### Top 15 Wards by Total Fees
![Fees by Ward](docs/visualizations/04_fees_by_ward.png)

### Processing Time Distribution by Year
![Processing Time](docs/visualizations/05_processing_time_by_year.png)

---

## How to Run

### Option 1 — Docker (recommended)

```bash
git clone https://github.com/emaadkalantarii/urban-analytics-pipeline.git
cd urban-analytics-pipeline
```

Download the dataset from the [Chicago Data Portal](https://data.cityofchicago.org/Buildings/Building-Permits/ydr8-5enu) and save it as `data/raw/building_permits.csv`, then:

```bash
docker-compose up
```

Outputs will appear in `data/processed/` and `docs/visualizations/`.

### Option 2 — Local Python

```bash
git clone https://github.com/emaadkalantarii/urban-analytics-pipeline.git
cd urban-analytics-pipeline
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python scripts/load_to_db.py
python scripts/sql_analysis.py
python scripts/pipeline.py
```

---

## Project Structure

urban-analytics-pipeline/
├── scripts/
│   ├── load_to_db.py             # Ingest raw CSV → SQLite database
│   ├── sql_analysis.py           # SQL aggregations → processed CSVs
│   ├── pipeline.py               # Full ETL + visualization pipeline
│   ├── export_dashboard_data.py  # Export dashboard-ready CSV
│   ├── inspect_columns.py        # Column inspection utility
│   └── diagnose.py               # Data quality diagnostic utility
├── data/
│   ├── raw/                      # Raw source data (not tracked in Git)
│   └── processed/                # Cleaned and aggregated CSVs
├── notebooks/
│   └── 01_eda.ipynb              # Exploratory data analysis
├── docs/
│   └── visualizations/           # Pipeline output charts (PNG)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt              # Full local environment
└── requirements.docker.txt       # Minimal Docker environment

---

## Dataset

**Source:** [City of Chicago — Building Permits](https://data.cityofchicago.org/Buildings/Building-Permits/ydr8-5enu)  
**Size:** 833,978 records | 819,820 after cleaning  
**Period covered:** 2006–2024 (pipeline filters to 2018–2023)  
**License:** Public domain via Chicago Open Data Portal