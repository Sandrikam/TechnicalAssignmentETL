import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from db_config import DB_CONFIG

# Connect via SQLAlchemy
engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
)


staging = pd.read_sql("SELECT * FROM staging_sales", engine)

dim_date = pd.read_sql("SELECT id AS date_id, full_date FROM dim_date", engine)
dim_date['full_date'] = pd.to_datetime(dim_date['full_date'], errors='coerce')


dim_aff = pd.read_sql("SELECT id AS affiliate_id, name FROM dim_affiliate", engine)

dim_cat = pd.read_sql("SELECT id AS category_id, name FROM dim_category", engine)

dim_curr = pd.read_sql("SELECT id AS currency_id, currency_code, rate_to_usd FROM dim_currency", engine)

# -- Clean
staging['sale_date'] = pd.to_datetime(staging['sale_date'], errors='coerce')

df = staging.merge(dim_date, left_on='sale_date', right_on='full_date', how='left')
df = df.merge(dim_aff, left_on='affiliate', right_on='name', how='left')
df = df.merge(dim_cat, left_on='category', right_on='name', how='left')
df = df.merge(dim_curr, left_on='currency', right_on='currency_code', how='left')

# -- Calculate USD
df['amount_usd'] = df['amount'] / df['rate_to_usd']

# -- Prepare fact table
fact = df[['sale_id', 'date_id', 'currency_id', 'affiliate_id', 'category_id', 'amount_usd']]
fact = fact.astype(object).where(pd.notnull(fact), None)

# -- Insert
conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

cursor.executemany("""
    INSERT INTO fact_sales (sale_id, date_id, currency_id, affiliate_id, category_id, amount_usd)
    VALUES (%s, %s, %s, %s, %s, %s)
""", fact.values.tolist())

conn.commit()
cursor.close()
conn.close()

print(f"Inserted {len(fact)} rows into fact_sales")
