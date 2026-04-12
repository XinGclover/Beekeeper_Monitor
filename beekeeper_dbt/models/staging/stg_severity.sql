with source as (
  select * from {{ source('ingestion', 'severity_level') }}
),

cleaned as (
  select 
    cast(severity_level_id as integer) as severity_id,
    nullif(trim(severity_name), '') as severity_name
  from source
)

select * from cleaned 