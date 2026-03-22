import sqlite3
import pandas as pd

# Load enhanced data
#df = pd.read_csv("../data/enhanced_data.csv")
df = pd.read_csv("../data/segmented_data.csv")

""""
# Connect to SQLite DB
conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Save dataframe to DB
df.to_sql("customers", conn, if_exists="replace", index=False)

print("✅ Data inserted into database successfully!")

conn.close()
"""

conn = sqlite3.connect("ecommerce.db")
cursor = conn.cursor()

# Create predictions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Recency INTEGER,
    Frequency INTEGER,
    Monetary REAL,
    Avg_Order_Value REAL,
    Purchase_Prediction INTEGER,
    Churn_Prediction INTEGER
)
""")

conn.commit()
conn.close()

print("✅ Predictions table created!")