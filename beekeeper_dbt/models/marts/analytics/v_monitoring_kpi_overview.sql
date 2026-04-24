with all_alarms as (
  select triggered_at from {{ ref('fact_sensor_alarm_event') }}
  union all
  select triggered_at from {{ ref('fact_weather_alarm_event') }}
  union all
  select triggered_at from {{ ref('fact_wildfire_alarm_event') }}
)

select
    (select count(*) from all_alarms) as total_alarm_count,
    (select count(*) from {{ ref('dim_sensor') }} where is_current = true) as active_sensor_count,
    (select max(measured_at) from {{ ref('fact_sensor_measurements') }}) as latest_measurement_at,
    (select avg(measured_value) from {{ ref('fact_sensor_measurements') }} where measured_at >= now() - interval '24 hours') as avg_sensor_value_last_24h,
    (select count(*) from all_alarms where triggered_at >= now() - interval '24 hours') as alarm_count_last_24h