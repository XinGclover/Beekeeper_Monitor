with source as (
  select * from {{ source('ingestion', 'sensor_data') }}
),

cleaned as (
  select 
    cast(sensor_data_id as integer) as sensor_data_id,
    cast(sensor_id as integer) as sensor_id,
    cast(measurement as decimal(11,2)) as measured_value,
    cast(measured_at as timestamp) as measured_at,
    cast(fetched_at as timestamp) as fetched_at
  from source
)

select * from cleaned