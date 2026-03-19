SELECT *
FROM ingestion.alarm_event
WHERE weather_id IS NOT NULL
ORDER BY event_id;


SELECT *
FROM ingestion.alarm_event
WHERE wildfire_id IS NOT NULL
ORDER BY event_id;

SELECT
    art.rule_id,
    art.target_type_id,
    tt.target_type_name,
    art.target_id
FROM ingestion.alarm_rule_target art
JOIN ingestion.target_type tt
  ON art.target_type_id = tt.target_type_id
WHERE art.rule_id IN (7, 8, 9);

SELECT COUNT(*) FROM ingestion.alarm_event;

select
  event_id,
  rule_id,
  triggered_at
from ingestion.alarm_event
order by triggered_at desc
limit 20;