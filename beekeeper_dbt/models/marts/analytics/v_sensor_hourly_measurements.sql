select
    date_trunc('hour', measured_at) as measurement_hour,
    sensor_key,
    avg(measured_value) as avg_measured_value,
    min(measured_value) as min_measured_value,
    max(measured_value) as max_measured_value,
    count(*) as measurement_count
from {{ ref('fact_sensor_measurements') }}
group by 1,2
order by 1,2