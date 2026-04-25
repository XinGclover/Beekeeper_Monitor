with unioned_alarms as (
  select triggered_at, event_source_type from {{ ref('fact_sensor_alarm_event') }}
  union all
  select triggered_at, event_source_type from {{ ref('fact_weather_alarm_event') }}
  union all
  select triggered_at, event_source_type from {{ ref('fact_wildfire_alarm_event') }}
)

select
  date_trunc('hour', triggered_at) as alert_hour,
  event_source_type,
  count(*) as alarm_count
from unioned_alarms
group by 1, 2
order by 1, 2