DROP TABLE IF EXISTS ingestion.wildfire_data;

CREATE TABLE IF NOT EXISTS ingestion.wildfire_data (
    wildfire_id SERIAL PRIMARY KEY,
    job_id INT NOT NULL REFERENCES ingestion.scraping_job(job_id),
    location_id INT REFERENCES ingestion.location(location_id),
    latitude DECIMAL(8, 5) NOT NULL,
    longitude DECIMAL(8, 5) NOT NULL,
    brightness DECIMAL(8, 2),
    confidence CHAR(1),
    frp DECIMAL(10, 2),
    satellite VARCHAR(10),
    instrument VARCHAR(20),
    daynight CHAR(1),
    severity_level_id INT REFERENCES ingestion.severity_level(severity_level_id),
    STATUS VARCHAR(20),
    detected_at TIMESTAMP NOT NULL,
    fetched_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_wildfire_lat_lon_detected UNIQUE (latitude, longitude, detected_at)
);