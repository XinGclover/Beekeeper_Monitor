with source as (
  select * from {{ source('ingestion', 'apiary') }}
),

cleaned as (
  select 
    cast(apiary_id as integer) as apiary_id,
    cast(location_id as integer) as location_id,
    cast(amount_units as integer) as amount_units
  from source
)

select * from cleaned
