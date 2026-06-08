import pandas as pd
import sqlite3
import os

print("Day 3: Data Cleaning Deep Dive Starting")

conn = sqlite3.connect('data/processed/mutual_funds.db')
df = pd.read_sql("SELECT * FROM '01_fund_master'", conn)
conn.close()

print("Original Data Shape:", df.shape)
print("Columns in table:", df.columns.tolist())
print("Null Values BEFORE Cleaning:")
print(df.isnull().sum())

for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].fillna('Unknown')
    else:
        df[col] = df[col].fillna(0)

if 'scheme_name' in df.columns and 'fund_house' in df.columns:
    rows_before = len(df)
    df = df.drop_duplicates(subset=['scheme_name', 'fund_house'], keep='first')
    rows_after = len(df)
    print("Removed duplicate rows:", rows_before - rows_after)

numeric_cols = ['expense_ratio_pct', 'exit_load_pct', 'min_sip_amount', 'min_lumpsum_amount']
for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

print("Null Values AFTER Cleaning:")
print(df.isnull().sum())
print("Cleaned Data Shape:", df.shape)

os.makedirs('data/processed', exist_ok=True)
conn_clean = sqlite3.connect('data/processed/mutual_funds_cleaned.db')
df.to_sql('fund_master_clean', conn_clean, if_exists='replace', index=False)
conn_clean.close()

print("Clean data saved: data/processed/mutual_funds_cleaned.db")
print("Day 3 Complete") 
import sqlite3
conn = sqlite3.connect('data/processed/mutual_funds_cleaned.db')
df.to_sql('funds', conn, if_exists='replace', index=False)
conn.close()
print("✅ DB me 'funds' table ban gayi with", len(df), "rows")