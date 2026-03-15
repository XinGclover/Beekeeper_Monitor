CREATE TABLE IF NOT EXISTS ingestion.alarm_event (
    event_id SERIAL PRIMARY KEY,
    rule_id INT NOT NULL REFERENCES ingestion.alarm_rule(rule_id),
    sensor_data_id INT NULL REFERENCES ingestion.sensor_data(sensor_data_id),
    weather_id INT NULL REFERENCES ingestion.weather_data(weather_id),
    wildfire_id INT NULL REFERENCES ingestion.wildfire_data(wildfire_id),
    triggered_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    STATUS VARCHAR(50) NOT NULL DEFAULT 'new',
    CONSTRAINT chk_one_source_only CHECK (
        (
            CASE
                WHEN sensor_data_id IS NOT NULL THEN 1
                ELSE 0
            END
        ) + (
            CASE
                WHEN weather_id IS NOT NULL THEN 1
                ELSE 0
            END
        ) + (
            CASE
                WHEN wildfire_id IS NOT NULL THEN 1
                ELSE 0
            END
        ) = 1
    )
);


CREATE UNIQUE INDEX IF NOT EXISTS uq_alarm_event_sensor
ON ingestion.alarm_event(rule_id, sensor_data_id)
WHERE sensor_data_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_alarm_event_weather
ON ingestion.alarm_event(rule_id, weather_id)
WHERE weather_id IS NOT NULL;

CREATE UNIQUE INDEX IF NOT EXISTS uq_alarm_event_wildfire
ON ingestion.alarm_event(rule_id, wildfire_id)
WHERE wildfire_id IS NOT NULL;