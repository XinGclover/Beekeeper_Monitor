with sensor as (

    select *
    from {{ ref('stg_sensor') }}
),
sensor_type as (

    select *
    from {{ ref('stg_sensor_type') }}
),
hive as (
    select *
    from {{ ref('stg_hive') }}
),
hive_type as (

    select *
    from {{ ref('stg_hive_type') }}
),
apiary as (

    select *
    from {{ ref('stg_apiary') }}
),
location as (

    select *
    from {{ ref('stg_location') }}
),
country as (  

    select *
    from {{ ref('stg_country') }}
)


select
    {{ dbt_utils.generate_surrogate_key(['s.sensor_id']) }} as sensor_key,
    s.sensor_id,
    st.sensor_type_name as sensor_type,
    s.is_hive_level,
    s.hive_id,
    ht.hive_type_name as hive_type,
    a.apiary_id,
    l.location_id,
    l.city,
    c.country_name as country,
    s.installed_at,
    s.status,
    s.installed_at as valid_from,
    cast(null as timestamp) as valid_to,
    true as current_flag
from sensor s
left join sensor_type st on s.sensor_type_id = st.sensor_type_id
left join hive h on s.hive_id = h.hive_id
left join hive_type ht on h.hive_type_id = ht.hive_type_id
left join apiary a on h.apiary_id = a.apiary_id
left join location l on a.location_id = l.location_id
left join country c on l.country_id = c.country_id




