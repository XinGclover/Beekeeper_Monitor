CREATE TABLE IF NOT EXISTS ingestion.external_source (
    source_id SERIAL PRIMARY KEY,
    source_name VARCHAR(100) NOT NULL,
    base_url VARCHAR(255),
    data_type VARCHAR(50),
    update_frequency VARCHAR(50)
);