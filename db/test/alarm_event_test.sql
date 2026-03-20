SELECT *
FROM ingestion.alarm_event
WHERE weather_id IS NOT NULL
ORDER BY event_id;


SELECT *
FROM ingestion.alarm_event
WHERE wildfire_id IS NOT NULL
ORDER BY event_id;

SELECT
    art.rule_id,
    art.target_type_id,
    tt.target_type_name,
    art.target_id
FROM ingestion.alarm_rule_target art
JOIN ingestion.target_type tt
  ON art.target_type_id = tt.target_type_id
WHERE art.rule_id IN (7, 8, 9);

SELECT COUNT(*) FROM ingestion.alarm_event;

select
  event_id,
  rule_id,
  triggered_at
from ingestion.alarm_event
order by triggered_at desc
limit 20;


SELECT *
FROM ingestion.sensor_data
WHERE measurement > 35
ORDER BY measured_at DESC
LIMIT 20;


-- Debug: There are sensor_data that should trigger alarm, but there is no alarm_event
-- Step 1: Verify the data (is there really >35?)
SELECT 
    s.sensor_id,
    s.sensor_type_id,
    st.sensor_type_name
FROM ingestion.sensor s
JOIN ingestion.sensor_type st
ON s.sensor_type_id = st.sensor_type_id;

-- Step 2: Verify that sensor → metric mapping is correct
SELECT 
    s.sensor_id,
    s.sensor_type_id,
    st.sensor_type_name
FROM ingestion.sensor s
JOIN ingestion.sensor_type st
ON s.sensor_type_id = st.sensor_type_id;

-- Step 3: Check alarm_rule
SELECT *
FROM ingestion.alarm_rule
WHERE metric_type_id = 1
AND is_active = TRUE;


-- Step 4: Check rule_target (IMPORTANT!)
SELECT *
FROM ingestion.alarm_rule_target
WHERE target_type_id = 4;   -- target_type = 'sensor'

-- no result means no sensor connect to rules

-- Step 5: Test the JOIN manually (SIMULATE RULE ENGINE)
SELECT
    sd.sensor_id,
    sd.measurement,
    ar.rule_id,
    ar.threshold
FROM ingestion.sensor_data sd
JOIN ingestion.sensor s ON sd.sensor_id = s.sensor_id
JOIN ingestion.alarm_rule ar ON ar.metric_type_id = 1
JOIN ingestion.alarm_rule_target art 
    ON art.rule_id = ar.rule_id
    AND art.target_id = sd.sensor_id
WHERE sd.measurement > ar.threshold
ORDER BY sd.measured_at DESC;


-- step 4 shows no result, so continue debug to other way
-- 1. finde temperature_regelns rule_id:
SELECT rule_id, name, metric_type_id, threshold
FROM ingestion.alarm_rule
WHERE metric_type_id = 1;          
-- rule_id = 1,2

-- 2. insert right sensor and rule, in alarm_rule_target_seed.sql




-- 1. kontrollera att koppling finns
SELECT *
FROM ingestion.alarm_rule_target
WHERE target_type_id = 4
ORDER BY rule_id, target_id;
-- 2. kontrollera temperature-data över threshold
SELECT *
FROM ingestion.sensor_data
WHERE sensor_id IN (1, 4)
  AND measurement > 35
ORDER BY measured_at DESC;
-- 3. kör pipeline igen
-- 4. kolla alarm_event
SELECT *
FROM ingestion.alarm_event
ORDER BY created_at DESC;
