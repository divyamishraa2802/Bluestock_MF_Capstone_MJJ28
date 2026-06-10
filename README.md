# BlueStock Mutual Fund Performance Analysis

Capstone project analyzing 1-year performance of 300+ mutual funds using Python, SQL, and Power BI.

## Tech Stack
**Languages:** Python, SQL  
**Libraries:** Pandas, Matplotlib, Seaborn  
**Database:** MySQL  
**Visualization:** Power BI, Python Charts

## Project Structure
- `scripts/` : Data ingestion, cleaning, and analysis Python scripts
- `data/` : Raw, processed, and curated datasets
- `reports/figures/` : Charts and visualizations

## Key Insights
1. Analyzed 1-year returns for 300+ mutual funds
2. Top 5 funds by AUM identified and visualized
3. Created ETL pipeline from raw CSV to curated tables
4. Built interactive Power BI dashboard for fund comparison

 ## Power BI Dashboard - Mutual Fund Industry Analysis
   
Built a 2-page interactive Power BI dashboard analyzing 3 years of AMFI data from Jul 2022 to Jun 2025.

**Key Highlights:**
- Industry AUM doubled from ₹37.7 Lakh Cr to ₹74.4 Lakh Cr
- Equity AUM share increased from 36% to 47% 
- Page 1: Industry Overview with KPI Cards + AUM Trend
- Page 2: Category & AMC Deep Dive using Bar Charts + Treemap

**Tools:** Power BI, DAX, Data Modeling, Data Visualization

**View Dashboard:** [Divya_MutualFund_Dashboard_powerBI.pdf](./MutualFund_Dashboard.pdf)

## How to Run
1. Run `scripts/01_ingest_raw_to_db.py` to load data into MySQL
2. Execute analysis scripts from `scripts/` folder
3. Check `reports/figures/top5_aum.png` for output chart
