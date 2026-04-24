with alarm_events as (
  select
    event_id,
    rule_id,
    sensor_data_id,
    status,
    triggered_at,
    observed_value,
    threshold
  from {{ ref('stg_alarm_event') }}
  where event_source_type = 'sensor'
),

sensor_data as (
  select
    sensor_data_id,
    sensor_id
  from {{ ref('stg_sensor_data') }}
),

sensor as (
  select
    sensor_id,
    sensor_key
  from {{ ref('dim_sensor') }}
),

alarm_rule as (
  select
    rule_id,
    alarm_rule_key
  from {{ ref('dim_alarm_rule') }}
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
  ae.event_id,
  ae.sensor_data_id,
  ae.status,
  ae.triggered_at,
  dd.date_key,
  td.time_key,
  ar.alarm_rule_key,
  s.sensor_key,
  ae.observed_value,
  ae.threshold
from alarm_events ae
left join sensor_data sd on ae.sensor_data_id = sd.sensor_data_id
left join sensor s on sd.sensor_id = s.sensor_id
left join alarm_rule ar on ae.rule_id = ar.rule_id
left join date_dim dd on ae.triggered_at::date = dd.full_date
left join time_dim td
on date_trunc('second', ae.triggered_at)::time = td.full_time