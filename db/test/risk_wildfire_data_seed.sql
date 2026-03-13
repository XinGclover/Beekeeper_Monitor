INSERT INTO ingestion.wildfire_data
(job_id, location_id, latitude, longitude, brightness, confidence, frp, satellite, instrument, daynight, severity_level_id, status, detected_at)
VALUES
-- medium wildfire
(4, 1, 64.88, 21.35, 380.50, 'h', 12.50, 'N', 'VIIRS', 'D', 3, 'detected', '2026-03-13 18:00:00'),

-- very strong wildfire
(4, 1, 65.02, 21.40, 420.00, 'h', 18.90, 'N', 'VIIRS', 'D', 4, 'detected', '2026-03-13 19:00:00');