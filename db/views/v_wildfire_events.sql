CREATE
OR REPLACE VIEW ingestion.v_wildfire_events AS
SELECT
  w.wildfire_id,
  w.location_id,
  l.city,
  l.latitude,
  l.longitude,
  w.brightness,
  w.frp,
  w.detected_at,
  s.severity_level_id,
  s.severity_name
FROM
  ingestion.wildfire_data w
  JOIN ingestion.location l ON w.location_id = l.location_id
  JOIN ingestion.severity_level s ON w.severity_level_id = s.severity_level_id;