"""
Bluestock Mutual Fund Capstone Project - Master ETL Pipeline
Author: Divya Mishra
"""

print("Starting Bluestock MF ETL Pipeline...")

import scripts.01_ingest_raw_to_db
print("Step 1/3: Raw data ingestion complete")

import scripts.02_data_cleaning  
print("Step 2/3: Data cleaning complete")

import scripts.05_performance
print("Step 3/3: Performance calculation complete")

print("Pipeline finished! Clean data ready in /data/processed folder.") 