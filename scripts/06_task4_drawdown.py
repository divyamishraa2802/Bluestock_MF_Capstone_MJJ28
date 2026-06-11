import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("\n=== TASK 4: MAXIMUM DRAWDOWN ===")

# Step 1: Load NAV data
nav = pd.read_csv('data/raw/02_nav_history.csv')
nav['date_parsed'] = pd.to_datetime(nav['date'])
nav = nav.sort_values(['amfi_code', 'date_parsed'])

# Step 2: Calculate Max Drawdown for each scheme
def calculate_max_drawdown(nav_series):
    # Cumulative max - running peak
    running_max = nav_series.cummax()
    # Drawdown = (NAV - Peak) / Peak
    drawdown = (nav_series - running_max) / running_max
    # Max drawdown = minimum value of drawdown
    max_drawdown = drawdown.min()
    return max_drawdown

# Apply to all schemes
max_dd_results = nav.groupby('amfi_code')['nav'].apply(calculate_max_drawdown).reset_index()
max_dd_results.columns = ['amfi_code', 'Max_Drawdown']
max_dd_results['Max_Drawdown_Pct'] = max_dd_results['Max_Drawdown'] * 100

# Sort by worst drawdown
max_dd_results = max_dd_results.sort_values('Max_Drawdown_Pct')

print("\n=== TOP 5 WORST MAX DRAWDOWNS ===")
print("Schemes with highest risk - Biggest peak-to-trough fall")
print(max_dd_results.head(5))

print("\n=== TOP 5 BEST MAX DRAWDOWNS ===")
print("Schemes with lowest risk - Smallest peak-to-trough fall")
print(max_dd_results.tail(5))

# Step 3: Plot bar chart of worst 10 drawdowns
plt.figure(figsize=(12, 6))
worst_10 = max_dd_results.head(10)
plt.bar(worst_10['amfi_code'].astype(str), worst_10['Max_Drawdown_Pct'], color='crimson')
plt.xlabel('Scheme AMFI Code')
plt.ylabel('Max Drawdown %')
plt.title('Top 10 Schemes with Worst Max Drawdown')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('reports/task4_max_drawdown.png', dpi=300)
print("\nChart saved: reports/task4_max_drawdown.png")

# Save CSV
max_dd_results.to_csv('reports/task4_max_drawdown.csv', index=False)
print("File saved: reports/task4_max_drawdown.csv")
print("\n=== TASK 4 COMPLETE ===")
print("\n🎉 ALL 4 TASKS COMPLETE! 🎉") 