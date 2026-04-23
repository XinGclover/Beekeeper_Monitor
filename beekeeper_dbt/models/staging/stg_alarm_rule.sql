with source as (
  select * from {{ source('ingestion', 'alarm_rule') }}
),

cleaned as (
  select
    rule_id,
    rule_name,
    metric_type_id,
    condition_type,
    threshold,
    severity_level_id,
    is_active
  from source
)

select * from cleaned