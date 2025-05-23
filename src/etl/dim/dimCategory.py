import pandas as pd
from sqlalchemy import create_engine
import sys
import os

# Import DB config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from db_config import DB_CONFIG

# -- Engine
engine = create_engine(
    f"postgresql+psycopg2://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['dbname']}"
)

# -- Load staging_sales
df = pd.read_sql("SELECT category FROM staging_sales", engine)

df = df.dropna(subset=['category']).drop_duplicates()
df = df.rename(columns={'category': 'name'})

# -- Insert
df.to_sql('dim_category', engine, if_exists='append', index=False, method='multi')

print(f"Inserted {len(df)} rows into dim_category")
