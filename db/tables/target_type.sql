CREATE TABLE IF NOT EXISTS ingestion.target_type (
    target_type_id SERIAL PRIMARY KEY,
    target_type_name VARCHAR(25) NOT NULL UNIQUE
);