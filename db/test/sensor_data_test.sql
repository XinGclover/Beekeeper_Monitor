select
  sd.sensor_data_id,
  st.sensor_type_name,
  sd.measurement,
  sd.measured_at
from ingestion.sensor_data sd
join ingestion.sensor s
  on sd.sensor_id = s.sensor_id
join ingestion.sensor_type st
  on s.sensor_type_id = st.sensor_type_id
where lower(st.sensor_type_name) like '%temp%'
order by sd.measured_at desc
limit 20;