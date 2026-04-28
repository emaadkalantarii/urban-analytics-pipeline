import pandas as pd
from sqlalchemy import create_engine
import os

DB_PATH = os.path.join("data", "urban_analytics.db")
OUTPUT_DIR = os.path.join("data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}")

df = pd.read_sql("SELECT * FROM permits_clean", con=engine)

df["issue_date"] = pd.to_datetime(df["issue_date"], errors="coerce")
df["application_start_date"] = pd.to_datetime(df["application_start_date"], errors="coerce")
df = df.dropna(subset=["issue_date"])

df["year"] = df["issue_date"].dt.year
df["month"] = df["issue_date"].dt.month
df["month_name"] = df["issue_date"].dt.strftime("%B")
df["quarter"] = df["issue_date"].dt.quarter
df["year_month"] = df["issue_date"].dt.strftime("%Y-%m")
df["days_to_issue"] = (df["issue_date"] - df["application_start_date"]).dt.days

df = df[(df["year"] >= 2018) & (df["year"] <= 2023)].copy()
df = df[df["total_fee"] <= df["total_fee"].quantile(0.99)].copy()
df = df[df["days_to_issue"] >= 0].copy()

df["ward"] = pd.to_numeric(df["ward"], errors="coerce")
df["community_area"] = pd.to_numeric(df["community_area"], errors="coerce")

output_cols = [
    "id", "permit_num", "permit_type", "permit_status", "review_type",
    "work_type", "issue_date", "year", "month", "month_name", "quarter",
    "year_month", "days_to_issue", "total_fee", "building_fee_paid",
    "zoning_fee_paid", "reported_cost", "ward", "community_area",
    "census_tract", "latitude", "longitude"
]

df = df[output_cols]

output_path = os.path.join(OUTPUT_DIR, "permits_final.csv")
df.to_csv(output_path, index=False)

print(f"Exported {len(df):,} rows to permits_final.csv")
print(f"\nColumns: {list(df.columns)}")
print(f"\nYear range: {df['year'].min()} – {df['year'].max()}")
print(f"Permit types: {df['permit_type'].nunique()}")
print(f"Wards covered: {df['ward'].nunique()}")
print(f"Avg total fee: ${df['total_fee'].mean():,.2f}")