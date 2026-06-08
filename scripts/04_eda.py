import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import os

print("Day 3: EDA Starting")

conn = sqlite3.connect('data/processed/mutual_funds_cleaned.db')
df = pd.read_sql("SELECT * FROM 'fund_master_clean'", conn)
conn.close()

print("Total Funds in Data:", len(df))
print("\nColumn Names:")
print(df.columns.tolist())

print("\n1. Konsa Fund House Sabse Bada Hai:")
print(df['fund_house'].value_counts().head(5))

print("\n2. Kis Category Me Kitne Funds:")
print(df['category'].value_counts())

print("\n3. Risk Level Ka Distribution:")
if 'risk_category' in df.columns:
    print(df['risk_category'].value_counts())

print("\n4. Expense Ratio Ka Average:")
if 'expense_ratio_pct' in df.columns:
    print("Average Expense Ratio:", df['expense_ratio_pct'].mean().round(2), "%")

os.makedirs('data/processed', exist_ok=True)

plt.figure(figsize=(10, 6))
df['fund_house'].value_counts().head(5).plot(kind='bar', color='purple')
plt.title('Top 5 Fund Houses')
plt.xlabel('Fund House Name')
plt.ylabel('Number of Funds')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('data/processed/day3_fund_house.png')
print("\nGraph 1 Saved: data/processed/day3_fund_house.png")

plt.figure(figsize=(8, 8))
df['category'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Funds by Category')
plt.ylabel('')
plt.tight_layout()
plt.savefig('data/processed/day3_category.png')
print("Graph 2 Saved: data/processed/day3_category.png")

plt.show()
print("\nDay 3 EDA Complete") 