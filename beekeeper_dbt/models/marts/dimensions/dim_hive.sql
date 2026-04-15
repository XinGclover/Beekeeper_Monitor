with hive as (
    select *
    from {{ ref('sn_hive') }}
),

hive_type as (
    select *
    from {{ ref('stg_hive_type') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['hive_id', 'dbt_valid_from']) }} as hive_key,
    h.hive_id,
    h.apiary_id,
    h.hive_type_id,
    ht.hive_type_name as hive_type,
    h.installed_at,
    h.dbt_valid_from as valid_from,
    h.dbt_valid_to as valid_to,
    case
        when h.dbt_valid_to is null then true
        else false
    end as is_current
from hive h
left join hive_type ht
    on h.hive_type_id = ht.hive_type_id