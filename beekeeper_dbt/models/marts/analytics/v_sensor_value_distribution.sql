select
    fsm.measured_value,
    fsm.sensor_key,
    fsm.measured_at,
    ds.sensor_name,
    ds.sensor_label
from {{ ref('fact_sensor_measurements') }} fsm
left join {{ ref('dim_sensor') }} ds on fsm.sensor_key = ds.sensor_key