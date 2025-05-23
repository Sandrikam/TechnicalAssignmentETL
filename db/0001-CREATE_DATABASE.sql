-- STAGING
CREATE TABLE public.staging_sales (
    id SERIAL PRIMARY KEY,
    sale_id TEXT,
    sale_date TEXT,
    amount NUMERIC,
    currency TEXT,
    affiliate TEXT,
    category TEXT
);

-- DIMENSION TABLES
CREATE TABLE public.dim_currency (
    id SERIAL PRIMARY KEY,
    currency_code TEXT UNIQUE,
    rate_to_usd NUMERIC,
    rate_date DATE
);

CREATE TABLE public.dim_affiliate (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE public.dim_category (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE
);

CREATE TABLE public.dim_date (
    id SERIAL PRIMARY KEY,
    full_date DATE UNIQUE,
    year INT,
    month INT,
    day INT
);

-- FACT TABLE
CREATE TABLE public.fact_sales (
    id SERIAL PRIMARY KEY,
    sale_id TEXT,
    date_id INT REFERENCES dim_date(id),
    currency_id INT REFERENCES dim_currency(id),
    affiliate_id INT REFERENCES dim_affiliate(id),
    category_id INT REFERENCES dim_category(id),
    amount_usd NUMERIC
);
