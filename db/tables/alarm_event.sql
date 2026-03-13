CREATE TABLE IF NOT EXISTS ingestion.alarm_event (
    event_id SERIAL PRIMARY KEY,
    rule_id INT NOT NULL REFERENCES ingestion.alarm_rule(rule_id),
    sensor_data_id INT REFERENCES ingestion.sensor_data(sensor_data_id),
    wildfire_id INT REFERENCES ingestion.wildfire_data(wildfire_id),
    weather_id INT REFERENCES ingestion.weather_data(weather_id),
    triggered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    STATUS VARCHAR(10) NOT NULL,
    observed_value DECIMAL(11, 5),
    CONSTRAINT chk_one_source CHECK (
        (sensor_data_id IS NOT NULL) :: INT + (wildfire_id IS NOT NULL) :: INT + (weather_id IS NOT NULL) :: INT = 1
    )
);