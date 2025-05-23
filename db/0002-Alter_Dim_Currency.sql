ALTER TABLE dim_currency
ADD CONSTRAINT uniq_currency_date UNIQUE (currency_code, rate_date);
