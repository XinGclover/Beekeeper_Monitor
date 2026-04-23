with source as (
  select * from {{ source('ingestion', 'alarm_rule_target') }}
),

cleaned as (
  select
    rule_id,
    target_type_id,
    target_id
  from source
)

select * from cleaned