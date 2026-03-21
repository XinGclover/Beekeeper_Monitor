create or replace view ingestion.v_sensor_latest as
select
    s.sensor_id,
	concat(st.sensor_type_name, ' #', s.sensor_id) as sensor_name,
    s.hive_id,
    h.apiary_id,
    s.sensor_type_id,
    st.sensor_type_name,
    s.is_hive_level,
    s.installed_at,
    s.status,
    l.location_id,
    l.city,
    sd.measurement,
    sd.measured_at
from ingestion.sensor s
join ingestion.sensor_type st
    on s.sensor_type_id = st.sensor_type_id
join ingestion.hives h
    on s.hive_id = h.hive_id
join ingestion.apiary ap
    on h.apiary_id = ap.apiary_id
join ingestion.location l
    on ap.location_id = l.location_id
join lateral (
    select *
    from ingestion.sensor_data sd
    where sd.sensor_id = s.sensor_id
    order by sd.measured_at desc
    limit 1
) sd on true
where s.status = 'active';