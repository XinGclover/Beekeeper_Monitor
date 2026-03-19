INSERT INTO ingestion.alarm_rule
(name, metric_type_id, condition_type, threshold, severity_level_id, is_active)
VALUES
-- Temperature (sensor_temperature = 1)
('Hive temperature too high', 1, '>', 35, 2, TRUE),
('Hive temperature too low', 1, '<', 10, 2, TRUE),

-- Humidity (sensor_humidity = 2)
('Hive humidity too high', 2, '>', 70, 2, TRUE),

-- Weight (sensor_hive_weight = 6)
('Hive weight too low', 6, '<', 20, 3, TRUE),

-- 🔥 FIX: rename (NOT rapid loss!)
('Hive weight critically low', 6, '<', 15, 4, TRUE),

('Hive weight very high', 6, '>', 80, 1, TRUE),

-- ======================
-- WEATHER RULES
-- ======================

('Extreme outdoor temperature', 3, '>', 32, 2, TRUE),
('Cold weather risk', 3, '<', -5, 2, TRUE),
('Strong wind warning', 4, '>', 20, 3, TRUE),

-- ======================
-- WILDFIRE RULES
-- ======================

('Wildfire risk nearby', 5, '>', 3, 4, TRUE),
('Severe wildfire danger', 5, '>', 4, 5, TRUE);





