insert into ingestion.sensor_type (sensor_type_name, unit, description)
values
('TEMPERATURE', 'C', 'Hive temperature sensor'),
('HUMIDITY', '%', 'Hive humidity sensor'),
('WEIGHT', 'kg', 'Hive weight sensor')
on conflict (sensor_type_name) do nothing;