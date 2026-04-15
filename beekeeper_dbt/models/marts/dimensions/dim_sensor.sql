with sensor as (
    select *
    from {{ ref('sn_sensor') }}
),

sensor_type as (
    select *
    from {{ ref('stg_sensor_type') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['sensor_id', 'dbt_valid_from']) }} as sensor_key,
    s.sensor_id,
    s.sensor_type_id,
    st.sensor_type_name as sensor_type,
    s.is_hive_level,
    s.hive_id,
    s.status,
    s.installed_at,
    s.dbt_valid_from as valid_from,
    s.dbt_valid_to as valid_to,
    case
        when s.dbt_valid_to is null then true
        else false
    end as is_current
from sensor s
left join sensor_type st
    on s.sensor_type_id = st.sensor_type_id