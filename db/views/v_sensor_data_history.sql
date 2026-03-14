create or replace view ingestion.v_sensor_history as
select
    s.sensor_id,
    s.hive_id,
    h.apiary_id,
    s.sensor_type_id,
    st.sensor_type_name,
    l.location_id,
    l.city,
    date(sd.measured_at) as period_date,
    avg(sd.measurement) as measurement_avg,
    min(sd.measurement) as measurement_min,
    max(sd.measurement) as measurement_max,
    count(*) as measurement_count
from ingestion.sensor_data sd
join ingestion.sensor s
    on sd.sensor_id = s.sensor_id
join ingestion.sensor_type st
    on s.sensor_type_id = st.sensor_type_id
join ingestion.hives h
    on s.hive_id = h.hive_id
join ingestion.apiary ap
    on h.apiary_id = ap.apiary_id
join ingestion.location l
    on ap.location_id = l.location_id
group by
    s.sensor_id,
    s.hive_id,
    h.apiary_id,
    s.sensor_type_id,
    st.sensor_type_name,
    l.location_id,
    l.city,
    date(sd.measured_at);