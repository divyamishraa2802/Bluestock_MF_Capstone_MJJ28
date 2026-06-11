import pandas as pd
from datetime import datetime, timedelta

print("\n=== TASK 6: SIP Continuity Analysis ===")

# Step 1: Load data
txn = pd.read_csv('data/raw/08_investor_transactions.csv')
txn['transaction_date'] = pd.to_datetime(txn['transaction_date'])

# Step 2: Filter SIP only
sip_txn = txn[txn['transaction_type'] == 'SIP'].copy()

# DEBUG: Ye 2 lines se check karo kitne SIP hain
print("Total SIP transactions:", len(sip_txn))
print("Max SIP count per investor-fund:", sip_txn.groupby(['investor_id', 'amfi_code']).size().max())

# Step 3: Count SIPs per investor per fund
sip_counts = sip_txn.groupby(['investor_id', 'amfi_code']).size().reset_index(name='sip_count')

# Step 4: 6+ SIP wale filter karo. Agar empty aaye toh 2 kar dena testing ke liye
eligible = sip_counts[sip_counts['sip_count'] >= 2]  # Pehle 2 se test karo, baad me 6 kar dena

# Step 5: Get last SIP date for eligible investors
last_sip = sip_txn.merge(eligible[['investor_id', 'amfi_code']], on=['investor_id', 'amfi_code'])
last_sip = last_sip.groupby(['investor_id', 'amfi_code'])['transaction_date'].max().reset_index()
last_sip = last_sip.rename(columns={'transaction_date': 'last_sip_date'})

# Step 6: Calculate days since last SIP - aaj ki date 10-06-2026
today = pd.to_datetime('2026-06-10')
last_sip['days_since_last'] = (today - last_sip['last_sip_date']).dt.days

# Step 7: Flag at-risk: 60+ days gap
last_sip['at_risk'] = last_sip['days_since_last'] > 60

# Step 8: Merge SIP count back
final = last_sip.merge(eligible, on=['investor_id', 'amfi_code'])

# Step 9: Save CSV
final = final[['investor_id', 'amfi_code', 'sip_count', 'last_sip_date', 'days_since_last', 'at_risk']]
final.to_csv('reports/task6_sip_continuity.csv', index=False)
print("Saved: reports/task6_sip_continuity.csv")
print(f"Total at-risk investors: {final['at_risk'].sum()} out of {len(final)}")
print(final.head(10))
print("=== TASK 6 COMPLETE ===") 