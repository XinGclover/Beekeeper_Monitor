CREATE TABLE IF NOT EXISTS ingestion.sensor_data (
    sensor_data_id SERIAL PRIMARY KEY,
    job_id INT NOT NULL REFERENCES ingestion.scraping_job(job_id),
    sensor_id INT NOT NULL REFERENCES ingestion.sensor(sensor_id),
    measurement DECIMAL(11, 5) NOT NULL,
    measured_at TIMESTAMP NOT NULL,
    fetched_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_sensor_measured_at UNIQUE (sensor_id, measured_at)
);