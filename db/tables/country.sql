CREATE TABLE IF NOT EXISTS ingestion.country (
    country_id SERIAL PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL UNIQUE,
    country_code CHAR(3) NOT NULL UNIQUE
);