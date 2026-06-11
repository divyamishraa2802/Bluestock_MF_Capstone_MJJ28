import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("\n=== TASK 1: Historical VaR & CVaR ===")

nav = pd.read_csv('data/raw/02_nav_history.csv')
nav['date_parsed'] = pd.to_datetime(nav['date'])
nav = nav.sort_values(['amfi_code', 'date_parsed'])
nav['daily_return'] = nav.groupby('amfi_code')['nav'].pct_change()
nav = nav.dropna()

# Naya tareeka - 100% working
all_results = []
for code, group in nav.groupby('amfi_code'):
    returns = group['daily_return']
    if len(returns) > 5:  # Kam se kam 5 din ka data chahiye
        var_95 = np.percentile(returns, 5) * 100
        cvar_95 = returns[returns <= np.percentile(returns, 5)].mean() * 100
        all_results.append({'amfi_code': code, 'VaR_95': var_95, 'CVaR_95': cvar_95})

results = pd.DataFrame(all_results)
results = results.sort_values('VaR_95')

print("\n=== TOP 5 RISKIEST FUNDS - 95% VaR ===")
print(results.head(5))

results.to_csv('reports/task1_var_cvar.csv', index=False)

plt.figure(figsize=(12, 6))
top_10_risky = results.head(10)
plt.bar(top_10_risky['amfi_code'].astype(str), top_10_risky['VaR_95'], color='crimson')
plt.xlabel('Scheme AMFI Code')
plt.ylabel('VaR 95% (%)')
plt.title('Top 10 Riskiest Funds - 95% Value at Risk')
plt.xticks(rotation=45)
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('reports/task1_var_cvar.png', dpi=300)
print("Chart saved: reports/task1_var_cvar.png")
print("=== TASK 1 COMPLETE ===")



print("\n\n=== TASK 2: Rolling 90-Day Sharpe Ratio ===")

# Step 1: Risk free rate le lo. India me approx 6% per year = 0.06/252 per day
RISK_FREE_DAILY = 0.06 / 252

# Step 2: Har scheme ke liye 90-day rolling Sharpe nikalo
sharpe_results = []

for scheme in nav['amfi_code'].unique():
    scheme_data = nav[nav['amfi_code'] == scheme].copy()
    scheme_data = scheme_data.sort_values('date_parsed')
    
    # 90-day rolling mean and std of daily returns
    rolling_mean = scheme_data['daily_return'].rolling(window=90).mean()
    rolling_std = scheme_data['daily_return'].rolling(window=90).std()
    
    # Sharpe Ratio = (Mean Return - Risk Free Rate) / Std Dev
    # Annualize by multiplying by sqrt(252) trading days
    sharpe_data = pd.DataFrame({
        'date': scheme_data['date_parsed'],
        'amfi_code': scheme,
        'sharpe_90d': ((rolling_mean - RISK_FREE_DAILY) / rolling_std) * np.sqrt(252)
    })
    
    sharpe_results.append(sharpe_data.dropna())

# Step 3: Sab schemes ka data jodo
all_sharpe = pd.concat(sharpe_results)

print("Sharpe Ratio calculated for all schemes")
print(all_sharpe.head(10))

# Step 4: CSV me save karo
# all_sharpe.to_csv('reports/task2_sharpe_90d.csv', index=False)
# print("\nFile saved: reports/task2_sharpe_90d.csv")

# Step 5: Graph banao - Top 5 schemes ka Sharpe Ratio time ke saath
import matplotlib.pyplot as plt

# Top 5 schemes by average Sharpe choose karo
top_5_schemes = all_sharpe.groupby('amfi_code')['sharpe_90d'].mean().nlargest(5).index

plt.figure(figsize=(12, 6))
for scheme in top_5_schemes:
    data = all_sharpe[all_sharpe['amfi_code'] == scheme]
    plt.plot(data['date'], data['sharpe_90d'], label=f'AMFI {scheme}')

plt.title('Rolling 90-Day Sharpe Ratio - Top 5 Schemes')
plt.xlabel('Date')
plt.ylabel('Sharpe Ratio')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('reports/task2_sharpe_graph.png')
print("Graph saved: reports/task2_sharpe_graph.png")
plt.show()

