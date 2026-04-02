with source as (
  select * from {{ source('ingestion', 'sensor_type') }}
),

cleaned as (
  select 
    cast(sensor_type_id as integer) as sensor_type_id,
    nullif(trim(sensor_type_name), '') as sensor_type_name,
    nullif(trim(unit), '') as sensor_type_unit
  from source
)

select * from cleaned