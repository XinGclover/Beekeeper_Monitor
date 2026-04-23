with alarm_rule as (
  select
    rule_id,
    rule_name,
    metric_type_id,
    condition_type,
    threshold,
    severity_level_id,
    is_active
  from {{ ref('stg_alarm_rule') }}
),

metric_type as (
  select
    metric_type_id,
    metric_type_name
  from {{ ref('dim_metric_type') }}
),

severity as (
  select
    severity_id,
    severity_name
  from {{ ref('dim_severity') }}
)

select
  ar.rule_id as alarm_rule_key,
  ar.rule_id,
  ar.rule_name,
  ar.metric_type_id,
  mt.metric_type_name,
  ar.condition_type,
  ar.threshold,
  ar.severity_level_id as severity_id,
  sl.severity_name,
  ar.is_active
from alarm_rule ar
left join metric_type mt
  on ar.metric_type_id = mt.metric_type_id
left join severity sl
  on ar.severity_level_id = sl.severity_id