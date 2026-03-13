CREATE TABLE IF NOT EXISTS ingestion.sensor_type (
    sensor_type_id SERIAL PRIMARY KEY,
    sensor_type_name VARCHAR(30) NOT NULL UNIQUE,
    unit VARCHAR(20) NOT NULL,
    description VARCHAR(100)
);