with source as (
  select * from {{ source('ingestion', 'role') }}
),

cleaned as (
  select 
    cast(role_id as integer) as role_id,
    nullif(trim(role_name), '') as role_name
  from source
)

select * from cleaned 