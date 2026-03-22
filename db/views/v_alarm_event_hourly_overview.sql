CREATE
OR REPLACE VIEW ingestion.v_alarm_event_hourly_overview AS
SELECT
  date_trunc('hour', triggered_at) AS HOUR,
  location_id,
  apiary_id,
  hive_id,
  count(*) AS alarm_count
FROM
  ingestion.v_alarm_event_latest
GROUP BY
  date_trunc('hour', triggered_at),
  location_id,
  apiary_id,
  hive_id
ORDER BY
  HOUR;