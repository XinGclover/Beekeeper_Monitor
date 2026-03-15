CREATE TABLE IF NOT EXISTS ingestion.sensor (
    sensor_id SERIAL PRIMARY KEY,
    hive_id INT NOT NULL REFERENCES ingestion.hives(hive_id),
    sensor_type_id SMALLINT NOT NULL REFERENCES ingestion.sensor_type(sensor_type_id),
    is_hive_level BOOLEAN NOT NULL DEFAULT TRUE,
    installed_at DATE,
    STATUS VARCHAR(20) DEFAULT 'active'
);