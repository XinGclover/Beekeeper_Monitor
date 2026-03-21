CREATE
OR REPLACE VIEW ingestion.v_filter_options AS
SELECT
  l.location_id,
  CONCAT(l.city,' #',l.country_id) AS location_name,
  a.apiary_id,
  CONCAT(ae.terrain_type,' #',a.apiary_id) AS apiary_name,
  h.hive_id,
  CONCAT(ht.name,' #',h.hive_id) AS hive_name,
  s.sensor_id,
  CONCAT(st.sensor_type_name, ' #', s.sensor_id) AS sensor_name
FROM
  ingestion.location l
  LEFT JOIN ingestion.apiary a ON a.location_id = l.location_id
  LEFT JOIN ingestion.apiary_environment ae ON a.apiary_id = ae.apiary_id
  LEFT JOIN ingestion.hives h ON h.apiary_id = a.apiary_id
  LEFT JOIN ingestion.hive_type ht ON h.hive_type_id = ht.hive_type_id
  LEFT JOIN ingestion.sensor s ON s.hive_id = h.hive_id
  LEFT JOIN ingestion.sensor_type st ON s.sensor_type_id = st.sensor_type_id;