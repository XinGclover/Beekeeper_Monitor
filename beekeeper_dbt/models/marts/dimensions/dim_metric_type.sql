with types as (
    select *
    from {{ ref('stg_metric_type') }}
)

select
    metric_type_id as metric_type_key,
    metric_type_id,
    metric_type_name
from types
