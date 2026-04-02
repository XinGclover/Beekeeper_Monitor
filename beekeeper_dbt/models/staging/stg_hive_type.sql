with source as (
  select * from {{ source('ingestion', 'hive_type') }}
),

cleaned as (
  select 
    cast(hive_type_id as integer) as hive_type_id,
    nullif(trim(name), '') as hive_type_name
  from source
)

select * from cleaned