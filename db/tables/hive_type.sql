CREATE TABLE IF NOT EXISTS ingestion.hive_type (
    hive_type_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(100)
);