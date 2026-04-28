import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
from sqlalchemy import create_engine
import os

DB_PATH = os.path.join("data", "urban_analytics.db")
OUTPUT_DIR = os.path.join("data", "processed")
VIZ_DIR = os.path.join("docs", "visualizations")
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(VIZ_DIR, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}")
df = pd.read_sql("SELECT * FROM permits_clean", con=engine)

df["issue_date"] = pd.to_datetime(df["issue_date"], errors="coerce")
df["application_start_date"] = pd.to_datetime(df["application_start_date"], errors="coerce")
df = df.dropna(subset=["issue_date"])
df["year"] = df["issue_date"].dt.year
df["month"] = df["issue_date"].dt.month
df["year_month"] = df["issue_date"].dt.to_period("M")
df["days_to_issue"] = (df["issue_date"] - df["application_start_date"]).dt.days
df = df[(df["year"] >= 2018) & (df["year"] <= 2023)].copy()
df = df[df["total_fee"] <= df["total_fee"].quantile(0.99)].copy()
df = df[df["days_to_issue"] >= 0].copy()

print(f"Pipeline dataset: {len(df):,} rows | {df['year'].min()}–{df['year'].max()}")

sns.set_theme(style="whitegrid", font_scale=1.1)
BLUE = "#2a6496"
PALETTE = sns.color_palette("Blues_d", 8)

monthly = (
    df.groupby("year_month")
    .agg(permits_issued=("id", "count"), total_fees=("total_fee", "sum"))
    .reset_index()
)
monthly["year_month_str"] = monthly["year_month"].astype(str)

fig, ax = plt.subplots(figsize=(14, 5))
ax.plot(monthly["year_month_str"], monthly["permits_issued"], color=BLUE, linewidth=2.2)
ax.fill_between(monthly["year_month_str"], monthly["permits_issued"], alpha=0.12, color=BLUE)
tick_positions = list(range(0, len(monthly), 6))
ax.set_xticks(tick_positions)
ax.set_xticklabels([monthly["year_month_str"].iloc[i] for i in tick_positions], rotation=45, ha="right")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_title("Monthly Building Permits Issued — Chicago (2018–2023)", fontsize=15, pad=14)
ax.set_xlabel("Month")
ax.set_ylabel("Permits Issued")
sns.despine()
plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, "01_monthly_trend.png"), dpi=150)
plt.close()
print("Saved 01_monthly_trend.png")

top_types = df["permit_type"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(11, 6))
bars = ax.barh(top_types.index[::-1], top_types.values[::-1], color=PALETTE)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax.set_title("Top 10 Permit Types by Volume", fontsize=15, pad=14)
ax.set_xlabel("Number of Permits")
ax.set_ylabel("")
for bar, val in zip(bars, top_types.values[::-1]):
    ax.text(bar.get_width() + 100, bar.get_y() + bar.get_height() / 2,
            f"{val:,}", va="center", fontsize=10)
sns.despine()
plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, "02_permit_types.png"), dpi=150)
plt.close()
print("Saved 02_permit_types.png")

yearly = df.groupby("year").agg(
    total_permits=("id", "count"),
    avg_processing_days=("days_to_issue", "mean")
).reset_index()

fig, ax1 = plt.subplots(figsize=(11, 5))
ax2 = ax1.twinx()
ax1.bar(yearly["year"], yearly["total_permits"], color=BLUE, alpha=0.75, width=0.5, label="Total permits")
ax2.plot(yearly["year"], yearly["avg_processing_days"], color="#e74c3c", marker="o",
         linewidth=2.2, markersize=7, label="Avg processing days")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
ax1.set_title("Annual Permit Volume vs Average Processing Time", fontsize=15, pad=14)
ax1.set_xlabel("Year")
ax1.set_ylabel("Total Permits", color=BLUE)
ax2.set_ylabel("Avg Days to Issue", color="#e74c3c")
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")
sns.despine(right=False)
plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, "03_yearly_volume_vs_processing.png"), dpi=150)
plt.close()
print("Saved 03_yearly_volume_vs_processing.png")

ward_fees = (
    df.groupby("ward")["total_fee"]
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)
ward_fees["total_fee_millions"] = ward_fees["total_fee"] / 1_000_000

fig, ax = plt.subplots(figsize=(11, 6))
sns.barplot(data=ward_fees, x="total_fee_millions", y="ward",
            palette="Blues_d", ax=ax, orient="h", order=ward_fees["ward"])
ax.set_title("Top 15 Wards by Total Permit Fees Collected (USD Millions)", fontsize=15, pad=14)
ax.set_xlabel("Total Fees (Millions USD)")
ax.set_ylabel("Ward")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.1f}M"))
sns.despine()
plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, "04_fees_by_ward.png"), dpi=150)
plt.close()
print("Saved 04_fees_by_ward.png")

processing_clean = df[df["days_to_issue"] <= df["days_to_issue"].quantile(0.95)]

fig, ax = plt.subplots(figsize=(11, 5))
sns.boxplot(data=processing_clean, x="year", y="days_to_issue",
            palette="Blues", ax=ax)
ax.set_title("Permit Processing Time Distribution by Year", fontsize=15, pad=14)
ax.set_xlabel("Year")
ax.set_ylabel("Days to Issue")
sns.despine()
plt.tight_layout()
plt.savefig(os.path.join(VIZ_DIR, "05_processing_time_by_year.png"), dpi=150)
plt.close()
print("Saved 05_processing_time_by_year.png")

summary = df.groupby("year").agg(
    total_permits=("id", "count"),
    avg_fee=("total_fee", "mean"),
    total_fees=("total_fee", "sum"),
    avg_reported_cost=("reported_cost", "mean"),
    avg_processing_days=("days_to_issue", "mean"),
    median_processing_days=("days_to_issue", "median")
).round(2).reset_index()

summary.to_csv(os.path.join(OUTPUT_DIR, "pipeline_summary.csv"), index=False)
print("Saved pipeline_summary.csv")

print("\nYearly summary:")
print(summary.to_string(index=False))