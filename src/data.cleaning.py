# Sales data cleaning project
# cleaning raw sales data for reliable analysis
import re
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# Welcome message
print("=" * 60)
print("Sales Data Cleaning Project!")
print("=" * 60)

# Step 1: Load raw sales data (project-relative path)
raw_data_csv = Path(__file__).parent.parent / "data" / "raw" / "sales_data_raw.csv"
df = pd.read_csv(raw_data_csv)

print("Raw data loaded successfully.")
print(f"Data shape: {df.shape}")
print(df.info())
print(df.head())

# Clean column names: strip, lowercase, replace spaces/special chars with underscores
def clean_column(col):
col = str(col).strip().lower()
col = re.sub(r'[^0-9a-zA-Z]+', '_', col)
col = re.sub(r'_+', '_', col)
return col.strip('_')

df.columns = [clean_column(c) for c in df.columns]
print("Cleaned column names:", df.columns.tolist())

# Step 2: Coerce numeric columns (price, qty)
if 'price' in df.columns:
df['price'] = pd.to_numeric(df['price'], errors='coerce')
elif df.shape[1] >= 3:
df['price'] = pd.to_numeric(df.iloc[:, -3], errors='coerce')

if 'qty' in df.columns:
df['qty'] = pd.to_numeric(df['qty'], errors='coerce')
elif df.shape[1] >= 2:
df['qty'] = pd.to_numeric(df.iloc[:, -2], errors='coerce')

missing_prices = df['price'].isna().sum()
missing_qty = df['qty'].isna().sum()
print(f"Missing prices: {missing_prices}")
print(f"Missing quantities: {missing_qty}")

# Step 3: Sort to make forward/backward fills more effective
sort_cols = [c for c in ['prodname', 'category', 'date_sold'] if c in df.columns]
if sort_cols:
df = df.sort_values(sort_cols)
print(f"Data sorted by {sort_cols} for better imputation.")

# Step 4: Impute missing price and qty within each product/category group, then fill remaining with overall median
group_cols = [c for c in ['prodname', 'category'] if c in df.columns]
for col in ['price', 'qty']:
if col not in df.columns:
continue
orig_missing = df[col].isna()
if group_cols:
df[col] = df.groupby(group_cols)[col].transform(lambda s: s.ffill().bfill())
else:
df[col] = df[col].ffill().bfill()
df[col].fillna(df[col].median(), inplace=True)
df[f'is_{col}_imputed'] = orig_missing.astype(int)
print(f"Imputed missing values in {col} (originally missing: {orig_missing.sum()}).")

# Step 5: Standardize product/category text columns
if 'prodname' in df.columns:
df['prodname'] = df['prodname'].astype('string').str.strip().str.lower()
if 'category' in df.columns:
df['category'] = df['category'].astype('string').str.strip().str.lower()
print("Standardized prodname and category columns where present.")

# Step 6: Remove invalid entries (negative or zero quantities/prices)
if 'qty' in df.columns and 'price' in df.columns:
df = df[(df['qty'] >= 0) & (df['price'] > 0)]
print("Removed invalid entries with negative or zero quantities/prices.")

# Step 7: Convert date_sold to datetime format
if 'date_sold' in df.columns:
df['date_sold'] = pd.to_datetime(df['date_sold'], errors='coerce')
print("Converted date_sold to datetime format.")

print(df.info())
print(df.head())

# Step 8: Save cleaned data to project data/processed folder
processed_dir = Path(__file__).parent.parent / 'data' / 'processed'
processed_dir.mkdir(parents=True, exist_ok=True)
processed_data_csv = processed_dir / 'sales_data_cleaned.csv'
df.to_csv(processed_data_csv, index=False)
print(f"Cleaned data saved to {processed_data_csv}")
