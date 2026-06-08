import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

print("🚀 Day 2: Data Cleaning & Analysis Starting...")

conn = sqlite3.connect('data/processed/mutual_funds.db')

print("\n📊 Checking 01_fund_master table...")
df_funds = pd.read_sql("SELECT * FROM '01_fund_master'", conn)
print(f"Total Funds: {len(df_funds)}")
print(f"Null Values:\n{df_funds.isnull().sum()}")

print("\n📊 Checking 03_aum_by_fund_house table...")
df_aum = pd.read_sql("SELECT * FROM '03_aum_by_fund_house'", conn)

print("\nColumns in AUM table:", df_aum.columns.tolist())

# FIX 1: Column number se uthao, naam se nahi
aum_column = df_aum.columns[3] # 4th column = aum_crore
print(f"Using column: {aum_column}")

top5 = df_aum.nlargest(5, aum_column)
print("\nTop 5 Fund Houses by AUM:")
print(top5[['fund_house', aum_column]])

plt.figure(figsize=(10,6))
plt.bar(top5['fund_house'], top5[aum_column], color='#1f77b4')
plt.title('Top 5 Fund Houses by AUM (in Cr)', fontsize=14, fontweight='bold')
plt.xlabel('Fund House')
plt.ylabel('AUM in Cr')
plt.xticks(rotation=45)
plt.tight_layout()

# FIX 2: Folder pehle banao, phir save karo
os.makedirs('data/processed', exist_ok=True)
plt.savefig('data/processed/top5_aum.png')
print("\n✅ Graph saved: data/processed/top5_aum.png")

plt.show()

conn.close()
print("\n🎉 Day 2 Complete! Data cleaned & first graph ready") 