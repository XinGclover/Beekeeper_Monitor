with source as (
  select * from {{ source('ingestion', 'sensor') }}
),

cleaned as (
  select 
    cast(sensor_id as integer) as sensor_id,
    cast(hive_id as integer) as hive_id,
    cast(sensor_type_id as integer) as sensor_type_id,
    is_hive_level,
    cast(installed_at as date) as installed_at,
    nullif(trim(status), '') as status
  from source
)

select * from cleaned