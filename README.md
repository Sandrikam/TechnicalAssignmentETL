# ETL-Reporting-PY

> A Python-based ETL pipeline for processing, normalizing, and reporting sales data.  
> Developed as part of a technical task for **Prime**.

---

## Project Overview

This project demonstrates a full data engineering workflow:

- **Extracts** sales data from a CSV and exchange rates from an API
- **Transforms** and normalizes it into relational `dim` and `fact` tables
- **Loads** the structured data into a PostgreSQL database
- **Generates reports** for downstream analysis and export (CSV, PDF)

---

## Architecture
sourceFile/ (CSV) API (Exchange Rates)
│                     │
▼                     ▼
staging_sales dim_currency
│
├──> dim_date
├──> dim_affiliate
├──> dim_category
▼
fact_sales
▼
reporting_exports/

## Features

- CSV & API ingestion
- Data cleaning and transformation
- Dimensional modeling (`dim_*` and `fact_sales`)
- PostgreSQL integration (via SQLAlchemy + psycopg2)
- Aggregation logic for monthly/category/affiliate reporting
- Export to CSV + PDF
-  Modular ETL script organization

---

## Directory Structure

PrimeTechnical/
├── sourceFile/ # Raw CSV input
├── src/
│ └── etl/
│ ├── dim/ # Dimension loaders
│ ├── fact/ # Fact loader
│ └── ingest/ # CSV/API ingestion
├── db_config.py # Local DB connection (excluded via .gitignore)
├── .gitignore
├── requirements.txt
└── README.md

---

## Setup & Run

### 1. Clone the repo

```bash
git clone https://github.com/Sandrikam/ETL-Reporting-PY.git
cd ETL-Reporting-PY

pip install -r requirements.txt

docker compose up -d

DB_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "dbname": "PrimeDB",
    "user": "admin",
    "password": "admin"
}
```
## Author
### Developed by Sandro Maisuradze
For technical assessment by Prime