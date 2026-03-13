INSERT INTO ingestion.sensor_data
(job_id, sensor_id, measurement, measured_at)
VALUES
-- temperature too high
(9, 1, 38.50, '2026-03-13 10:00:00'),

-- temperature too low
(9, 1, 8.20, '2026-03-13 11:00:00'),

-- humidity too high
(9, 2, 92.00, '2026-03-13 12:00:00'),

-- hive weight very low
(9, 3, 14.50, '2026-03-13 13:00:00'),

-- rapid hive weight loss
(9, 3, 12.00, '2026-03-13 14:00:00');