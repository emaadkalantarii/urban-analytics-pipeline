import pandas as pd
from sqlalchemy import create_engine
import os

DB_PATH = os.path.join("data", "urban_analytics.db")
OUTPUT_DIR = os.path.join("data", "processed")
os.makedirs(OUTPUT_DIR, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}")

queries = {
    "permits_by_type": """
        SELECT
            permit_type,
            COUNT(*) AS total_permits,
            ROUND(AVG(total_fee), 2) AS avg_fee,
            ROUND(SUM(total_fee), 2) AS total_fees
        FROM permits_clean
        GROUP BY permit_type
        ORDER BY total_permits DESC
    """,

    "permits_by_ward_year": """
        SELECT
            ward,
            CAST(SUBSTR(issue_date, 7, 4) AS INTEGER) AS issue_year,
            COUNT(*) AS total_permits,
            ROUND(AVG(total_fee), 2) AS avg_fee,
            ROUND(SUM(total_fee), 2) AS total_fees,
            ROUND(AVG(reported_cost), 2) AS avg_reported_cost
        FROM permits_clean
        WHERE CAST(SUBSTR(issue_date, 7, 4) AS INTEGER) BETWEEN 2018 AND 2023
          AND ward IS NOT NULL
        GROUP BY ward, issue_year
        ORDER BY issue_year, ward
    """,

    "top_zip_by_fees": """
        SELECT
            SUBSTR(location, 1, 50) AS area_label,
            community_area,
            COUNT(*) AS permit_count,
            ROUND(SUM(total_fee), 2) AS total_fees,
            ROUND(AVG(total_fee), 2) AS avg_fee,
            ROUND(SUM(reported_cost), 2) AS total_reported_cost
        FROM permits_clean
        WHERE community_area IS NOT NULL
        GROUP BY community_area
        ORDER BY total_fees DESC
        LIMIT 20
    """,

    "monthly_trend": """
        SELECT
            SUBSTR(issue_date, 7, 4) || '-' || SUBSTR(issue_date, 1, 2) AS year_month,
            COUNT(*) AS permits_issued,
            ROUND(SUM(total_fee), 2) AS total_fees,
            ROUND(AVG(total_fee), 2) AS avg_fee
        FROM permits_clean
        WHERE CAST(SUBSTR(issue_date, 7, 4) AS INTEGER) BETWEEN 2018 AND 2023
        GROUP BY year_month
        ORDER BY year_month
    """,

    "yearly_summary": """
        SELECT
            CAST(SUBSTR(issue_date, 7, 4) AS INTEGER) AS issue_year,
            COUNT(*) AS total_permits,
            ROUND(AVG(total_fee), 2) AS avg_fee,
            ROUND(SUM(total_fee), 2) AS total_fees,
            ROUND(AVG(reported_cost), 2) AS avg_reported_cost,
            ROUND(AVG(CAST(processing_time AS FLOAT)), 1) AS avg_processing_days
        FROM permits_clean
        WHERE CAST(SUBSTR(issue_date, 7, 4) AS INTEGER) BETWEEN 2018 AND 2023
        GROUP BY issue_year
        ORDER BY issue_year
    """,

    "permits_by_status": """
        SELECT
            permit_status,
            COUNT(*) AS total_permits,
            ROUND(AVG(total_fee), 2) AS avg_fee
        FROM permits_clean
        WHERE permit_status IS NOT NULL
        GROUP BY permit_status
        ORDER BY total_permits DESC
    """,

    "permits_by_work_type": """
        SELECT
            work_type,
            COUNT(*) AS total_permits,
            ROUND(AVG(total_fee), 2) AS avg_fee,
            ROUND(AVG(reported_cost), 2) AS avg_reported_cost
        FROM permits_clean
        WHERE work_type IS NOT NULL
        GROUP BY work_type
        ORDER BY total_permits DESC
    """,

    "permits_by_review_type": """
        SELECT
            review_type,
            COUNT(*) AS total_permits,
            ROUND(AVG(total_fee), 2) AS avg_fee,
            ROUND(SUM(total_fee), 2) AS total_fees
        FROM permits_clean
        WHERE review_type IS NOT NULL
        GROUP BY review_type
        ORDER BY total_permits DESC
    """
}

for name, query in queries.items():
    df = pd.read_sql(query, con=engine)
    output_path = os.path.join(OUTPUT_DIR, f"{name}.csv")
    df.to_csv(output_path, index=False)
    print(f"Saved {name}.csv — {len(df):,} rows")

print(f"\nAll processed CSVs saved to: {OUTPUT_DIR}")