import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from db_config import DB_CONFIG

# -- Generate Engine
engine = create_engine(f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}")

df = pd.read_sql("SELECT * FROM staging_sales", engine)

print (df)

# -- Clean Data
df['sale_date'] = pd.to_datetime(df['sale_date'], errors='coerce')
df = df.dropna(subset=['sale_date'])

dim_date = df.drop_duplicates().rename(columns={'sale_date': 'full_date'})
dim_date['year'] = dim_date['full_date'].dt.year
dim_date['month'] = dim_date['full_date'].dt.month
dim_date['day'] = dim_date['full_date'].dt.day

# -- Keep only expected columns
dim_date = dim_date[['full_date', 'year', 'month', 'day']]
# -- insert Data

dim_date.to_sql('dim_date', engine, if_exists='append', index=False, method='multi')
print(f"Inserted {len(dim_date)} rows into dim_date")
