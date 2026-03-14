create or replace view ingestion.v_sensor_data_timeline as
select
    sd.sensor_data_id,
    sd.sensor_id,
    s.hive_id,
    st.sensor_type_name,
    sd.measurement,
    sd.measured_at,
    l.city
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
where s.status = 'active';