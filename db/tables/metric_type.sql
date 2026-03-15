CREATE TABLE IF NOT EXISTS ingestion.metric_type (
    metric_type_id SERIAL PRIMARY KEY,
    metric_type_name VARCHAR(25) NOT NULL UNIQUE
);