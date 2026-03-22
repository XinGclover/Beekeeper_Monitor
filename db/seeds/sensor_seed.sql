insert into ingestion.sensor
(sensor_type_id, hive_id, is_hive_level)
values
(1, 1, true),
(2, 1, true),
(3, 2, true);

INSERT INTO ingestion.sensor
(hive_id, sensor_type_id, is_hive_level)
VALUES
(3, 1, TRUE),   -- TEMPERATURE
(3, 2, TRUE),   -- HUMIDITY
(3, 3, TRUE);   -- WEIGHT