INSERT INTO
  ingestion.severity_level (severity_level_id, severity_name, description)
VALUES
  (1, 'low', 'Low wildfire intensity'),
  (2, 'medium', 'Moderate wildfire intensity'),
  (3, 'high', 'High wildfire intensity') ON conflict (severity_level_id) DO nothing;

INSERT INTO
  ingestion.severity_level (severity_level_id, severity_name, description)
VALUES
  (4, 'high', 'Serious risk requiring attention'),
  (5, 'critical', 'Immediate action required');