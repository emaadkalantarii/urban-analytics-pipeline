import pandas as pd
import os

RAW_PATH = os.path.join("data", "raw", "building_permits.csv")

df = pd.read_csv(RAW_PATH, nrows=5, low_memory=False)
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

for col in df.columns:
    print(col)