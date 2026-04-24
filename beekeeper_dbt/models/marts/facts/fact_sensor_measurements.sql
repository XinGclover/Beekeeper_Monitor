with measurements as (
    select *
    from {{ ref('stg_sensor_data') }}
),
sensor as (
    select *
    from {{ ref('dim_sensor') }}
),
date as (
    select *
    from {{ ref('dim_date') }}
),
time as (
    select *
    from {{ ref('dim_time') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['s.sensor_key', 'd.date_key', 't.time_key']) }} as measurement_key,
    s.sensor_key,
    d.date_key,
    t.time_key,
    fm.measured_at,
    fm.measured_value
from measurements fm
left join sensor s on fm.sensor_id = s.sensor_id
left join date d on fm.measured_at::date = d.full_date
left join time t on fm.measured_at::time = t.full_time

