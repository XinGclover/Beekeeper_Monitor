with alarm_events as (
  select
    event_id,
    rule_id,
    weather_id,
    status,
    triggered_at,
    observed_value,
    threshold
  from {{ ref('stg_alarm_event') }}
  where event_source_type = 'weather'
),

weather_data as (
  select
    weather_id,
    location_id
  from {{ ref('stg_weather_data') }}
),

alarm_rule as (
  select
    rule_id,
    alarm_rule_key,
    severity_id
  from {{ ref('dim_alarm_rule') }}
),

severity as (
  select
    severity_id,
    severity_key
  from {{ ref('dim_severity') }}
),

date_dim as (
  select
    full_date,
    date_key
  from {{ ref('dim_date') }}
),

time_dim as (
  select
    full_time,
    time_key
  from {{ ref('dim_time') }}
)

select
  ae.event_id as alarm_event_key,
  ae.event_id,
  ae.rule_id,
  ar.alarm_rule_key,
  ae.weather_id,
  wd.location_id,
  sl.severity_key,
  dd.date_key,
  td.time_key,
  'weather' as event_source_type,
  ae.observed_value,
  ae.threshold,
  ae.status,
  ae.triggered_at
from alarm_events ae
left join weather_data wd on ae.weather_id = wd.weather_id
left join alarm_rule ar on ae.rule_id = ar.rule_id
left join severity sl on ar.severity_id = sl.severity_id
left join date_dim dd on ae.triggered_at::date = dd.full_date
left join time_dim td on date_trunc('second', ae.triggered_at)::time = td.full_time