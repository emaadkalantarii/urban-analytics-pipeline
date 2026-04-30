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

A multi-stage data analytics pipeline that ingests, cleans, transforms, and visualizes 833,978 Chicago municipal building permit records. The pipeline covers the full data lifecycle — SQL-based ingestion and cleaning, automated Python ETL with feature engineering, static visualization generation, interactive BI dashboard delivery, and Docker containerization for reproducible execution.

The pipeline is fully automated: a single Docker command runs all stages end-to-end and writes all outputs to your local machine.

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
  - Strips $ symbols, parses fee columns across 16 fields
  - Loads into SQLite (permits_raw table)
  - Filters nulls → permits_clean table (819,820 rows)
        │
        ▼
sql_analysis.py
  - 8 SQL aggregation queries (GROUP BY, COUNT, AVG, SUM, CAST, SUBSTR)
  - Exports: permits_by_type, monthly_trend,
    yearly_summary, permits_by_ward_year,
    top_zip_by_fees, permits_by_status,
    permits_by_work_type, permits_by_review_type
        │
        ▼
pipeline.py
  - Python ETL: date parsing, feature engineering, outlier removal
  - Filters to 2018–2023, removes top 1% fee outliers
  - Produces 5 Matplotlib/Seaborn visualizations (PNG)
  - Exports pipeline_summary.csv
        │
        ▼
export_dashboard_data.py
  - Builds permits_final.csv (dashboard-ready, 238,496 rows)
  - Adds derived columns: year, month, quarter,
    year_month, days_to_issue
        │
        ▼
Tableau Public
  - 4-view interactive dashboard
  - Monthly trend · permit types · geo dot map · yearly KPIs
```

---

## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Data ingestion | Python (Pandas) | Read, parse, clean raw CSV |
| Database | SQLite via SQLAlchemy | Store raw and clean tables |
| Data transformation | SQL | Aggregations, filtering, feature creation |
| Analysis & automation | Python (Pandas, NumPy) | ETL pipeline, feature engineering |
| Visualization | Matplotlib, Seaborn | Static chart generation (5 PNGs) |
| Dashboard | Tableau Public | Interactive stakeholder dashboard |
| Containerization | Docker, docker-compose | Reproducible single-command execution |
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

You have two options. **Option A (Docker)** is recommended — it requires no Python setup and runs the entire pipeline automatically with a single command. **Option B (Local)** runs each script manually in your own Python environment.

---

### Prerequisites — Dataset (required for both options)

1. Go to the [Chicago Data Portal — Building Permits](https://data.cityofchicago.org/Buildings/Building-Permits/ydr8-5enu)
2. Click **Export → CSV** and download the file
3. Rename it to `building_permits.csv` and place it at:

```
data/raw/building_permits.csv
```

> This file is excluded from Git (listed in `.gitignore`) because it is ~150 MB. It must be downloaded manually before running either option.

---

### Option A — Docker (recommended, fully automated)

**Requires:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

Docker installs all dependencies inside an isolated container and runs the full pipeline automatically — no Python installation needed on your machine. All output files are written to your local folders via volume mounts.

```bash
git clone https://github.com/emaadkalantarii/urban-analytics-pipeline.git
cd urban-analytics-pipeline
```

Add the dataset to `data/raw/building_permits.csv`, then run:

```bash
docker-compose up
```

**What happens automatically inside the container:**
1. All Python dependencies are installed from `requirements.docker.txt`
2. `pipeline.py` executes the full ETL and visualization pipeline
3. 5 chart PNGs are saved to `docs/visualizations/`
4. 10 processed CSVs are saved to `data/processed/`
5. Container exits cleanly with code 0

When finished:

```bash
docker-compose down
```

> To also run the SQL analysis and dashboard export steps inside Docker, you can override the default command:
> ```bash
> docker-compose run pipeline python scripts/load_to_db.py
> docker-compose run pipeline python scripts/sql_analysis.py
> docker-compose run pipeline python scripts/export_dashboard_data.py
> ```

---

### Option B — Local Python (manual, step-by-step)

**Requires:** Python 3.11+, Git.

```bash
git clone https://github.com/emaadkalantarii/urban-analytics-pipeline.git
cd urban-analytics-pipeline
```

Create and activate a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run each script in order:

```bash
# Step 1 — Load raw CSV into SQLite and create clean table (819,820 rows)
python scripts/load_to_db.py

# Step 2 — Run 8 SQL aggregation queries, export 8 processed CSVs
python scripts/sql_analysis.py

# Step 3 — Run full ETL pipeline, generate 5 visualizations, export summary
python scripts/pipeline.py

# Step 4 — Export dashboard-ready CSV for Tableau (238,496 rows)
python scripts/export_dashboard_data.py
```

**Expected outputs after all steps:**
- `data/urban_analytics.db` — SQLite database with raw and clean tables
- `data/processed/` — 10 analysis-ready CSV files
- `docs/visualizations/` — 5 PNG chart files
- Terminal prints a yearly summary table with permit counts, fees, and processing times per year

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
| `permits_final.csv` | Full dashboard-ready dataset (238,496 rows) |
