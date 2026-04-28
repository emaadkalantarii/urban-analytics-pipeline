import pandas as pd
from sqlalchemy import create_engine, text
import os

RAW_PATH = os.path.join("data", "raw", "building_permits.csv")
DB_PATH = os.path.join("data", "urban_analytics.db")

engine = create_engine(f"sqlite:///{DB_PATH}")

df = pd.read_csv(RAW_PATH, low_memory=False)
df.columns = [col.strip().lower().replace(" ", "_").replace("#", "_num") for col in df.columns]

fee_columns = [
    "building_fee_paid", "zoning_fee_paid", "other_fee_paid",
    "subtotal_paid", "building_fee_unpaid", "zoning_fee_unpaid",
    "other_fee_unpaid", "subtotal_unpaid", "building_fee_waived",
    "building_fee_subtotal", "zoning_fee_subtotal", "other_fee_subtotal",
    "zoning_fee_waived", "other_fee_waived", "subtotal_waived", "total_fee"
]

for col in fee_columns:
    if col in df.columns:
        df[col] = (
            df[col].astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

df["reported_cost"] = pd.to_numeric(
    df["reported_cost"].astype(str).str.replace("$", "", regex=False).str.replace(",", "", regex=False).str.strip(),
    errors="coerce"
)

df.to_sql("permits_raw", con=engine, if_exists="replace", index=False)
print(f"Loaded {len(df):,} rows into permits_raw.")

with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS permits_clean"))
    conn.execute(text("""
        CREATE TABLE permits_clean AS
        SELECT
            id,
            permit_num,
            permit_status,
            permit_milestone,
            permit_type,
            review_type,
            application_start_date,
            issue_date,
            processing_time,
            street_number,
            street_direction,
            street_name,
            work_type,
            work_description,
            building_fee_paid,
            zoning_fee_paid,
            other_fee_paid,
            total_fee,
            reported_cost,
            community_area,
            census_tract,
            ward,
            latitude,
            longitude,
            location
        FROM permits_raw
        WHERE issue_date IS NOT NULL
          AND latitude IS NOT NULL
          AND longitude IS NOT NULL
          AND total_fee > 0
    """))
    conn.commit()

with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM permits_clean"))
    count = result.fetchone()[0]

print(f"Clean table created with {count:,} rows.")
print(f"Database saved at: {DB_PATH}")