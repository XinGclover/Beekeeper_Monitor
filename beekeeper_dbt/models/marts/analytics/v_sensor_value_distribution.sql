select
    measured_value,
    sensor_key,
    measured_at
from {{ ref('fact_sensor_measurements') }}