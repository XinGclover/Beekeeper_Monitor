with source as (
  select * from {{ source('ingestion', 'weather_data') }}
),

cleaned as (
  select
    weather_id,
    location_id,
    air_temperature,
    relative_humidity,
    wind_speed,
    wind_direction,
    valid_time,
    fetched_at
  from source
)

select * from cleaned
