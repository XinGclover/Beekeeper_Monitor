CREATE OR REPLACE VIEW ingestion.v_alarm_event_hourly AS
SELECT
    DATE_TRUNC('hour', ae.triggered_at) AS hour,
    sl.severity_name,
    COUNT(*) AS alarm_count
FROM ingestion.alarm_event ae
JOIN ingestion.alarm_rule ar
    ON ae.rule_id = ar.rule_id
JOIN ingestion.severity_level sl
    ON ar.severity_level_id = sl.severity_level_id
GROUP BY 1, 2
ORDER BY 1;