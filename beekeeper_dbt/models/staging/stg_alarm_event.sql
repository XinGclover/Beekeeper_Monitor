with source as (
  select * from {{ source('ingestion', 'alarm_event') }}
),

cleaned as (
  select
    event_id,
    rule_id,
    sensor_data_id,
    weather_id,
    wildfire_id,
    triggered_at,
    status,
    observed_value,
    threshold_value as threshold,
    case
      when sensor_data_id is not null then 'sensor'
      when weather_id is not null then 'weather'
      when wildfire_id is not null then 'wildfire'
      else null
    end as event_source_type
  from source
)

select * from cleaned
