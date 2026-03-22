CREATE
OR REPLACE VIEW ingestion.v_alarm_event_latest AS
SELECT
  ae.event_id,
  ae.rule_id,
  ae.status,
  ae.triggered_at,
  ae.observed_value,
  ae.threshold_value,
  ar.rule_name,
  sl.severity_name,
  CASE
    WHEN ae.sensor_data_id IS NOT NULL THEN 'sensor'
    WHEN ae.weather_id IS NOT NULL THEN 'weather'
    WHEN ae.wildfire_id IS NOT NULL THEN 'wildfire'
    ELSE 'unknown'
  END AS source_type,
  sd.sensor_id,
  s.hive_id,
  h.apiary_id,
  l.location_id,
  CASE
    WHEN ae.sensor_data_id IS NOT NULL THEN concat(st.sensor_type_name, ' #', s.sensor_id)
    WHEN ae.weather_id IS NOT NULL THEN concat('Weather @ ', l.city)
    WHEN ae.wildfire_id IS NOT NULL THEN concat('Wildfire @ ', l.city)
    ELSE 'Unknown'
  END AS target_name
FROM
  ingestion.alarm_event ae
  JOIN ingestion.alarm_rule ar ON ae.rule_id = ar.rule_id
  JOIN ingestion.severity_level sl ON ar.severity_level_id = sl.severity_level_id
  LEFT JOIN ingestion.sensor_data sd ON ae.sensor_data_id = sd.sensor_data_id
  LEFT JOIN ingestion.sensor s ON sd.sensor_id = s.sensor_id
  LEFT JOIN ingestion.sensor_type st ON s.sensor_type_id = st.sensor_type_id
  LEFT JOIN ingestion.hives h ON s.hive_id = h.hive_id
  LEFT JOIN ingestion.apiary ap ON h.apiary_id = ap.apiary_id
  LEFT JOIN ingestion.location l ON ap.location_id = l.location_id
  LEFT JOIN ingestion.weather_data wd ON ae.weather_id = wd.weather_id
  LEFT JOIN ingestion.location wl ON wd.location_id = wl.location_id
  LEFT JOIN ingestion.wildfire_data wf ON ae.wildfire_id = wf.wildfire_id
  LEFT JOIN ingestion.location fl ON wf.location_id = fl.location_id;