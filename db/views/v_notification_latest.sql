CREATE
OR REPLACE VIEW ingestion.v_notification_latest AS
SELECT
  n.notification_id,
  n.user_id,
  u.username,
  n.event_id,
  n.notification_status,
  n.is_read,
  n.title,
  n.message,
  n.created_at,
  n.read_at,
  n.sent_at,
  ae.rule_name,
  ae.target_name,
  ae.severity_name,
  ae.source_type,
  ae.location_id,
  ae.apiary_id,
  ae.hive_id,
  ae.sensor_id,
  ae.triggered_at
FROM
  ingestion.notification n
  JOIN ingestion."user" u ON n.user_id = u.user_id
  JOIN ingestion.v_alarm_event_latest ae ON n.event_id = ae.event_id;