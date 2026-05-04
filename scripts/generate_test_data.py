import pandas as pd
import numpy as np
import os

np.random.seed(42)
N = 500

permit_types = [
    "PERMIT - EXPRESS PERMIT PROGRAM",
    "PERMIT - EASY PERMIT PROCESS",
    "PERMIT - RENOVATION/ALTERATION",
    "PERMIT - NEW CONSTRUCTION",
    "PERMIT - SIGNS",
    "PERMIT - WRECKING/DEMOLITION",
    "PERMIT - ELEVATOR EQUIPMENT",
    "PERMIT - SCAFFOLDING",
]

review_types = [
    "EXPRESS PERMIT PROGRAM",
    "EASY PERMIT",
    "STANDARD PLAN REVIEW",
    "SELF CERT",
    "SIGN PERMIT",
]

work_types = [
    "Electrical Work",
    "Monthly Maintenance Permit",
    "Administrative Change",
    "Fire Alarm System",
    "Masonry Work",
    "Reroofing",
]

statuses = ["COMPLETE", "ACTIVE", "PERMIT ISSUED"]

years = np.random.randint(2018, 2024, N)
months = np.random.randint(1, 13, N)
days = np.random.randint(1, 29, N)
issue_dates = [f"{m:02d}/{d:02d}/{y}" for y, m, d in zip(years, months, days)]

app_days_offset = np.random.randint(1, 60, N)
app_years = years.copy()
app_months = months.copy()
app_dates = [f"{m:02d}/{max(1, d - o):02d}/{y}" for y, m, d, o in zip(app_years, app_months, days, app_days_offset)]

fees = np.random.uniform(50, 5000, N).round(2)
fee_strings = [f"${f:,.2f}" for f in fees]

costs = np.random.uniform(5000, 500000, N).round(2)
cost_strings = [f"${c:,.2f}" for c in costs]

lats = np.random.uniform(41.65, 42.02, N)
lons = np.random.uniform(-87.94, -87.52, N)

wards = np.random.randint(1, 51, N)
community_areas = np.random.randint(1, 78, N)
census_tracts = np.random.randint(100000, 999999, N)

permit_nums = [f"#{np.random.randint(1000000, 9999999)}" for _ in range(N)]

