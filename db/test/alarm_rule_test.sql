select
    rule_id,
    name,
    condition_type,
    threshold,
    is_active
from ingestion.alarm_rule
order by rule_id;

select
    event_id,
    rule_id,
    sensor_data_id,
    weather_id,
    wildfire_id,
    triggered_at,
    status
from ingestion.alarm_event
order by triggered_at desc
limit 20;