with source as (
  select * from {{ source('ingestion', 'wildfire_data') }}
),

cleaned as (
  select
    wildfire_id,
    location_id,
    latitude,
    longitude,
    brightness,
    confidence,
    frp,
    satellite,
    instrument,
    daynight,
    severity_level_id,
    status,
    detected_at,
    fetched_at
  from source
)

select * from cleaned
