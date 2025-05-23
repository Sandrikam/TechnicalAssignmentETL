import pandas as pd
import psycopg2
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from db_config import DB_CONFIG

# -- Declare Globals
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.abspath(os.path.join(base_dir, '../../sourceFile/test_data.csv'))

# -- Connect To DB
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# -- Load CSV
df = pd.read_csv(csv_path)

# -- Clean Data
df['sales_amount'] = df['sales_amount'].fillna(0.0)
df['currency'] = df['currency'].fillna('USD')
df['order_date'] = df['order_date'].fillna('1900-01-01')
df['category'] = df['category'].replace({np.nan: None})

# -- Insert rows
insert_query = """
    INSERT INTO staging_sales (sale_id, affiliate, amount, currency, sale_date, category)
    VALUES (%s, %s, %s, %s, %s, %s)
"""


rows = df.astype(object).where(pd.notnull(df), None).values.tolist()
cursor.executemany(insert_query, rows)

conn.commit()
cursor.close()
conn.close()

print(f"Inserted {len(rows)} rows into staging_sales")
