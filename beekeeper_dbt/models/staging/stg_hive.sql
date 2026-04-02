with source as (
  select * from {{ source('ingestion', 'hives') }}
),

cleaned as (
  select 
    cast(hive_id as integer) as hive_id,
    cast(apiary_id as integer) as apiary_id,
    cast(hive_type_id as integer) as hive_type_id,
    cast(installation_date as date) as installed_at
  from source
)

select * from cleaned