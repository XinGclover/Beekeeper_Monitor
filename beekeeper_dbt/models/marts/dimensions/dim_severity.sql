with severity as (
    select *
    from {{ ref('stg_severity') }}
)

select
    severity_id as severity_key,
    severity_id,
    severity_name
from severity