DROP TABLE IF EXISTS ingestion.weather_data;

CREATE TABLE IF NOT EXISTS ingestion.weather_data (
    weather_id SERIAL PRIMARY KEY,
    job_id INT NOT NULL REFERENCES ingestion.scraping_job(job_id),
    location_id INT NOT NULL REFERENCES ingestion.location(location_id),
    air_temperature DECIMAL(5, 2),
    relative_humidity DECIMAL(5, 2),
    wind_speed DECIMAL(6, 2),
    wind_direction DECIMAL(6, 2),
    valid_time TIMESTAMP NOT NULL,
    fetched_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_weather_location_valid_time UNIQUE (location_id, valid_time)
);