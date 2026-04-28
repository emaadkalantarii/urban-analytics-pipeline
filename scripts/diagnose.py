import pandas as pd
from sqlalchemy import create_engine, text
import os

DB_PATH = os.path.join("data", "urban_analytics.db")
engine = create_engine(f"sqlite:///{DB_PATH}")

with engine.connect() as conn:
    total = conn.execute(text("SELECT COUNT(*) FROM permits_raw")).fetchone()[0]
    print(f"Total rows in permits_raw: {total:,}")

    sample = conn.execute(text("""
        SELECT issue_date, latitude, longitude, total_fee
        FROM permits_raw
        LIMIT 10
    """)).fetchall()

    print("\nSample rows (issue_date | latitude | longitude | total_fee):")
    for row in sample:
        print(row)

    null_dates = conn.execute(text("SELECT COUNT(*) FROM permits_raw WHERE issue_date IS NULL")).fetchone()[0]
    null_lat = conn.execute(text("SELECT COUNT(*) FROM permits_raw WHERE latitude IS NULL")).fetchone()[0]
    null_lon = conn.execute(text("SELECT COUNT(*) FROM permits_raw WHERE longitude IS NULL")).fetchone()[0]
    zero_fee = conn.execute(text("SELECT COUNT(*) FROM permits_raw WHERE total_fee <= 0")).fetchone()[0]
    null_fee = conn.execute(text("SELECT COUNT(*) FROM permits_raw WHERE total_fee IS NULL")).fetchone()[0]

    print(f"\nRows with NULL issue_date:  {null_dates:,}")
    print(f"Rows with NULL latitude:    {null_lat:,}")
    print(f"Rows with NULL longitude:   {null_lon:,}")
    print(f"Rows with NULL total_fee:   {null_fee:,}")
    print(f"Rows with total_fee <= 0:   {zero_fee:,}")