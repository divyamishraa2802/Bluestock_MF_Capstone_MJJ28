import pandas as pd
import numpy as np

print("\n=== TASK 5: Investor Cohort Analysis ===")

# Step 1: Load data with correct column names
txn = pd.read_csv('data/raw/08_investor_transactions.csv')
txn['date'] = pd.to_datetime(txn['transaction_date'])  # FIXED: transaction_date
txn['year'] = txn['date'].dt.year

# Step 2: Get first transaction year for each investor
first_txn = txn.groupby('investor_id')['date'].min().reset_index()
first_txn['cohort_year'] = first_txn['date'].dt.year

# Step 3: Merge cohort year back to all transactions
txn = txn.merge(first_txn[['investor_id', 'cohort_year']], on='investor_id')

# Step 4: Filter SIP transactions only - FIXED: transaction_type & amount_inr
sip_txn = txn[txn['transaction_type'] == 'SIP']

# Step 5: Calculate cohort metrics - FIXED: amount_inr
cohort_summary = sip_txn.groupby('cohort_year').agg(
    total_investors=('investor_id', 'nunique'),
    avg_sip_amount=('amount_inr', 'mean'),
    total_invested=('amount_inr', 'sum')
).reset_index()

# Step 6: Find top fund per cohort - FIXED: amount_inr
top_fund = sip_txn.groupby(['cohort_year', 'amfi_code'])['amount_inr'].sum().reset_index()
top_fund = top_fund.sort_values(['cohort_year', 'amount_inr'], ascending=[True, False])
top_fund = top_fund.groupby('cohort_year').first().reset_index()
top_fund = top_fund[['cohort_year', 'amfi_code']].rename(columns={'amfi_code': 'top_fund'})

# Step 7: Merge everything
final_cohort = cohort_summary.merge(top_fund, on='cohort_year')
final_cohort = final_cohort.round(2)

# Step 8: Save CSV
final_cohort.to_csv('reports/task5_cohort_analysis.csv', index=False)
print("Saved: reports/task5_cohort_analysis.csv")
print(final_cohort)
print("=== TASK 5 COMPLETE ===")

# import pandas as pd

# print("\n=== Checking Columns ===")
# txn = pd.read_csv('data/raw/08_investor_transactions.csv')
# print("Columns in file:", txn.columns.tolist())
# print("\nFirst 3 rows:")
# print(txn.head(3))