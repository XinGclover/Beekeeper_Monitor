SELECT *
FROM ingestion.alarm_event
WHERE weather_id IS NOT NULL
ORDER BY event_id;


SELECT *
FROM ingestion.alarm_event
WHERE wildfire_id IS NOT NULL
ORDER BY event_id;