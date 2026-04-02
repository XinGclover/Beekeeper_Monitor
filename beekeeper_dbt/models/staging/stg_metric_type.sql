with source as (
  select * from {{ source('ingestion', 'metric_type') }}
),

cleaned as (
  select 
    cast(metric_type_id as integer) as metric_type_id,
    nullif(trim(metric_type_name), '') as metric_type_name
  from source
)

select * from cleaned