df = pd.DataFrame({
    "ID": range(1, N + 1),
    "PERMIT#": permit_nums,
    "PERMIT_STATUS": np.random.choice(statuses, N),
    "PERMIT_MILESTONE": "PERMIT ISSUED",
    "PERMIT_TYPE": np.random.choice(permit_types, N),
    "REVIEW_TYPE": np.random.choice(review_types, N),
    "APPLICATION_START_DATE": app_dates,
    "ISSUE_DATE": issue_dates,
    "PROCESSING_TIME": app_days_offset,
    "STREET_NUMBER": np.random.randint(100, 9999, N),
    "STREET_DIRECTION": np.random.choice(["N", "S", "E", "W"], N),
    "STREET_NAME": "TEST ST",
    "WORK_TYPE": np.random.choice(work_types, N),
    "WORK_DESCRIPTION": "Test permit for CI pipeline validation",
    "PERMIT_CONDITION": "",
    "BUILDING_FEE_PAID": fee_strings,
    "ZONING_FEE_PAID": "$0.00",
    "OTHER_FEE_PAID": "$0.00",
    "SUBTOTAL_PAID": fee_strings,
    "BUILDING_FEE_UNPAID": "$0.00",
    "ZONING_FEE_UNPAID": "$0.00",
    "OTHER_FEE_UNPAID": "$0.00",
    "SUBTOTAL_UNPAID": "$0.00",
    "BUILDING_FEE_WAIVED": "$0.00",
    "BUILDING_FEE_SUBTOTAL": fee_strings,
    "ZONING_FEE_SUBTOTAL": "$0.00",
    "OTHER_FEE_SUBTOTAL": "$0.00",
    "ZONING_FEE_WAIVED": "$0.00",
    "OTHER_FEE_WAIVED": "$0.00",
    "SUBTOTAL_WAIVED": "$0.00",
    "TOTAL_FEE": fee_strings,
    "CONTACT_1_TYPE": "OWNER",
    "CONTACT_1_NAME": "TEST OWNER",
    "CONTACT_1_CITY": "CHICAGO",
    "CONTACT_1_STATE": "IL",
    "CONTACT_1_ZIPCODE": "60601",
    "CONTACT_2_TYPE": "",
    "CONTACT_2_NAME": "",
    "CONTACT_2_CITY": "",
    "CONTACT_2_STATE": "",
    "CONTACT_2_ZIPCODE": "",
    "CONTACT_3_TYPE": "",
    "CONTACT_3_NAME": "",
    "CONTACT_3_CITY": "",
    "CONTACT_3_STATE": "",
    "CONTACT_3_ZIPCODE": "",
    "CONTACT_4_TYPE": "",
    "CONTACT_4_NAME": "",
    "CONTACT_4_CITY": "",
    "CONTACT_4_STATE": "",
    "CONTACT_4_ZIPCODE": "",
    "CONTACT_5_TYPE": "",
    "CONTACT_5_NAME": "",
    "CONTACT_5_CITY": "",
    "CONTACT_5_STATE": "",
    "CONTACT_5_ZIPCODE": "",
    "CONTACT_6_TYPE": "",
    "CONTACT_6_NAME": "",
    "CONTACT_6_CITY": "",
    "CONTACT_6_STATE": "",
    "CONTACT_6_ZIPCODE": "",
    "CONTACT_7_TYPE": "",
    "CONTACT_7_NAME": "",
    "CONTACT_7_CITY": "",
    "CONTACT_7_STATE": "",
    "CONTACT_7_ZIPCODE": "",
    "CONTACT_8_TYPE": "",
    "CONTACT_8_NAME": "",
    "CONTACT_8_CITY": "",
    "CONTACT_8_STATE": "",
    "CONTACT_8_ZIPCODE": "",
    "CONTACT_9_TYPE": "",
    "CONTACT_9_NAME": "",
    "CONTACT_9_CITY": "",
    "CONTACT_9_STATE": "",
    "CONTACT_9_ZIPCODE": "",
    "CONTACT_10_TYPE": "",
    "CONTACT_10_NAME": "",
    "CONTACT_10_CITY": "",
    "CONTACT_10_STATE": "",
    "CONTACT_10_ZIPCODE": "",
    "CONTACT_11_TYPE": "",
    "CONTACT_11_NAME": "",
    "CONTACT_11_CITY": "",
    "CONTACT_11_STATE": "",
    "CONTACT_11_ZIPCODE": "",
    "CONTACT_12_TYPE": "",
    "CONTACT_12_NAME": "",
    "CONTACT_12_CITY": "",
    "CONTACT_12_STATE": "",
    "CONTACT_12_ZIPCODE": "",
    "CONTACT_13_TYPE": "",
    "CONTACT_13_NAME": "",
    "CONTACT_13_CITY": "",
    "CONTACT_13_STATE": "",
    "CONTACT_13_ZIPCODE": "",
    "CONTACT_14_TYPE": "",
    "CONTACT_14_NAME": "",
    "CONTACT_14_CITY": "",
    "CONTACT_14_STATE": "",
    "CONTACT_14_ZIPCODE": "",
    "CONTACT_15_TYPE": "",
    "CONTACT_15_NAME": "",
    "CONTACT_15_CITY": "",
    "CONTACT_15_STATE": "",
    "CONTACT_15_ZIPCODE": "",
    "REPORTED_COST": cost_strings,
    "PIN_LIST": "",
    "COMMUNITY_AREA": community_areas,
    "CENSUS_TRACT": census_tracts,
    "WARD": wards,
    "XCOORDINATE": np.random.uniform(1100000, 1200000, N).round(4),
    "YCOORDINATE": np.random.uniform(1800000, 1950000, N).round(4),
    "LATITUDE": lats.round(11),
    "LONGITUDE": lons.round(11),
    "LOCATION": [f"({lat:.11f}, {lon:.11f})" for lat, lon in zip(lats, lons)],
})

output_path = os.path.join("data", "raw", "building_permits.csv")
os.makedirs(os.path.join("data", "raw"), exist_ok=True)
df.to_csv(output_path, index=False)
print(f"Generated {N} synthetic permit records → {output_path}")
print(f"Columns: {len(df.columns)}")
print(f"Year range: {df['ISSUE_DATE'].str[-4:].unique().tolist()}")