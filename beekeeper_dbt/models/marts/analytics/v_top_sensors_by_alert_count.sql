select
    s.sensor_key,
    s.sensor_id,
    s.sensor_type,
    s.hive_id,
    h.apiary_id,
    count(*) as alarm_count
from {{ ref('fact_sensor_alarm_event') }} fae
left join {{ ref('dim_sensor') }} s on fae.sensor_key = s.sensor_key
left join {{ ref('dim_hive') }} h on s.hive_id = h.hive_id
group by 1,2,3,4,5
order by alarm_count desc