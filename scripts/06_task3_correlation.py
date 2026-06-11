import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("\n=== TASK 3: CORRELATION HEATMAP ===")

# Step 1: Load NAV data again - Isliye 'nav not defined' error nahi aayega
nav = pd.read_csv('data/raw/02_nav_history.csv')
nav['date_parsed'] = pd.to_datetime(nav['date'])  # Tera date column 'date' hai
nav = nav.sort_values(['amfi_code', 'date_parsed'])
nav['daily_return'] = nav.groupby('amfi_code')['nav'].pct_change()
nav = nav.dropna()

# Step 2: Pivot for correlation
returns_pivot = nav.pivot(index='date_parsed', columns='amfi_code', values='daily_return')
correlation_matrix = returns_pivot.corr()
print("Correlation Matrix calculated")
print("Shape:", correlation_matrix.shape)

# Step 3: Plot Heatmap
plt.figure(figsize=(14, 12))
sns.heatmap(correlation_matrix, cmap='RdYlGn', center=0, square=True, 
            cbar_kws={'shrink': 0.8})
plt.title('Mutual Fund Daily Returns Correlation Heatmap', fontsize=16)
plt.tight_layout()
plt.savefig('reports/task3_correlation_heatmap.png', dpi=300)
print("Heatmap saved: reports/task3_correlation_heatmap.png")
plt.show()

# Step 4: Extract top correlated and least correlated pairs - FINAL BOSS FIX
mask = np.triu(np.ones_like(correlation_matrix, dtype=bool), k=1)
corr_values = correlation_matrix.where(mask).unstack().dropna()

# Index ka naam clear kardo pehle, phir reset karo
corr_values.index.names = ['Scheme_1', 'Scheme_2']
corr_pairs = corr_values.reset_index(name='Correlation_Value')

corr_pairs = corr_pairs.sort_values('Correlation_Value', ascending=False)

print("\n=== TOP 5 HIGHLY CORRELATED PAIRS ===")
print("These schemes move together - Low diversification benefit")
print(corr_pairs.head(5))

print("\n=== TOP 5 LEAST CORRELATED PAIRS ===")
print("These schemes move independently - High diversification benefit")
print(corr_pairs.tail(5))

# Save CSV
corr_pairs.to_csv('reports/task3_correlation_pairs.csv', index=False)
print("\nFile saved: reports/task3_correlation_pairs.csv")
print("\n=== TASK 3 COMPLETE ===")