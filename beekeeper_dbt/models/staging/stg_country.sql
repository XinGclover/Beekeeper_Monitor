with source as (
  select * from {{ source('ingestion', 'country') }}
),

cleaned as (
  select 
    cast(country_id as integer) as country_id,
    nullif(trim(country_name), '') as country_name,
    nullif(trim(country_code), '') as country_code
  from source
)

select * from cleaned

