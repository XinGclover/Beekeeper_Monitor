INSERT INTO ingestion.alarm_rule
(name, metric_type_id, condition_type, threshold, severity_level_id, is_active)
VALUES
-- Sensor based rules
('Hive temperature too high', 1, '>', 35, 2, TRUE),
('Hive temperature too low', 1, '<', 10, 2, TRUE),
('Hive humidity too high', 2, '>', 85, 2, TRUE),
('Hive weight too low', 6, '<', 20, 3, TRUE),
('Rapid hive weight loss', 6, '<', 15, 4, TRUE),
('Hive weight very high', 6, '>', 80, 1, TRUE),

-- Weather based rules
('Extreme outdoor temperature', 3, '>', 32, 2, TRUE),
('Cold weather risk', 3, '<', -5, 2, TRUE),
('Strong wind warning', 4, '>', 20, 3, TRUE),

-- Wildfire rules
('Wildfire risk nearby', 5, '>', 3, 4, TRUE),
('Severe wildfire danger', 5, '>', 4, 5, TRUE);





