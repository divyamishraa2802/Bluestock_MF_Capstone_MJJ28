import pandas as pd
import sys

print("\n=== TASK 7: Simple Fund Recommender ===")

# Step 1: Risk appetite input lo
if len(sys.argv) > 1:
    risk_appetite = sys.argv[1].lower()
else:
    risk_appetite = input("Enter risk appetite [Low/Medium/High]: ").lower()

print(f"Risk Appetite: {risk_appetite.capitalize()}")

# Step 2: Load file
fund_master = pd.read_csv('data/raw/01_fund_master.csv')
print("Columns:", fund_master.columns.tolist())

# Step 3: risk_category column se filter karo
if 'risk_category' in fund_master.columns:
    if risk_appetite == 'low':
        eligible = fund_master[fund_master['risk_category'].str.contains('Low|Very Low', case=False, na=False)]
    elif risk_appetite == 'medium':
        eligible = fund_master[fund_master['risk_category'].str.contains('Moderate|Medium', case=False, na=False)]
    else: # high
        eligible = fund_master[fund_master['risk_category'].str.contains('High|Very High', case=False, na=False)]
else:
    # Agar risk_category nahi hai toh sub_category use karo
    eligible = fund_master[fund_master['sub_category'].str.contains('Mid|Small|Flexi', case=False, na=False)]

# Step 4: expense_ratio kam ho toh better - usse sort karo
if 'expense_ratio_pct' in eligible.columns:
    top_funds = eligible.sort_values('expense_ratio_pct', ascending=True).head(3)
else:
    top_funds = eligible.head(3)

# Step 5: Save karo
cols_to_save = ['amfi_code', 'scheme_name', 'risk_category', 'sub_category', 'expense_ratio_pct']
cols_to_save = [col for col in cols_to_save if col in top_funds.columns]
top_funds[cols_to_save].to_csv('reports/recommender.py', index=False)

print("\n=== TOP 3 RECOMMENDED FUNDS ===")
print(top_funds[cols_to_save])
print("Saved: reports/recommender.py")
print("=== TASK 7 COMPLETE ===") 