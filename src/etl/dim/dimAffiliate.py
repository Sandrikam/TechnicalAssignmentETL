import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from db_config import DB_CONFIG

# -- Generate Engine
engine = create_engine(f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}")

df = pd.read_sql("SELECT affiliate FROM staging_sales", engine)

print (df)

# -- Clean Data
df = df.dropna(subset=['affiliate']).drop_duplicates()
df = df.rename(columns={'affiliate': 'name'})

# -- Insert
df.to_sql('dim_affiliate', engine, if_exists='append', index=False, method='multi')
print(f"Inserted {len(df)} rows into dim_date")
