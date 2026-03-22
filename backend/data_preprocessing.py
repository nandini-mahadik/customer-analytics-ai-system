import pandas as pd

# Load dataset
file_path = "../data/Ecommerce_Customer_Sales_Dataset.csv"
df = pd.read_csv(file_path)

print("Original Data Shape:", df.shape)

# Preview data
print(df.head())

# -----------------------------
# 1. Handle Missing Values
# -----------------------------
print("\nMissing Values:\n", df.isnull().sum())

# Fill numeric missing values with mean
numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

# Fill categorical missing values with mode
categorical_cols = df.select_dtypes(include=['object']).columns
for col in categorical_cols:
    df[col].fillna(df[col].mode()[0], inplace=True)

# -----------------------------
# 2. Remove Duplicates
# -----------------------------
df.drop_duplicates(inplace=True)

# -----------------------------
# 3. Convert Date Columns
# -----------------------------
for col in df.columns:
    if "date" in col.lower():
        df[col] = pd.to_datetime(df[col], errors='coerce')

# -----------------------------
# 4. Save Cleaned Data
# -----------------------------
cleaned_path = "../data/cleaned_data.csv"
df.to_csv(cleaned_path, index=False)

print("\nCleaned Data Shape:", df.shape)
print("Cleaned data saved at:", cleaned_path)

# -----------------------------
# 5. FEATURE ENGINEERING
# -----------------------------

print("\nStarting Feature Engineering...")

# Ensure we have Customer ID
print(df.columns)
if 'Customer_ID' not in df.columns:
    raise Exception("CustomerID column is required")

# Detect required columns (adjust if names differ)
# Try printing df.columns if unsure
print("\nColumns:", df.columns)

# Example assumptions (update if needed)
customer_col = 'Customer_ID'
amount_col = 'Total_Amount'
date_col = 'Order_Date'

# Try to auto-detect columns
for col in df.columns:
    if 'amount' in col.lower() or 'price' in col.lower() or 'sales' in col.lower():
        amount_col = col
    if 'date' in col.lower():
        date_col = col

if amount_col is None or date_col is None:
    raise Exception("Could not detect Amount or Date column. Check dataset.")

print("Using Amount Column:", amount_col)
print("Using Date Column:", date_col)

# -----------------------------
# RFM Calculation
# -----------------------------

# Reference date (latest date in dataset)
reference_date = df[date_col].max()

# Group by customer
rfm = df.groupby(customer_col).agg({
    date_col: lambda x: (reference_date - x.max()).days,  # Recency
    customer_col: 'count',                               # Frequency
    amount_col: 'sum'                                    # Monetary
})

# Rename columns
rfm.columns = ['Recency', 'Frequency', 'Monetary']

# Reset index
rfm = rfm.reset_index()

print("\nRFM Sample:")
print(rfm.head())

# -----------------------------
# Merge RFM back to original data
# -----------------------------
df = df.merge(rfm, on=customer_col, how='left')

# -----------------------------
# Additional Features
# -----------------------------

# Average Order Value
df['Avg_Order_Value'] = df['Monetary'] / df['Frequency']

# -----------------------------
# Save Enhanced Data
# -----------------------------
enhanced_path = "../data/enhanced_data.csv"
df.to_csv(enhanced_path, index=False)

print("\nEnhanced data saved at:", enhanced_path)