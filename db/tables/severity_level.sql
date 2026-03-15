CREATE TABLE IF NOT EXISTS ingestion.severity_level (
    severity_level_id SMALLINT PRIMARY KEY,
    severity_name VARCHAR(10) NOT NULL,
    description VARCHAR(100)
);