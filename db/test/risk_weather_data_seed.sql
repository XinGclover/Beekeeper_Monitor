INSERT INTO ingestion.weather_data
(job_id, location_id, air_temperature, relative_humidity, wind_speed, wind_direction, valid_time)
VALUES
-- extreme heat
(5, 1, 36.50, 40.00, 5.00, 180, '2026-03-13 15:00:00'),

-- strong wind
(5, 1, 12.00, 60.00, 24.00, 200, '2026-03-13 16:00:00'),

-- cold risk
(5, 1, -7.50, 70.00, 3.00, 150, '2026-03-13 17:00:00');