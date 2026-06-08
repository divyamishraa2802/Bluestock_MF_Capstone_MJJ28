
import pandas as pd
import sqlite3
import os
from pathlib import Path

print("🚀 Day 1: CSV Ingestion Starting...")

# Paths set karo
RAW_PATH = Path("data/raw")
DB_PATH = Path("data/processed/mutual_funds.db")
os.makedirs(DB_PATH.parent, exist_ok=True)

# DB connect karo
conn = sqlite3.connect(DB_PATH)

# Saari 10 CSV files ko loop me padho
csv_files = list(RAW_PATH.glob("*.csv"))

for csv_file in csv_files:
    table_name = csv_file.stem  # file ka naam = table ka naam
    df = pd.read_csv(csv_file)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"✅ Loaded {csv_file.name}: {len(df)} rows")

conn.close()
print("🎉 Day 1 Complete! All 10 CSVs ingested to SQLite DB")
print(f"📊 Database created: {DB_PATH}")