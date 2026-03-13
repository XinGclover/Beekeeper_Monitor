CREATE TABLE IF NOT EXISTS ingestion.scraping_job (
    job_id SERIAL PRIMARY KEY,
    source_id INT NOT NULL REFERENCES ingestion.external_source(source_id),
    run_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    STATUS VARCHAR(30),
    records_collected INT DEFAULT 0
);