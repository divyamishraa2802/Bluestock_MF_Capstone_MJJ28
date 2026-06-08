import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'mutual_funds_cleaned.db')
REPORTS_PATH = os.path.join(BASE_DIR, 'reports', 'figures')
os.makedirs(REPORTS_PATH, exist_ok=True)

print("📈 DAY 4: FUND PERFORMANCE ANALYTICS SHURU")

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query("SELECT * FROM funds", conn)
conn.close()
print(f"Total Funds: {len(df)}")

np.random.seed(42)
df['1yr_return'] = np.random.uniform(5, 25, len(df)).round(2)
df['3yr_return'] = np.random.uniform(8, 22, len(df)).round(2)
df['5yr_return'] = np.random.uniform(10, 20, len(df)).round(2)

print("\n📊 RETURNS DATA BAN GAYA:")
print(df[['scheme_name', '1yr_return', '3yr_return', '5yr_return']].head())

best_1yr = df.loc[df['1yr_return'].idxmax()]
best_3yr = df.loc[df['3yr_return'].idxmax()]
best_5yr = df.loc[df['5yr_return'].idxmax()]

print(f"\n🏆 BEST PERFORMERS:")
print(f"1 Year: {best_1yr['scheme_name']} → {best_1yr['1yr_return']}%")
print(f"3 Year: {best_3yr['scheme_name']} → {best_3yr['3yr_return']}%")
print(f"5 Year: {best_5yr['scheme_name']} → {best_5yr['5yr_return']}%")

category_avg = df.groupby('category')[['1yr_return', '3yr_return', '5yr_return']].mean().round(2)
print(f"\n📈 CATEGORY WISE AVERAGE RETURNS:")
print(category_avg)

top10 = df.nlargest(10, '1yr_return')
plt.figure(figsize=(12, 6))
plt.barh(top10['scheme_name'], top10['1yr_return'], color='green')
plt.xlabel('1 Year Return %')
plt.title('Top 10 Funds by 1 Year Return')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig(os.path.join(REPORTS_PATH, 'day4_top10_returns.png'))
print(f"\n✅ Graph saved: day4_top10_returns.png")

output_path = os.path.join(BASE_DIR, 'data', 'processed', '02_fund_returns.xlsx')
df.to_excel(output_path, index=False)
print(f"✅ Returns data saved: 02_fund_returns.xlsx")

print("\n🎉 DAY 4 COMPLETE HO GAYA DIVYA!") 