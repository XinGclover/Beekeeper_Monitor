INSERT INTO ingestion.alarm_rule_target (rule_id, target_type_id, target_id)
VALUES

-- ======================
-- SENSOR RULES → HIVE
-- ======================

-- rule 1: temperature high → hive 1
(1, 3, 1),

-- rule 2: temperature low → hive 2
(2, 3, 2),

-- rule 3: humidity high → hive 3
(3, 3, 3),

-- rule 4: weight low → hive 1
(4, 3, 1),

-- rule 5: weight critical → hive 2
(5, 3, 2),

-- rule 6: weight very high → hive 3
(6, 3, 3),

-- ======================
-- WEATHER RULES → LOCATION
-- ======================

-- rule 7: extreme temperature → location 1
(7, 1, 1),

-- rule 8: cold weather → location 3
(8, 1, 3),

-- rule 9: strong wind → location 4
(9, 1, 4),

-- ======================
-- WILDFIRE RULE → LOCATION
-- ======================

-- rule 10: wildfire risk → location 5
(10, 1, 5);



DELETE FROM ingestion.alarm_rule_target
WHERE rule_id IN (1,2,3,4,5,6);


-- Insert matched rule with right sensor_type 
-- hive temperature, rule_id= 1,2
-- temperature sensor, sensor_type_id = 1
INSERT INTO ingestion.alarm_rule_target (rule_id, target_type_id, target_id)
SELECT
    1,
    4,
    s.sensor_id
FROM ingestion.sensor s
WHERE s.sensor_type_id = 1  --temperature
AND NOT EXISTS (
    SELECT 1
    FROM ingestion.alarm_rule_target art
    WHERE art.rule_id = 1
      AND art.target_type_id = 4   -- sensor
      AND art.target_id = s.sensor_id
);

INSERT INTO ingestion.alarm_rule_target (rule_id, target_type_id, target_id)
SELECT
    2,
    4,
    s.sensor_id
FROM ingestion.sensor s
WHERE s.sensor_type_id = 1     --temperature
AND NOT EXISTS (
    SELECT 1
    FROM ingestion.alarm_rule_target art
    WHERE art.rule_id = 2
      AND art.target_type_id = 4   -- sensor
      AND art.target_id = s.sensor_id
);

-- hive humidity, rule_id= 3
-- humidity sensor,sensor_type_id = 2
INSERT INTO ingestion.alarm_rule_target (rule_id, target_type_id, target_id)
SELECT
    3,
    4,
    s.sensor_id
FROM ingestion.sensor s
WHERE s.sensor_type_id = 2  --humidity
AND NOT EXISTS (
    SELECT 1
    FROM ingestion.alarm_rule_target art
    WHERE art.rule_id = 3
      AND art.target_type_id = 4
      AND art.target_id = s.sensor_id
);

-- hive weight, rule_id= 4,5,6
-- weight sensor,sensor_type_id = 3
INSERT INTO ingestion.alarm_rule_target (rule_id, target_type_id, target_id)
SELECT
    4,
    4,
    s.sensor_id
FROM ingestion.sensor s
WHERE s.sensor_type_id = 3     --weight
AND NOT EXISTS (
    SELECT 1
    FROM ingestion.alarm_rule_target art
    WHERE art.rule_id = 4
      AND art.target_type_id = 4
      AND art.target_id = s.sensor_id
);

INSERT INTO ingestion.alarm_rule_target (rule_id, target_type_id, target_id)
SELECT
    5,
    4,
    s.sensor_id
FROM ingestion.sensor s
WHERE s.sensor_type_id = 3     --weight
AND NOT EXISTS (
    SELECT 1
    FROM ingestion.alarm_rule_target art
    WHERE art.rule_id = 5
      AND art.target_type_id = 4
      AND art.target_id = s.sensor_id
);

INSERT INTO ingestion.alarm_rule_target (rule_id, target_type_id, target_id)
SELECT
    6,
    4,
    s.sensor_id
FROM ingestion.sensor s
WHERE s.sensor_type_id = 3     --weight
AND NOT EXISTS (
    SELECT 1
    FROM ingestion.alarm_rule_target art
    WHERE art.rule_id = 6
      AND art.target_type_id = 4
      AND art.target_id = s.sensor_id
);