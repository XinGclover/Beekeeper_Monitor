with source as (
  select * from {{ source('ingestion', 'location') }}
),

cleaned as (
  select 
    cast(location_id as integer) as location_id,
    cast(country_id as integer) as country_id,
    nullif(trim(city), '') as city,
    nullif(trim(address), '') as address,
    nullif(trim(postal_code), '') as postal_code,
    cast(latitude as float) as latitude,
    cast(longitude as float) as longitude
  from source
)

select * from cleaned

